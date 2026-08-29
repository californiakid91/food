#!/usr/bin/env python3
"""Banco de sabotaje: demuestra que la puerta MUERDE.

Un control que nunca se ha visto rojo no se ha visto. Por cada control de
tools/verify.sh, este banco lo rompe a proposito, comprueba que sale rojo con
el codigo y el mensaje esperados, y REVIERTE.

Precauciones que se toman aqui porque ya han fallado en otros sitios:
  - CONTROL DE VACUIDAD: antes de nada, sin ningun sabotaje puesto, la puerta
    tiene que estar VERDE. Sin esto, una puerta siempre-roja pasaria todos los
    sabotajes y pareceria perfecta.
  - UNICIDAD DEL ANCLA: cada mutacion afirma que su texto anda aparece EXACTAMENTE
    una vez antes de tocar nada. Un patron que no casa produciria un falso
    "el control no muerde" cuando el defecto esta en el banco.
  - HASH DEL ARBOL antes y despues: si al terminar el arbol no es identico, el
    banco lo dice a gritos en vez de dejar el repo sucio.
  - Se exige el MENSAJE, no solo el codigo de salida: un traceback tambien da
    rc distinto de cero.

Uso:  python3 tools/sabotage.py        (rc=0 si todos los controles muerden)
"""
import hashlib
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / 'index.html'
FUNCSIZE = ROOT / 'tools' / 'funcsize.py'
BASELINE = ROOT / '.paul' / 'baseline-funcs.json'


def hash_arbol():
    """Huella de los ficheros que el banco puede tocar."""
    h = hashlib.sha256()
    for p in sorted([INDEX, FUNCSIZE, BASELINE]):
        h.update(p.read_bytes() if p.is_file() else b'<ausente>')
    return h.hexdigest()


def puerta():
    """Corre la puerta marcandola como interna, para que no reentre en el banco."""
    env = dict(os.environ, VERIFY_INNER='1')
    r = subprocess.run([str(ROOT / 'tools' / 'verify.sh')],
                       capture_output=True, text=True, check=False, cwd=ROOT, env=env)
    return r.returncode, r.stdout + r.stderr


def sustituir_unico(fichero, viejo, nuevo):
    """Muta afirmando primero que el ancla es unica. Devuelve el texto original."""
    t = fichero.read_text(encoding='utf-8')
    n = t.count(viejo)
    if n != 1:
        raise AssertionError(
            f"ancla no unica en {fichero.name}: {n} apariciones de {viejo!r}. "
            "El defecto esta en el BANCO, no en el control.")
    fichero.write_text(t.replace(viejo, nuevo), encoding='utf-8')
    return t


class Caso:
    def __init__(self, nombre, fichero, viejo, nuevo, rc, texto):
        self.nombre, self.fichero = nombre, fichero
        self.viejo, self.nuevo = viejo, nuevo
        self.rc_esperado, self.texto_esperado = rc, texto


CASOS = [
    Caso("sintaxis rota", INDEX,
         "function runSelfTests() {", "function runSelfTests() { (",
         1, "sintaxis de index.html"),
    Caso("invariante roto (parseNum deja de leer la coma)", INDEX,
         "const last = Math.max(s.lastIndexOf(','), s.lastIndexOf('.'));",
         "const last = s.lastIndexOf('.');",
         1, "autopruebas"),
    Caso("el monolito engorda", INDEX,
         "function runSelfTests() {",
         "function runSelfTests() {\n" + "  // relleno de sabotaje\n" * 80,
         1, "EL MONOLITO HA ENGORDADO"),
    # Controles positivos del plan 01-01: cada arreglo, revertido, debe matar
    # su propia prueba. Un test que pasa CON y SIN el arreglo no mide nada.
    Caso("el libro deja de cargarse si META falla", INDEX,
         "  ops = loadOpsAll();\n  try {\n    const raw = localStorage.getItem(META_KEY);",
         "  try {\n    const raw = localStorage.getItem(META_KEY);",
         1, "AC-1"),
    Caso("deja de rescatarse el libro ilegible", INDEX,
         "    opsIlegible = true;\n    rescatarOpsIlegible(raw);",
         "    opsIlegible = true;",
         1, "AC-3"),
    Caso("el guardado vuelve a mentir sobre si pudo", INDEX,
         "    console.error('No se pudo guardar el libro de operaciones:', e);\n    return false;",
         "    console.error('No se pudo guardar el libro de operaciones:', e);\n    return true;",
         1, "AC-2"),
    Caso("el fallo de guardado vuelve a anunciarse como exito", INDEX,
         "  showSaveIndicator(todoBien ? (saveMensaje || 'Guardado \u2713') : 'No se pudo guardar', todoBien);",
         "  showSaveIndicator('Guardado \u2713', true);",
         1, "AC-2"),
    Caso("los activos vuelven a cantar exito antes de tiempo", INDEX,
         "  const okRows = saveRows(false);   // el aviso lo decide esta función, al final",
         "  const okRows = saveRows(true);",
         1, "AC-2"),
    # Las dos suites escriben en el localStorage REAL del usuario (?selftest=1
    # tambien corre en su navegador), asi que cada una tiene su propio control
    # de que devuelve las cosas como estaban. El ancla lleva la linea siguiente
    # porque el bloque de restauracion es identico en las dos: sin ella el banco
    # casaria de mas y no sabria cual esta midiendo.
    Caso("pruebasGuardado deja de restaurar los datos del usuario", INDEX,
         "    localStorage.clear();\n    Object.keys(copiaSeguridad).forEach(k => localStorage.setItem(k, copiaSeguridad[k]));\n    ops = estadoPrevio.ops;",
         "    ops = estadoPrevio.ops;",
         1, "AC-4"),
    Caso("pruebasSincronizacion deja de restaurar los datos del usuario", INDEX,
         "    localStorage.clear();\n    Object.keys(copiaSeguridad).forEach(k => localStorage.setItem(k, copiaSeguridad[k]));\n    ops = previo.ops;",
         "    ops = previo.ops;",
         1, "AC-4"),
    # Una funcion enorme escondida tras `throw /}/;` — JavaScript valido que
    # despistaba al contador de llaves y le hacia medirla como si tuviera 2
    # lineas, en silencio y sin rc=2. El instrumento tiene que VERLA.
    Caso("funcion gigante escondida tras una regex con llave", INDEX,
         "function sembrarCentinelas() {",
         "function trampaDeRegex() {\n  throw /}/;\n" + "  // relleno\n" * 85 + "}\n\nfunction sembrarCentinelas() {",
         1, "EL MONOLITO HA ENGORDADO"),
    # Controles positivos del plan 01-02 (sincronizacion). Mismo criterio: cada
    # arreglo, revertido, tiene que matar su propia prueba.
    Caso("los identificadores vuelven a poder chocar", INDEX,
         "  const seq = (opIdSeq++).toString(36).padStart(6, '0');\n"
         "  return 'o' + Date.now().toString(36) + seq + Math.random().toString(36).slice(2, 5);",
         "  return 'o' + Date.now().toString(36) + Math.random().toString(36).slice(2, 5);",
         1, "AC-1"),
    Caso("el sync vuelve a deduplicar por huella y se come operaciones", INDEX,
         "saveOpsAll(dedupeOpsById(data.opsAll))",
         "saveOpsAll(dedupeOps(data.opsAll))",
         1, "AC-2"),
    Caso("se quita la guarda de no-vaciado al aplicar", INDEX,
         "    if (vaciariaElLibro(opsDelDocumento(data), ops)) {",
         "    if (false) {",
         1, "AC-4"),
    Caso("se quita la guarda de no-vaciado al subir", INDEX,
         "        if (vaciariaElLibro(payload.opsAll, cloudOps)) {",
         "        if (false) {",
         1, "AC-4"),
    # El fallo mas caro encontrado en la revision del 01-02: las autopruebas
    # sembraban centinelas SOBRE las claves reales, la foto de seguridad
    # retrataba a los centinelas y al final se borraban esas claves. Abrir
    # ?selftest=1 en el navegador borraba el libro de operaciones del usuario
    # imprimiendo "Autopruebas OK". El control vive en el arnes, no en la suite.
    Caso("las autopruebas se comen el libro real del usuario", INDEX,
         "    'centinela-libro': JSON.stringify([{ id: 'centinela'",
         "    'balance-ops': JSON.stringify([{ id: 'centinela'",
         1, "se comieron datos reales"),
    # Contar claves no basta: hay que comparar VALORES. Este sabotaje devuelve
    # el almacenamiento con TODAS las claves puestas pero con la basura dentro.
    # Con la comprobacion ciega al valor, salia verde.
    Caso("la restauracion devuelve las claves pero con la basura dentro", INDEX,
         "    Object.keys(copiaSeguridad).forEach(k => localStorage.setItem(k, copiaSeguridad[k]));\n"
         "    ops = previo.ops;",
         "    Object.keys(copiaSeguridad).forEach(k => localStorage.setItem(k, 'BASURA'));\n"
         "    ops = previo.ops;",
         1, "AC-4"),
    Caso("la guarda de subida vuelve a ser ciega al formato antiguo", INDEX,
         "  Object.values(data.opsData || {}).forEach(l => juntas.push(...(Array.isArray(l) ? l : [])));",
         "  Object.values({}).forEach(l => juntas.push(...(Array.isArray(l) ? l : [])));",
         1, "AC-4 un documento en formato antiguo"),
    Caso("el identificador puede cambiar de anchura", INDEX,
         "  const seq = (opIdSeq++).toString(36).padStart(6, '0');",
         "  const seq = (opIdSeq++).toString(36).padStart(2, '0');",
         1, "AC-1 el identificador no cambia de anchura"),
    Caso("deriva: se afloja la vara de medir", FUNCSIZE,
         "'umbral_lineas': 60,", "'umbral_lineas': 500,",
         3, "DERIVA"),
    Caso("no se puede medir: index.html vacio", INDEX,
         None, "",
         2, "INSTRUMENTO ROTO"),
]


def main():
    fallos = []
    h0 = hash_arbol()

    # CONTROL DE VACUIDAD. Sin el, una puerta siempre-roja aprobaria este banco.
    rc, salida = puerta()
    if rc != 0:
        print("CONTROL DE VACUIDAD FALLIDO: la puerta ya esta roja SIN sabotaje.")
        print("   Nada de lo que siga significaria nada.")
        print(salida)
        return 2
    print("  OK    control de vacuidad: sin sabotaje, la puerta esta verde")

    for c in CASOS:
        original = c.fichero.read_text(encoding='utf-8')
        try:
            if c.viejo is None:
                c.fichero.write_text(c.nuevo, encoding='utf-8')
            else:
                sustituir_unico(c.fichero, c.viejo, c.nuevo)
            rc, salida = puerta()
            ok_rc = rc == c.rc_esperado
            ok_txt = c.texto_esperado in salida
            if ok_rc and ok_txt:
                print(f"  OK    muerde: {c.nombre} (rc={rc})")
            else:
                detalle = []
                if not ok_rc:
                    detalle.append(f"esperaba rc={c.rc_esperado}, dio rc={rc}")
                if not ok_txt:
                    detalle.append(f"no aparece {c.texto_esperado!r} en la salida")
                print(f"  NO MUERDE: {c.nombre} — {'; '.join(detalle)}")
                fallos.append(c.nombre)
        except AssertionError as e:
            print(f"  BANCO ROTO: {c.nombre} — {e}")
            fallos.append(f"{c.nombre} (banco)")
        finally:
            c.fichero.write_text(original, encoding='utf-8')

    # El veredicto no puede confundir "tu codigo esta mal" con "no pude medir".
    # Sin esto, un hallazgo real sale como rc=2 y manda a mirar las herramientas
    # en vez del codigo. Se descubrio saboteando el hook, no razonandolo.
    original = INDEX.read_text(encoding='utf-8')
    try:
        sustituir_unico(INDEX,
                        "const last = Math.max(s.lastIndexOf(','), s.lastIndexOf('.'));",
                        "const last = s.lastIndexOf('.');")
        # Puerta COMPLETA (sin VERIFY_INNER): con el arbol roto omite el banco,
        # asi que no reentra.
        r = subprocess.run([str(ROOT / 'tools' / 'verify.sh')],
                           capture_output=True, text=True, check=False, cwd=ROOT)
        if r.returncode != 1 or 'OMITIDO banco de sabotaje' not in r.stdout:
            print(f"  NO MUERDE: un hallazgo real da rc={r.returncode} en vez de rc=1, "
                  "o el banco no se omitio")
            fallos.append("veredicto confunde hallazgo con instrumento roto")
        else:
            print("  OK    un hallazgo real da rc=1, no rc=2 (y el banco se omite)")
    finally:
        INDEX.write_text(original, encoding='utf-8')

    # --check NUNCA escribe: se comprueba con un hash, no con confianza.
    antes = hashlib.sha256(BASELINE.read_bytes()).hexdigest()
    subprocess.run([sys.executable, str(FUNCSIZE), '--check'],
                   capture_output=True, text=True, check=False, cwd=ROOT)
    if hashlib.sha256(BASELINE.read_bytes()).hexdigest() != antes:
        print("  NO MUERDE: --check ha ESCRITO en la foto sellada")
        fallos.append("--check escribe")
    else:
        print("  OK    --check no escribe en la foto sellada")

    # Aflojar tiene que costar decirlo en voz alta.
    original = INDEX.read_text(encoding='utf-8')
    try:
        sustituir_unico(INDEX, "function runSelfTests() {",
                        "function runSelfTests() {\n" + "  // relleno\n" * 80)
        r = subprocess.run([sys.executable, str(FUNCSIZE), '--update'],
                           capture_output=True, text=True, check=False, cwd=ROOT)
        if r.returncode == 0 or 'NO SE SELLA' not in r.stdout:
            print("  NO MUERDE: --update sello un empeoramiento sin amnistia explicita")
            fallos.append("--update sella empeoramiento")
        else:
            print("  OK    --update se niega a sellar un empeoramiento sin --amnesty")
    finally:
        INDEX.write_text(original, encoding='utf-8')

    h1 = hash_arbol()
    if h0 != h1:
        print(f"\n  ARBOL SUCIO: el banco no dejo las cosas como estaban ({h0[:12]} -> {h1[:12]})")
        fallos.append("arbol sucio")
    else:
        print(f"  OK    arbol identico antes y despues ({h0[:12]})")

    print()
    if fallos:
        print(f"CONTROLES QUE NO MUERDEN ({len(fallos)}): {', '.join(fallos)}")
        return 1
    print("Todos los controles de la puerta muerden.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
