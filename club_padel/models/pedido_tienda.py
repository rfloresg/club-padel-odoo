from odoo import models, fields, api


class PedidoTienda(models.Model):
    _name = "club_padel.pedido_tienda"
    _description = "Pedido Tienda"
    _rec_name = "referencia"

    referencia = fields.Char(string="Referencia", default="Nuevo", readonly=True)
    cliente_id = fields.Many2one("res.partner", string="Cliente", required=True)
    reserva_id = fields.Many2one("club_padel.reserva", string="Reserva vinculada")
    fecha = fields.Datetime(string="Fecha", default=fields.Datetime.now)

    linea_ids = fields.One2many("club_padel.pedido_tienda_linea", "pedido_id", string="Líneas")

    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id.id)
    total = fields.Monetary(string="Total", compute="_compute_total", store=True)

    estado = fields.Selection([
        ("borrador", "Borrador"),
        ("pagado", "Pagado"),
        ("cancelado", "Cancelado"),
    ], default="borrador", string="Estado")

    @api.model
    def create(self, vals):
        if vals.get("referencia", "Nuevo") == "Nuevo":
            vals["referencia"] = self.env["ir.sequence"].next_by_code("club_padel.pedido_tienda") or "PED-0000"
        return super().create(vals)

    @api.depends("linea_ids.subtotal")
    def _compute_total(self):
        for p in self:
            p.total = sum(p.linea_ids.mapped("subtotal"))

    def accion_marcar_pagado(self):
        for p in self:
            p.estado = "pagado"

    def accion_cancelar(self):
        for p in self:
            p.estado = "cancelado"


class PedidoTiendaLinea(models.Model):
    _name = "club_padel.pedido_tienda_linea"
    _description = "Línea Pedido Tienda"

    pedido_id = fields.Many2one("club_padel.pedido_tienda", required=True, ondelete="cascade")
    producto_id = fields.Many2one("product.product", string="Producto", required=True)
    cantidad = fields.Float(string="Cantidad", default=1)
    precio = fields.Float(string="Precio", related="producto_id.lst_price", store=True, readonly=False)
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)

    @api.depends("cantidad", "precio")
    def _compute_subtotal(self):
        for l in self:
            l.subtotal = (l.cantidad or 0) * (l.precio or 0)
