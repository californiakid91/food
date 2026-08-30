#!/usr/bin/env python3
"""La puerta unica de escritura a la nube, y su aviso.

D-33: habia TRES escrituras al documento de Firestore y solo DOS pasaban por la
guarda de no-vaciado. Enumerar a mano esas tres habria repetido el defecto: una
lista blanca solo protege de lo que ya conoce (§5.15). Asi que aqui se DERIVA
del codigo el conjunto de escrituras y se exige que TODAS esten dentro de la
puerta unica; si aparece una cuarta, esto se pone rojo.

DOS REDES DISJUNTAS, a proposito. Dos revisores ciegos que coinciden no se
corroboran: comparten el punto ciego. Estas dos miden cosas distintas.

  Red A — por el RECEPTOR. Deriva que variables estan ligadas a una referencia
    de Firestore (asignadas desde `userDocRef()` o desde una cadena
    `db.collection(...)`). Sobre ellas, CUALQUIER metodo mutador
    (set/update/add/delete/merge) fuera de la puerta unica es un hallazgo.
    Caza un `ref.delete()`, que borra el documento entero y que la red B no ve.

  Red B — por el METODO. Toda llamada `.set(` del fichero tiene que estar
    dentro de la puerta unica, salvo que su receptor este ligado a `new Map(`
    o `new Set(` en el cuerpo de su propia funcion. Caza una referencia
    obtenida por un camino que la red A no modela.

Y una tercera comprobacion, del AVISO (D-31, cerrada por la CLASE): cero
llamadas literales a `setSyncUI` con 'ok'. El verde del indicador solo se
alcanza a traves de `estadoSync(...)`, que es una funcion pura y medible.

Los tres hallazgos tienen MENSAJES DISTINTOS: el defecto vive en el mensaje,
que es lo que dirige la mano (§4.4).

CEGUERAS DECLARADAS (antes de que alguien las descubra):
  - No ve escrituras por reflexion: `ref['s' + 'et'](payload)`.
  - No ve un `ref` PASADO COMO ARGUMENTO a otra funcion que escriba dentro:
    la red A solo modela asignaciones, no parametros.
  - No ve un alias creado por desestructuracion ni por `Object.assign`.
  - No ve escrituras hechas desde sw.js, worker.js ni desde la consola.
  - La atribucion usa el escaner compartido de funcsize.py con las `async
    function` incluidas, pero no ve funciones flecha. Una escritura metida
    dentro de una flecha de primer nivel se atribuye a '<nivel superior>', y
    como eso NO es la puerta unica, sale roja igual: la ceguera falla CERRADO.

Codigos de salida (nominales, cada uno con su mensaje):
  0  verde
  1  hallazgo real: una escritura fuera de la puerta, o un verde incondicional
  2  instrumento roto: no pudo medir. NO es lo mismo que "0 hallazgos".
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from funcsize import (
    EscanerRoto,
    enmascarar,
    extraer_js,
    localizar_funciones,
)

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / 'index.html'

PUERTA = 'subirALaNube'
MUTADORES = ('set', 'update', 'add', 'delete', 'merge')

RE_MUTADOR = re.compile(r'\.\s*(' + '|'.join(MUTADORES) + r')\s*\(')
RE_SET = re.compile(r'\.\s*set\s*\(')
# Variables ligadas a una referencia de Firestore.
RE_REF = re.compile(r'\b(?:const|let|var)\s+(\w+)\s*=\s*(?:await\s+)?'
                    r'(?:userDocRef\s*\(|db\s*\.\s*collection\s*\()')
# Receptores que son colecciones locales, no la nube.
RE_COLECCION = re.compile(r'\b(?:const|let|var)\s+(\w+)\s*=\s*new\s+(?:Map|Set)\s*\(')
# El verde del indicador, escrito a mano.
RE_VERDE = re.compile(r'setSyncUI\s*\(\s*[\'"]ok[\'"]\s*\)')

IDENT = re.compile(r'[A-Za-z0-9_$]')


def roto(msg):
    print(f"rc=2 INSTRUMENTO ROTO: {msg}", file=sys.stderr)
    sys.exit(2)


def receptor(codigo, punto):
    """('nombre', ident) | ('miembro', txt) | ('llamada', txt) para el `.` en `punto`.

    Falla CERRADO: si no puede decidir que hay antes del punto, lanza
    EscanerRoto. Un escaner que "no sabe" y calla certifica pase lo que pase.
    """
    k = punto - 1
    while k >= 0 and codigo[k] in ' \t\n\r':
        k -= 1
    if k < 0:
        raise EscanerRoto(f"no hay nada antes del metodo en el desplazamiento {punto}")
    if codigo[k] in ')]':
        return ('llamada', codigo[k])
    if IDENT.match(codigo[k]):
        fin = k + 1
        while k >= 0 and IDENT.match(codigo[k]):
            k -= 1
        nombre = codigo[k + 1:fin]
        j = k
        while j >= 0 and codigo[j] in ' \t\n\r':
            j -= 1
        if j >= 0 and codigo[j] == '.':
            return ('miembro', nombre)
        return ('nombre', nombre)
    raise EscanerRoto(
        f"no se que receptor tiene el metodo en el desplazamiento {punto}: "
        f"antes hay {codigo[k]!r}")


def ambito(funciones, pos, codigo):
    """(nombre_de_funcion, texto_de_su_cuerpo) para ese desplazamiento."""
    for nombre, ini, fin in funciones:
        if ini <= pos <= fin:
            return nombre, codigo[ini:fin + 1]
    return '<nivel superior>', codigo


def linea(js, pos):
    return js[:pos].count('\n') + 1


def main():
    try:
        js = extraer_js(INDEX)
        funciones = localizar_funciones(js, incluir_async=True)
    except EscanerRoto as e:
        roto(str(e))

    if not any(n == PUERTA for n, _, _ in funciones):
        roto(f"no existe la puerta unica `{PUERTA}` en index.html: "
             f"o la han renombrado, o este control ya no mide nada")

    codigo = enmascarar(js, cadenas=True)     # sin prosa: metodos de verdad
    sin_comentarios = enmascarar(js)          # con cadenas: para ver 'ok'

    # ── Red A — por el RECEPTOR ──────────────────────────────────────────────
    refs = {m.group(1) for m in RE_REF.finditer(codigo)}
    if not refs:
        roto("no he derivado NINGUNA referencia de Firestore: la red A no mide "
             "nada. O el codigo cambio de forma, o el patron dejo de casar.")

    hallazgos_a = []
    try:
        for m in RE_MUTADOR.finditer(codigo):
            tipo, nombre = receptor(codigo, m.start())
            if tipo != 'nombre' or nombre not in refs:
                continue
            fn, _ = ambito(funciones, m.start(), codigo)
            if fn != PUERTA:
                hallazgos_a.append(
                    f"linea {linea(js, m.start())}: `{nombre}.{m.group(1)}(` sobre una "
                    f"referencia de Firestore, dentro de `{fn}` y no de `{PUERTA}`")
    except EscanerRoto as e:
        roto(str(e))

    # ── Red B — por el METODO ────────────────────────────────────────────────
    hallazgos_b = []
    try:
        for m in RE_SET.finditer(codigo):
            tipo, nombre = receptor(codigo, m.start())
            fn, cuerpo = ambito(funciones, m.start(), codigo)
            if fn == PUERTA:
                continue
            if tipo == 'nombre' and nombre in {c.group(1) for c in RE_COLECCION.finditer(cuerpo)}:
                continue    # es un Map/Set local, no la nube
            hallazgos_b.append(
                f"linea {linea(js, m.start())}: `.set(` sobre {tipo} "
                f"`{nombre}` dentro de `{fn}`, fuera de `{PUERTA}`")
    except EscanerRoto as e:
        roto(str(e))

    # ── El AVISO — cero verdes escritos a mano ───────────────────────────────
    hallazgos_c = [f"linea {linea(js, m.start())}: {m.group(0)}"
                   for m in RE_VERDE.finditer(sin_comentarios)]

    if hallazgos_a or hallazgos_b or hallazgos_c:
        if hallazgos_a:
            print(f"rc=1 RED A — ESCRITURA A LA NUBE FUERA DE LA PUERTA ({len(hallazgos_a)}):")
            for h in hallazgos_a:
                print(f"   - {h}")
            print(f"   Toda mutacion del documento tiene que pasar por `{PUERTA}`, que es")
            print("   quien pregunta a `decidirSubida`. Esto es exactamente D-33.")
        if hallazgos_b:
            print(f"rc=1 RED B — LLAMADA `.set(` FUERA DE LA PUERTA ({len(hallazgos_b)}):")
            for h in hallazgos_b:
                print(f"   - {h}")
            print("   Si de verdad es una coleccion local, ligala a `new Map(`/`new Set(`")
            print("   en su propio ambito. No hay lista de nombres permitidos.")
        if hallazgos_c:
            print(f"rc=1 AVISO — EL INDICADOR SE PONE VERDE A MANO ({len(hallazgos_c)}):")
            for h in hallazgos_c:
                print(f"   - {h}")
            print("   El verde solo se alcanza por `estadoSync(...)`, que es puro y medible.")
            print("   Un verde escrito a mano es lo que tapaba D-33 mientras ocurria (D-31).")
        sys.exit(1)

    print(f"Verde: 1 escritura a la nube, dentro de `{PUERTA}`; "
          f"{len(refs)} referencia(s) de Firestore vigiladas; 0 verdes escritos a mano.")


if __name__ == '__main__':
    main()
