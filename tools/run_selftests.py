#!/usr/bin/env python3
"""Ejecuta runSelfTests() de index.html fuera del navegador.

Extrae el bloque <script> inline entero (descubrir, no enumerar: si las
autopruebas empiezan a usar otra funcion, sigue estando ahi) y lo evalua en
node sobre un DOM minimo de mentira.

Falla CERRADO: si no puede extraer, cargar o encontrar runSelfTests, sale con
rc=2 (instrumento roto). Nunca "0 hallazgos" cuando no pudo medir.
"""
import json
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

    # Identificadores del MARCADO, DERIVADOS del propio fichero (nunca una
    # lista escrita aqui: una lista blanca solo protege de lo que ya conoce).
    # El arnes observable del 01-06 los necesita para poder devolver `null` a
    # todo id que no exista de verdad -- un DOM de mentira permisivo fabrica
    # falsos verdes que el navegador no tiene. Falla CERRADO: cero ids es
    # instrumento roto, jamas "0 hallazgos".
    marcado = re.sub(r'<script(?![^>]*\bsrc=)[^>]*>.*?</script>', '', html,
                     flags=re.DOTALL)
    # `\bid=` casaba tambien `data-id=` (el guion es frontera de palabra) y se
    # dejaba fuera `id='...'` con comilla simple. Sobre-derivar hace el DOM de
    # mentira mas permisivo que un navegador; sub-derivar lo hace mas estricto.
    # Las dos direcciones falsean, y esta lista es el ancla del fallo cerrado.
    ids = sorted(set(re.findall(r'(?:^|[\s"\'])id\s*=\s*["\']([^"\']+)["\']',
                                marcado)))
    if not ids:
        broken("no derive ningun id del marcado de index.html: el patron no casa")

    harness = (ROOT / 'tools' / 'dom_stub.js').read_text(encoding='utf-8')
    harness += "\nglobalThis.__IDS_DEL_MARCADO = " + json.dumps(ids) + ";\n"
    # Datos REALES de mentira, sembrados por el arnés ANTES de cargar la app:
    # ?selftest=1 tambien corre en el navegador del usuario, con sus datos
    # delante, y ya se comio el libro de operaciones una vez -- silenciosamente,
    # imprimiendo "Autopruebas OK". Este control vive FUERA de la suite a
    # proposito: uno que corriera dentro seria juez y parte.
    siembra = """
const __real = {
  'balance-ops': JSON.stringify([{ id: 'REAL1', date: '2024-05-05', type: 'buy',
                                   ticker: 'REAL', titulos: 99, price: 1, currency: 'EUR' }]),
  'balance-meta-v2': JSON.stringify({ portfolios: [{ id: 7, name: 'Mi cartera real' }], currentPortId: 7 }),
  'balance-rows-7': JSON.stringify({ rows: [{ id: 1, name: 'REAL' }] }),
  'ajeno-del-usuario': 'ni tocarlo',
};
Object.keys(__real).forEach(k => localStorage.setItem(k, __real[k]));
"""
    comprobacion = """
const __perdidas = Object.keys(__real).filter(k => localStorage.getItem(k) !== __real[k]);
if (__perdidas.length) {
  console.error('HALLAZGO: las autopruebas se comieron datos reales del usuario: ' +
                __perdidas.map(k => k + ' -> ' + localStorage.getItem(k)).join(', '));
  process.exit(1);
}
"""
    # runSelfTests es ASINCRONA desde el 01-04: el manejador de inicio de sesion
    # lo es, y partir el veredicto en dos sitios seria justo la puerta por donde
    # entra un falso verde. Se espera de verdad; una promesa que se rechaza o
    # que no resuelve una lista da rc=2, no "0 hallazgos".
    # Una promesa sin manejar mataba el proceso con rc=1 y SIN UNA PALABRA: un
    # rojo sin nombre, que manda a mirar al sitio equivocado. Se descubrio
    # saboteando el `await` que cablea las suites asincronas: el crash tapaba el
    # mensaje que ese sabotaje existe para producir. Falla CERRADO con nombre.
    guardia = """
process.on('unhandledRejection', (e) => {
  console.error('INSTRUMENTO ROTO: una promesa quedo sin manejar: ' + (e && e.stack || e));
  process.exit(2);
});
"""
    runner = guardia + harness + siembra + "\n" + js + """
if (typeof runSelfTests !== 'function') {
  console.error('INSTRUMENTO ROTO: runSelfTests no quedo definida tras cargar el script');
  process.exit(2);
}
(async () => {
  let fails;
  try { fails = await runSelfTests(); }
  catch (e) {
    console.error('INSTRUMENTO ROTO: runSelfTests lanzo: ' + (e && e.stack || e));
    process.exit(2);
  }
  if (!Array.isArray(fails)) {
    console.error('INSTRUMENTO ROTO: runSelfTests no devolvio la lista de fallos');
    process.exit(2);
  }
  if (fails.length) {
    // ESCRITURA SINCRONA. `console.error` sobre una tuberia es asincrono, y
    // `process.exit` no la vacia: con suites asincronas aun vivas, el veredicto
    // se PERDIA y la puerta imprimia un rojo SIN UNA PALABRA. Un rojo sin
    // nombre manda a mirar al sitio equivocado. Se descubrio saboteando el
    // `await` que cablea las suites, no razonandolo.
    require('fs').writeSync(2, '\\u274c ' + fails.length +
                            ' autopruebas fallidas:\\n' + fails.join('\\n') + '\\n');
    process.exit(1);
  }
""" + comprobacion + """
  process.exit(0);
})();
"""
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write(runner)
        tmp = f.name
    try:
        # check=False a proposito: el rc del hijo ES el veredicto.
        # Con timeout: una promesa que nunca resuelve dejaba el arnes COLGADO
        # para siempre, sin salida y sin rc. Colgarse no es un veredicto; hay
        # que fallar CERRADO con nombre.
        r = subprocess.run(['node', tmp], capture_output=True, text=True,
                           check=False, timeout=120)
    except FileNotFoundError:
        broken("node no esta instalado")
    except subprocess.TimeoutExpired:
        broken("runSelfTests no termino en 120s: alguna promesa no resuelve")
    finally:
        pathlib.Path(tmp).unlink(missing_ok=True)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    sys.exit(r.returncode)

if __name__ == '__main__':
    main()
