#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validación para la documentación generada.
Comprueba enlaces internos, existencia de recursos, relaciones básicas y metadatos.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TERM_DIR = DOCS / "terminos"
RESUM_DIR = DOCS / "resumenes"
ERRORS = []
WARNINGS = []

def check_file_exists(path):
    return Path(path).exists()

def validate_terms():
    if not TERM_DIR.exists():
        ERRORS.append(f"Directorio {TERM_DIR} no existe.")
        return
    for md in TERM_DIR.glob("*.md"):
        try:
            text = md.read_text(encoding="utf-8")
        except Exception as e:
            ERRORS.append(f"No se puede leer {md}: {e}")
            continue
        # frontmatter
        m = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL | re.MULTILINE)
        if not m:
            ERRORS.append(f"{md} no tiene frontmatter YAML.")
            continue
        fm = m.group(1)
        required = ['termino', 'fecha_creacion', 'fecha_actualizacion', 'estado', 'etiquetas']
        for r in required:
            if not re.search(rf'^{r}\b', fm, re.MULTILINE):
                ERRORS.append(f"{md} falta campo requerido: {r}")
        # mermaid presence? al menos una mención o bloque mermaid
        if '```mermaid' not in text and 'mermaid' not in text.lower():
            WARNINGS.append(f"{md} podría no tener diagrama Mermaid explícito.")

def validate_resumenes():
    if not RESUM_DIR.exists():
        return
    for md in RESUM_DIR.glob("*.md"):
        try:
            text = md.read_text(encoding="utf-8")
        except Exception as e:
            ERRORS.append(f"No se puede leer {md}: {e}")
            continue
        m = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL | re.MULTILINE)
        if not m:
            ERRORS.append(f"{md} no tiene frontmatter YAML.")
            continue
        fm = m.group(1)
        required = ['titulo', 'tema', 'fecha_creacion', 'fecha_actualizacion',
                    'estado', 'etiquetas', 'fuente']
        for r in required:
            if not re.search(rf'^{r}\b', fm, re.MULTILINE):
                WARNINGS.append(f"{md} falta campo recomendado: {r}")
        if '```mermaid' not in text:
            WARNINGS.append(f"{md} no tiene diagrama Mermaid explícito.")

def validate_links():
    # enlaces internos a terminos/recursos dentro de docs
    link_re = re.compile(r'\]\(([^)]+)\)')
    for md in DOCS.rglob("*.md"):
        try:
            text = md.read_text(encoding="utf-8")
        except:
            continue
        for lm in link_re.findall(text):
            # ignorar externos
            if lm.startswith('http://') or lm.startswith('https://') or lm.startswith('#'):
                continue
            # resolver relativo
            target = (md.parent / lm.split('#')[0].split('?')[0])
            if not target.exists():
                # también intentar desde docs root?
                target2 = (DOCS / lm.split('#')[0].split('?')[0])
                if not target2.exists():
                    ERRORS.append(f"Enlace roto en {md}: {lm}")

def validate_originals_preserved():
    # comprobar que archivos originales siguen ahí
    checks = ['Glosario.md', 'README.md', 'AGENTS.md']
    for c in checks:
        if not (ROOT / c).exists():
            ERRORS.append(f"Archivo original faltante: {c}")

def validate_nav():
    """
    Comprueba que todos los resúmenes de docs/resumenes/ están en el nav de
    mkdocs.yml. MkDocs avisa en el build, pero aquí el error es más claro.
    Los términos no se comprueban uno a uno: se listan en las páginas de índice
    (glosario.md, terminos.md, categorias.md), que sí están en el nav.
    """
    yml = ROOT / "mkdocs.yml"
    if not yml.exists():
        ERRORS.append("Falta mkdocs.yml.")
        return
    texto = yml.read_text(encoding="utf-8")
    m = re.search(r'^nav:\s*\n(.*)$', texto, re.DOTALL | re.MULTILINE)
    if not m:
        ERRORS.append("mkdocs.yml no tiene la clave nav.")
        return
    nav = m.group(1)
    if not RESUM_DIR.exists():
        return
    for md in sorted(RESUM_DIR.glob("*.md")):
        ruta = f"resumenes/{md.name}"
        if ruta not in nav:
            ERRORS.append(f"{md.name} no aparece en el nav de mkdocs.yml ({ruta}).")

def validate_resumen_bloques():
    """Cada resumen debe declarar su bloque temático (campo `bloque`)."""
    if not RESUM_DIR.exists():
        return
    for md in sorted(RESUM_DIR.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        m = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL | re.MULTILINE)
        fm = m.group(1) if m else ''
        if not re.search(r'^bloque\b', fm, re.MULTILINE):
            ERRORS.append(f"{md} falta el campo 'bloque' (tema del resumen).")

def main():
    validate_terms()
    validate_resumenes()
    validate_resumen_bloques()
    validate_links()
    validate_nav()
    validate_originals_preserved()
    if ERRORS:
        print("ERRORES ENCONTRADOS:")
        for e in ERRORS:
            print(f"  - {e}")
        sys.exit(1)
    if WARNINGS:
        print("ADVERTENCIAS:")
        for w in WARNINGS:
            print(f"  - {w}")
    print("Validación OK.")
    sys.exit(0)

if __name__ == "__main__":
    main()
