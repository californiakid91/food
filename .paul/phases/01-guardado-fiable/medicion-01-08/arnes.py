#!/usr/bin/env python3
"""Arnes de medicion: carga el <script> de un index.html dado y ejecuta un
caso escrito aparte. Falla CERRADO: si no puede extraer o cargar, rc=2."""
import json
import pathlib
import re
import subprocess
import sys

# DIRECTORIO FIJADO EN ABSOLUTO Y AFIRMADO (§3.4, quinta transicion).
BASE = pathlib.Path(sys.argv[1]).resolve()
CASO = pathlib.Path(sys.argv[2]).resolve()
assert BASE.is_dir(), f"BASE no es directorio: {BASE}"
INDEX = BASE / 'index.html'
if not INDEX.is_file() or not INDEX.read_text(encoding='utf-8').strip():
    print(f"INSTRUMENTO ROTO: {INDEX} ausente o vacio", file=sys.stderr); sys.exit(2)
html = INDEX.read_text(encoding='utf-8')
blocks = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', html, re.DOTALL)
if len(blocks) != 1:
    print(f"INSTRUMENTO ROTO: esperaba 1 bloque script, hay {len(blocks)}", file=sys.stderr); sys.exit(2)
js = blocks[0]
marcado = re.sub(r'<script(?![^>]*\bsrc=)[^>]*>.*?</script>', '', html, flags=re.DOTALL)
ids = sorted(set(re.findall(r'(?:^|[\s"\'])id\s*=\s*["\']([^"\']+)["\']', marcado)))
if not ids:
    print("INSTRUMENTO ROTO: cero ids derivados del marcado", file=sys.stderr); sys.exit(2)
stub = (BASE / 'tools' / 'dom_stub.js').read_text(encoding='utf-8')
runner = ("process.on('unhandledRejection', e => { console.error('INSTRUMENTO ROTO: promesa sin manejar: ' + (e && e.stack || e)); process.exit(2); });\n"
          + stub
          + "\nglobalThis.__IDS_DEL_MARCADO = " + json.dumps(ids) + ";\n"
          + js + "\n" + CASO.read_text(encoding='utf-8'))
out = BASE / '_runner_medicion.js'
out.write_text(runner, encoding='utf-8')
try:
    r = subprocess.run(['node', str(out)], cwd=str(BASE), timeout=45, check=False)
    rc = r.returncode
except subprocess.TimeoutExpired:
    print('INSTRUMENTO ROTO: node no termino en 45s', file=sys.stderr)
    rc = 2
out.unlink()
sys.exit(rc)
