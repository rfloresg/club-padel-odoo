# Club Pádel — Módulo Odoo 16

![Odoo](https://img.shields.io/badge/Odoo-16.0-714B67?logo=odoo&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-LGPL--3-blue)

Proyecto de 2º DAM — Implantación y customización de Odoo 16 para la gestión integral de un club deportivo de pádel.

**Autores:** Rubén Flores · Ángel Martínez

---

## Descripción

Este proyecto implementa tres módulos interconectados sobre Odoo 16 Community que cubren las operaciones principales de un club de pádel: gestión de pistas, reservas con control de solapamientos, ficha de socio extendida con datos de jugador, tienda interna de productos y un módulo puente que une reservas con carritos de compra.

---

## Características principales

### Pistas
- Alta de pistas con tipo (Indoor / Outdoor), superficie (césped artificial, cristal, moqueta) e iluminación
- Precio por hora con validación (`@api.constrains`)
- Código de pista único (restricción SQL)
- Campos calculados automáticos (`@api.depends`):
  - **Etiqueta** — resumen compacto: `Pista Central · Indoor · 18.00€/h`
  - **Reservas activas** — conteo excluyendo canceladas
  - **Ingresos totales** — suma de reservas realizadas

### Reservas
- Referencia automática por secuencia (`ir.sequence`): `RES-0001`, `RES-0002`...
- Máquina de estados con botones de acción:

  ```
  Borrador ──► Confirmada ──► Realizada
      └──────────────────────► Cancelada
  ```

- Duración y total calculados en tiempo real sobre el precio/hora de la pista
- Validación de fechas: el fin debe ser posterior al inicio
- **Validación de solapamientos**: impide reservar la misma pista en el mismo horario
- `@api.onchange`: rellena automáticamente las observaciones al seleccionar pista
- Chatter integrado (`mail.thread`) — registro de cambios de estado
- Informe PDF de confirmación de reserva (QWeb)

### Clientes / Socios
- Herencia de `res.partner` (módulo estándar de contactos de Odoo)
- Campos adicionales por jugador: nivel, mano dominante, marca y modelo de pala
- Visibilidad condicional: los campos de pádel solo aparecen si el contacto es jugador
- Campo calculado **descripción del jugador**: `Rubén Flores · Avanzado · Bullpadel`
- Historial de reservas del socio integrado en su ficha de contacto

### Tienda y ventas
- Catálogo de productos propio (`tienda_padel`) con stock e imagen
- Carrito vinculado a una reserva (`club_padel_tienda`) — patrón módulo puente para evitar dependencias circulares
- Ventas directas sin reserva (`club_padel.venta`)
- Pedidos con líneas de detalle (`club_padel.pedido_tienda`)

---

## Arquitectura de módulos

| Módulo | Rol | Depende de |
|--------|-----|-----------|
| `tienda_padel` | Catálogo independiente de la tienda | `base`, `web` |
| `club_padel` | Núcleo: pistas, reservas, clientes, ventas | `base`, `contacts`, `product`, `mail` |
| `club_padel_tienda` | Puente: une reservas con carritos | `club_padel`, `tienda_padel` |

> El orden de instalación importa: `tienda_padel` → `club_padel` → `club_padel_tienda`

---

## Entorno de desarrollo (Windows)

El proyecto se ha desarrollado en un ordenador con **Windows 11** usando las siguientes herramientas:

### Herramientas instaladas

| Herramienta | Versión | Para qué se usa |
|-------------|---------|-----------------|
| **Docker Desktop** | Latest | Ejecutar Odoo y PostgreSQL sin instalarlos manualmente |
| **PyCharm** | Community | Editar el código Python y XML del módulo |
| **Git** | Latest | Control de versiones y subida a GitHub |

### Cómo está montado el entorno

```
Windows 11
│
├── Docker Desktop (WSL2 en segundo plano)
│   ├── Contenedor: odoo:16.0  ──► accesible en http://localhost:8069
│   └── Contenedor: postgres:15 ──► base de datos "padel"
│
└── PyCharm
    └── Abre la carpeta del repositorio directamente
        └── Los cambios en el código se leen en tiempo real por Docker
            (volumen montado: .:/mnt/extra-addons)
```

### Pasos que seguimos para montar el entorno desde cero

**1. Instalar Docker Desktop**
- Descargar desde [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
- Instalar y reiniciar el ordenador
- Verificar que funciona: abrir una terminal y ejecutar `docker --version`

**2. Instalar PyCharm Community**
- Descargar desde [jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/download/)
- Instalar con las opciones por defecto
- Abrir la carpeta del repositorio con *File → Open*

**3. Clonar el repositorio**
```bash
git clone https://github.com/rfloresg/club-padel-odoo.git
cd club-padel-odoo
```

**4. Levantar los contenedores**
```bash
docker compose up -d
```
Esto descarga las imágenes de Odoo 16 y PostgreSQL 15 (solo la primera vez tarda, unos minutos) y arranca ambos servicios.

**5. Instalar los módulos en la base de datos**
```bash
docker compose run --rm odoo odoo \
  -d padel \
  -i tienda_padel,club_padel,club_padel_tienda \
  --without-demo=all \
  --stop-after-init
```

**6. Flujo de trabajo diario**

Cada vez que se modifica un archivo `.py` o `.xml`:
1. Guardar el archivo en PyCharm
2. Ejecutar el comando de actualización de módulos (ver sección siguiente)
3. Refrescar el navegador en `http://localhost:8069`

> No hace falta reiniciar Docker cada vez. El volumen montado hace que Docker lea los archivos directamente desde la carpeta del proyecto en Windows.

---

## Instalación con Docker

**Requisito previo:** Docker Desktop instalado y en ejecución.

### Primera vez

```bash
# 1. Clonar el repositorio
git clone https://github.com/rfloresg/club-padel-odoo.git
cd club-padel-odoo

# 2. Levantar la base de datos
docker compose up -d db

# 3. Instalar los módulos (crea la base de datos y carga datos demo)
docker compose run --rm odoo odoo \
  -d padel \
  -i tienda_padel,club_padel,club_padel_tienda \
  --without-demo=all \
  --stop-after-init

# 4. Arrancar Odoo
docker compose up -d odoo
```

### Acceder a Odoo

```
URL:        http://localhost:8069
Usuario:    admin
Contraseña: admin
```

---

## Comandos de uso diario

| Acción | Comando |
|--------|---------|
| Arrancar todo | `docker compose up -d` |
| Parar todo | `docker compose down` |
| Ver logs en tiempo real | `docker compose logs -f odoo` |
| Actualizar módulos tras cambios en el código | `docker compose run --rm odoo odoo -d padel -u club_padel,tienda_padel,club_padel_tienda --stop-after-init` |
| Reiniciar solo Odoo (sin BD) | `docker compose restart odoo` |
| Borrar todo y empezar de cero | `docker compose down -v` |

---

## Estructura del proyecto

```
club_padel/
├── models/
│   ├── pista_padel.py          → Pistas (computed fields, constrains de precio)
│   ├── reserva_padel.py        → Reservas (estado, solapamiento, secuencia, PDF)
│   ├── cliente_contacto.py     → Herencia res.partner con campos de jugador
│   ├── producto_padel.py       → Extensión del producto estándar de Odoo
│   ├── venta_tienda.py         → Ventas directas sin carrito
│   └── pedido_tienda.py        → Pedidos con líneas de detalle
├── views/
│   ├── pistas_vistas.xml       → Form, lista y kanban de pistas
│   ├── reservas_vistas.xml     → Gestión de reservas con botones de estado
│   ├── clientes_vistas.xml     → Pestaña Pádel en ficha de contacto
│   └── menu.xml                → Menú principal del módulo
├── data/
│   ├── secuencia.xml           → Secuencia automática RES-XXXX
│   ├── demo_pistas.xml         → Pistas de ejemplo
│   └── demo_reservas.xml       → Reservas de ejemplo
├── report/
│   └── reporte_reserva.xml     → Informe PDF QWeb de reserva
├── security/
│   └── ir.model.access.csv     → Permisos de acceso a modelos
└── static/src/css/
    └── club_padel.css          → Estilos del backend (kanban, badges)

tienda_padel/
└── models/
    └── tienda_producto.py      → Productos independientes de la tienda

club_padel_tienda/
└── models/
    └── carrito.py              → Carrito vinculado a una reserva
```

---

## Tecnologías

| Tecnología | Uso |
|-----------|-----|
| **Odoo 16 Community** | ERP base — framework MVC, ORM, vistas XML |
| **Python 3.10** | Modelos, lógica de negocio, decoradores de API |
| **PostgreSQL 15** | Base de datos relacional |
| **QWeb** | Motor de plantillas para informes PDF |
| **Docker / Docker Compose** | Entorno de desarrollo reproducible |
| **Git / GitHub** | Control de versiones y colaboración |

---

## Equipo

| Miembro | GitHub | Contribución |
|---------|--------|-------------|
| Rubén Flores | [@rfloresg](https://github.com/rfloresg) | **70% del código** — modelos de pistas, reservas y clientes, vistas XML, CSS personalizado, informes QWeb, módulo `tienda_padel` y módulo puente `club_padel_tienda` |
| Ángel Martínez | [@AngelMartinez10](https://github.com/AngelMartinez10) | **70% de la documentación** — redacción de la memoria técnica, análisis de requisitos, diagramas, registro de conversaciones con IA y valoración del trabajo en equipo |

---

## Contexto académico

Proyecto final de **Implantación de Sistemas ERP-CRM** — 2º DAM.

El objetivo es demostrar la capacidad de extender un ERP real mediante módulos propios: herencia de modelos estándar, campos computados, validaciones, informes y arquitectura modular.
