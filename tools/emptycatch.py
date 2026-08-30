#!/usr/bin/env python3
"""Censo de `catch` vacios de index.html, contra una foto sellada.

Un `catch` vacio se traga un error y sigue como si nada. En el camino de subida
eso costo D-34: una cartera cuyo blob no parseaba desaparecia del paquete y,
como `ref.set` REEMPLAZA el documento entero, se borraba de la nube en silencio.

Esto NO es un grep de un acta: es un control con foto sellada, que se pone rojo
cuando aparece uno nuevo y que NOMBRA cuales tolera y por que.

CEGUERAS DECLARADAS (antes de que alguien las descubra):
  - SI ve `catch { /* solo un comentario */ }` y lo cuenta como vacio: los
    comentarios se borran antes de buscar, y un comentario que dice "aqui no
    hace falta hacer nada" no cablea nada (trampa 5.1). Es a proposito, y es
    mas estricto de lo que decia el PLAN 01-04.
  - No ve `catch { ; }` ni un cuerpo con solo `return;`.
  - No ve los EQUIVALENTES FUNCIONALES de tragarse un error: `.catch(() => {})`,
    callbacks de error vacios como el que tenia `onSnapshot`, o un `try` sin
    `catch` alrededor de una promesa. El del `onSnapshot` lo arreglo la Tarea 1
    del 01-04 a mano; este censo no lo habria visto.
  - Solo mira el <script> inline de index.html. No mira sw.js ni worker.js.
  - Atribuye cada `catch` a la funcion de PRIMER NIVEL que lo contiene,
    `async function` incluidas. Un `catch` dentro de una funcion flecha o de
    una IIFE se atribuye a '<nivel superior>'.

Huella: MULTICONJUNTO {funcion: cuantos}, SIN numero de linea.
  - Un conteo TOTAL seria un control de paridad: quitar uno aqui y meter otro
    alla dejaria la misma cifra y saldria verde.
  - Con numero de linea, reordenar el fichero moveria todo y esto seria
    inservible.

Codigos de salida (nominales, cada uno con su mensaje):
  0  verde
  1  hallazgo real: un `catch` vacio nuevo, o uno en el camino de subida
  2  instrumento roto: no pudo medir
  3  deriva: cambio la regla de medida, la foto ya no es comparable
"""
import argparse
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from funcsize import (
    EscanerRoto,
    enmascarar,
    extraer_js,
    funcion_de,
    localizar_funciones,
)

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / 'index.html'
BASELINE = ROOT / '.paul' / 'baseline-catches.json'

# Las DOS variantes. Contar solo una era la asimetria de D-34 (§5.16): dos
# predicados sobre el mismo conjunto tienen que ser el MISMO predicado.
PATRON = re.compile(r'catch\s*(?:\([^)]*\))?\s*\{\s*\}')

# Las funciones del camino de subida. CERO tolerados aqui, pase lo que pase.
# Lista ENUMERADA A SABIENDAS: no se deriva del codigo porque "estar en el
# camino de subida" es un juicio, no una propiedad sintactica. Cambiarla es
# visible en el diff, que es justo lo que se quiere.
CAMINO_SUBIDA = [
    'alIniciarSesion', 'applySyncPayload', 'buildSyncPayload', 'decidirSubida',
    'estadoSync', 'observarNube', 'pullFromFirestore', 'schedulePush',
    'subirALaNube',
]

SEMANTICA = {
    'variantes': ['catch (x) {}', 'catch {}'],
    'ambito': '<script> inline de index.html, atribuido a la function/async function de primer nivel',
    'metrica': 'multiconjunto {funcion: cuantos catch vacios}, sin numero de linea',
    'camino_subida': CAMINO_SUBIDA,
    'version': 1,
}


def roto(msg):
    print(f"rc=2 INSTRUMENTO ROTO: {msg}", file=sys.stderr)
    sys.exit(2)


def censar():
    """Devuelve ({funcion: cuantos}, total). Falla CERRADO si no puede medir."""
    try:
        js = extraer_js(INDEX)
        funciones = localizar_funciones(js, incluir_async=True)
    except EscanerRoto as e:
        roto(str(e))
    # Se busca sobre el CODIGO, no sobre la prosa: un comentario que menciona
    # un catch vacio no es un catch vacio. Los desplazamientos se conservan, asi
    # que la atribucion a la funcion sigue valiendo.
    codigo = enmascarar(js, cadenas=True)
    cuenta = {}
    total = 0
    for m in PATRON.finditer(codigo):
        nombre = funcion_de(funciones, m.start()) or '<nivel superior>'
        cuenta[nombre] = cuenta.get(nombre, 0) + 1
        total += 1
    return cuenta, total


def cargar_baseline():
    if not BASELINE.is_file():
        roto(f"no existe la foto sellada {BASELINE}; sellala con --update")
    try:
        d = json.loads(BASELINE.read_text(encoding='utf-8'))
    except Exception as e:  # noqa: BLE001 - fallar CERRADO ante cualquier lectura mala
        roto(f"la foto sellada no se puede leer: {e}")
    if not isinstance(d, dict) or 'semantica' not in d or 'tolerados' not in d:
        roto("la foto sellada no tiene la forma esperada")
    return d


def comparar(actual, sellado):
    """Compara por DOMINACION: quitar catches vacios nunca es una regresion."""
    peor, mejor = [], []
    for n in sorted(set(actual) | set(sellado)):
        a, s = actual.get(n, 0), sellado.get(n, 0)
        if a > s:
            peor.append(f"{n}: {s} -> {a} catch vacio(s) (han aparecido {a - s})")
        elif a < s:
            mejor.append(f"{n}: {s} -> {a} catch vacio(s) (han desaparecido {s - a})")
    return peor, mejor


def en_camino_de_subida(actual):
    return [f"{n}: {actual[n]} catch vacio(s) en el camino de subida"
            for n in sorted(actual) if n in CAMINO_SUBIDA]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--check', action='store_true',
                   help='comprueba contra la foto sellada; NUNCA escribe')
    g.add_argument('--update', action='store_true', help='sella el censo actual')
    ap.add_argument('--amnesty', action='store_true',
                    help='con --update: acepta sellar un EMPEORAMIENTO, enumerandolo')
    args = ap.parse_args()

    actual, total = censar()

    # CERO tolerados en el camino de subida, con o sin foto. Esto no se sella:
    # el instrumento MIDE, y aqui el criterio no exime a nadie.
    prohibidos = en_camino_de_subida(actual)

    if args.update:
        if prohibidos:
            print("NO SE SELLA: hay catch vacios en el camino de subida, y ahi no se tolera ninguno.")
            for p in prohibidos:
                print(f"   - {p}")
            sys.exit(1)
        peor, mejor = ([], [])
        if BASELINE.is_file():
            sellado = cargar_baseline()
            if sellado['semantica'] != SEMANTICA:
                print("rc=3 DERIVA: la regla de medida ha cambiado respecto a la foto sellada.")
                print("   La foto anterior no es comparable. Revisa POR QUE cambio la regla")
                print("   antes de sellar nada: aflojar la vara borra hallazgos en silencio.")
                sys.exit(3)
            peor, mejor = comparar(actual, sellado['tolerados'])
        if peor and not args.amnesty:
            print("NO SE SELLA: esto es un EMPEORAMIENTO, no una mejora.")
            for p in peor:
                print(f"   - {p}")
            print("\nApretar cuesta un comando; aflojar cuesta decirlo en voz alta.")
            print("Si de verdad quieres sellarlo, repite con --amnesty y quedara en el diff.")
            sys.exit(1)
        previo = cargar_baseline()['motivos'] if BASELINE.is_file() else {}
        motivos = {n: previo.get(n, 'SIN MOTIVO ESCRITO — escribelo') for n in actual}
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        BASELINE.write_text(json.dumps(
            {'semantica': SEMANTICA, 'total': total, 'tolerados': actual, 'motivos': motivos},
            indent=2, ensure_ascii=False, sort_keys=True) + '\n', encoding='utf-8')
        if peor:
            print(f"SELLADO CON AMNISTIA ({len(peor)} empeoramiento(s)):")
            for p in peor:
                print(f"   - {p}")
        else:
            print(f"Foto sellada: {total} catch vacio(s) en {len(actual)} funcion(es).")
        return

    # --check: no escribe NUNCA.
    sellado = cargar_baseline()
    if sellado['semantica'] != SEMANTICA:
        print("rc=3 DERIVA: la regla de medida ha cambiado respecto a la foto sellada.")
        print("   Variantes contadas, ambito o metrica ya no son los que se sellaron, asi")
        print("   que comparar las cifras no significa nada. Esto NO se arregla resellando.")
        sys.exit(3)

    peor, mejor = comparar(actual, sellado['tolerados'])

    # El orden del veredicto es una decision: ante delta mixto gana el
    # EMPEORAMIENTO, y NO se imprime el comando de resellado. Si ganara el
    # mensaje de "mejora", el operador obedeceria y el empeoramiento quedaria
    # amnistiado dentro.
    if prohibidos or peor:
        if prohibidos:
            print(f"rc=1 CATCH VACIO EN EL CAMINO DE SUBIDA ({len(prohibidos)}):")
            for p in prohibidos:
                print(f"   - {p}")
            print("   Ahi un error tragado borra datos de la nube en silencio (D-34).")
        if peor:
            print(f"rc=1 HAN APARECIDO CATCH VACIOS NUEVOS ({len(peor)}):")
            for p in peor:
                print(f"   - {p}")
        if mejor:
            print(f"   (tambien hay {len(mejor)} mejora(s), pero no compensan lo anterior)")
        print("\nUn catch vacio se traga el error y sigue. Si de verdad no hay nada que")
        print("hacer, escribelo y sellalo a proposito, para que quede en el diff.")
        sys.exit(1)
    if mejor:
        print(f"Verde, y ademas {len(mejor)} mejora(s):")
        for m in mejor:
            print(f"   - {m}")
        print("\nSella la mejora para que no se pueda deshacer:  tools/emptycatch.py --update")
        return
    print(f"Verde: {total} catch vacio(s), los mismos que nombra la foto, "
          f"y ninguno en el camino de subida.")


if __name__ == '__main__':
    main()
