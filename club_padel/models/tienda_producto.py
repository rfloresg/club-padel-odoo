from odoo import models, fields


class TiendaProducto(models.Model):
    _name = "club_padel.tienda_producto"
    _description = "Producto de Tienda"

    name = fields.Char(string="Nombre", required=True)
    precio = fields.Float(string="Precio (€)", required=True, default=0.0)
    stock = fields.Integer(string="Stock", default=0)
    activo = fields.Boolean(string="Activo", default=True)
    descripcion = fields.Text(string="Descripción")
