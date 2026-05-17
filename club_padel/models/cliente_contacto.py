from odoo import models, fields, api


class ClienteContacto(models.Model):
    _inherit = "res.partner"

    es_jugador_padel = fields.Boolean(string="Es jugador/a de pádel", default=False)

    nivel_padel = fields.Selection(
        [
            ("iniciante", "Iniciante"),
            ("intermedio", "Intermedio"),
            ("avanzado", "Avanzado"),
            ("competicion", "Competición"),
        ],
        string="Nivel de pádel",
    )

    mano_dominante = fields.Selection(
        [("diestra", "Diestra"), ("zurda", "Zurda")],
        string="Mano dominante",
    )

    marca_pala = fields.Selection(
        [
            ("bullpadel", "Bullpadel"),
            ("head", "Head"),
            ("babolat", "Babolat"),
            ("adidas", "Adidas"),
            ("nox", "Nox"),
            ("otra", "Otra"),
        ],
        string="Marca de la pala",
    )

    modelo_pala = fields.Char(string="Modelo de la pala")

    descripcion_jugador = fields.Char(
        string="Descripción del jugador",
        compute="_compute_descripcion_jugador",
        store=True,
        readonly=True,
    )

    reserva_ids = fields.One2many(
        "club_padel.reserva",
        "cliente_id",
        string="Reservas del socio",
    )

    total_reservas = fields.Integer(
        string="Total de reservas",
        compute="_compute_total_reservas",
        store=True,
    )

    @api.depends("nivel_padel", "marca_pala", "es_jugador_padel", "name")
    def _compute_descripcion_jugador(self):
        for rec in self:
            if rec.es_jugador_padel:
                nivel = dict(rec._fields["nivel_padel"].selection).get(
                    rec.nivel_padel, "Sin nivel"
                )
                marca = (
                    dict(rec._fields["marca_pala"].selection).get(rec.marca_pala, "Sin marca")
                    if rec.marca_pala
                    else "Sin marca registrada"
                )
                rec.descripcion_jugador = f"{rec.name} · {nivel} · {marca}"
            else:
                rec.descripcion_jugador = ""

    @api.depends("reserva_ids")
    def _compute_total_reservas(self):
        for rec in self:
            rec.total_reservas = len(rec.reserva_ids)
