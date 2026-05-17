# Club Pádel — Módulo Odoo 16

Proyecto de 2º DAM. Implantación y customización de Odoo 16 para un club deportivo de pádel.

**Autores:** Rubén Flores · Ángel Martínez

---

## ¿Qué hace este proyecto?

Gestiona un club de pádel desde Odoo: reservas de pistas, tienda de productos y la integración entre ambos. Está dividido en tres módulos que se instalan juntos.

| Módulo | Qué hace |
|--------|----------|
| `club_padel` | Pistas, reservas, clientes, ventas directas |
| `tienda_padel` | Catálogo de productos de la tienda |
| `club_padel_tienda` | Une reservas con carritos de la tienda |

---

## Cómo arrancarlo (con Docker)

Requisitos: tener Docker Desktop instalado y corriendo.

**1. Clonar el repositorio**
```bash
git clone https://github.com/rfloresg/club-padel-odoo.git
cd club-padel-odoo
```

**2. Levantar la base de datos**
```bash
docker compose up -d db
```

**3. Instalar los módulos (solo la primera vez)**
```bash
docker compose run --rm odoo odoo -d padel -i tienda_padel,club_padel,club_padel_tienda --without-demo=all --stop-after-init
```

**4. Arrancar Odoo**
```bash
docker compose up -d odoo
```

**5. Abrir el navegador**
```
http://localhost:8069
Usuario: admin
Contraseña: admin
```

---

## Comandos de uso diario

| Acción | Comando |
|--------|---------|
| Parar todo | `docker compose down` |
| Ver logs | `docker compose logs -f odoo` |
| Actualizar módulos tras cambios | `docker compose run --rm odoo odoo -d padel -u club_padel,tienda_padel,club_padel_tienda --stop-after-init` |
| Borrar todo y empezar de cero | `docker compose down -v` |

---

## Estructura del proyecto

```
club_padel/
  models/
    pista_padel.py         → Pistas (con computed fields: etiqueta, reservas activas)
    reserva_padel.py       → Reservas (máquina de estados, validación solapamientos)
    cliente_contacto.py    → Herencia res.partner con campos de jugador de pádel
    producto_padel.py      → Extensión del producto estándar de Odoo
    venta_tienda.py        → Ventas directas sin carrito
    pedido_tienda.py       → Pedidos con líneas de detalle
  views/
    pistas_vistas.xml      → Formulario, lista y kanban de pistas
    reservas_vistas.xml    → Gestión de reservas con estados
    clientes_vistas.xml    → Pestaña Pádel en ficha de contacto
  report/                  → Informe PDF de reserva (QWeb)
  static/src/css/          → Estilos personalizados del backend

tienda_padel/
  models/tienda_producto.py → Productos independientes de la tienda

club_padel_tienda/
  models/carrito.py         → Carrito vinculado a una reserva
```

---

## Tecnologías usadas

- **Odoo 16 Community** — ERP base
- **Python 3** — Modelos y lógica de negocio
- **XML** — Vistas del backend
- **PostgreSQL 15** — Base de datos
- **Docker** — Entorno de desarrollo local
- **Git / GitHub** — Control de versiones
