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

    _sql_constraints = [
        ("codigo_unico", "unique(codigo)", "El código de pista ya existe."),
    ]

    @api.constrains("precio_hora")
    def _comprobar_precio(self):
        for rec in self:
            if rec.precio_hora < 0:
                raise ValidationError("El precio por hora no puede ser negativo.")
