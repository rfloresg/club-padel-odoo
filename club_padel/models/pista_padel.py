from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PistaPadel(models.Model):
    _name = "club_padel.pista"
    _description = "Pista de pádel"
    _rec_name = "nombre"

    nombre = fields.Char(string="Nombre", required=True)
    codigo = fields.Char(string="Código", required=True)
    activa = fields.Boolean(default=True)

    tipo_pista = fields.Selection(
        [("indoor", "Indoor"), ("outdoor", "Outdoor")],
        string="Tipo de pista",
        default="indoor",
        required=True,
    )

    precio_hora = fields.Float(string="Precio por hora (€)", required=True, default=18.0)
    notas = fields.Text(string="Notas")

    iluminacion = fields.Boolean(string="Tiene iluminación", default=False)

    superficie = fields.Selection(
        [
            ("cesped_artificial", "Césped artificial"),
            ("cristal", "Cristal"),
            ("moqueta", "Moqueta"),
        ],
        string="Superficie",
        default="cesped_artificial",
    )

    etiqueta_pista = fields.Char(
        string="Etiqueta",
        compute="_compute_etiqueta_pista",
        store=True,
    )

    reserva_ids = fields.One2many(
        "club_padel.reserva",
        "pista_id",
        string="Reservas",
    )

    reservas_activas = fields.Integer(
        string="Reservas activas",
        compute="_compute_reservas_activas",
        store=True,
    )

    _sql_constraints = [
        ("codigo_unico", "unique(codigo)", "El código de pista ya existe."),
    ]

    @api.depends("nombre", "tipo_pista", "precio_hora")
    def _compute_etiqueta_pista(self):
        for rec in self:
            tipo = dict(rec._fields["tipo_pista"].selection).get(rec.tipo_pista, "")
            rec.etiqueta_pista = f"{rec.nombre} · {tipo} · {rec.precio_hora:.2f}€/h"

    @api.depends("reserva_ids", "reserva_ids.estado")
    def _compute_reservas_activas(self):
        for rec in self:
            rec.reservas_activas = len(
                rec.reserva_ids.filtered(lambda r: r.estado != "cancelada")
            )

    @api.constrains("precio_hora")
    def _comprobar_precio(self):
        for rec in self:
            if rec.precio_hora < 0:
                raise ValidationError("El precio por hora no puede ser negativo.")
