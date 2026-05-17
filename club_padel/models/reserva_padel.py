
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ReservaPadel(models.Model):
    _name = "club_padel.reserva"
    _description = "Reserva de pista"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "referencia"

    referencia = fields.Char(string="Referencia", required=True, copy=False, readonly=True, default="Nuevo")

    cliente_id = fields.Many2one("res.partner", string="Cliente", required=True)
    pista_id = fields.Many2one("club_padel.pista", string="Pista", required=True)

    inicio = fields.Datetime(string="Inicio", required=True)
    fin = fields.Datetime(string="Fin", required=True)

    telefono_contacto = fields.Char(string="Teléfono", related="cliente_id.phone", readonly=True)
    email_contacto = fields.Char(string="Email", related="cliente_id.email", readonly=True)

    estado = fields.Selection(
        [
            ("borrador", "Borrador"),
            ("confirmada", "Confirmada"),
            ("realizada", "Realizada"),
            ("cancelada", "Cancelada"),
        ],
        string="Estado",
        default="borrador",
        required=True,
        tracking=True,
    )

    duracion_horas = fields.Float(string="Duración (h)", compute="_calcular_duracion", store=True)
    total = fields.Float(string="Total (€)", compute="_calcular_total", store=True)

    observaciones = fields.Text(string="Observaciones")

    @api.model
    def create(self, vals):
        if vals.get("referencia", "Nuevo") == "Nuevo":
            vals["referencia"] = self.env["ir.sequence"].next_by_code("club_padel.reserva.seq") or "RES-0000"
        return super().create(vals)

    @api.depends("inicio", "fin")
    def _calcular_duracion(self):
        for rec in self:
            if rec.inicio and rec.fin:
                delta = rec.fin - rec.inicio
                rec.duracion_horas = delta.total_seconds() / 3600.0
            else:
                rec.duracion_horas = 0

    @api.depends("duracion_horas", "pista_id.precio_hora")
    def _calcular_total(self):
        for rec in self:
            rec.total = rec.duracion_horas * (rec.pista_id.precio_hora or 0)

    @api.constrains("inicio", "fin")
    def _comprobar_fechas(self):
        for rec in self:
            if rec.inicio and rec.fin and rec.fin <= rec.inicio:
                raise ValidationError("La fecha/hora de fin debe ser posterior al inicio.")

    @api.constrains("pista_id", "inicio", "fin", "estado")
    def _comprobar_solape(self):
        for rec in self:
            if not rec.pista_id or not rec.inicio or not rec.fin:
                continue
            if rec.estado == "cancelada":
                continue

            dominio = [
                ("id", "!=", rec.id),
                ("pista_id", "=", rec.pista_id.id),
                ("estado", "!=", "cancelada"),
                ("inicio", "<", rec.fin),
                ("fin", ">", rec.inicio),
            ]
            if self.search_count(dominio) > 0:
                raise ValidationError("Ya existe una reserva que se solapa en esa pista y horario.")

    # --- BOTONES DEL FORMULARIO (coinciden con la vista) ---
    def accion_confirmar(self):
        for rec in self:
            rec.estado = "confirmada"

    def accion_realizada(self):
        for rec in self:
            rec.estado = "realizada"

    def accion_cancelar(self):
        for rec in self:
            rec.estado = "cancelada"

    def accion_imprimir_confirmacion(self):
        accion = self.env.ref("club_padel.accion_reporte_reserva")
        return accion.report_action(self)
