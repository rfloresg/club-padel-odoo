# Guía de ejecución — Club Pádel (Odoo 16)

## Requisito previo

Tener **Docker Desktop** instalado y ejecutándose.
Descargar desde: https://www.docker.com/products/docker-desktop/

> Si Docker Desktop está abierto y en la barra de tareas aparece el icono de la ballena, está listo.

---

## Pasos para arrancar el proyecto

### 1. Clonar el repositorio

Abrir una terminal (PowerShell o CMD) y ejecutar:

```bash
git clone https://github.com/rfloresg/club-padel-odoo.git
cd club-padel-odoo
```

---

### 2. Instalar los módulos (solo la primera vez)

Este comando crea la base de datos y carga los datos de demostración:

```bash
docker compose run --rm odoo odoo -d padel -i tienda_padel,club_padel,club_padel_tienda --without-demo=all --stop-after-init
```

> Tarda unos minutos la primera vez porque descarga las imágenes de Odoo y PostgreSQL.

---

### 3. Arrancar Odoo

```bash
docker compose up -d
```

---

### 4. Abrir en el navegador

```
http://localhost:8069
```

| Campo | Valor |
|-------|-------|
| Usuario | `admin` |
| Contraseña | `admin` |

---

## Qué ver en la aplicación

Una vez dentro, ir al menú **Club Pádel** (barra superior):

| Sección | Qué muestra |
|---------|-------------|
| **Pistas** | Vista kanban y formulario con superficie, iluminación y campos calculados |
| **Reservas** | Lista con badges de color por estado (borrador, confirmada, realizada, cancelada) |
| **Contactos** | Ficha de socio con pestaña Pádel (nivel, mano dominante, pala) |
| **Tienda** | Catálogo de productos |

---

## Parar el proyecto

```bash
docker compose down
```

Para borrar también los datos y empezar de cero:

```bash
docker compose down -v
```
