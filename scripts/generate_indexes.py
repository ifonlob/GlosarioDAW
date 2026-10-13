#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera índices automáticos para MkDocs:
- docs/index.md (portada con estadísticas reales)
- docs/glosario.md (índice completo)
- docs/terminos.md (página de términos)
- docs/categorias.md (agrupado por etiquetas/categorías)
- docs/etiquetas.md (tags)
- docs/mapa-conceptual.md (mapa conceptual automático desde enlaces)
- docs/sobre.md (sobre el proyecto)
"""

import re
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TERM_DIR = DOCS / "terminos"

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

def write_index_page(items):
    DOCS.mkdir(exist_ok=True)
    total = len(items)
    etiquetas = set()
    for i in items:
        etiquetas.update(i['tags'])
    # fecha
    hoy = datetime.now().strftime('%Y-%m-%d')
    content = f"""# Glosario DAW

¡Bienvenido al glosario personal de Desarrollo de Aplicaciones Web!

## Estadísticas reales

- **Términos totales:** {total}
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
- [Explorar por categorías](categorias.md)
- [Explorar por etiquetas](etiquetas.md)
- [Mapa conceptual](mapa-conceptual.md)
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

def build_relations(items):
    # map slug -> {name, file}
    slugmap = {i['slug']: i for i in items}
    rels_out = defaultdict(list)  # from -> to
    for i in items:
        fpath = TERM_DIR / i['file']
        try:
            text = fpath.read_text(encoding='utf-8')
        except:
            continue
        # Enlaces a otras fichas: dentro de docs/terminos son relativos y sin
        # carpeta, por ejemplo [HTTP](http.md) o [HTTP](http.md#seccion).
        for m in re.finditer(r'\]\((?:\.\./)?(?:terminos/)?([\w\-]+)\.md(?:#[^)]*)?\)', text):
            lslug = m.group(1)
            if lslug in slugmap and lslug != i['slug']:
                rels_out[i['slug']].append(lslug)
    return rels_out, slugmap

def write_mapa_conceptual(items):
    rels_out, slugmap = build_relations(items)
    lines = ["# Mapa conceptual", "", "Representación automática de relaciones explícitas entre fichas.", "", "```mermaid", "graph LR"]
    # nodos (evitar duplicados)
    nodes = set(slugmap.keys())
    for a in rels_out:
        nodes.add(a)
        for b in rels_out[a]:
            nodes.add(b)
    # escribir nodos con labels
    for n in sorted(nodes):
        label = slugmap[n]['term'].replace('"', "'") if n in slugmap else n
        # limpiar comillas
        label = label.replace('"', "'")
        # acortar si muy largo
        if len(label) > 30:
            label = label[:27] + '...'
        lines.append(f'  {n}["{label}"]')
    # relaciones (sin duplicados)
    seen = set()
    for a in rels_out:
        for b in rels_out[a]:
            key = tuple(sorted((a,b)))
            if key in seen:
                continue
            seen.add(key)
            lines.append(f'  {a} --> {b}')
    lines.append("```")
    lines.append("")
    lines.append("> *Nota*: Solo se muestran relaciones explícitas detectadas en los enlaces Markdown entre fichas.")
    (DOCS / "mapa-conceptual.md").write_text('\n'.join(lines), encoding="utf-8")

def write_sobre(items):
    total = len(items)
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
    write_index_page(items)
    write_glosario_md(items)
    write_terminos_md(items)
    write_categorias_md(items)
    write_etiquetas_md(items)
    write_mapa_conceptual(items)
    write_sobre(items)
    print(f"Índices generados: {len(items)} términos procesados.")

if __name__ == "__main__":
    main()
