from odoo import models, fields


class TiendaPadelProducto(models.Model):
    _name = "tienda_padel.producto"
    _description = "Producto Tienda Pádel"
    _rec_name = "nombre"

    nombre = fields.Char(string="Nombre", required=True)
    categoria = fields.Selection(
        [
            ("palas", "Palas"),
            ("pelotas", "Pelotas"),
            ("textil", "Textil"),
            ("accesorios", "Accesorios"),
        ],
        string="Categoría",
        default="accesorios",
        required=True
    )
    precio = fields.Float(string="Precio (€)", default=0.0)
    stock = fields.Integer(string="Stock", default=0)
    activo = fields.Boolean(string="Activo", default=True)
    descripcion = fields.Text(string="Descripción")
    imagen = fields.Image(string="Imagen")
