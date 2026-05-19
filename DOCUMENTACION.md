# Documentación técnica — Club Pádel Odoo

**Proyecto:** Implantación y Customización de Odoo 16 — Club Deportivo de Pádel  
**Autores:** Rubén Flores García · Ángel Martínez  
**Módulo:** 2º DAM  
**Fecha:** Mayo 2026

---

## 1. Fuentes consultadas

### Documentación oficial de Odoo

| Fuente | URL | Para qué se usó |
|--------|-----|-----------------|
| Odoo 16 Developer Docs | https://www.odoo.com/documentation/16.0/developer.html | Estructura de módulos, `__manifest__.py`, campos, vistas |
| Odoo ORM API Reference | https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html | `@api.depends`, `@api.constrains`, `@api.onchange`, `_inherit` |
| Odoo View Architectures | https://www.odoo.com/documentation/16.0/developer/reference/backend/views.html | Formularios, listas, kanban, calendar, graph, pivot, search |
| Odoo Security — Access Rights | https://www.odoo.com/documentation/16.0/developer/reference/backend/security.html | Fichero `ir.model.access.csv` |
| Odoo QWeb Reports | https://www.odoo.com/documentation/16.0/developer/reference/backend/reports.html | Informe PDF de reserva con plantilla QWeb |
| Odoo Mail — Chatter | https://www.odoo.com/documentation/16.0/developer/reference/backend/mixins.html | `mail.thread`, `mail.activity.mixin`, `tracking=True` |
| Odoo Data Files | https://www.odoo.com/documentation/16.0/developer/reference/backend/data.html | Archivos XML de datos demo (`noupdate="1"`) |
| Odoo Frontend Assets | https://www.odoo.com/documentation/16.0/developer/reference/frontend/assets.html | CSS personalizado cargado con `web.assets_backend` |

### Recursos técnicos adicionales

| Fuente | URL | Para qué se usó |
|--------|-----|-----------------|
| Foro oficial Odoo Community | https://www.odoo.com/forum/help-1 | Resolución de errores de carga de módulos |
| Stack Overflow — etiqueta `odoo` | https://stackoverflow.com/questions/tagged/odoo | Problemas con XML views, assets y caché |
| GitHub — addons oficiales Odoo 16 | https://github.com/odoo/odoo/tree/16.0/addons | Referencia de estructura y patrones de módulos estándar |
| Docker Hub — imagen odoo:16.0 | https://hub.docker.com/_/odoo | Configuración del entorno Docker con variables de entorno |

---

## 2. Entorno de desarrollo y herramientas utilizadas

### 2.1 IDE: PyCharm Professional

El desarrollo del proyecto se realizó íntegramente con **PyCharm Professional** (JetBrains) en lugar de editores de terminal como `nano`. PyCharm ofrece resaltado de sintaxis para Python y XML, autocompletado inteligente, navegación directa entre archivos y depuración con puntos de interrupción (breakpoints), lo que permite identificar errores en el código Python sin necesidad de releer los logs completos de Odoo.

**Flujo de trabajo real:**

1. Se edita el código Python o XML directamente en PyCharm.
2. Se ejecuta el comando de actualización del módulo desde la terminal integrada:
   ```bash
   docker compose run --rm odoo odoo -d padel -u club_padel --stop-after-init
   ```
3. Si hay error, se lee el traceback en la terminal y se navega directamente a la línea indicada desde PyCharm.
4. Se confirman los cambios con Git desde la pestaña de control de versiones integrada del IDE.

### 2.2 Plugins instalados en PyCharm

| Plugin | Para qué se usó |
|--------|-----------------|
| **Python** (built-in) | Autocompletado, análisis estático y depurador de Python |
| **Docker** | Ver contenedores, logs y estado de Odoo y PostgreSQL sin salir del IDE |
| **Git Integration** (built-in) | Commits, historial y comparación de cambios desde el IDE |
| **Rainbow CSV** | Edición del archivo `ir.model.access.csv` con columnas coloreadas |
| **XML** (built-in) | Validación y formateo automático de los archivos de vistas XML de Odoo |
| **.env files support** | Lectura de variables de entorno del `docker-compose.yml` |

### 2.3 Control de versiones con Git y GitHub

El repositorio está alojado en GitHub: `https://github.com/rfloresg/club-padel-odoo`. Se trabajó con una sola rama (`main`) haciendo commits frecuentes para mantener un historial claro del progreso de cada miembro. Para el trabajo remoto se usó `git push` / `git pull` entre los dos ordenadores, evitando conflictos al no editar el mismo archivo simultáneamente.

---

## 3. Uso de herramientas de Inteligencia Artificial

Se utilizaron dos herramientas de IA a lo largo del proyecto: **ChatGPT (OpenAI)** en la fase inicial y **Claude Code (Anthropic)** en la fase de corrección y mejoras.

---

### 3.1 ChatGPT — Fase inicial del proyecto

**Herramienta:** ChatGPT (chat de grupo compartido entre Rubén y Ángel)  
**Fecha:** Febrero 2026  
**Entorno:** Ubuntu 22 · Odoo 16 como servicio systemd (`odoo16.service`) · usuario `operador_odoo`

---

**Interacción 1: Crear el módulo desde cero**

**Prompt utilizado:**
> "Tengo que realizar este trabajo con mi compañero. Nos gustaría que fuese sobre el pádel... tenemos un usuario operador_odoo y odoo como servicio, es Ubuntu22 y Odoo16. Es en parejas con Angel, hazme el codigo y todo lo necesario para poder hacerlo paso por paso."

**Respuesta obtenida (resumen):**  
ChatGPT generó la estructura completa del módulo con carpetas en inglés (`models/`, `views/`, `security/`), todos los modelos Python, vistas XML, el archivo `ir.model.access.csv`, la secuencia `ir.sequence` y la plantilla QWeb del informe PDF. También incluyó los comandos de Ubuntu para crear archivos y carpetas.

**Cómo se aplicó:**  
Sirvió de base para la estructura del proyecto: organización de carpetas, modelos de pistas y reservas, herencia de `res.partner` para datos de jugador, y herencia de `product.template` para el catálogo de productos.

---

**Interacción 2: Renombrar todo al español**

**Prompts utilizados:**
> "espera hazmelo de 0, en español y ponme los comandos necesarios teniendo en cuenta todo, entrar en carpeta salir de carpeta cambiar de usuario y todo. y en español"  
> "creame todas las carpetas en español y luego los .py tambien"

**Respuesta obtenida (resumen):**  
ChatGPT regeneró la estructura con nombres en español: `modelos/`, `vistas/`, `seguridad/`, `datos/`, `informes/`, `estatico/` y los archivos `.py` con nombres en español. Incluyó comandos `mkdir`, `touch` y `nano` con cambios de usuario (`sudo -i -u operador_odoo`).

**Cómo se aplicó:**  
Se creó el módulo con esa estructura. Al migrar a Docker se renombraron al estándar de Odoo (`models/`, `views/`, etc.) para compatibilidad.

---

**Interacción 3: Problema con `addons_path` — servicio sin config**

**Prompt utilizado:**
> "no existe el odoo16.conf o el odoo.conf he puesto los 4 y en ninguno me pone que existe... No encuentro el addonspath"

**Respuesta y seguimiento:**  
ChatGPT identificó que el servicio era `odoo16.service` y arrancaba solo con `ExecStart=/opt/odoo/odoo-bin` sin archivo de configuración. La solución fue un override del servicio:

```
[Service]
ExecStart=
ExecStart=/opt/odoo/odoo-bin --addons-path=/opt/odoo/odoo/addons,/opt/odoo/custom_addons
```

Luego `sudo systemctl daemon-reload && sudo systemctl restart odoo16.service`.

**Cómo se aplicó:**  
Permitió que Odoo detectase la carpeta `custom_addons` y cargase el módulo `club_padel`.

---

**Interacción 4: Referencias rotas al renombrar carpetas**

**Prompt utilizado:**
> "algo pasa a ver piensa, no hay otros ficheros que cogen los nombres de las carpetas en español... solo he cambiado eso, tengo que cambiar algo mas"

**Respuesta obtenida:**  
Al renombrar carpetas no basta con el `__manifest__.py`. Hay que actualizar también el `__init__.py` raíz y el `models/__init__.py`. Proporcionó el comando `grep -R "informes\|vistas\|modelos" -n /opt/odoo/custom_addons/club_padel` para detectar referencias antiguas.

---

**Interacción 5: Orden del manifest y error en CSS**

**Prompt utilizado:**
> *(pegó el `__manifest__.py`)* "es correcto todo?"

**Respuesta obtenida:**  
Dos problemas: (1) los reportes deben cargarse **antes** que las vistas que los referencian; orden correcto: `security → data → report → views → menu`. (2) El archivo CSS tenía el comando `cat > estatico/... << 'EOF'` pegado como primera línea en lugar de CSS válido.

---

### 3.2 Claude Code — Fase de corrección de errores (Docker)

**Herramienta:** Claude Code CLI (modelo claude-sonnet-4-6) · **Fecha:** Mayo 2026

---

**Problema 1: `ImportError` — `cliente_contacto.py` inexistente**

**Prompt:**
> `ImportError: cannot import name 'cliente_contacto' from partially initialized module`

**Solución:** `models/__init__.py` importaba `cliente_contacto` pero el archivo no existía. Se creó con herencia completa de `res.partner` incluyendo campos de jugador (`nivel_padel`, `mano_dominante`, `marca_pala`) y campos computed (`descripcion_jugador`, `total_reservas`).

```python
class ClienteContacto(models.Model):
    _inherit = "res.partner"

    nivel_padel = fields.Selection([
        ("iniciante", "Iniciante"), ("intermedio", "Intermedio"),
        ("avanzado", "Avanzado"), ("competicion", "Competición"),
    ], string="Nivel de pádel")

    @api.depends("nivel_padel", "marca_pala", "es_jugador_padel", "name")
    def _compute_descripcion_jugador(self):
        for rec in self:
            nivel = dict(rec._fields["nivel_padel"].selection).get(rec.nivel_padel, "")
            rec.descripcion_jugador = f"{rec.name} · {nivel} · {rec.marca_pala or ''}"
```

---

**Problema 2: `model_club_padel_tienda_producto` no encontrado**

**Prompt:**
> `No matching record found for external id 'model_club_padel_tienda_producto'`

**Solución:** El modelo existía en `tienda_producto.py` pero no estaba importado en `models/__init__.py`. Se añadió `from . import tienda_producto`.

---

**Problema 3: `FileNotFoundError` — archivos demo inexistentes**

**Prompt:**
> `FileNotFoundError: File not found: club_padel/data/demo.xml`

**Solución:** El manifest declaraba `data/demo.xml` y `data/productos_demo.xml` que no existían. Se eliminaron esas líneas del `__manifest__.py`.

---

**Problema 4: Filtros de búsqueda sin atributo `name`**

**Prompt:**
> `Element filter failed to validate attributes` al cargar `pistas_vistas.xml`

**Solución:** En Odoo 16, todos los `<filter>` requieren atributo `name`, incluyendo los de agrupación dentro de `<group>`. Se añadieron los atributos faltantes.

---

**Mejora: Campos computed en `pista_padel.py`**

**Prompt:**
> Añade al modelo pista_padel los campos `iluminacion`, `superficie`, `etiqueta_pista` (computed) y `reservas_activas` (computed)

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

### 3.3 Claude Code — Fase de mejoras (tercer trimestre)

**Herramienta:** Claude Code CLI (modelo claude-sonnet-4-6) · **Fecha:** Mayo 2026

---

**Mejora 1: Módulo `mail` — chatter en reservas**

**Prompt:**
> Quiero añadir el chatter de Odoo a las reservas para que queden registrados los cambios de estado y se puedan dejar notas. ¿Qué hay que hacer?

**Respuesta obtenida:**  
El módulo `mail` de Odoo incluye dos mixins: `mail.thread` añade el panel de mensajes y `mail.activity.mixin` añade actividades programadas. Se necesita: (1) añadir `"mail"` a `depends` en el manifest, (2) añadir `_inherit = ["mail.thread", "mail.activity.mixin"]` al modelo, (3) añadir el bloque `<div class="oe_chatter">` en la vista. El campo `tracking=True` registra automáticamente cada cambio de estado en el historial.

**Fuente consultada:** https://www.odoo.com/documentation/16.0/developer/reference/backend/mixins.html

```python
class ReservaPadel(models.Model):
    _name = "club_padel.reserva"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    estado = fields.Selection([...], tracking=True)
```

```xml
<div class="oe_chatter">
    <field name="message_follower_ids"/>
    <field name="activity_ids"/>
    <field name="message_ids"/>
</div>
```

---

**Mejora 2: `@api.onchange` — autocompletar al elegir pista**

**Prompt:**
> Quiero que cuando el usuario seleccione una pista en el formulario de reserva, se rellene el campo de observaciones automáticamente. ¿Qué decorador uso?

**Respuesta obtenida:**  
`@api.onchange` se ejecuta en tiempo real mientras el usuario rellena el formulario (antes de guardar), a diferencia de `@api.depends` (que actúa al guardar) y `@api.constrains` (que valida al guardar). Es el tercer decorador del proyecto.

**Fuente consultada:** https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html

```python
@api.onchange("pista_id")
def _onchange_pista_id(self):
    if self.pista_id and not self.observaciones:
        self.observaciones = (
            f"Pista {self.pista_id.nombre} "
            f"({self.pista_id.tipo_pista}) — "
            f"{self.pista_id.precio_hora:.2f}€/h"
        )
```

---

**Mejora 3: Vistas `graph` y `pivot` — análisis de reservas**

**Prompt:**
> Añade al módulo de reservas una vista de gráfico de barras y una tabla dinámica para ver los ingresos y horas por pista y por estado.

**Respuesta obtenida:**  
Las vistas `graph` y `pivot` se definen en XML igual que las demás vistas. En `graph`, `type="bar"` genera barras. En `pivot`, los campos con `type="row"` son filas, `type="col"` son columnas y `type="measure"` son los valores numéricos. Se añade `graph,pivot` al `view_mode` de la acción.

**Fuente consultada:** https://www.odoo.com/documentation/16.0/developer/reference/backend/views.html

```xml
<graph string="Ingresos por pista" type="bar">
    <field name="pista_id" type="row"/>
    <field name="total" type="measure"/>
    <field name="duracion_horas" type="measure"/>
</graph>

<pivot string="Análisis de reservas">
    <field name="pista_id" type="row"/>
    <field name="estado" type="col"/>
    <field name="total" type="measure"/>
</pivot>
```

---

**Mejora 4: Campo computed `ingresos_totales` en pista**

**Prompt:**
> Añade a la pista un campo que sume el total de todas sus reservas que estén en estado "realizada".

**Respuesta obtenida:**  
Se añadió un campo `Float` computed que depende de `reserva_ids`, `reserva_ids.total` y `reserva_ids.estado`. Usa `.filtered()` para seleccionar solo las realizadas y `.mapped()` para extraer los totales antes de sumarlos.

```python
@api.depends("reserva_ids", "reserva_ids.total", "reserva_ids.estado")
def _compute_ingresos_totales(self):
    for rec in self:
        rec.ingresos_totales = sum(
            rec.reserva_ids.filtered(lambda r: r.estado == "realizada").mapped("total")
        )
```

---

**Mejora 5: Vista Kanban de reservas con colores por estado**

**Prompt:**
> Añade una vista kanban a las reservas agrupada por estado, con tarjetas de color diferente según el estado (borrador, confirmada, realizada, cancelada).

**Respuesta obtenida:**  
En Odoo, las tarjetas kanban se colorean usando `t-attf-class` en el template QWeb, que permite construir el nombre de una clase CSS de forma dinámica incluyendo el valor del campo (`#{record.estado.raw_value}`). Luego en el CSS se define el color para cada clase.

**Fuente consultada:** https://www.odoo.com/documentation/16.0/developer/reference/backend/views.html

```xml
<div t-attf-class="oe_kanban_card oe_kanban_global_click
                   padel_reserva_card padel_estado_#{record.estado.raw_value}">
```

```css
.padel_estado_borrador   { border-left: 5px solid #adb5bd; }
.padel_estado_confirmada { border-left: 5px solid #198754; }
.padel_estado_realizada  { border-left: 5px solid #0d6efd; }
.padel_estado_cancelada  { border-left: 5px solid #dc3545; }
```

---

**Mejora 6: Datos demo — socios, proveedores, pistas y reservas**

**Prompt:**
> Añade datos demo realistas: 3 proveedores de material de pádel, 4 socios con sus datos de jugador, 3 pistas y 5 reservas de ejemplo con distintos estados.

**Respuesta obtenida:**  
En Odoo, los datos de ejemplo se definen en archivos XML con `noupdate="1"` dentro de la etiqueta `<data>`, lo que significa que se cargan solo la primera vez y no se sobreescriben en actualizaciones. Los campos de modelos estándar como `res.partner` se rellenan igual que en cualquier record. Los campos custom del módulo (como `es_jugador_padel`) también se pueden rellenar en el XML de demo.

**Fuente consultada:** https://www.odoo.com/documentation/16.0/developer/reference/backend/data.html

```xml
<record id="socio_maria_garcia" model="res.partner">
    <field name="name">María García López</field>
    <field name="es_jugador_padel">True</field>
    <field name="nivel_padel">avanzado</field>
    <field name="marca_pala">bullpadel</field>
    <field name="modelo_pala">Hack 03</field>
</record>
```

---

**Problema técnico: Caché de assets CSS en Odoo**

**Prompt:**
> He cambiado el CSS pero en el navegador sigue saliendo el estilo antiguo aunque haga Ctrl+Shift+R.

**Respuesta obtenida:**  
En Odoo, los archivos CSS no se sirven directamente desde disco: se combinan en un "bundle" (un solo archivo grande) que se guarda en la base de datos como un adjunto (`ir.attachment`). El Ctrl+Shift+R solo borra la caché del navegador, pero el bundle antiguo sigue en la base de datos. La solución es borrarlo con SQL y reiniciar Odoo:

```sql
DELETE FROM ir_attachment WHERE url LIKE '/web/assets/%';
```

```bash
docker compose restart odoo
```

---

**Mejora 7: Personalización CSS del backend**

**Prompt:**
> Mejora el aspecto visual del módulo: colores en las tarjetas kanban según el estado de la reserva, colores en la lista, tema verde en la barra de navegación y en las cabeceras de tablas.

**Respuesta obtenida:**  
Los estilos del backend de Odoo se añaden en un archivo `.css` declarado en `web.assets_backend` dentro de `assets` en el manifest. Se pueden sobreescribir las clases CSS propias de Odoo (`.o_main_navbar`, `.o_list_view thead`, `.btn-primary`, etc.) usando `!important`. Las tarjetas kanban se colorean con clases personalizadas aplicadas condicionalmente desde QWeb. Las filas de la lista se colorean con los atributos `decoration-success`, `decoration-info`, `decoration-danger` en la etiqueta `<tree>`.

**Fuente consultada:** https://www.odoo.com/documentation/16.0/developer/reference/frontend/assets.html

```xml
<!-- En __manifest__.py -->
"assets": {
    "web.assets_backend": [
        "club_padel/static/src/css/club_padel.css",
    ],
}
```

```xml
<!-- En la vista lista -->
<tree decoration-success="estado == 'confirmada'"
      decoration-info="estado == 'realizada'"
      decoration-danger="estado == 'cancelada'">
```

---

## 4. División del trabajo entre miembros del equipo

| Tarea | Responsable | Commit |
|-------|-------------|--------|
| Estructura inicial de los tres módulos | Rubén Flores | `feat: add club_padel module` |
| Docker Compose para entorno local en Windows | Rubén Flores | `chore: añadir docker-compose.yml` |
| Crear `cliente_contacto.py` (herencia `res.partner`) | Rubén Flores | `fix: crear cliente_contacto.py` |
| Corrección de imports y limpieza del manifest | Rubén Flores | `fix: añadir import tienda_producto` |
| Campos computed `etiqueta_pista` y `reservas_activas` | Rubén Flores | `feat: campos computed etiqueta_pista` |
| Campo computed `ingresos_totales` en pista | Rubén Flores | `feat: añadir campo computed ingresos_totales` |
| Módulo `mail` — chatter y `tracking` en reservas | Rubén Flores | `feat: añadir mail.thread a reservas` |
| `@api.onchange` en reservas | Rubén Flores | `feat: añadir @api.onchange en reservas` |
| Datos demo socios, proveedores y productos | Rubén Flores | `feat: añadir datos demo de socios...` |
| Datos demo pistas y reservas de ejemplo | Rubén Flores | `feat: añadir datos demo de pistas y reservas` |
| Productos demo para tienda interna del club | Rubén Flores | `feat: añadir productos demo a tienda interna` |
| Ampliar vista de contactos (pestaña Pádel) | Ángel Martínez | `feat: ampliar vista contactos` |
| Actualizar formulario de pistas con nuevos campos | Ángel Martínez | `feat: mostrar nuevos campos de pista` |
| Vistas `graph` y `pivot` para análisis de reservas | Ángel Martínez | `feat: añadir vistas graph y pivot` |
| Vista Kanban de reservas agrupada por estado | Ángel Martínez | `feat: añadir vista kanban de reservas` |
| Mejoras CSS — tema verde, colores kanban y lista | Ángel Martínez | `feat: mejorar estilos CSS y colores kanban` |
| Documentación técnica completa | Ángel Martínez | `docs: *` |

El historial completo de commits está disponible en: https://github.com/rfloresg/club-padel-odoo/commits/main

---

### 4.1 Valoración del trabajo — Rubén Flores

**Autovaloración:**

Me encargué de la parte técnica más compleja del proyecto: diseñar la arquitectura de los tres módulos desde cero, configurar el entorno Docker para que funcionara en local en Windows, y resolver todos los errores de arranque (imports rotos, archivos inexistentes en el manifest, filtros XML sin atributo obligatorio). Implementé toda la lógica Python: los campos computed con `@api.depends` en pistas y contactos, las validaciones con `@api.constrains` para evitar solapamientos de reservas, el decorador `@api.onchange` para autocompletar campos, la integración del módulo `mail` para el chatter con historial de cambios, y el campo `ingresos_totales` que acumula los ingresos de reservas realizadas por pista. También creé todos los datos demo de socios, proveedores, pistas y reservas.

**Valoración de Ángel:**

Ángel asumió la parte visual del proyecto con buen criterio. Amplió la ficha de contacto de Odoo con la pestaña de pádel, mostrando de forma clara los datos del jugador y su historial de reservas. Actualizó el formulario de pistas para que reflejara todos los campos nuevos. Añadió las vistas de gráfico, tabla dinámica y kanban al módulo de reservas, que son las que más impacto visual dan al proyecto. Mejoró el CSS del backend con un tema verde deportivo, colores por estado en las tarjetas kanban y decoraciones en la lista. También llevó el peso de la documentación escrita y colaboró en la preparación de la presentación oral.

---

### 4.2 Valoración del trabajo — Ángel Martínez

**Autovaloración:**

Me centré en la parte de vistas XML e interfaz de usuario, que es lo que el profesor ve al navegar por Odoo. Desarrollé la pestaña de pádel en la ficha de contacto con visibilidad condicional de campos. Actualicé el formulario de pistas con los nuevos campos de superficie e iluminación, y añadí las vistas de análisis (gráfico, tabla dinámica y kanban) al módulo de reservas. La vista kanban muestra las reservas agrupadas por estado con tarjetas de colores distintos mediante clases CSS condicionales en QWeb. Mejoré también el aspecto general del backend con el CSS personalizado. Me encargué de mantener actualizada la documentación del proyecto y participé activamente en la exposición oral respondiendo preguntas del profesor.

**Valoración de Rubén:**

Rubén fue el motor técnico del proyecto desde el primer día. Organizó los módulos correctamente, configuró Git y montó el entorno Docker, lo que nos permitió trabajar de forma ordenada en local. Resolvió todos los errores técnicos que aparecieron, algunos bastante difíciles de diagnosticar como el problema del `addons_path` o los imports rotos. Implementó las partes más complejas del código Python: campos calculados encadenados, validaciones de solapamiento de reservas, el `@api.onchange` para autocompletar y la integración con el módulo de mensajería de Odoo. Sin su trabajo técnico el proyecto no habría funcionado.

---

## 5. Customizaciones técnicas implementadas

### 5.1 Herencia de modelo estándar (`_inherit`)

En lugar de crear modelos nuevos desde cero, se amplían los modelos existentes de Odoo sin modificar el núcleo del sistema. Se usan en dos casos:

**Herencia de `res.partner`** (contactos nativos de Odoo) para añadir datos de jugador de pádel:

```python
class ClienteContacto(models.Model):
    _inherit = "res.partner"
    es_jugador_padel = fields.Boolean(string="Es jugador/a de pádel", default=False)
    nivel_padel = fields.Selection([...], string="Nivel de pádel")
    marca_pala = fields.Selection([...], string="Marca de la pala")
```

**Herencia de `product.template`** (productos nativos de Odoo) para añadir categorización de pádel:

```python
class ProductoPadel(models.Model):
    _inherit = "product.template"
    es_producto_padel = fields.Boolean(string="Producto de pádel", default=False)
    tipo_producto_padel = fields.Selection([("pala","Pala"), ("pelotas","Pelotas"), ...])
```

**Herencia de mixins de `mail`** para añadir el chatter a las reservas:

```python
class ReservaPadel(models.Model):
    _name = "club_padel.reserva"
    _inherit = ["mail.thread", "mail.activity.mixin"]
```

### 5.2 Campos calculados automáticamente (`@api.depends`)

Los campos computed se recalculan solos cuando cambian los campos declarados en `@api.depends`. El proyecto usa varios:

```python
# Etiqueta legible de la pista
@api.depends("nombre", "tipo_pista", "precio_hora")
def _compute_etiqueta_pista(self):
    for rec in self:
        tipo = dict(rec._fields["tipo_pista"].selection).get(rec.tipo_pista, "")
        rec.etiqueta_pista = f"{rec.nombre} · {tipo} · {rec.precio_hora:.2f}€/h"

# Ingresos totales sumando reservas realizadas
@api.depends("reserva_ids", "reserva_ids.total", "reserva_ids.estado")
def _compute_ingresos_totales(self):
    for rec in self:
        rec.ingresos_totales = sum(
            rec.reserva_ids.filtered(lambda r: r.estado == "realizada").mapped("total")
        )
```

### 5.3 Validaciones con restricciones (`@api.constrains`)

Se valida que los datos sean correctos antes de guardarlos en la base de datos:

```python
# Precio no negativo
@api.constrains("precio_hora")
def _comprobar_precio(self):
    for rec in self:
        if rec.precio_hora < 0:
            raise ValidationError("El precio por hora no puede ser negativo.")

# Sin solapamientos de reservas en la misma pista
@api.constrains("pista_id", "inicio", "fin", "estado")
def _comprobar_solape(self):
    for rec in self:
        dominio = [
            ("id", "!=", rec.id), ("pista_id", "=", rec.pista_id.id),
            ("estado", "!=", "cancelada"),
            ("inicio", "<", rec.fin), ("fin", ">", rec.inicio),
        ]
        if self.search_count(dominio) > 0:
            raise ValidationError("Ya existe una reserva solapada en esa pista.")
```

### 5.4 Autocompletar en tiempo real (`@api.onchange`)

`@api.onchange` se ejecuta mientras el usuario rellena el formulario, sin esperar a guardar. Cuando se selecciona una pista, se rellena automáticamente el campo de observaciones:

```python
@api.onchange("pista_id")
def _onchange_pista_id(self):
    if self.pista_id and not self.observaciones:
        self.observaciones = (
            f"Pista {self.pista_id.nombre} ({self.pista_id.tipo_pista})"
            f" — {self.pista_id.precio_hora:.2f}€/h"
        )
```

### 5.5 Máquina de estados con botones de acción

Las reservas tienen cuatro estados (Borrador → Confirmada → Realizada / Cancelada) con botones que cambian el estado y quedan visibles u ocultos según el estado actual usando `attrs`:

```xml
<button name="accion_confirmar" string="Confirmar" class="btn-primary"
        attrs="{'invisible':[('estado','!=','borrador')]}"/>
```

### 5.6 Secuencias automáticas (`ir.sequence`)

Las reservas generan automáticamente una referencia única (RES-0001, RES-0002...) definida en `data/secuencia.xml` y llamada al crear un registro:

```python
@api.model
def create(self, vals):
    if vals.get("referencia", "Nuevo") == "Nuevo":
        vals["referencia"] = self.env["ir.sequence"].next_by_code("club_padel.reserva.seq")
    return super().create(vals)
```

### 5.7 Vistas con visibilidad condicional (`attrs`)

Los campos de la pestaña Pádel solo aparecen cuando el contacto está marcado como jugador:

```xml
<field name="nivel_padel"
       attrs="{'invisible': [('es_jugador_padel', '=', False)],
               'required': [('es_jugador_padel', '=', True)]}"/>
```

### 5.8 Vistas de análisis de datos (`graph` y `pivot`)

Las reservas se pueden analizar en gráfico de barras y tabla dinámica, vistas estándar de Odoo definidas en XML:

```xml
<graph string="Ingresos por pista" type="bar">
    <field name="pista_id" type="row"/>
    <field name="total" type="measure"/>
</graph>
```

### 5.9 Vista Kanban con colores dinámicos por estado

El kanban de reservas usa `t-attf-class` de QWeb para construir el nombre de una clase CSS incluyendo el valor del campo `estado`. Esto permite colorear cada tarjeta de forma diferente:

```xml
<div t-attf-class="oe_kanban_card padel_reserva_card padel_estado_#{record.estado.raw_value}">
```

```css
.padel_estado_confirmada { border-left: 5px solid #198754; }
.padel_estado_cancelada  { border-left: 5px solid #dc3545; }
```

### 5.10 Informe PDF con QWeb

Se genera un informe imprimible de cada reserva usando el motor de plantillas QWeb, definido en `report/plantilla_reporte_reserva.xml` y declarado como acción de tipo `qweb-pdf`.

### 5.11 Personalización del entorno gráfico (CSS)

El CSS personalizado sobreescribe los estilos del backend de Odoo: barra de navegación con degradado verde, cabeceras de tabla en verde oscuro, filas alternas, y botones redondeados. Se carga declarándolo en `web.assets_backend` dentro del `__manifest__.py`.

---

## 6. Estructura modular y dependencias

```
tienda_padel          ← Sin dependencias propias
      ↓
club_padel            ← Depende de: base, contacts, product, web, mail
      ↓
club_padel_tienda     ← Depende de: club_padel + tienda_padel
```

Odoo carga los módulos respetando las dependencias declaradas en cada `__manifest__.py`. El orden es importante: `tienda_padel` se carga primero porque `club_padel` lo necesita, y `club_padel_tienda` se carga al final porque depende de los dos anteriores.
