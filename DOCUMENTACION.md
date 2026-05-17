# Documentación técnica — Club Pádel Odoo

**Proyecto:** Implantación y Customización de Odoo 16 — Club Deportivo de Pádel  
**Autores:** Rubén Flores García · Ángel Martínez  
**Módulo:** 2º DAM  
**Fecha:** Mayo 2026

---

## 1. Fuentes consultadas

### Documentación oficial

| Fuente | URL | Para qué se usó |
|--------|-----|-----------------|
| Odoo 16 Developer Documentation | https://www.odoo.com/documentation/16.0/developer.html | Estructura de módulos, `__manifest__.py`, campos, vistas |
| Odoo ORM API Reference | https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html | `@api.depends`, `@api.constrains`, `_inherit` |
| Odoo View Architectures | https://www.odoo.com/documentation/16.0/developer/reference/backend/views.html | Formularios XML, listas, vistas de búsqueda |
| Odoo Security — Access Rights | https://www.odoo.com/documentation/16.0/developer/reference/backend/security.html | Fichero `ir.model.access.csv` |
| Odoo QWeb Reports | https://www.odoo.com/documentation/16.0/developer/reference/backend/reports.html | Informe PDF de reserva |

### Recursos técnicos adicionales

| Fuente | URL | Para qué se usó |
|--------|-----|-----------------|
| Foro oficial Odoo Community | https://www.odoo.com/forum/help-1 | Resolución de errores de carga de módulos |
| Stack Overflow — etiqueta `odoo` | https://stackoverflow.com/questions/tagged/odoo | Problemas con XML views y assets |
| GitHub — módulos de ejemplo Odoo | https://github.com/odoo/odoo/tree/16.0/addons | Referencia de estructura de módulos estándar |
| Docker Hub — imagen odoo:16.0 | https://hub.docker.com/_/odoo | Configuración del entorno Docker |

---

## 2. Uso de herramientas de Inteligencia Artificial

Se utilizaron dos herramientas de IA a lo largo del proyecto: **ChatGPT (OpenAI)** y **Claude Code (Anthropic)**.

---

### 2.1 ChatGPT — Fase inicial del proyecto

**Herramienta:** ChatGPT (chat de grupo compartido entre Rubén y Ángel)  
**Fecha:** Febrero 2026  
**Entorno:** Ubuntu 22 · Odoo 16 como servicio systemd (`odoo16.service`) · usuario `operador_odoo`

---

**Interacción 1: Crear el módulo desde cero**

**Prompt utilizado:**
> "Tengo que realizar este trabajo con mi compañero. Sabemos la temática pero no precisa, nos gustaría que fuese sobre el pádel... Es la segunda vez que pongo este prompt, porque en otro chat se estaba complicando demasiado hasta en la instalación tenemos un usuario operador_odoo y odoo como servicio al encender el ordenador se enciende el servicio, es Ubuntu22 y Odoo16. Es en parejas con Angel, hazme el codigo y todo lo necesario para poder hacerlo paso por paso."

**Respuesta obtenida (resumen):**  
ChatGPT generó la estructura completa del módulo (`padel_club`) con carpetas en inglés (`models/`, `views/`, `security/`), todos los modelos Python (`padel_court.py`, `padel_booking.py`, `res_partner.py`, `product_template.py`), vistas XML, el archivo `ir.model.access.csv`, la secuencia `ir.sequence` y la plantilla QWeb del informe PDF. También incluyó los comandos de Ubuntu para crear archivos y carpetas.

**Cómo se aplicó:**  
Sirvió de base para la estructura completa del proyecto: la organización de carpetas, los modelos de pistas y reservas, la herencia de `res.partner` para datos de jugador, y la herencia de `product.template` para el catálogo de productos.

---

**Interacción 2: Renombrar carpetas al español**

**Prompt utilizado:**
> "espera hazmelo de 0, en español y ponme los comandos necesarios teniendo en cuenta todo, entrar en carpeta salir de carpeta cambiar de usuario y todo. y en español"  
> *(y después)* "creame todas las carpetas en español y luego los .py tambien"

**Respuesta obtenida (resumen):**  
ChatGPT regeneró toda la estructura con nombres en español: `modelos/`, `vistas/`, `seguridad/`, `datos/`, `informes/`, `estatico/` y los archivos `.py` también con nombres en español (`pista_padel.py`, `reserva_padel.py`, `cliente_contacto.py`, `producto_padel.py`). Incluyó los comandos de `mkdir`, `touch` y `nano` con cambios de usuario (`sudo -i -u operador_odoo`).

**Cómo se aplicó:**  
Se creó el módulo `club_padel` con esta estructura. Más adelante, al migrar al entorno Docker se renombraron las carpetas al estándar de Odoo (`models/`, `views/`, etc.) para compatibilidad.

---

**Interacción 3: Problema con `addons_path` — servicio sin config**

**Prompt utilizado:**
> "no existe el odoo16.conf o el odoo.conf he puesto los 4 y en ninguno me pone que existe, y quiero que hagas todo con el usuario operador_odoo que es el que tiene permisos, y si necesito salir del operador_odoo o entrar, dimelo. No encuentro el addonspath"

**Respuesta obtenida (resumen):**  
ChatGPT explicó que si no existe archivo `.conf`, Odoo se lanza sin él y hay que buscar el servicio con `systemctl list-units --type=service | grep -i odoo`. Una vez identificado el servicio (`odoo16.service`), se ve su configuración con `systemctl cat odoo16.service`.

**Prompt de seguimiento:**
> "es odoo16.service y veo solo esto ExecStart=/opt/odoo/odoo-bin"

**Respuesta obtenida:**  
Al no existir config, la solución fue crear un override del servicio con `sudo systemctl edit odoo16.service` añadiendo la línea `--addons-path` con la ruta de los addons del core y la carpeta custom:

```
[Service]
ExecStart=
ExecStart=/opt/odoo/odoo-bin --addons-path=/opt/odoo/odoo/addons,/opt/odoo/custom_addons
```

Y luego `sudo systemctl daemon-reload && sudo systemctl restart odoo16.service`.

**Cómo se aplicó:**  
Permitió que Odoo detectase la carpeta `custom_addons` y cargase el módulo `club_padel`.

---

**Interacción 4: Referencias rotas al renombrar carpetas**

**Prompt utilizado:**
> "algo pasa a ver piensa, no hay otros ficheros que cogen los nombres de las carpetas en español o algo así porque ha sido al cambiar el nombre de la carpeta y el manifest de las carpetas, solo he cambiado eso, tengo que cambiar algo mas"

**Respuesta obtenida (resumen):**  
ChatGPT identificó que al renombrar carpetas no basta con cambiar el `__manifest__.py`. También hay que actualizar: (1) el `__init__.py` raíz (`from . import models`, no `modelos`), (2) el `models/__init__.py` con los nombres correctos de archivos, y (3) cualquier referencia interna en los XML. Proporcionó el comando `grep -R "informes\|vistas\|modelos\|seguridad\|datos\|estatico" -n /opt/odoo/custom_addons/club_padel` para detectar referencias antiguas.

**Cómo se aplicó:**  
Se corrigieron los `__init__.py` y se actualizaron los `report_file` y `report_name` en los XML de informes para que coincidieran con las nuevas rutas.

---

**Interacción 5: Orden del manifest y error en CSS**

**Prompt utilizado:**
> *(pegó el `__manifest__.py` con el orden: vistas → menú → informes)* "es correcto todo?"

**Respuesta obtenida (resumen):**  
ChatGPT señaló dos problemas: (1) los informes deben cargarse **antes** que las vistas si las vistas referencian una acción de informe; el orden correcto es `security → data → report → views → menu`. (2) El archivo CSS tenía el propio comando `cat > estatico/... << 'EOF'` pegado dentro como primera línea en lugar de ser CSS válido, lo que rompía los assets del backend.

**Cómo se aplicó:**  
Se reordenó la lista `data` del manifest y se reescribió el CSS con el contenido correcto. El módulo arrancó sin errores tras estos cambios.

---

### 2.2 Claude Code (Anthropic) — Fase de corrección y mejoras

**Herramienta:** Claude Code CLI (modelo claude-sonnet-4-6)  
**Fecha:** Mayo 2026  
**Conversación completa disponible en el historial del repositorio**

Se utilizó Claude Code para resolver los errores que impedían arrancar los módulos en Docker y para implementar las mejoras de customización requeridas por la corrección del profesor.

---

**Problema 1: Archivo `cliente_contacto.py` inexistente**

**Prompt utilizado:**
> El módulo club_padel no arranca, da este error: `ImportError: cannot import name 'cliente_contacto' from partially initialized module`

**Respuesta obtenida:**  
La IA identificó que `models/__init__.py` importaba `cliente_contacto` pero el archivo no existía. Creó el archivo con la herencia completa de `res.partner` incluyendo campos de jugador de pádel (`nivel_padel`, `mano_dominante`, `marca_pala`, etc.) y dos campos computed: `descripcion_jugador` y `total_reservas`.

**Código generado (fragmento):**
```python
class ClienteContacto(models.Model):
    _inherit = "res.partner"

    es_jugador_padel = fields.Boolean(string="Es jugador/a de pádel", default=False)
    nivel_padel = fields.Selection([
        ("iniciante", "Iniciante"),
        ("intermedio", "Intermedio"),
        ("avanzado", "Avanzado"),
        ("competicion", "Competición"),
    ], string="Nivel de pádel")

    @api.depends("nivel_padel", "marca_pala", "es_jugador_padel", "name")
    def _compute_descripcion_jugador(self):
        for rec in self:
            if rec.es_jugador_padel:
                nivel = dict(rec._fields["nivel_padel"].selection).get(rec.nivel_padel, "Sin nivel")
                rec.descripcion_jugador = f"{rec.name} · {nivel} · ..."
```

---

**Problema 2: Error en `ir.model.access.csv`**

**Prompt utilizado:**
> Nuevo error: `No matching record found for external id 'model_club_padel_tienda_producto'`

**Respuesta obtenida:**  
La IA identificó que el modelo `club_padel.tienda_producto` existía en `tienda_producto.py` pero no estaba importado en `models/__init__.py`. Añadió la línea `from . import tienda_producto` para registrar el modelo en Odoo.

---

**Problema 3: Archivos de demo inexistentes en el manifest**

**Prompt utilizado:**
> Error: `FileNotFoundError: File not found: club_padel/data/demo.xml`

**Respuesta obtenida:**  
El manifest referenciaba `data/demo.xml` y `data/productos_demo.xml` que no existían en el repositorio. Se eliminaron esas líneas del `__manifest__.py`.

---

**Problema 4: Atributo `name` obligatorio en filtros de búsqueda**

**Prompt utilizado:**
> Error al cargar `pistas_vistas.xml`: `Element filter failed to validate attributes`

**Respuesta obtenida:**  
En Odoo 16, todos los elementos `<filter>` de una vista de búsqueda requieren el atributo `name`, incluyendo los de agrupación dentro de `<group>`. Se añadieron los atributos faltantes.

---

**Mejora 5: Campos computed en `pista_padel.py`**

**Prompt utilizado:**
> Añade al modelo pista_padel los campos iluminacion, superficie, etiqueta_pista (computed) y reservas_activas (computed)

**Código generado (fragmento):**
```python
@api.depends("nombre", "tipo_pista", "precio_hora")
def _compute_etiqueta_pista(self):
    for rec in self:
        tipo = dict(rec._fields["tipo_pista"].selection).get(rec.tipo_pista, "")
        rec.etiqueta_pista = f"{rec.nombre} · {tipo} · {rec.precio_hora:.2f}€/h"

@api.depends("reserva_ids", "reserva_ids.estado")
def _compute_reservas_activas(self):
    for rec in self:
        rec.reservas_activas = len(
            rec.reserva_ids.filtered(lambda r: r.estado != "cancelada")
        )
```

---

## 3. División del trabajo entre miembros del equipo

| Tarea | Responsable | Commits relacionados |
|-------|-------------|----------------------|
| Estructura inicial de los tres módulos | Rubén Flores | `feat: add club_padel module` |
| Docker Compose para entorno local | Rubén Flores | `chore: añadir docker-compose.yml` |
| Crear `cliente_contacto.py` (herencia `res.partner`) | Rubén Flores | `fix: crear cliente_contacto.py` |
| Corrección de imports y manifest | Rubén Flores | `fix: añadir import tienda_producto` |
| Campos computed en `pista_padel.py` | Rubén Flores | `feat: campos computed etiqueta_pista` |
| Ampliar vista de contactos (pestaña Pádel) | Ángel Martínez | `feat: ampliar vista contactos` |
| Actualizar formulario de pistas con nuevos campos | Ángel Martínez | `feat: mostrar nuevos campos de pista` |

El historial completo de commits está disponible en: https://github.com/rfloresg/club-padel-odoo/commits/main

---

## 4. Customizaciones técnicas implementadas

### 4.1 Herencia de modelo estándar (`_inherit`)

Se extiende `res.partner` (el modelo de contactos nativo de Odoo) para añadir información específica de jugadores de pádel. Esto es una de las técnicas más importantes de Odoo: en lugar de crear un modelo nuevo desde cero, se añaden campos al modelo existente sin modificar el núcleo del sistema.

```python
class ClienteContacto(models.Model):
    _inherit = "res.partner"   # Hereda y amplía el modelo existente
    es_jugador_padel = fields.Boolean(...)
    nivel_padel = fields.Selection(...)
```

### 4.2 Campos calculados automáticamente (`@api.depends`)

Los campos computed se recalculan solos cuando cambian los campos de los que dependen. Por ejemplo, `descripcion_jugador` se actualiza automáticamente cada vez que cambia el nombre, nivel o marca del jugador:

```python
@api.depends("nivel_padel", "marca_pala", "es_jugador_padel", "name")
def _compute_descripcion_jugador(self):
    for rec in self:
        rec.descripcion_jugador = f"{rec.name} · {nivel} · {marca}"
```

### 4.3 Validaciones con restricciones (`@api.constrains`)

Se valida que los datos sean correctos antes de guardarlos. Por ejemplo, que una reserva no se solape con otra en la misma pista, o que el precio de la pista no sea negativo:

```python
@api.constrains("precio_hora")
def _comprobar_precio(self):
    for rec in self:
        if rec.precio_hora < 0:
            raise ValidationError("El precio no puede ser negativo.")
```

### 4.4 Secuencias automáticas (`ir.sequence`)

Las reservas y ventas generan automáticamente un número de referencia único (RES/0001, RES/0002...) usando el sistema de secuencias de Odoo, definido en `data/secuencia.xml`.

### 4.5 Vistas con visibilidad condicional (`attrs`)

Los campos de la pestaña Pádel en la ficha de contacto solo aparecen cuando el contacto está marcado como jugador, evitando mostrar información irrelevante:

```xml
<field name="nivel_padel"
       attrs="{'invisible': [('es_jugador_padel', '=', False)],
               'required': [('es_jugador_padel', '=', True)]}"/>
```

### 4.6 Informe PDF con QWeb

Se genera un informe imprimible de cada reserva usando el motor de plantillas QWeb de Odoo, definido en `report/plantilla_reporte_reserva.xml`.

---

## 5. Estructura modular y dependencias

```
tienda_padel          ← Sin dependencias propias
      ↓
club_padel            ← Depende de: base, contacts, product, web
      ↓
club_padel_tienda     ← Depende de: club_padel + tienda_padel
```

Este orden es importante: Odoo carga los módulos respetando las dependencias declaradas en cada `__manifest__.py`.
