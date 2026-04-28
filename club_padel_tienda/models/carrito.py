from odoo import models, fields, api


class ClubPadelTiendaCarrito(models.Model):
    _name = "club_padel_tienda.carrito"
    _description = "Carrito de tienda para una reserva"
    _rec_name = "name"

    name = fields.Char(string="Carrito", compute="_compute_name", store=True)
    reserva_id = fields.Many2one("club_padel.reserva", string="Reserva", required=True, ondelete="cascade")

    linea_ids = fields.One2many(
        "club_padel_tienda.carrito_linea",
        "carrito_id",
        string="Líneas"
    )

    total = fields.Float(string="Total (€)", compute="_compute_total", store=True)

    @api.depends("reserva_id")
    def _compute_name(self):
        for rec in self:
            # No asumimos el nombre de campo de la reserva (puede ser referencia, name, etc.)
            # Mostramos "Reserva <id>" para no fallar nunca.
            rec.name = f"Carrito - Reserva {rec.reserva_id.id}" if rec.reserva_id else "Carrito"

    @api.depends("linea_ids.subtotal")
    def _compute_total(self):
        for rec in self:
            rec.total = sum(rec.linea_ids.mapped("subtotal"))


class ClubPadelTiendaCarritoLinea(models.Model):
    _name = "club_padel_tienda.carrito_linea"
    _description = "Línea de carrito"

    carrito_id = fields.Many2one("club_padel_tienda.carrito", string="Carrito", required=True, ondelete="cascade")
    producto_id = fields.Many2one("tienda_padel.producto", string="Producto", required=True)

    cantidad = fields.Float(string="Cantidad", default=1.0)
    precio = fields.Float(string="Precio (€)", related="producto_id.precio", store=True, readonly=True)
    subtotal = fields.Float(string="Subtotal (€)", compute="_compute_subtotal", store=True)

    @api.depends("cantidad", "precio")
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = (line.cantidad or 0.0) * (line.precio or 0.0)
