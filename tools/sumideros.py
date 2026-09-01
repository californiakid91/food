#!/usr/bin/env python3
"""Censo de los SUMIDEROS DEL DANO de index.html, contra una foto sellada.

La meta de la Fase 1 es que ningun fallo de guardado ni de arranque pueda
borrar el libro de operaciones EN SILENCIO. El dano no es «alguien ignora un
booleano»: el dano es lo que SALE al mundo cuando se ignora. Y sale por dos
sitios, no por doce:

  SUMIDERO A -- SUBIR. Toda llamada al lanzador de subidas (`schedulePush`) y a
    la funcion de subida en si (`subirALaNube`). Subir lo que hay en memoria
    despues de un guardado local fallido machaca la copia buena de la nube, que
    puede ser la ultima que quede.

  SUMIDERO B -- ANUNCIAR. Toda emision de aviso de guardado al operador
    (`showSaveIndicator`). Un fallo pintado en verde ES el silencio que da
    nombre a la fase.

POR QUE ESTO Y NO UN CENSO DE LLAMANTES. Se debatio y se descarto: un censo de
«quien ignora el resultado de un guardado» nace con una decena de exenciones
escritas por NOMBRE --la lista blanca que 5.15 prohibe-- y mide un proxy
sintactico (5.11). Los sumideros, en cambio, se derivan del codigo y son pocos.

LO QUE ESTE INSTRUMENTO PROMETE Y LO QUE NO
  Promete: *ningun sumidero nuevo nace sin que alguien lo mire*.
  NO promete: «cada llamada esta gobernada por un veredicto». Eso no es
  decidible estaticamente sobre JS sin analisis de flujo: o se atribuye por
  funcion contenedora --presencia, no precedencia (5.11)-- o se sella una
  huella. Se sella la huella y se REBAJA la promesa a lo que la huella sostiene.
  Un instrumento con juicio dentro es un instrumento que se dobla (9): el
  instrumento MIDE; quien EXIME es el criterio, escrito en `motivos`.

DIRECCION DE LA COMPARACION, con su motivo -- es la decision CONTRARIA a la de
avisos.py en una mitad, y hay que decir por que para que nadie herede la
direccion equivocada por analogia:
  - 'subir'    -> por DOMINACION. Un sumidero de subida que APARECE es una
                  salida nueva sin gobernar: HALLAZGO. Uno que desaparece es
                  menos superficie de dano: se anota y pasa.
  - 'anunciar' -> en LAS DOS direcciones. Aqui desaparecer tambien es dano: una
                  boca que se cierra deja al operador sin saber que su guardado
                  fallo, que es literalmente el silencio de la fase. Es la misma
                  razon por la que avisos.py no compara por dominacion.
La direccion viaja DENTRO de la semantica sellada: cambiarla es DERIVA (rc=3).

CEGUERAS DECLARADAS (antes de que alguien las descubra):
  - ES ESTATICO y por NOMBRE. Una llamada indirecta --`const f = schedulePush;
    f();`, o pasarlo como argumento-- le es invisible. Cerrar esa clase exigiria
    un analisis de flujo que este proyecto no tiene.
  - Presencia no es precedencia (5.11): que un sumidero este en una funcion que
    ademas consulta un veredicto NO demuestra que ese veredicto lo gobierne.
  - El AMBITO es TODO el <script>: todas las funciones de primer nivel mas el
    codigo suelto, SIN cortes. Las suites de autoprueba tambien se censan: sus
    llamadas a `subirALaNube` y a `showSaveIndicator` se sellan con su motivo,
    como cualquier otra. Recortar el ambito para que cuadre con lo que a uno le
    interesa es meterle juicio al instrumento.
  - Atribuye cada sumidero a la funcion de PRIMER NIVEL que lo contiene. Uno
    dentro de una flecha o de una IIFE se atribuye a '<nivel superior>'.
  - Los comentarios se borran antes de medir; las CADENAS se conservan, asi que
    el nombre de un sumidero escrito dentro de una cadena contaria. No se ha
    dado el caso; si se diera, saldria como hallazgo y se veria.

Huella: MULTICONJUNTO {funcion|sumidero|receptor: cuantos}, SIN numero de linea.
  - Un conteo TOTAL seria un control de paridad: quitar uno aqui y meter otro
    alla dejaria la misma cifra y saldria verde.
  - Con numero de linea, reordenar el fichero moveria todo y esto seria
    inservible.

Codigos de salida (nominales, cada uno con su mensaje):
  0  verde
  1  hallazgo real: un sumidero nuevo, o una boca de aviso que se ha cerrado
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
    funcion_de,
    localizar_funciones,
)

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / 'index.html'
BASELINE = ROOT / '.paul' / 'baseline-sumideros.json'

# La SEMANTICA de la medida. Si esto cambia, la foto anterior no es comparable
# y el instrumento dice DERIVA (rc=3) SIN ofrecer el comando de resellado.
SEMANTICA = {
    'version': 1,
    'ambito': 'bloque <script> inline de index.html',
    'ambito_funciones': 'todas las de primer nivel, mas el codigo suelto; SIN cortes',
    # receptor -> sumidero. El nombre del receptor viaja en la huella para que
    # cambiar `schedulePush(` por `subirALaNube(` en el mismo sitio se vea.
    'receptores': {
        'schedulePush': 'subir',
        'subirALaNube': 'subir',
        'showSaveIndicator': 'anunciar',
    },
    # Direccion de la comparacion POR SUMIDERO, con su motivo en la cabecera.
    # Las dos formas de REFERENCIA van por dominacion: lo peligroso es que
    # APAREZCA una salida nueva pasada como valor. Que desaparezca no es una
    # boca que se cierra --las bocas de verdad son las LLAMADAS, y esas se
    # cuentan aparte con direccion 'ambas'--, asi que exigirlo pondria la puerta
    # roja por retirar un espia de prueba.
    'direccion': {'subir': 'dominacion', 'anunciar': 'ambas',
                  'subir-referencia': 'dominacion', 'anunciar-referencia': 'dominacion'},
    'huella': 'multiconjunto {funcion|sumidero|receptor}: cuantos, sin numero de linea',
}

# El marcador que `--update` deja en los motivos nuevos. Vive en una constante
# porque lo escribe `--update` y lo PROHIBE `cargar_baseline`: dos sitios que
# tienen que hablar del mismo texto, no de dos copias que se desincronizan.
MARCA_DE_RELLENO = 'SIN MOTIVO ESCRITO'

REMEDIO_FOTO = ("Si la foto esta corrupta y quieres volver a sellarla desde cero: "
                "borra el fichero y corre --update (con el fichero ausente, "
                "--update sella sin comparar).")


def roto(msg, remedio=None):
    print(f"rc=2 INSTRUMENTO ROTO: {msg}", file=sys.stderr)
    if remedio:
        print(f"   {remedio}", file=sys.stderr)
    sys.exit(2)


def leer():
    """(codigo sin prosa, funciones). Falla CERRADO ante cualquier sorpresa."""
    if not INDEX.is_file():
        roto(f"no existe {INDEX}")
    try:
        js = extraer_js(INDEX)
        funciones = localizar_funciones(js, incluir_async=True)
    except EscanerRoto as e:
        roto(str(e))
    if not funciones:
        roto("no localice ninguna funcion en index.html: el escaner no mide nada")
    return enmascarar(js), funciones


def es_declaracion(codigo, inicio):
    """True si lo que hay en `inicio` es la DECLARACION del sumidero, no una llamada.

    `function schedulePush(` casa el mismo patron que `schedulePush(`. Contarla
    inflaria la huella con un sumidero que no existe.
    """
    antes = codigo[:inicio].rstrip()
    return antes.endswith('function')


def censar():
    """{funcion|sumidero|receptor: cuantos}. Falla CERRADO si no puede medir."""
    codigo, funciones = leer()
    nombres = {n for n, _, _ in funciones}
    ausentes = [r for r in SEMANTICA['receptores'] if r not in nombres]
    if ausentes:
        # Un receptor sellado que ya no existe es un sumidero que dejo de
        # medirse: callarlo seria vigilar una ficcion.
        roto("hay sumideros sellados que ya no existen en index.html: "
             + ', '.join(sorted(ausentes)),
             "Si la funcion se renombro o se borro, el receptor hay que "
             "reescribirlo A PROPOSITO: es un cambio de la regla de medida.")
    cuenta = {}
    for receptor, sumidero in SEMANTICA['receptores'].items():
        # `?.(` es una llamada DIRECTA por nombre, no una indireccion: dejarla
        # fuera era una ceguera NO declarada por la que se abria un sumidero de
        # subida sin que nada se pusiera rojo. La destapo un brazo adversario
        # ejecutando `schedulePush?.()` y viendo rc=0.
        patron = r'\b' + re.escape(receptor) + r'\s*(?:\?\.)?\s*\('
        for m in re.finditer(patron, codigo):
            if es_declaracion(codigo, m.start()):
                continue
            quien = funcion_de(funciones, m.start()) or '<nivel superior>'
            clave = f"{quien}|{sumidero}|{receptor}"
            cuenta[clave] = cuenta.get(clave, 0) + 1
        # El sumidero PASADO COMO VALOR. `alIniciarSesion` recibe la funcion de
        # subida como dependencia (`subir: subirALaNube`) y la llama por el
        # alias: sin contar la referencia, el sumidero REAL del arranque se
        # quedaba fuera de la foto -- invisible en vez de exento, que es
        # exactamente lo que el plan de este ciclo NO queria (5.15).
        for m in re.finditer(r'\b' + re.escape(receptor) + r'\b(?!\s*(?:\?\.)?\s*\()',
                             codigo):
            if es_declaracion(codigo, m.start()):
                continue
            quien = funcion_de(funciones, m.start()) or '<nivel superior>'
            clave = f"{quien}|{sumidero}-referencia|{receptor}"
            cuenta[clave] = cuenta.get(clave, 0) + 1
    if not cuenta:
        roto("el censo de sumideros salio VACIO: o el ambito no se derivo o los "
             "patrones no casan. Cero sumideros no es 'ningun hallazgo'.")
    return cuenta


def cargar_baseline():
    """Lee la foto validando TIPO y no solo presencia."""
    if not BASELINE.is_file():
        roto(f"no existe la foto sellada {BASELINE}; sellala con --update")
    try:
        d = json.loads(BASELINE.read_text(encoding='utf-8'))
    except Exception as e:  # noqa: BLE001 - fallar CERRADO ante cualquier lectura mala
        roto(f"la foto sellada no se puede leer: {e}", REMEDIO_FOTO)
    if not isinstance(d, dict):
        roto(f"sumideros: la foto sellada {BASELINE.name} no es un objeto JSON, "
             f"es {type(d).__name__}", REMEDIO_FOTO)
    for clave in ('semantica', 'sumideros', 'motivos'):
        if clave not in d:
            roto(f"sumideros: la foto sellada {BASELINE.name} no tiene la clave "
                 f"'{clave}'", REMEDIO_FOTO)
        if not isinstance(d[clave], dict):
            roto(f"sumideros: la foto sellada {BASELINE.name}: la clave '{clave}' es "
                 f"{type(d[clave]).__name__}, se esperaba un objeto", REMEDIO_FOTO)
    for k, v in d['sumideros'].items():
        if not isinstance(v, int) or isinstance(v, bool):
            roto(f"sumideros: la foto sellada {BASELINE.name}: 'sumideros[{k}]' "
                 "deberia ser un entero", REMEDIO_FOTO)
    for k, v in d['motivos'].items():
        if not isinstance(v, str):
            roto(f"sumideros: la foto sellada {BASELINE.name}: 'motivos[{k}]' "
                 "deberia ser un texto", REMEDIO_FOTO)
    # El MOTIVO, CABLEADO. La cabecera prometia «quien EXIME es el criterio,
    # escrito en motivos», y eso era prosa: un sumidero sellado con el marcador
    # de relleno --o sin motivo ninguno-- pasaba verde para siempre. Un
    # comentario que promete un freno no cablea ningun freno (5.1). Lo destapo
    # un brazo adversario sellando con `--update --amnesty` y viendo rc=0.
    sin_motivo = sorted(set(d['sumideros']) - set(d['motivos']))
    if sin_motivo:
        roto("sumideros: hay sumideros sellados SIN motivo escrito: "
             + ', '.join(sin_motivo),
             "Escribe por que existe cada uno en 'motivos', en el mismo commit.")
    relleno = sorted(k for k, v in d['motivos'].items() if MARCA_DE_RELLENO in v)
    if relleno:
        roto("sumideros: hay sumideros sellados con el marcador de relleno, "
             "sin motivo de verdad: " + ', '.join(relleno),
             "Sustituye el marcador por el motivo real en 'motivos'.")
    return d


def sumidero_de(clave):
    """'anunciar' o 'subir' a partir de la clave de la huella. Falla CERRADO."""
    partes = clave.split('|')
    if len(partes) != 3 or partes[1] not in SEMANTICA['direccion']:
        raise ValueError(f"clave de huella con forma desconocida: {clave!r}")
    return partes[1]


def comparar(actual, sellado):
    """(peor, mejor). La direccion depende del SUMIDERO, no del capricho.

    'subir'    -> dominacion: solo APARECER es peor.
    'anunciar' -> ambas: aparecer es una salida sin gobernar y desaparecer es
                  una boca que se cierra. Las dos son dano de esta fase.
    """
    peor, mejor = [], []
    for k in sorted(set(actual) | set(sellado)):
        a, s = actual.get(k, 0), sellado.get(k, 0)
        if a == s:
            continue
        if a > s:
            peor.append(f"{k}  ({s} -> {a}): sumidero NUEVO, sin cobertura sellada")
        elif SEMANTICA['direccion'][sumidero_de(k)] == 'ambas':
            peor.append(f"{k}  ({s} -> {a}): ha DESAPARECIDO una boca de aviso")
        else:
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
        roto(f"sumideros: no pude comparar contra la clave '{clave}' de "
             f"{BASELINE.name}: {type(e).__name__}: {e}")


def imprimir_censo(actual):
    print(f"CENSO de sumideros ({sum(actual.values())} en {len(actual)} claves):")
    for k in sorted(actual):
        print(f"   {actual[k]}x  {k}")


def sellar(actual, args):
    previo, peor = {}, []
    if BASELINE.is_file():
        sellado = cargar_baseline()
        if sellado['semantica'] != SEMANTICA:
            print("rc=3 DERIVA: la regla de medida ha cambiado respecto a la foto sellada.")
            print("   Receptores, ambito o DIRECCION de la comparacion ya no son los")
            print("   que se sellaron. Esto NO se arregla resellando: averigua por que.")
            sys.exit(3)
        peor, _ = comparar_o_roto(actual, sellado['sumideros'], 'sumideros')
        previo = sellado['motivos']
    if peor and not args.amnesty:
        print("NO SE SELLA: esto es un EMPEORAMIENTO, no una mejora.")
        for p in peor:
            print(f"   - {p}")
        print("\nApretar cuesta un comando; aflojar cuesta decirlo en voz alta.")
        print("Si de verdad quieres sellarlo, repite con --amnesty y quedara en el diff.")
        sys.exit(1)
    motivos = {k: previo.get(k, MARCA_DE_RELLENO + ' — escribelo') for k in actual}
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    BASELINE.write_text(json.dumps(
        {'semantica': SEMANTICA, 'sumideros': actual, 'motivos': motivos},
        indent=2, ensure_ascii=False, sort_keys=True) + '\n', encoding='utf-8')
    if peor:
        print(f"SELLADO CON AMNISTIA ({len(peor)} empeoramiento(s)):")
        for p in peor:
            print(f"   - {p}")
    else:
        print(f"Foto sellada: {sum(actual.values())} sumidero(s) en "
              f"{len(actual)} claves.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--check', action='store_true',
                   help='comprueba contra la foto sellada; NUNCA escribe')
    g.add_argument('--update', action='store_true', help='sella el censo actual')
    g.add_argument('--censo', action='store_true',
                   help='imprime el censo derivado; no compara nada')
    ap.add_argument('--amnesty', action='store_true',
                    help='con --update: acepta sellar un EMPEORAMIENTO, enumerandolo')
    args = ap.parse_args()

    actual = censar()

    if args.censo:
        imprimir_censo(actual)
        return
    if args.update:
        sellar(actual, args)
        return

    # --check: no escribe NUNCA.
    sellado = cargar_baseline()
    if sellado['semantica'] != SEMANTICA:
        print("rc=3 DERIVA: la regla de medida ha cambiado respecto a la foto sellada.")
        print("   Receptores, ambito o DIRECCION de la comparacion ya no son los que se")
        print("   sellaron, asi que comparar las cifras no significa nada.")
        print("   Esto NO se arregla resellando: averigua POR QUE cambio la regla.")
        sys.exit(3)

    peor, mejor = comparar_o_roto(actual, sellado['sumideros'], 'sumideros')

    # El orden del veredicto es una decision: ante delta mixto gana el
    # EMPEORAMIENTO, y NO se imprime el comando de resellado. Si ganara el
    # mensaje de "mejora", el operador obedeceria y el empeoramiento quedaria
    # amnistiado dentro. Los dos casos dan rc distinto de cero en otros
    # instrumentos, asi que el defecto vive en el MENSAJE, que es lo que dirige
    # la mano del operador (CLAUDE.md 4.4).
    if peor:
        print("HALLAZGO (rc=1): los sumideros del dano han cambiado sin que la foto lo sepa.")
        for p in peor:
            print(f"   - {p}")
        print("\nUn sumidero NUEVO es una salida al mundo que nadie ha mirado; una boca")
        print("de aviso que desaparece es el silencio que esta fase existe para impedir.")
        print("Miralo, decide, y sella con su MOTIVO escrito en el mismo commit.")
        sys.exit(1)
    if mejor:
        print(f"Sumideros: {sum(actual.values())} en {len(actual)} claves. "
              "Han desaparecido salidas de SUBIDA (menos superficie de dano):")
        for m in mejor:
            print(f"   - {m}")
        print("Cuando el cambio sea deliberado, resella con --update.")
        return
    print(f"Sumideros sin cambios: {sum(actual.values())} en {len(actual)} claves.")


if __name__ == '__main__':
    main()
