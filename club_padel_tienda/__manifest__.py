{
    "name": "Club Pádel - Tienda (Integración)",
    "version": "16.0.1.0.0",
    "category": "Services",
    "summary": "Conecta reservas del club con productos de la tienda",
    "author": "Rubén y Ángel",
    "depends": ["base", "club_padel", "tienda_padel"],
    "data": [
        "security/ir.model.access.csv",
        "views/carrito_views.xml",
        "views/menu.xml",
    ],
    "application": False,
    "installable": True,
    "license": "LGPL-3",
}
