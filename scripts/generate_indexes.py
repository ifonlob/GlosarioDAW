#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera índices automáticos para MkDocs:
- docs/index.md (portada con estadísticas reales)
- docs/glosario.md (índice completo)
- docs/terminos.md (página de términos)
- docs/categorias.md (agrupado por etiquetas/categorías)
- docs/etiquetas.md (tags)
- docs/resumenes.md (índice de resúmenes agrupado por bloques de tema)
- docs/sobre.md (sobre el proyecto)
- mkdocs.yml (bloque nav de Resúmenes, agrupado por bloques)

Bloques de tema: cada resumen declara el suyo en el frontmatter (campo `bloque`).
El orden de los bloques es fijo y vive en BLOQUES; un resumen sin bloque o con un
bloque desconocido se agrupa al final en "Otros".
"""

import re
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TERM_DIR = DOCS / "terminos"
RESUM_DIR = DOCS / "resumenes"
MKDOCS_YML = ROOT / "mkdocs.yml"

# Bloques temáticos de los resúmenes, en el orden en que aparecen en el sitio.
BLOQUES = [
    ("http", "HTTP y protocolo"),
    ("servidor", "Cliente, servidor e infraestructura"),
    ("spring", "Spring Boot y Java (DWES)"),
    ("tdd", "TDD y pruebas"),
]
BLOQUE_OTROS = "Otros"

NAV_INICIO = "# >>> nav: resúmenes (generado por scripts/generate_indexes.py) >>>"
NAV_FIN = "# <<< nav: resúmenes <<<"

def read_frontmatter(md_file):
    try:
        text = md_file.read_text(encoding="utf-8")
    except:
        return {}
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL | re.MULTILINE)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                fm[k.strip()] = v.strip()
    return fm, text

def extract_tags(tag_str):
    # extraer tags como [tag1, tag2] o separados
    tags = re.findall(r'([\w\-]+)', tag_str)
    return sorted(set(tags))

def build_index():
    items = []
    for md in sorted(TERM_DIR.glob("*.md")):
        fm, text = read_frontmatter(md)
        term = fm.get('termino') or md.stem
        estado = fm.get('estado', '')
        tags = extract_tags(fm.get('etiquetas', ''))
        items.append({
            'file': md.name,
            'term': term,
            'estado': estado,
            'tags': tags,
            'slug': md.stem
        })
    return items

def build_resumenes_index():
    """Lee los resúmenes de docs/resumenes/ y devuelve sus datos."""
    items = []
    if not RESUM_DIR.exists():
        return items
    for md in sorted(RESUM_DIR.glob("*.md")):
        try:
            fm, text = read_frontmatter(md)
        except Exception:
            fm = {}
        items.append({
            'file': md.name,
            'titulo': fm.get('titulo') or md.stem,
            'tema': fm.get('tema') or md.stem,
            'estado': fm.get('estado', ''),
            'bloque': fm.get('bloque', ''),
            'fuente': fm.get('fuente', ''),
            'paginas': fm.get('paginas', ''),
            'tags': extract_tags(fm.get('etiquetas', '')),
        })
    return items

def agrupar_por_bloque(resumenes):
    """Devuelve [(nombre_bloque, [resúmenes])] en el orden de BLOQUES."""
    claves = [b for b, _ in BLOQUES]
    titulos = dict(BLOQUES)
    grupos = defaultdict(list)
    for r in resumenes:
        b = r.get('bloque', '').strip()
        if b not in claves:
            b = BLOQUE_OTROS
        grupos[b].append(r)
    salida = [(titulos[b], sorted(grupos[b], key=lambda x: x['titulo'].lower()))
              for b in claves if grupos.get(b)]
    if grupos.get(BLOQUE_OTROS):
        salida.append((BLOQUE_OTROS,
                       sorted(grupos[BLOQUE_OTROS], key=lambda x: x['titulo'].lower())))
    return salida

def write_resumenes_md(resumenes):
    total = len(resumenes)
    grupos = agrupar_por_bloque(resumenes)
    lines = [
        "# Resúmenes por temas",
        "",
        "Resúmenes de material de clase (PDF) explicados con el mismo método que "
        "las fichas: capas, ejemplo mínimo, diagrama y preguntas de repaso.",
        "",
    ]
    if total == 0:
        lines += [
            "Todavía no hay resúmenes.", "",
            "Para crear uno, deja el PDF en `Entrada/PDF/` y escribe en el chat:",
            "",
            "```text",
            "/resumir Entrada/PDF/mi-tema.pdf — tema: Nombre del tema",
            "```",
            "",
        ]
    else:
        lines.append(f"Total: {total} resúmenes, agrupados en {len(grupos)} temas.")
        lines.append("")
        # índice rápido de temas
        lines.append("## Temas")
        lines.append("")
        for nombre, items in grupos:
            lines.append(f"- **{nombre}** ({len(items)})")
        lines.append("")
        for nombre, items in grupos:
            lines.append(f"## {nombre}")
            lines.append("")
            for r in items:
                detalles = []
                if r['fuente']:
                    detalles.append(f"fuente: `{r['fuente']}`")
                if r['paginas']:
                    detalles.append(f"páginas: {r['paginas']}")
                if r['tags']:
                    detalles.append("etiquetas: " + ", ".join(f"`{t}`" for t in r['tags']))
                linea = f"- [{r['titulo']}](resumenes/{r['file']})"
                if detalles:
                    linea += "  \n  " + " · ".join(detalles)
                lines.append(linea)
            lines.append("")
    (DOCS / "resumenes.md").write_text('\n'.join(lines), encoding="utf-8")

def nav_titulo(texto):
    """Cita un título para el nav: muchos llevan ':' y romperían el YAML."""
    return '"' + str(texto).replace('\\', '\\\\').replace('"', '\\"') + '"'

def write_nav_resumenes(resumenes):
    """
    Escribe en mkdocs.yml el apartado de nav de Resúmenes, con una sección por
    bloque temático. Solo toca el texto entre NAV_INICIO y NAV_FIN.
    """
    if not MKDOCS_YML.exists():
        return
    texto = MKDOCS_YML.read_text(encoding="utf-8")
    if NAV_INICIO not in texto or NAV_FIN not in texto:
        return
    grupos = agrupar_por_bloque(resumenes)
    bloque = [NAV_INICIO,
              "  - Resúmenes:",
              "      - Resúmenes por temas: resumenes.md"]
    for nombre, items in grupos:
        bloque.append(f"      - {nav_titulo(nombre)}:")
        for r in items:
            bloque.append(f"          - {nav_titulo(r['titulo'])}: resumenes/{r['file']}")
    bloque.append(NAV_FIN)
    nuevo = re.sub(re.escape(NAV_INICIO) + r".*?" + re.escape(NAV_FIN),
                   '\n'.join(bloque), texto, flags=re.DOTALL)
    if nuevo != texto:
        MKDOCS_YML.write_text(nuevo, encoding="utf-8")

def write_index_page(items, resumenes=None):
    DOCS.mkdir(exist_ok=True)
    total = len(items)
    total_resumenes = len(resumenes) if resumenes else 0
    etiquetas = set()
    for i in items:
        etiquetas.update(i['tags'])
    # fecha
    hoy = datetime.now().strftime('%Y-%m-%d')
    content = f"""# Glosario DAW

¡Bienvenido al glosario personal de Desarrollo de Aplicaciones Web!

## Estadísticas reales

- **Términos totales:** {total}
- **Resúmenes por temas:** {total_resumenes}
- **Etiquetas distintas:** {len(etiquetas)}
- **Actualización del índice:** {hoy}

## ¿Qué es esto?

Un glosario pedagógico creado para aprender paso a paso. Cada ficha explica un concepto con:

- Explicación por capas (qué es → cómo funciona → diagrama → ejemplo mínimo)
- Al menos un diagrama Mermaid
- Ejemplos prácticos relacionados con DAW
- Preguntas de repaso
- Enlaces a conceptos relacionados

## Acceso rápido

- [Ver glosario completo](glosario.md)
- [Leer resúmenes por temas](resumenes.md)
- [Explorar por categorías](categorias.md)
- [Explorar por etiquetas](etiquetas.md)
"""
    (DOCS / "index.md").write_text(content, encoding="utf-8")

def write_glosario_md(items):
    lines = ["# Glosario completo", "", "Índice alfabético de todas las fichas.", ""]
    # agrupar por primera letra
    from collections import OrderedDict
    by_letter = defaultdict(list)
    for i in sorted(items, key=lambda x: x['term'].lower()):
        first = i['term'][0].upper() if i['term'] else '#'
        by_letter[first].append(i)
    for letter in sorted(by_letter.keys()):
        lines.append(f"## {letter}")
        for i in by_letter[letter]:
            lines.append(f"- [{i['term']}](terminos/{i['file']})")
        lines.append("")
    (DOCS / "glosario.md").write_text('\n'.join(lines), encoding="utf-8")

def write_terminos_md(items):
    lines = ["# Términos", "", f"Total: {len(items)} términos.", ""]
    for i in sorted(items, key=lambda x: x['term'].lower()):
        tags = ', '.join(f"`{t}`" for t in i['tags']) if i['tags'] else ''
        lines.append(f"- [{i['term']}](terminos/{i['file']})")
        if tags:
            lines.append(f"  - Etiquetas: {tags}")
    (DOCS / "terminos.md").write_text('\n'.join(lines), encoding="utf-8")

def write_categorias_md(items):
    # agrupar por primera etiqueta como categoría aproximada
    cat = defaultdict(list)
    for i in items:
        if i['tags']:
            for t in i['tags']:
                cat[t].append(i)
        else:
            cat['sin-categoria'].append(i)
    lines = ["# Categorías", "", "Agrupación por etiquetas.", ""]
    for c in sorted(cat.keys()):
        lines.append(f"## {c.replace('-', ' ').title()}")
        for i in sorted(cat[c], key=lambda x: x['term'].lower()):
            lines.append(f"- [{i['term']}](terminos/{i['file']})")
        lines.append("")
    (DOCS / "categorias.md").write_text('\n'.join(lines), encoding="utf-8")

def write_etiquetas_md(items):
    # simple tags page
    all_tags = set()
    for i in items:
        for t in i['tags']:
            all_tags.add(t)
    lines = ["# Etiquetas", "", ""]
    for t in sorted(all_tags):
        lines.append(f"- `{t}`")
    (DOCS / "etiquetas.md").write_text('\n'.join(lines), encoding="utf-8")

def write_sobre(items, resumenes=None):
    total = len(items)
    total_resumenes = len(resumenes) if resumenes else 0
    content = f"""# Sobre el glosario

## Objetivo

Glosario personal de Desarrollo de Aplicaciones Web (DAW), orientado a aprendizaje gradual y principiante.

## Características

- **Fuente de verdad en Markdown**: Las fichas originales se mantienen inalteradas para Obsidian y otros editores.
- **Publicación web**: Generado con MkDocs Material, con búsqueda, modo claro/oscuro, navegación alfabética y diagramas Mermaid.
- **Proceso de preparación**: Se genera una copia para MkDocs sin sobrescribir los apuntes originales.
- **Pedagogía activa**: Explicación por capas, ejemplo mínimo, confusiones típicas y preguntas de repaso.
- **Estadísticas reales**: Los contadores se calculan automáticamente a partir de las fichas existentes.

## Datos actuales

- Términos registrados: {total}
- Resúmenes por temas: {total_resumenes}

## Tecnología

- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
- [Mermaid](https://mermaid.js.org/)
- [GitHub Actions](https://github.com/features/actions)
- [GitHub Pages](https://pages.github.com/)

## Notas

- Los diagramas Mermaid requieren comprobación visual en algunos visores (se indica cuando procede).
- Las imágenes se enlazan con rutas relativas y se conservan.
- La sección *Mis notas* de cada ficha nunca se borra ni sobrescribe.
"""
    (DOCS / "sobre.md").write_text(content, encoding="utf-8")

def main():
    items = build_index()
    resumenes = build_resumenes_index()
    write_resumenes_md(resumenes)
    write_nav_resumenes(resumenes)
    write_index_page(items, resumenes)
    write_glosario_md(items)
    write_terminos_md(items)
    write_categorias_md(items)
    write_etiquetas_md(items)
    write_sobre(items, resumenes)
    print(f"Índices generados: {len(items)} términos y {len(resumenes)} resúmenes procesados.")

if __name__ == "__main__":
    main()
