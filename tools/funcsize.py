#!/usr/bin/env python3
"""Trinquete de tamano de funciones de index.html.

La app es un fichero unico por decision de proyecto, asi que no se puede exigir
"modulos hoja". Lo que si se puede exigir es que el monolito no engorde: ninguna
funcion nueva pasa del umbral, y las que ya lo pasaban solo pueden encoger.

CEGUERAS DECLARADAS (antes de que alguien las descubra):
  - Solo ve funciones declaradas como `function NOMBRE(` o `async function
    NOMBRE(` a nivel superior del bloque <script> inline. NO ve funciones
    flecha, metodos de objeto, funciones anonimas asignadas a variables ni
    closures anidadas. Una funcion de 300 lineas escrita como
    `const f = () => {...}` es INVISIBLE a este instrumento.
    Las `async function` se anadieron al ambito en el 01-04 (version 2 de la
    semantica) porque volver `runSelfTests` asincrona la habia sacado de la
    medida SIN QUE NADA se pusiera rojo: el banco de sabotaje lo destapo al
    engordarla 80 lineas y ver que la puerta seguia verde. Es un APRIETE de la
    vara, y por eso obliga a resellar la foto a proposito.
  - Cuenta lineas crudas del cuerpo, comentarios y blancos incluidos.
  - De la foto sellada valida la PRESENCIA y el TIPO de `semantica`, `excede` y
    de cada lista de `excede`. NO valida `funciones_vistas` (es informativa y
    no dirige ninguna decision) ni el contenido de `semantica` clave por clave:
    esa se compara ENTERA contra SEMANTICA, y cualquier diferencia es deriva.
  - La huella no lleva numero de linea: reordenar el fichero no la mueve.
  - Al contar llaves salta cadenas, plantillas, comentarios y expresiones
    regulares. Distinguir una regex de una division se hace por heuristica
    (que caracter la precede), como cualquier tokenizador sin gramatica
    completa. Si se equivocara, el instrumento no calla: da rc=2.

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
    'ambito': 'funciones `function NOMBRE(` y `async function NOMBRE(` de primer nivel '
              'del <script> inline de index.html',
    'metrica': 'lineas crudas del cuerpo, comentarios y blancos incluidos',
    'version': 2,
}


def fin_de_cadena(js, i):
    """Devuelve el indice justo despues de la cadena que empieza en i."""
    comilla = js[i]
    k = i + 1
    while k < len(js):
        if js[k] == '\\':
            k += 2
            continue
        if js[k] == comilla:
            return k + 1
        # Interpolacion de plantilla: puede contener llaves y cadenas propias.
        if comilla == '`' and js[k] == '$' and k + 1 < len(js) and js[k + 1] == '{':
            prof, k = 1, k + 2
            while k < len(js) and prof:
                if js[k] in '"\'`':
                    k = fin_de_cadena(js, k)
                    continue
                if js[k] == '{':
                    prof += 1
                elif js[k] == '}':
                    prof -= 1
                k += 1
            continue
        k += 1
    return k


def es_regex(js, i):
    """¿La barra en i abre un literal /.../ o es una division?

    Heuristica del tokenizador pobre: mira el ultimo caracter con significado
    que hay antes. Tras un valor (identificador, numero, cierre de parentesis)
    una barra divide; tras un operador o un separador, abre una expresion
    regular.
    """
    k = i - 1
    while k >= 0 and js[k] in ' \t\n\r':
        k -= 1
    if k < 0:
        return True
    c = js[k]
    if c in ')]}':
        return False
    if c.isalnum() or c in '_$':
        # Palabras clave tras las que una barra abre regex, no divide.
        fin = k + 1
        while k >= 0 and (js[k].isalnum() or js[k] in '_$'):
            k -= 1
        return js[k + 1:fin] in {'return', 'typeof', 'case', 'in', 'of', 'new',
                                 'delete', 'do', 'else', 'instanceof', 'void',
                                 'throw', 'yield', 'await'}
    return True


def fin_de_regex(js, i):
    """Devuelve el indice justo despues del literal regex que empieza en i."""
    k = i + 1
    en_clase = False
    while k < len(js):
        c = js[k]
        if c == '\\':
            k += 2
            continue
        if c == '[':
            en_clase = True
        elif c == ']':
            en_clase = False
        elif c == '/' and not en_clase:
            k += 1
            while k < len(js) and js[k].isalpha():   # banderas: g, i, m...
                k += 1
            return k
        elif c == '\n':
            return k   # una regex no cruza lineas: era una division
        k += 1
    return k


def fin_de_comentario(js, i):
    """Devuelve el indice justo despues del comentario que empieza en i."""
    if js[i + 1] == '/':
        n = js.find('\n', i)
        return len(js) if n == -1 else n
    n = js.find('*/', i + 2)
    return len(js) if n == -1 else n + 2


def roto(msg, remedio=None):
    print(f"rc=2 INSTRUMENTO ROTO: {msg}", file=sys.stderr)
    if remedio:
        print(f"   {remedio}", file=sys.stderr)
    sys.exit(2)


# Una foto MALFORMADA bloquea los DOS modos: `--update` tambien la lee antes de
# escribir, asi que sin esto el instrumento nombraba la clave rota y no ofrecia
# ninguna salida. Un mensaje que nombra el defecto y no el remedio deja al
# operador editando JSON a mano, que es como se afloja una vara sin querer.
REMEDIO_FOTO = ("Si la foto esta corrupta y quieres volver a sellarla desde cero: "
                "borra el fichero y corre --update (con el fichero ausente, "
                "--update sella sin comparar).")


class EscanerRoto(Exception):
    """El escaner no pudo decidir. Se propaga para que cada instrumento le ponga
    SU mensaje de rc=2: "no pude medir" y "0 hallazgos" no comparten salida."""


def extraer_js(ruta):
    """Devuelve el JS del UNICO bloque <script> inline de ese fichero.

    Descubre el bloque en vez de enumerar nada. Lanza EscanerRoto en cuanto algo
    no cuadra: fichero ausente, vacio, o un numero de bloques distinto de uno.
    """
    if not ruta.is_file():
        raise EscanerRoto(f"no existe {ruta}")
    html = ruta.read_text(encoding='utf-8')
    if not html.strip():
        raise EscanerRoto(f"{ruta} esta vacio")
    bloques = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', html, re.DOTALL)
    if len(bloques) != 1:
        raise EscanerRoto(f"esperaba 1 bloque <script> inline, encontre {len(bloques)}")
    return bloques[0]


def localizar_funciones(js, incluir_async=False):
    """[(nombre, inicio, fin), ...] de las `function NOMBRE(` de primer nivel.

    `inicio` es el desplazamiento de la `f` de `function`; `fin`, el de la llave
    que cierra el cuerpo (inclusive). Salta cadenas, plantillas, comentarios y
    expresiones regulares al contar llaves.

    Extraida de `medir()` en el ciclo 01-04 para que `cloudwrites.py` y
    `emptycatch.py` usen ESTE escaner y no una copia: dos escaneres se
    desincronizan a la primera. El boundary se cruzo a proposito y se dijo en
    voz alta en el PLAN 01-04.

    `incluir_async=True` amplia el ambito a `async function NOMBRE(`. Desde el
    01-04 lo usan TODOS los instrumentos, `medir()` incluido: ampliarlo cambio
    lo que se MIDE, se declaro DERIVA (rc=3), se subio la version de la
    SEMANTICA de 1 a 2 y se resello la foto a proposito. Este parrafo decia
    antes lo contrario que el codigo, que es la trampa 5.1 con otro disfraz.
    """
    patron = r'^(?:async\s+)?function\s+(\w+)\s*\(' if incluir_async else r'^function\s+(\w+)\s*\('
    encontradas = []
    for m in re.finditer(patron, js, re.MULTILINE):
        try:
            j = js.index('{', m.end() - 1)
        except ValueError:
            raise EscanerRoto(f"no encuentro el cuerpo de {m.group(1)}") from None
        prof, k = 0, j
        while k < len(js):
            c = js[k]
            # Saltar cadenas y comentarios: una llave dentro de un texto no
            # abre nada. Sin esto, escribir '{' en una cadena deja ciego al
            # instrumento entero (medido el 2026-08-29).
            if c in '"\'`':
                k = fin_de_cadena(js, k)
                continue
            if c == '/' and k + 1 < len(js) and js[k + 1] in '/*':
                k = fin_de_comentario(js, k)
                continue
            if c == '/' and es_regex(js, k):
                k = fin_de_regex(js, k)
                continue
            if c == '{':
                prof += 1
            elif c == '}':
                prof -= 1
                if prof == 0:
                    break
            k += 1
        else:
            raise EscanerRoto(f"llave sin cerrar en {m.group(1)}")
        encontradas.append((m.group(1), m.start(), k))
    if not encontradas:
        raise EscanerRoto("no encontre ninguna funcion: el patron de busqueda no casa")
    return encontradas


def enmascarar(js, cadenas=False):
    """Copia de `js` del MISMO largo con los comentarios pasados a espacios.

    Con `cadenas=True` vacia ademas el interior de cadenas, plantillas y
    expresiones regulares, dejando en su sitio las comillas y las barras.

    Los desplazamientos se conservan, asi que lo que se encuentre en la copia
    esta en la misma posicion del original. Existe porque un instrumento que
    busca patrones sobre el texto crudo mide PROSA: un comentario que menciona
    `catch {}` contaba como un catch vacio de verdad (medido el 2026-08-30).
    """
    out = list(js)
    k = 0
    n = len(js)
    while k < n:
        c = js[k]
        if c == '/' and k + 1 < n and js[k + 1] in '/*':
            fin = fin_de_comentario(js, k)
            for i in range(k, min(fin, n)):
                if js[i] != '\n':
                    out[i] = ' '
            k = fin
            continue
        if c in '"\'`':
            fin = fin_de_cadena(js, k)
            if cadenas:
                for i in range(k + 1, min(fin - 1, n)):
                    if js[i] != '\n':
                        out[i] = ' '
            k = fin
            continue
        if c == '/' and es_regex(js, k):
            fin = fin_de_regex(js, k)
            if cadenas:
                for i in range(k + 1, min(fin, n)):
                    if js[i] != '\n':
                        out[i] = ' '
            k = fin
            continue
        k += 1
    return ''.join(out)


def funcion_de(funciones, pos):
    """Nombre de la funcion de primer nivel que contiene ese desplazamiento."""
    for nombre, ini, fin in funciones:
        if ini <= pos <= fin:
            return nombre
    return None


def medir():
    """Devuelve {nombre: [lineas, ...]} de las funciones que exceden el umbral."""
    try:
        js = extraer_js(INDEX)
        funciones = localizar_funciones(js, incluir_async=True)
    except EscanerRoto as e:
        roto(str(e))

    excede = {}
    for nombre, ini, fin in funciones:
        lineas = js[ini:fin + 1].count('\n') + 1
        if lineas > SEMANTICA['umbral_lineas']:
            excede.setdefault(nombre, []).append(lineas)
    return {n: sorted(v, reverse=True) for n, v in excede.items()}, len(funciones)


def cargar_baseline():
    """Lee la foto sellada validando el TIPO de cada clave, no solo su presencia.

    `"excede": null` es JSON valido y pasaba el chequeo de forma anterior: el
    instrumento reventaba DESPUES con un TypeError sin capturar y rc=1, o sea
    rotulado como "el codigo ha engordado". Un instrumento roto que se disfraza
    de hallazgo manda a mirar el sitio equivocado (CLAUDE.md 4.3).
    """
    if not BASELINE.is_file():
        roto(f"no existe la foto sellada {BASELINE}; sellala con --update")
    try:
        d = json.loads(BASELINE.read_text(encoding='utf-8'))
    except Exception as e:  # noqa: BLE001 - fallar CERRADO ante cualquier lectura mala
        roto(f"la foto sellada no se puede leer: {e}", REMEDIO_FOTO)
    if not isinstance(d, dict):
        roto(f"funcsize: la foto sellada {BASELINE.name} no es un objeto JSON, "
             f"es {type(d).__name__}", REMEDIO_FOTO)
    for clave in ('semantica', 'excede'):
        if clave not in d:
            roto(f"funcsize: la foto sellada {BASELINE.name} no tiene la clave "
                 f"'{clave}'", REMEDIO_FOTO)
        if not isinstance(d[clave], dict):
            roto(f"funcsize: la foto sellada {BASELINE.name}: la clave '{clave}' "
                 f"es {type(d[clave]).__name__}, se esperaba un objeto", REMEDIO_FOTO)
    for nombre, valores in d['excede'].items():
        if not isinstance(valores, list) or not all(
                isinstance(v, int) and not isinstance(v, bool) for v in valores):
            roto(f"funcsize: la foto sellada {BASELINE.name}: la clave "
                 f"'excede[{nombre}]' deberia ser una lista de enteros",
                 REMEDIO_FOTO)
    return d


def comparar_o_roto(actual, sellado, clave):
    """`comparar` fallando CERRADO: cualquier sorpresa sale como rc=2 CON NOMBRE.

    El `except` es ESTRECHO a proposito. `SystemExit` no esta en la lista, asi
    que un hallazgo real (rc=1) NUNCA se convierte en rc=2: capturar demasiado
    ancho taparia el hallazgo con el aviso y mandaria a mirar las herramientas
    en vez del codigo. Ese defecto ya se cometio una vez, el 2026-08-29.

    SIN ORACULO, Y SE DICE: hoy este `except` es INALCANZABLE por construccion.
    `cargar_baseline` ya valida los tipos de todo lo que llega aqui, asi que
    `comparar` no puede lanzar ninguna de esas excepciones, y los sabotajes de
    la foto malformada pasan CON y SIN este envoltorio -- lo que miden es la
    validacion, no esto. Se deja como red por si manana se anade una clave sin
    validarla, pero NO cuenta como control medido: esta fichado en .paul/DEUDAS.md.
    """
    try:
        return comparar(actual, sellado)
    except (TypeError, AttributeError, KeyError, ValueError) as e:
        roto(f"funcsize: no pude comparar contra la clave '{clave}' de "
             f"{BASELINE.name}: {type(e).__name__}: {e}")


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
            peor, mejor = comparar_o_roto(actual, sellado['excede'], 'excede')
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

    peor, mejor = comparar_o_roto(actual, sellado['excede'], 'excede')

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
