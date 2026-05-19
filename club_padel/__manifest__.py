{
    "name": "Club Pádel",
    "version": "16.0.1.0.0",
    "category": "Services",
    "summary": "Gestión de pistas, reservas y tienda para un club de pádel",
    "author": "Rubén y Ángel",
    "depends": ["base", "contacts", "product", "web", "mail"],
    "data": [
        # ======================
        # SEGURIDAD
        # ======================
        "security/ir.model.access.csv",

        # ======================
        # DATOS / DEMO / SECUENCIAS
        # ======================
        "data/secuencia.xml",
        "data/secuencia_ventas.xml",
        "data/demo_pistas.xml",
        "data/tienda_productos_demo.xml",
        "data/demo_socios_proveedores.xml",
        "data/demo_reservas.xml",

        # ======================
        # REPORTES
        # ======================
        "report/reporte_reserva.xml",

        # ======================
        # VISTAS PRINCIPALES
        # ======================
        "views/pistas_vistas.xml",
        "views/reservas_vistas.xml",
        "views/clientes_vistas.xml",
        "views/productos_vistas.xml",

        # ======================
        # TIENDA (NUEVO)
        # ======================
        "views/tienda_producto_views.xml",
        "views/tienda_productos_action.xml",

        # ======================
        # MENÚ (SIEMPRE AL FINAL)
        # ======================
        "views/menu.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "club_padel/static/src/css/club_padel.css",
        ],
    },
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}
