from odoo import models, fields

class ProductoPadel(models.Model):
    _inherit = "product.template"

    es_producto_padel = fields.Boolean(string="Producto de pádel", default=False)
    tipo_producto_padel = fields.Selection(
        [
            ("pala", "Pala"),
            ("pelotas", "Pelotas"),
            ("grip", "Grip/Overgrip"),
            ("textil", "Textil"),
            ("otros", "Otros"),
        ],
        string="Tipo de producto (pádel)",
    )
