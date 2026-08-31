#!/usr/bin/env python3
"""Censo de los AVISOS AL OPERADOR de index.html, contra una foto sellada.

La meta de la Fase 1 es que ningun fallo de guardado ni de arranque pueda
borrar el libro de operaciones EN SILENCIO. Un fallo pintado en verde, o
degradado a un mensaje informativo, o que cambia de texto sin que nadie se
entere, ES ese silencio. Hasta el 01-06 la capa de aviso no tenia oraculo
ninguno (D-38): nueve mutantes de esa capa sobrevivian a la puerta ENTERA.

Dos redes DISJUNTAS, como en cloudwrites.py:

  RED A -- por RECEPTOR. Los elementos del aviso (el indicador de guardado y
  los del indicador de sincronizacion) se DERIVAN del texto de los pintores, y
  luego se exige que NADIE mas los toque. Cierra la clase: un tercer pintor
  futuro que escribiera directamente sobre ellos seria invisible para una
  lista de canales, y aqui sale rojo con su nombre.

  RED B -- por CANAL. Censo de los avisos de consola y de ventana emergente
  alcanzables desde el guardado, la subida, el arranque y el camino de sesion,
  con su NIVEL y su PREFIJO LITERAL, contra una foto sellada. Degradar un
  `console.error` a `console.info`, o cambiar el texto, mueve la huella y la
  puerta se pone roja.

CEGUERAS DECLARADAS (antes de que alguien las descubra):
  - ES ESTATICO. Presencia no es precedencia (CLAUDE.md 5.11): un literal
    escrito dentro de una CADENA cuenta como cobertura. Los comentarios SI se
    borran antes de medir, asi que un comentario no cuela.
  - La RED A solo ve `getElementById` con un literal (comillas simples, dobles
    o invertidas). Un `getElementById(variable)` que acabara resolviendo a un
    elemento de aviso le es invisible. No se cierra por lista blanca de
    variables porque el fichero tiene decenas de identificadores compuestos
    legitimos (`'bar-' + id`).
  - El AMBITO de la RED B es TODO el <script>: todas las funciones de primer
    nivel mas el codigo suelto. NO hay cierre transitivo, ni raices. Se probaron
    las dos cosas y las dos perdieron avisos reales del camino de la fase
    (medido dos veces por brazos adversarios, 2026-08-31). Lo unico escrito a
    mano son los CORTES, nombrados uno a uno con su motivo; cambiarlos es
    DERIVA (rc=3). Lo que queda fuera esta en la ficha D-44 de .paul/DEUDAS.md.
  - Como el ambito es TODO, el censo incluye avisos que NO son de guardado ni
    de arranque (borrado de carteras y de operaciones, vaciado de activos,
    reconocimiento de capturas). No se excluyen: se sellan con su motivo. Un
    instrumento con juicio dentro es un instrumento que se dobla.
  - Un aviso que DESAPARECE es un HALLAZGO, no una mejora. Aqui la direccion
    buena no es "menos": una boca que se cierra es exactamente el silencio que
    esta fase existe para impedir. Por eso este instrumento NO compara por
    dominacion como funcsize o emptycatch.
  - Atribuye cada aviso a la funcion de PRIMER NIVEL que lo contiene. Uno
    dentro de una flecha o de una IIFE se atribuye a '<nivel superior>'.

Huella: MULTICONJUNTO {funcion|nivel|prefijo: cuantos}, SIN numero de linea.
  - Un conteo TOTAL seria un control de paridad: quitar uno aqui y meter otro
    alla dejaria la misma cifra y saldria verde.
  - Con numero de linea, reordenar el fichero moveria todo y esto seria
    inservible.

Codigos de salida (nominales, cada uno con su mensaje):
  0  verde
  1  hallazgo real: un aviso nuevo o cambiado, o un receptor fuera de los pintores
  2  instrumento roto: no pudo medir (con su REMEDIO impreso)
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
    fin_de_cadena,
    funcion_de,
    localizar_funciones,
)

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / 'index.html'
BASELINE = ROOT / '.paul' / 'baseline-avisos.json'

# La SEMANTICA de la medida. Si esto cambia, la foto anterior no es comparable
# y el instrumento dice DERIVA (rc=3) SIN ofrecer el comando de resellado.
SEMANTICA = {
    'version': 1,
    'ambito': 'bloque <script> inline de index.html',
    # '<nivel superior>' NO es una funcion: es el codigo suelto del <script>,
    # que es literalmente el ARRANQUE (init de Firebase, el listener de `load`,
    # el registro del service worker). Dejarlo fuera habria dejado sin censo
    # justo la mitad de la meta de la fase, que dice «guardado NI DE ARRANQUE».
    # AMBITO: TODO el <script>, sin cierre transitivo ninguno.
    #
    # Hubo dos intentos antes, y los dos fallaron POR MEDICION, no por teoria:
    #   1) ocho raices escritas a mano -> un brazo adversario encontro nueve
    #      avisos reales del camino de la fase fuera del censo. Cada agujero se
    #      tapaba anadiendo la novena raiz: la lista blanca que este instrumento
    #      existe para NO necesitar (5.15).
    #   2) raices derivadas (arranque + manejadores del marcado) con cierre
    #      transitivo -> se PERDIO `guardarTodo`, que es el guardado en persona,
    #      porque solo se alcanza como ARGUMENTO (`setTimeout(guardarTodo, 600)`)
    #      y el cierre no seguia esa arista. Un cierre transitivo sobre JS tiene
    #      mas formas de escaparse de las que uno puede enumerar.
    #
    # Asi que no se enumera: se mide TODO y se EXIME por nombre. El instrumento
    # MIDE; quien exime es el criterio, escrito en 'cortes' con su motivo.
    'ambito_funciones': 'todas las de primer nivel, mas el codigo suelto, menos los cortes',
    'pintores': ['setSyncUI', 'showSaveIndicator'],
    # CORTES: se alcanzan desde una raiz pero su subarbol NO es «aviso al
    # operador», asi que el cierre transitivo se para ahi. Nombrados UNO A UNO
    # con su motivo, nunca una regla que exima categorias enteras.
    #   runSelfTests: el listener de `?selftest=1` cuelga del nivel superior.
    #     Sus avisos son el VEREDICTO de la propia suite, no un aviso de la app,
    #     y ya tienen juez propio: el codigo de salida de la puerta.
    'cortes': ['runSelfTests'],
    'canales': {'console.error': 'error', 'console.warn': 'aviso',
                'alert': 'emergente', 'confirm': 'emergente'},
    'huella': 'multiconjunto {funcion|nivel|prefijo}: cuantos, sin numero de linea',
}

REMEDIO_FOTO = ("Si la foto esta corrupta y quieres volver a sellarla desde cero: "
                "borra el fichero y corre --update (con el fichero ausente, "
                "--update sella sin comparar).")


def roto(msg, remedio=None):
    print(f"rc=2 INSTRUMENTO ROTO: {msg}", file=sys.stderr)
    if remedio:
        print(f"   {remedio}", file=sys.stderr)
    sys.exit(2)


def leer():
    """(codigo, funciones). Falla CERRADO ante cualquier sorpresa."""
    try:
        js = extraer_js(INDEX)
        funciones = localizar_funciones(js, incluir_async=True)
    except EscanerRoto as e:
        roto(str(e))
    # Se mide sobre el CODIGO, no sobre la prosa: los comentarios se borran.
    # Las CADENAS se conservan porque el prefijo literal de un aviso vive
    # justamente dentro de una cadena.
    return enmascarar(js), funciones


def cuerpo_de(js, funciones, nombre):
    """Cuerpo de una funcion, o el codigo SUELTO si se pide '<nivel superior>'.

    Antes esto devolvia None para '<nivel superior>' y `alcanzables()` lo
    convertia en '': la raiz aportaba sus avisos pero sus LLAMADAS no se seguian
    NUNCA. Consecuencia medida el 2026-08-31 por un brazo adversario: un aviso
    sembrado en `migrateOpsToGlobal` --llamada desde el listener de `load`, o
    sea desde el ARRANQUE-- salia rc=0. Por eso `initPortfolios` y `schedSave`
    habian tenido que anadirse a mano como raices, que es la lista blanca que
    este instrumento existe para no necesitar.
    """
    if nombre == '<nivel superior>':
        suelto = list(js)
        for _, ini, fin in funciones:
            for i in range(ini, min(fin + 1, len(suelto))):
                if suelto[i] != '\n':
                    suelto[i] = ' '
        return ''.join(suelto)
    for n, ini, fin in funciones:
        if n == nombre:
            return js[ini:fin + 1]
    return None


def ids_de_los_pintores(codigo, funciones):
    """Elementos del aviso, DERIVADOS del texto de los pintores."""
    ids = set()
    for pintor in SEMANTICA['pintores']:
        cuerpo = cuerpo_de(codigo, funciones, pintor)
        if cuerpo is None:
            roto(f"no encuentro el pintor '{pintor}' en index.html: el ambito "
                 "sellado ya no existe")
        ids |= set(re.findall(r"getElementById\(\s*['\"`]([^'\"`]+)['\"`]\s*\)", cuerpo))
    if not ids:
        roto("no derive ningun elemento de aviso del texto de los pintores: "
             "el patron no casa y la RED A estaria midiendo el vacio")
    return sorted(ids)


def red_a(codigo, funciones, ids, exentos):
    """Quien toca los elementos del aviso desde FUERA de los pintores."""
    fuera = []
    for m in re.finditer(r"getElementById\(\s*['\"`]([^'\"`]+)['\"`]\s*\)", codigo):
        if m.group(1) not in ids:
            continue
        quien = funcion_de(funciones, m.start()) or '<nivel superior>'
        if quien in SEMANTICA['pintores'] or quien in exentos:
            continue
        fuera.append(f"{quien}: toca '{m.group(1)}' fuera de los pintores")
    return sorted(fuera)


def ambito(codigo, funciones):
    """TODAS las funciones de primer nivel + el codigo suelto, menos los cortes.

    Sin cierre transitivo: ver el comentario de SEMANTICA['ambito_funciones'].
    Falla CERRADO si un corte sellado ya no existe: un corte que no exime a
    nadie es un corte que dejo de decir la verdad, y callarlo seria seguir
    eximiendo a ciegas.
    """
    nombres = {n for n, _, _ in funciones}
    huerfanos = [c for c in SEMANTICA['cortes'] if c not in nombres]
    if huerfanos:
        roto("hay cortes sellados que ya no existen en index.html: "
             + ', '.join(huerfanos),
             "Si la funcion se renombro o se borro, el corte hay que quitarlo o "
             "reescribirlo A PROPOSITO: es un cambio de la regla de medida.")
    return (nombres | {'<nivel superior>'}) - set(SEMANTICA['cortes'])


def prefijo_literal(codigo, i):
    """Prefijo literal del aviso que abre en `i` (el parentesis), o None.

    Es el texto LITERAL COMPLETO hasta el primer dato variable. "Una subcadena
    lo bastante larga" no es un criterio: quien juzga "bastante" seria el mismo
    que escribe el aserto, que es la trampa de `\\btest\\b` del catalogo.
    """
    k = i + 1
    while k < len(codigo) and codigo[k] in ' \t\n\r':
        k += 1
    if k >= len(codigo) or codigo[k] not in '"\'`':
        return None
    fin = fin_de_cadena(codigo, k)
    bruto = codigo[k + 1:fin - 1]
    return bruto.split('${')[0]


def censar():
    """{funcion|nivel|prefijo: cuantos}. Falla CERRADO si no puede medir."""
    codigo, funciones = leer()
    alcance = ambito(codigo, funciones)
    cuenta = {}
    for canal, nivel in SEMANTICA['canales'].items():
        patron = re.escape(canal) + r'\s*\('
        for m in re.finditer(patron, codigo):
            # `console.error = ...` (un espia de las autopruebas) no es un aviso.
            quien = funcion_de(funciones, m.start()) or '<nivel superior>'
            if quien not in alcance:
                continue
            prefijo = prefijo_literal(codigo, m.end() - 1)
            if prefijo is None:
                prefijo = '<sin literal>'
            clave = f"{quien}|{nivel}|{prefijo}"
            cuenta[clave] = cuenta.get(clave, 0) + 1
    if not cuenta:
        roto("el censo de avisos salio VACIO: o el ambito no se derivo o los "
             "patrones no casan. Cero avisos no es 'ningun hallazgo'.")
    return cuenta, sorted(alcance)


def cargar_baseline():
    """Lee la foto validando TIPO y no solo presencia, `motivos` incluida."""
    if not BASELINE.is_file():
        roto(f"no existe la foto sellada {BASELINE}; sellala con --update")
    try:
        d = json.loads(BASELINE.read_text(encoding='utf-8'))
    except Exception as e:  # noqa: BLE001 - fallar CERRADO ante cualquier lectura mala
        roto(f"la foto sellada no se puede leer: {e}", REMEDIO_FOTO)
    if not isinstance(d, dict):
        roto(f"avisos: la foto sellada {BASELINE.name} no es un objeto JSON, "
             f"es {type(d).__name__}", REMEDIO_FOTO)
    for clave in ('semantica', 'avisos', 'motivos', 'exentos_red_a'):
        if clave not in d:
            roto(f"avisos: la foto sellada {BASELINE.name} no tiene la clave "
                 f"'{clave}'", REMEDIO_FOTO)
    for clave in ('semantica', 'avisos', 'motivos'):
        if not isinstance(d[clave], dict):
            roto(f"avisos: la foto sellada {BASELINE.name}: la clave '{clave}' es "
                 f"{type(d[clave]).__name__}, se esperaba un objeto", REMEDIO_FOTO)
    if not isinstance(d['exentos_red_a'], dict):
        roto(f"avisos: la foto sellada {BASELINE.name}: 'exentos_red_a' es "
             f"{type(d['exentos_red_a']).__name__}, se esperaba un objeto "
             "{funcion: motivo}", REMEDIO_FOTO)
    for k, v in d['avisos'].items():
        if not isinstance(v, int) or isinstance(v, bool):
            roto(f"avisos: la foto sellada {BASELINE.name}: 'avisos[{k}]' deberia "
                 "ser un entero", REMEDIO_FOTO)
    for grupo in ('motivos', 'exentos_red_a'):
        for k, v in d[grupo].items():
            if not isinstance(v, str):
                roto(f"avisos: la foto sellada {BASELINE.name}: '{grupo}[{k}]' "
                     "deberia ser un texto", REMEDIO_FOTO)
    return d


def comparar(actual, sellado):
    """Compara por DOMINACION: un aviso que desaparece no es una regresion."""
    peor, mejor = [], []
    for k in sorted(set(actual) | set(sellado)):
        a, s = actual.get(k, 0), sellado.get(k, 0)
        if a > s:
            peor.append(f"{k}  ({s} -> {a}): aviso NUEVO o CAMBIADO, sin cobertura sellada")
        elif a < s:
            mejor.append(f"{k}  ({s} -> {a}): ha desaparecido")
    return peor, mejor


def comparar_o_roto(actual, sellado, clave):
    """`comparar` fallando CERRADO: cualquier sorpresa sale como rc=2 CON NOMBRE.

    `except` ESTRECHO a proposito: `SystemExit` queda fuera, asi que un hallazgo
    real (rc=1) nunca se convierte en rc=2.
    """
    try:
        return comparar(actual, sellado)
    except (TypeError, AttributeError, KeyError, ValueError) as e:
        roto(f"avisos: no pude comparar contra la clave '{clave}' de "
             f"{BASELINE.name}: {type(e).__name__}: {e}")


def imprimir_censo(actual, alcance):
    print(f"AMBITO ({len(alcance)} funciones: TODO el <script> menos los cortes "
          f"{', '.join(SEMANTICA['cortes'])}):")
    for n in alcance:
        print(f"   - {n}")
    print(f"\nCENSO de avisos ({sum(actual.values())} en {len(actual)} claves):")
    for k in sorted(actual):
        print(f"   {actual[k]}x  {k}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--check', action='store_true',
                   help='comprueba contra la foto sellada; NUNCA escribe')
    g.add_argument('--update', action='store_true', help='sella el censo actual')
    g.add_argument('--censo', action='store_true',
                   help='imprime el ambito y el censo derivados; no compara nada')
    ap.add_argument('--amnesty', action='store_true',
                    help='con --update: acepta sellar un EMPEORAMIENTO, enumerandolo')
    args = ap.parse_args()

    actual, alcance = censar()

    if args.censo:
        imprimir_censo(actual, alcance)
        return

    codigo, funciones = leer()
    ids = ids_de_los_pintores(codigo, funciones)
    exentos = {}
    if BASELINE.is_file():
        exentos = cargar_baseline()['exentos_red_a']
    intrusos = red_a(codigo, funciones, ids, exentos)

    if args.update:
        if intrusos:
            print("NO SE SELLA: hay quien toca los elementos del aviso desde fuera "
                  "de los pintores. Eso no se sella: se arregla o se exime por NOMBRE.")
            for i in intrusos:
                print(f"   - {i}")
            sys.exit(1)
        peor, mejor = ([], [])
        previo = {}
        if BASELINE.is_file():
            sellado = cargar_baseline()
            if sellado['semantica'] != SEMANTICA:
                print("rc=3 DERIVA: la regla de medida ha cambiado respecto a la foto sellada.")
                print("   Raices, canales, pintores o ambito ya no son los que se sellaron.")
                print("   Esto NO se arregla resellando: averigua POR QUE cambio la regla.")
                sys.exit(3)
            peor, mejor = comparar_o_roto(actual, sellado['avisos'], 'avisos')
            previo = sellado['motivos']
            exentos = sellado['exentos_red_a']
        if peor and not args.amnesty:
            print("NO SE SELLA: esto es un EMPEORAMIENTO, no una mejora.")
            for p in peor:
                print(f"   - {p}")
            print("\nApretar cuesta un comando; aflojar cuesta decirlo en voz alta.")
            print("Si de verdad quieres sellarlo, repite con --amnesty y quedara en el diff.")
            sys.exit(1)
        motivos = {k: previo.get(k, 'SIN MOTIVO ESCRITO — escribelo') for k in actual}
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        BASELINE.write_text(json.dumps(
            {'semantica': SEMANTICA, 'avisos': actual, 'motivos': motivos,
             'exentos_red_a': exentos, 'elementos_de_aviso': ids},
            indent=2, ensure_ascii=False, sort_keys=True) + '\n', encoding='utf-8')
        if peor:
            print(f"SELLADO CON AMNISTIA ({len(peor)} empeoramiento(s)):")
            for p in peor:
                print(f"   - {p}")
        else:
            print(f"Foto sellada: {sum(actual.values())} aviso(s) en {len(actual)} claves.")
        return

    # --check: no escribe NUNCA.
    sellado = cargar_baseline()
    if sellado['semantica'] != SEMANTICA:
        print("rc=3 DERIVA: la regla de medida ha cambiado respecto a la foto sellada.")
        print("   Raices, canales, pintores o ambito ya no son los que se sellaron, asi")
        print("   que comparar las cifras no significa nada. Esto NO se arregla resellando.")
        sys.exit(3)

    peor, mejor = comparar_o_roto(actual, sellado['avisos'], 'avisos')

    # El orden del veredicto es una decision: ante delta mixto gana el
    # EMPEORAMIENTO, y NO se imprime el comando de resellado. Si ganara el
    # mensaje de "mejora", el operador obedeceria y el empeoramiento quedaria
    # amnistiado dentro. Los dos casos dan rc distinto de cero, asi que ningun
    # sabotaje que mire solo el rc lo cazaria: el defecto vive en el MENSAJE.
    if intrusos:
        print("HALLAZGO (rc=1): alguien toca los elementos del aviso desde fuera "
              "de los pintores.")
        for i in intrusos:
            print(f"   - {i}")
        sys.exit(1)
    if peor:
        print("HALLAZGO (rc=1): la capa de aviso ha cambiado sin que la foto lo sepa.")
        for p in peor:
            print(f"   - {p}")
        print("\nUn aviso nuevo, con otro texto o con otro NIVEL es un aviso sin oraculo.")
        sys.exit(1)
    if mejor:
        # NO se imprime el comando de resellado, a proposito. Un aviso que
        # desaparece --degradado a un canal no censado, o borrado-- es la
        # categoria de dano que da nombre a la fase. Si aqui se ofreciera el
        # resellado, el operador obedeceria y el silencio quedaria amnistiado
        # dentro (CLAUDE.md 4.4). Medido: degradar un `console.error` del
        # arranque a `console.log` salia rotulado como "ha desaparecido" y con
        # el comando de sellado debajo.
        print("HALLAZGO (rc=1): han DESAPARECIDO avisos que la foto sellaba.")
        for m in mejor:
            print(f"   - {m}")
        print("\nUna boca que se cierra es el silencio que esta fase existe para impedir.")
        print("Si de verdad sobra, quitalo del codigo Y de la foto en el MISMO commit,")
        print("diciendo por que en el libro de deudas. No se resella de tramite.")
        sys.exit(1)
    print(f"Capa de aviso sin cambios: {sum(actual.values())} aviso(s) en "
          f"{len(actual)} claves; elementos {', '.join(ids)} solo los tocan los pintores.")


if __name__ == '__main__':
    main()
