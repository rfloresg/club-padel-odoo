from odoo import models, fields, api


class ClubPadelVenta(models.Model):
    _name = "club_padel.venta"
    _description = "Venta Tienda Club Pádel"
    _rec_name = "referencia"

    referencia = fields.Char(string="Referencia", readonly=True, copy=False, default="Nueva")

    cliente_id = fields.Many2one("res.partner", string="Cliente", required=True)
    producto_id = fields.Many2one("product.product", string="Producto", required=True)

    cantidad = fields.Integer(string="Cantidad", default=1, required=True)

    precio_unitario = fields.Float(string="Precio unitario", readonly=True)
    total = fields.Float(string="Total", compute="_compute_total", store=True)

    fecha = fields.Datetime(string="Fecha", default=fields.Datetime.now, required=True)
    notas = fields.Text(string="Notas")

    estado = fields.Selection([
        ("borrador", "Borrador"),
        ("pagada", "Pagada"),
        ("cancelada", "Cancelada"),
    ], string="Estado", default="borrador", required=True)

    @api.model
    def create(self, vals):
        if vals.get("referencia", "Nueva") == "Nueva":
            vals["referencia"] = self.env["ir.sequence"].next_by_code("club_padel.venta") or "V000"
        return super().create(vals)

    @api.onchange("producto_id")
    def _onchange_producto(self):
        if self.producto_id:
            self.precio_unitario = self.producto_id.lst_price

    @api.depends("cantidad", "precio_unitario")
    def _compute_total(self):
        for r in self:
            r.total = (r.cantidad or 0) * (r.precio_unitario or 0)

    def accion_marcar_pagada(self):
        for r in self:
            r.estado = "pagada"

    def accion_cancelar(self):
        for r in self:
            r.estado = "cancelada"
