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

def main():
    validate_terms()
    validate_links()
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
