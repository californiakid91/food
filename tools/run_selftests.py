#!/usr/bin/env python3
"""Ejecuta runSelfTests() de index.html fuera del navegador.

Extrae el bloque <script> inline entero (descubrir, no enumerar: si las
autopruebas empiezan a usar otra funcion, sigue estando ahi) y lo evalua en
node sobre un DOM minimo de mentira.

Falla CERRADO: si no puede extraer, cargar o encontrar runSelfTests, sale con
rc=2 (instrumento roto). Nunca "0 hallazgos" cuando no pudo medir.
"""
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / 'index.html'

def broken(msg):
    print(f"INSTRUMENTO ROTO: {msg}", file=sys.stderr)
    sys.exit(2)

def main():
    if not INDEX.is_file():
        broken(f"no existe {INDEX}")
    html = INDEX.read_text(encoding='utf-8')
    if not html.strip():
        broken(f"{INDEX} esta vacio")

    blocks = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', html, re.DOTALL)
    if len(blocks) != 1:
        broken(f"esperaba 1 bloque <script> inline, encontre {len(blocks)}")
    js = blocks[0]
    if 'function runSelfTests' not in js:
        broken("runSelfTests() no esta en index.html")

    harness = (ROOT / 'tools' / 'dom_stub.js').read_text(encoding='utf-8')
    runner = harness + "\n" + js + """
if (typeof runSelfTests !== 'function') {
  console.error('INSTRUMENTO ROTO: runSelfTests no quedo definida tras cargar el script');
  process.exit(2);
}
let fails;
try { fails = runSelfTests(); }
catch (e) {
  console.error('INSTRUMENTO ROTO: runSelfTests lanzo: ' + (e && e.stack || e));
  process.exit(2);
}
if (!Array.isArray(fails)) {
  console.error('INSTRUMENTO ROTO: runSelfTests no devolvio la lista de fallos');
  process.exit(2);
}
process.exit(fails.length ? 1 : 0);
"""
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write(runner)
        tmp = f.name
    try:
        # check=False a proposito: el rc del hijo ES el veredicto.
        r = subprocess.run(['node', tmp], capture_output=True, text=True, check=False)
    except FileNotFoundError:
        broken("node no esta instalado")
    finally:
        pathlib.Path(tmp).unlink(missing_ok=True)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    sys.exit(r.returncode)

if __name__ == '__main__':
    main()
