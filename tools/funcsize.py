#!/usr/bin/env python3
"""Trinquete de tamano de funciones de index.html.

La app es un fichero unico por decision de proyecto, asi que no se puede exigir
"modulos hoja". Lo que si se puede exigir es que el monolito no engorde: ninguna
funcion nueva pasa del umbral, y las que ya lo pasaban solo pueden encoger.

CEGUERAS DECLARADAS (antes de que alguien las descubra):
  - Solo ve funciones declaradas como `function NOMBRE(` a nivel superior del
    bloque <script> inline. NO ve funciones flecha, metodos de objeto, funciones
    anonimas asignadas a variables ni closures anidadas. Una funcion de 300
    lineas escrita como `const f = () => {...}` es INVISIBLE a este instrumento.
  - Cuenta lineas crudas del cuerpo, comentarios y blancos incluidos.
  - La huella no lleva numero de linea: reordenar el fichero no la mueve.

Codigos de salida (nominales, cada uno con su mensaje):
  0  verde
  1  hallazgo real: una funcion nueva excede, o una que ya excedia ha crecido
  2  instrumento roto: no pudo medir
  3  deriva: cambio la regla de medida, la foto ya no es comparable
"""
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / 'index.html'
BASELINE = ROOT / '.paul' / 'baseline-funcs.json'

# La SEMANTICA de la medida. Si esto cambia, la foto anterior no es comparable.
SEMANTICA = {
    'umbral_lineas': 60,
    'ambito': 'funciones `function NOMBRE(` de primer nivel del <script> inline de index.html',
    'metrica': 'lineas crudas del cuerpo, comentarios y blancos incluidos',
    'version': 1,
}


def roto(msg):
    print(f"rc=2 INSTRUMENTO ROTO: {msg}", file=sys.stderr)
    sys.exit(2)


def medir():
    """Devuelve {nombre: [lineas, ...]} de las funciones que exceden el umbral."""
    if not INDEX.is_file():
        roto(f"no existe {INDEX}")
    html = INDEX.read_text(encoding='utf-8')
    if not html.strip():
        roto(f"{INDEX} esta vacio")
    bloques = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', html, re.DOTALL)
    if len(bloques) != 1:
        roto(f"esperaba 1 bloque <script> inline, encontre {len(bloques)}")
    js = bloques[0]

    excede = {}
    vistas = 0
    for m in re.finditer(r'^function\s+(\w+)\s*\(', js, re.MULTILINE):
        try:
            j = js.index('{', m.end() - 1)
        except ValueError:
            roto(f"no encuentro el cuerpo de {m.group(1)}")
        prof, k = 0, j
        while k < len(js):
            if js[k] == '{':
                prof += 1
            elif js[k] == '}':
                prof -= 1
                if prof == 0:
                    break
            k += 1
        else:
            roto(f"llave sin cerrar en {m.group(1)}")
        vistas += 1
        lineas = js[m.start():k + 1].count('\n') + 1
        if lineas > SEMANTICA['umbral_lineas']:
            excede.setdefault(m.group(1), []).append(lineas)

    if vistas == 0:
        roto("no encontre ninguna funcion: el patron de busqueda no casa")
    return {n: sorted(v, reverse=True) for n, v in excede.items()}, vistas


def cargar_baseline():
    if not BASELINE.is_file():
        roto(f"no existe la foto sellada {BASELINE}; sellala con --update")
    try:
        d = json.loads(BASELINE.read_text(encoding='utf-8'))
    except Exception as e:  # noqa: BLE001 - fallar CERRADO ante cualquier lectura mala
        roto(f"la foto sellada no se puede leer: {e}")
    if not isinstance(d, dict) or 'semantica' not in d or 'excede' not in d:
        roto("la foto sellada no tiene la forma esperada")
    return d


def comparar(actual, sellado):
    """Compara por DOMINACION: encoger nunca es regresion.

    Devuelve (empeoramientos, mejoras) como listas de textos.
    """
    peor, mejor = [], []
    nombres = set(actual) | set(sellado)
    for n in sorted(nombres):
        a = sorted(actual.get(n, []), reverse=True)
        s = sorted(sellado.get(n, []), reverse=True)
        if a == s:
            continue
        if len(a) > len(s):
            peor.append(f"{n}: aparece {len(a)} vez/veces excediendo, la foto sellaba {len(s)}")
            continue
        if len(a) < len(s):
            mejor.append(f"{n}: ya no excede en {len(s) - len(a)} sitio(s)")
            continue
        for va, vs in zip(a, s):
            if va > vs:
                peor.append(f"{n}: {vs} -> {va} lineas (ha crecido {va - vs})")
            elif va < vs:
                mejor.append(f"{n}: {vs} -> {va} lineas (ha encogido {vs - va})")
    return peor, mejor


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--check', action='store_true', help='comprueba contra la foto sellada; NUNCA escribe')
    g.add_argument('--update', action='store_true', help='sella la foto actual')
    ap.add_argument('--amnesty', action='store_true',
                    help='con --update: acepta sellar un EMPEORAMIENTO, enumerandolo uno a uno')
    args = ap.parse_args()

    actual, vistas = medir()

    if args.update:
        peor, mejor = ([], [])
        if BASELINE.is_file():
            sellado = cargar_baseline()
            if sellado['semantica'] != SEMANTICA:
                print("rc=3 DERIVA: la regla de medida ha cambiado respecto a la foto sellada.")
                print("   La foto anterior no es comparable. Revisa POR QUE cambio la regla")
                print("   antes de sellar nada: aflojar la vara borra hallazgos en silencio.")
                sys.exit(3)
            peor, mejor = comparar(actual, sellado['excede'])
        if peor and not args.amnesty:
            print("NO SE SELLA: esto es un EMPEORAMIENTO, no una mejora.")
            for p in peor:
                print(f"   - {p}")
            print("\nApretar cuesta un comando; aflojar cuesta decirlo en voz alta.")
            print("Si de verdad quieres sellarlo, repite con --amnesty y quedara en el diff.")
            sys.exit(1)
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        BASELINE.write_text(json.dumps(
            {'semantica': SEMANTICA, 'funciones_vistas': vistas, 'excede': actual},
            indent=2, ensure_ascii=False, sort_keys=True) + '\n', encoding='utf-8')
        if peor:
            print(f"SELLADO CON AMNISTIA ({len(peor)} empeoramiento(s)):")
            for p in peor:
                print(f"   - {p}")
        else:
            print(f"Foto sellada: {sum(len(v) for v in actual.values())} funcion(es) por encima "
                  f"de {SEMANTICA['umbral_lineas']} lineas, sobre {vistas} vistas.")
        return

    # --check: no escribe nunca.
    sellado = cargar_baseline()
    if sellado['semantica'] != SEMANTICA:
        print("rc=3 DERIVA: la regla de medida ha cambiado respecto a la foto sellada.")
        print("   Umbral, ambito o metrica ya no son los que se sellaron, asi que")
        print("   comparar las cifras no significa nada. Esto NO se arregla resellando.")
        sys.exit(3)

    peor, mejor = comparar(actual, sellado['excede'])

    # El orden del veredicto es una decision: ante un delta mixto gana el
    # EMPEORAMIENTO, para que el mensaje no dirija la mano hacia un sellado que
    # amnistiaria la regresion de rebote.
    if peor:
        print(f"rc=1 EL MONOLITO HA ENGORDADO ({len(peor)} empeoramiento(s)):")
        for p in peor:
            print(f"   - {p}")
        if mejor:
            print(f"   (tambien hay {len(mejor)} mejora(s), pero no compensan lo anterior)")
        print(f"\nUna funcion nueva no deberia pasar de {SEMANTICA['umbral_lineas']} lineas.")
        print("Si el crecimiento es deliberado, sellalo a proposito y que quede en el diff.")
        sys.exit(1)
    if mejor:
        print(f"Verde, y ademas {len(mejor)} mejora(s):")
        for m in mejor:
            print(f"   - {m}")
        print("\nSella la mejora para que no se pueda deshacer:  tools/funcsize.py --update")
        return
    print(f"Verde: {sum(len(v) for v in actual.values())} funcion(es) por encima del umbral, "
          f"las mismas que sella la foto.")


if __name__ == '__main__':
    main()
