# Despliegue con Docker — Club Pádel Odoo

## Requisito previo — Instalar Docker

### En Windows

Instala **Docker Desktop** y asegúrate de que esté ejecutándose (icono de la ballena en la barra de tareas).

Descarga: https://www.docker.com/products/docker-desktop/

### En Ubuntu / Linux

Instala Docker Engine y el plugin de Compose con:

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker
```

> El comando `usermod` permite usar Docker sin `sudo`. Si no funciona, cierra sesión y vuelve a entrar.

---

## Paso 1 — Abrir la terminal en la carpeta del proyecto

Abre una terminal (PowerShell o CMD) y navega hasta la carpeta del proyecto:

```bash
cd ruta/a/club-padel-odoo
```

> Si ya estás dentro de la carpeta, puedes saltarte este paso.

---

## Paso 2 — Construir la imagen y preparar la base de datos

Ejecuta este comando **solo la primera vez**. Construye tu imagen personalizada con los módulos del club de pádel e inicializa la base de datos:

```bash
docker compose run --rm odoo odoo -d padel -i tienda_padel,club_padel,club_padel_tienda --without-demo=all --stop-after-init
```

> Tarda unos minutos la primera vez porque descarga las imágenes base de Odoo y PostgreSQL.

---

## Paso 3 — Arrancar los servicios

```bash
docker compose up -d
```

Esto levanta dos contenedores que se quedan corriendo en segundo plano:

| Contenedor | Qué hace |
|------------|----------|
| `odoo` | Servidor web de la aplicación (construido desde tu Dockerfile) |
| `db` | Base de datos PostgreSQL |

---

## Paso 4 — Abrir la aplicación en el navegador

Abre tu navegador y ve a:

```
http://localhost:8069
```

Inicia sesión con:

| Campo | Valor |
|-------|-------|
| Usuario | `admin` |
| Contraseña | `admin` |

---

## Paso 5 — Qué ver dentro de la aplicación

Una vez dentro, ve al menú **Club Pádel** en la barra superior:

| Sección | Qué muestra |
|---------|-------------|
| **Pistas** | Vista kanban y formulario con superficie e iluminación |
| **Reservas** | Lista con estados: borrador, confirmada, realizada, cancelada |
| **Contactos** | Ficha de socio con pestaña Pádel (nivel, mano dominante, pala) |
| **Tienda** | Catálogo de productos del club |

---

## Parar los servicios

```bash
docker compose down
```

Para borrar también los datos y empezar desde cero:

```bash
docker compose down -v
```

---

## Resumen del flujo Docker

```
Dockerfile
    └── define cómo construir la imagen con los módulos del club
            │
            ▼
docker-compose.yml
    ├── construye la imagen con build: .
    ├── levanta el contenedor odoo (puerto 8069) ← aquí está la app
    └── levanta el contenedor db (PostgreSQL)
```
