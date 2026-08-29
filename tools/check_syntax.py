#!/usr/bin/env python3
"""Comprueba con node la sintaxis del <script> inline de index.html.

Falla CERRADO: si no puede extraer el bloque o node no esta, rc=2 (no pudo
medir), nunca un verde silencioso.
"""
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / 'index.html'


def roto(msg):
    print(f"INSTRUMENTO ROTO: {msg}", file=sys.stderr)
    sys.exit(2)


def main():
    if not INDEX.is_file():
        roto(f"no existe {INDEX}")
    html = INDEX.read_text(encoding='utf-8')
    if not html.strip():
        roto(f"{INDEX} esta vacio")
    bloques = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', html, re.DOTALL)
    if len(bloques) != 1:
        roto(f"esperaba 1 bloque <script> inline, encontre {len(bloques)}")
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write(bloques[0])
        tmp = f.name
    try:
        # check=False a proposito: el rc del hijo ES el veredicto.
        r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True, check=False)
    except FileNotFoundError:
        roto("node no esta instalado")
    finally:
        pathlib.Path(tmp).unlink(missing_ok=True)
    if r.returncode != 0:
        print(r.stderr.replace(tmp, 'index.html:<script>'), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
