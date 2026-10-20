#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de preparación para MkDocs.
Copia los archivos Markdown originales a docs/ para su publicación,
preservando los apuntes originales (no los sobrescribe).
Corrige enlaces relativos para funcionar dentro de la estructura de MkDocs.
"""

import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TERM_DIR_ORIG = ROOT / "Terminos"
RESUMENES_ORIG = ROOT / "Resumenes"
RECURSOS_ORIG = ROOT / "Recursos"
PLANTILLAS_ORIG = ROOT / "Plantillas"
GLOSARIO_ORIG = ROOT / "Glosario.md"
README_ORIG = ROOT / "README.md"
AGENTS_ORIG = ROOT / "AGENTS.md"
ENTRADA_ORIG = ROOT / "Entrada"

def clean_docs():
    """Limpia docs/ para regenerar"""
    if DOCS.exists():
        # No borrar todo; preservar si necesario, pero regenerar
        pass
    DOCS.mkdir(exist_ok=True)

def copy_terms():
    """Copia fichas de términos a docs/terminos/"""
    dest = DOCS / "terminos"
    dest.mkdir(exist_ok=True)
    for md in sorted(TERM_DIR_ORIG.glob("*.md")):
        shutil.copy2(md, dest / md.name)

def copy_resumenes():
    """Copia resúmenes de temas a docs/resumenes/"""
    if RESUMENES_ORIG.exists():
        dest = DOCS / "resumenes"
        dest.mkdir(exist_ok=True)
        for md in sorted(RESUMENES_ORIG.glob("*.md")):
            shutil.copy2(md, dest / md.name)

def copy_resources():
    """Copia recursos a docs/recursos/"""
    if RECURSOS_ORIG.exists():
        dest = DOCS / "recursos"
        shutil.copytree(RECURSOS_ORIG, dest, dirs_exist_ok=True)

def copy_misc():
    """Copia archivos de apoyo si es necesario"""
    # Entrada opcional (solo texto; los PDF de clase no se publican)
    if ENTRADA_ORIG.exists():
        dest = DOCS / "entrada"
        shutil.copytree(ENTRADA_ORIG, dest, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("*.pdf"))

def fix_links_in_file(filepath):
    """
    Corrige enlaces relativos dentro de docs/.
    Convierte Terminos/xxx.md -> terminos/xxx.md
    Convierte ../Recursos/Imagenes/xxx -> ../recursos/imagenes/xxx
    Convierte Recursos/Imagenes/xxx -> recursos/imagenes/xxx
    """
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return

    # Índice general: ../Glosario.md -> ../glosario.md, Glosario.md -> glosario.md
    text = re.sub(r'\]\(\.\./Glosario\.md([^)#]*)', r'](../glosario.md\1', text)
    text = re.sub(r'\]\(Glosario\.md([^)#]*)', r'](glosario.md\1', text)

    # Enlaces a Terminos/, con la ruta relativa correcta según la profundidad
    # del archivo dentro de docs/ (p. ej. desde docs/resumenes/ es ../terminos/)
    prefix = "../" * (len(filepath.relative_to(DOCS).parts) - 1)
    text = re.sub(r'\]\(\.\./Terminos/([^)#]+)', rf']({prefix}terminos/\1', text)
    text = re.sub(r'\]\(Terminos/([^)#]+)', rf']({prefix}terminos/\1', text)

    # Imágenes y enlaces a Recursos
    text = re.sub(r'\]\(Recursos/([^)#]+)', r'](recursos/\1', text)
    text = re.sub(r'\]\(\.\./Recursos/([^)#]+)', r'](../recursos/\1', text)

    # Resúmenes de temas (siempre viven en docs/resumenes/)
    text = re.sub(r'\]\(\.\./Resumenes/([^)#]+)', rf']({prefix}resumenes/\1', text)
    text = re.sub(r'\]\(Resumenes/([^)#]+)', rf']({prefix}resumenes/\1', text)

    # Entrada
    text = re.sub(r'\]\(\.\./Entrada/([^)#]+)', rf']({prefix}entrada/\1', text)
    text = re.sub(r'\]\(Entrada/([^)#]+)', rf']({prefix}entrada/\1', text)

    filepath.write_text(text, encoding="utf-8")

def fix_all_links():
    """Corrige enlaces en todos los .md dentro de docs/"""
    for md in DOCS.rglob("*.md"):
        fix_links_in_file(md)

def main():
    clean_docs()
    copy_terms()
    copy_resumenes()
    copy_resources()
    copy_misc()
    # Generará índices después - pero también copiar Glosario base si queremos? Lo generamos nosotros
    fix_all_links()
    print("Preparación completada: docs/ actualizado.")

if __name__ == "__main__":
    main()
