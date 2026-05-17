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

**Conversación 1: Estructura del proyecto Odoo**  
*Título del chat: "Proyecto Odoo Padel"*

Se consultó cómo crear la estructura de un módulo Odoo desde cero, incluyendo qué archivos son obligatorios y cómo se relacionan entre sí.

**Prompt utilizado:**
> "Estoy haciendo un módulo de Odoo 16 para gestionar un club de pádel. ¿Cuáles son los archivos mínimos que necesita un módulo para funcionar?"

**Respuesta obtenida (resumen):**  
La IA explicó que un módulo Odoo necesita mínimo: `__init__.py`, `__manifest__.py`, y una carpeta `models/` con otro `__init__.py`. Indicó que los archivos de vistas van en `views/`, la seguridad en `security/ir.model.access.csv`, y que el orden de carga en `data:` dentro del manifest es importante (seguridad antes que vistas).

**Cómo se aplicó:**  
Se utilizó esta estructura para crear los tres módulos del proyecto (`club_padel`, `tienda_padel`, `club_padel_tienda`), respetando el orden de dependencias: `tienda_padel` → `club_padel` → `club_padel_tienda`.

---

**Conversación 2: Error 5000 en el módulo Tienda**  
*Título del chat: "Error 5000 Odoo Tienda"*

Durante el desarrollo apareció un error 5000 (error interno del servidor) al cargar el módulo `club_padel_tienda`.

**Prompt utilizado:**
> "En Odoo 16 me aparece Error 5000 al intentar instalar mi módulo. El módulo depende de otro módulo propio. ¿Qué puede estar fallando?"

**Respuesta obtenida (resumen):**  
La IA indicó que los errores 5000 suelen deberse a: (1) un modelo referenciado en las vistas que no existe todavía, (2) un campo `Many2one` apuntando a un modelo no registrado, o (3) un `_inherit` de un modelo que aún no está cargado. Recomendó revisar el orden de dependencias en `__manifest__.py` y comprobar los logs con `--log-level=debug`.

**Cómo se aplicó:**  
Se corrigió el orden de dependencias en el manifest de `club_padel_tienda` para asegurar que `club_padel` y `tienda_padel` se cargaran antes. También se revisaron las relaciones `Many2one` entre modelos.

---

**Conversación 3: Mejoras en la documentación**  
*Título del chat: "Mejoras en PDF Proyecto"*

Se consultó cómo mejorar la estructura y contenido del documento de memoria del proyecto.

**Prompt utilizado:**
> "Tengo que entregar una memoria de un proyecto de Odoo para clase. ¿Qué secciones debería incluir y cómo documentar el uso de IA?"

**Respuesta obtenida (resumen):**  
La IA sugirió incluir: descripción del escenario, documentación técnica con fuentes reales (URLs), sección específica de uso de IA con prompts reales y respuestas obtenidas, descripción de los modelos creados, y una sección de pruebas realizadas.

**Cómo se aplicó:**  
Se reorganizó la memoria del proyecto siguiendo estas recomendaciones, añadiendo la sección de fuentes con URLs y los ejemplos de prompts utilizados.

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
