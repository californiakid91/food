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
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import hookcheck  # tras ajustar sys.path arriba, como hace emptycatch con funcsize

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / 'index.html'
FUNCSIZE = ROOT / 'tools' / 'funcsize.py'
BASELINE = ROOT / '.paul' / 'baseline-funcs.json'
CLOUDWRITES = ROOT / 'tools' / 'cloudwrites.py'
EMPTYCATCH = ROOT / 'tools' / 'emptycatch.py'
CATCHES = ROOT / '.paul' / 'baseline-catches.json'
AVISOS = ROOT / 'tools' / 'avisos.py'
BASELINE_AVISOS = ROOT / '.paul' / 'baseline-avisos.json'
SUMIDEROS = ROOT / 'tools' / 'sumideros.py'
BASELINE_SUMIDEROS = ROOT / '.paul' / 'baseline-sumideros.json'
RUNSELFTESTS = ROOT / 'tools' / 'run_selftests.py'
VERIFY = ROOT / 'tools' / 'verify.sh'
SABOTAGE = ROOT / 'tools' / 'sabotage.py'
INSTALLHOOKS = ROOT / 'tools' / 'install-hooks.sh'
HOOKCHECK = ROOT / 'tools' / 'hookcheck.py'


def _dir_de_hooks():
    """Donde git guarda los enganches DE VERDAD.

    Suponer `.git/hooks` es la misma suposicion que el 01-05 quito de
    `install-hooks.sh` y de `hookcheck.py`: con `core.hooksPath` puesto, o en un
    `git worktree`, el enganche vive en otro sitio y esto vigilaba un fichero
    que nadie instala. Dos predicados sobre el mismo objeto tienen que ser el
    MISMO predicado (CLAUDE.md 5.16).
    """
    try:
        r = subprocess.run(['git', 'rev-parse', '--git-path', 'hooks'],
                           capture_output=True, text=True, check=False, cwd=ROOT)
        if r.returncode == 0 and r.stdout.strip():
            return (ROOT / r.stdout.strip()).resolve()
    except OSError:
        pass
    return ROOT / '.git' / 'hooks'


PREPUSH = _dir_de_hooks() / 'pre-push'

# Verde de la puerta corrida DESDE DENTRO del banco. Desde el ciclo 01-05 esa
# variante devuelve 4 y no 0: un 0 ahi era una puerta verde con el banco
# apagado, y bastaba tener VERIFY_INNER=1 exportado para que todos los push
# pasaran sin que nada demostrara que los controles muerden (D-40).
# Este es el UNICO consumidor que acepta el 4 como base verde.
VERDE_INTERIOR = 4

# Ficheros cuya huella se toma antes y despues. Hasta el 01-05 eran seis fijos
# y NO incluian ni la puerta, ni el banco, ni el enganche: el "arbol identico"
# de un sabotaje que los mutara no probaba nada sobre ellos.
TOCABLES = [INDEX, FUNCSIZE, BASELINE, CLOUDWRITES, EMPTYCATCH, CATCHES,
            VERIFY, SABOTAGE, INSTALLHOOKS, HOOKCHECK, PREPUSH,
            AVISOS, BASELINE_AVISOS, RUNSELFTESTS,
            SUMIDEROS, BASELINE_SUMIDEROS]


def hash_arbol():
    """Huella de los ficheros que el banco puede tocar."""
    h = hashlib.sha256()
    for p in sorted(TOCABLES):
        h.update(p.read_bytes() if p.is_file() else b'<ausente>')
    return h.hexdigest()


def puerta():
    """Corre la puerta marcandola como interna, para que no reentre en el banco."""
    env = dict(os.environ, VERIFY_INNER='1')
    r = subprocess.run([str(VERIFY)],
                       capture_output=True, text=True, check=False, cwd=ROOT, env=env)
    return r.returncode, r.stdout + r.stderr


def sustituir_unico_mismo_largo(fichero, viejo, nuevo):
    """Como `sustituir_unico`, pero AFIRMA que la mutacion no mueve los bytes.

    Existe para el unico caso en que se mutila un script que se esta EJECUTANDO:
    `verify.sh`, cuyo proceso bash padre lo lee por trozos y recuerda su
    desplazamiento. Cambiar su longitud a media corrida le haria leer basura.
    Aqui no basta con escribirlo en un comentario -- un comentario que promete
    un freno no cablea ninguno (CLAUDE.md 5.1) --, asi que se comprueba: si
    alguien edita este sabotaje y descuadra la longitud, el banco dice que el
    defecto esta en el BANCO en vez de romper la puerta por debajo.
    """
    if len(viejo) != len(nuevo):
        raise AssertionError(
            f"sabotaje sobre {fichero.name}, que se esta ejecutando: la sustitucion "
            f"cambia la longitud ({len(viejo)} -> {len(nuevo)} bytes) y desplazaria "
            "lo que el bash padre aun no ha leido. El defecto esta en el BANCO.")
    return sustituir_unico(fichero, viejo, nuevo)


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
    # Ancla REDISENADA en el 01-07: el mismo reparto --y el mismo comentario--
    # viven ahora tambien en `persistOps`, asi que la linea sola aparecia DOS
    # veces y el banco lo canto como "el defecto esta en el BANCO". Se ancla con
    # la firma de la funcion, que es lo que distingue una de otra.
    Caso("los activos vuelven a cantar exito antes de tiempo", INDEX,
         "function guardarTodo() {\n  const okRows = saveRows(false);",
         "function guardarTodo() {\n  const okRows = saveRows(true);",
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
    # Ancla REDISENADA en el 01-03: la llamada `saveOpsAll(dedupeOpsById(...))`
    # desaparecio al separar el cerrojo de la escritura. El criterio de deduplicacion
    # vive ahora en la primera linea de la rama, y sigue siendo lo que se sabotea.
    Caso("el sync vuelve a deduplicar por huella y se come operaciones", INDEX,
         "    const entrante = dedupeOpsById(data.opsAll);",
         "    const entrante = dedupeOps(data.opsAll);",
         1, "AC-2"),
    Caso("se quita la guarda de no-vaciado al aplicar", INDEX,
         "    if (vaciariaElLibro(opsDelDocumento(data), ops)) {",
         "    if (false) {",
         1, "AC-4"),
    Caso("se quita la guarda de no-vaciado al subir", INDEX,
         "  if (vaciariaElLibro(estado.opsLocales, nube.ops)) {",
         "  if (false) {",
         1, "esperaba vaciaria"),
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
    # Controles positivos del plan 01-03 (el cerrojo del libro ilegible). Cada
    # pieza del arreglo, revertida, tiene que matar su propia prueba. El caso 4
    # existe porque sin el ningun mutante tocaria el UNICO camino que LEVANTA el
    # cerrojo: todos caerian dentro de la rama que ya se mira.
    Caso("el cerrojo vuelve a levantarse antes de reparar", INDEX,
         "    const entrante = dedupeOpsById(data.opsAll);",
         "    const entrante = dedupeOpsById(data.opsAll);\n    opsIlegible = false;",
         1, "AC-1 el blob ilegible sigue en disco byte a byte"),
    Caso("una nube vacia vuelve a contar como reparacion", INDEX,
         "      if (!tieneOperaciones(entrante)) {",
         "      if (false) {",
         1, "AC-1 el blob ilegible sigue en disco byte a byte"),
    Caso("la reparacion levanta el cerrojo aunque la escritura falle", INDEX,
         "  const ok = escribirOpsAll(list);\n  if (ok) {",
         "  opsIlegible = false;\n  const ok = escribirOpsAll(list);\n  if (ok) {",
         1, "AC-3 el cerrojo sigue puesto tras la escritura fallida"),
    Caso("la reparacion buena NO levanta el cerrojo", INDEX,
         "    opsIlegible = false;\n    console.warn('Libro local ilegible REPARADO",
         "    console.warn('Libro local ilegible REPARADO",
         1, "AC-2 y baja el cerrojo ella misma, sin releer el disco"),
    # H3 de la revision: nada demostraba que la reparacion use la escritura CRUDA.
    # Si usara la puerta, con el cerrojo puesto no podria escribir jamas y el libro
    # quedaria bloqueado para siempre. Es la pieza (a) del arreglo.
    Caso("la reparacion vuelve a pasar por la puerta y no puede escribir", INDEX,
         "  const ok = escribirOpsAll(list);",
         "  const ok = saveOpsAll(list);",
         1, "AC-2 la reparaci\u00f3n devuelve true cuando la escritura entra"),
    # H2 de la revision: los checks de AC-5 (formato antiguo) nunca se habian
    # visto rojos. Un test que pasa CON y SIN el arreglo no mide nada.
    Caso("el formato antiguo vuelve a reparar por la puerta", INDEX,
         "      const ok = opsIlegible ? repararLibroIlegible(fusionadas) : saveOpsAll(fusionadas);",
         "      const ok = saveOpsAll(fusionadas);",
         1, "AC-5 el formato antiguo tambi\u00e9n escribe la reparaci\u00f3n"),
    Caso("se invierte la PRECEDENCIA de las dos guardas del cruce", INDEX,
         "    if (vaciariaElLibro(opsDelDocumento(data), ops)) {\n      console.warn('[SYNC] libro recibido vacío: se conservan las', ops.length,\n                   'operaciones locales');\n    } else if (opsIlegible) {\n      // El CRUCE: libro local ilegible + lo que llega. Una nube sin operaciones\n      // no es una reparación, así que el cerrojo se queda puesto.\n      if (!tieneOperaciones(entrante)) {\n        console.error('Libro local ilegible y no llega nada con que repararlo: el cerrojo sigue puesto.');\n      } else if (!repararLibroIlegible(entrante)) {\n        console.error('No se pudo reparar el libro ilegible: el cerrojo sigue puesto.');\n      }\n",
         "    if (opsIlegible) {\n      // El CRUCE: libro local ilegible + lo que llega. Una nube sin operaciones\n      // no es una reparación, así que el cerrojo se queda puesto.\n      if (!tieneOperaciones(entrante)) {\n        console.error('Libro local ilegible y no llega nada con que repararlo: el cerrojo sigue puesto.');\n      } else if (!repararLibroIlegible(entrante)) {\n        console.error('No se pudo reparar el libro ilegible: el cerrojo sigue puesto.');\n      }\n    } else if (vaciariaElLibro(opsDelDocumento(data), ops)) {\n      console.warn('[SYNC] libro recibido vacío: se conservan las', ops.length,\n                   'operaciones locales');\n",
         1, "AC-1 en el cruce gana el aviso de no-vaciado"),
    Caso("la reparacion buena deja de dejar constancia", INDEX,
         "    console.warn('Libro local ilegible REPARADO con', list.length, 'operaciones de la nube.');\n",
         "",
         1, "AC-2 la reparaci\u00f3n deja constancia de que ocurri\u00f3"),
    Caso("saveOpsAll deja de consultar el cerrojo", INDEX,
         "  if (opsIlegible) {\n"
         "    console.error('No se guarda el libro: el que hay en disco es ilegible y est\u00e1 rescatado.');\n"
         "    return false;\n"
         "  }\n"
         "  return escribirOpsAll(list);",
         "  return escribirOpsAll(list);",
         1, "AC-3 no se escribe encima del ilegible"),
    # ── Controles positivos del plan 01-04 (la puerta unica de la nube). ────
    # 1. Una CUARTA escritura fuera de la puerta. Es la clase que cierra D-33:
    #    no hay lista de sitios permitidos, hay una puerta y todo lo demas es rojo.
    # Ancla REDISENADA en el 01-07: vivia dentro del `pullFromFirestore` viejo,
    # que este ciclo reescribio entero para hacerlo inyectable. Se re-ancla en la
    # lectura de la nube del camino de bajada, que sigue siendo el sitio donde
    # una escritura colada seria mas dificil de ver.
    Caso("aparece una cuarta escritura a la nube fuera de la puerta", INDEX,
         "    const doc = await d.ref.get();",
         "    const colada = userDocRef();\n"
         "    if (colada) await colada.set({ colado: 1 });\n"
         "    const doc = await d.ref.get();",
         1, "ESCRITURA A LA NUBE FUERA DE LA PUERTA"),
    # 1b. La forma que trajo la INYECCION de dependencias: la referencia viaja
    #     como propiedad (`d.ref`), no como nombre suelto. Con el `.set(` la
    #     cazaba la red B de rebote; con `.update(` no la veia NADIE, y esa es
    #     exactamente la forma que este ciclo introdujo en el codigo. La red A se
    #     amplio a receptores compuestos por culpa de este sabotaje.
    #     La llamada va tras un `if (false)`: lo que se mide es que el analisis
    #     ESTATICO la vea. Ejecutarla reventaria las pruebas con un rc=2 de
    #     instrumento roto que TAPARIA el hallazgo que este caso persigue.
    Caso("escritura a la nube por RECEPTOR COMPUESTO (d.ref.update)", INDEX,
         "    const doc = await d.ref.get();",
         "    if (false) await d.ref.update({ colado: 1 });\n    const doc = await d.ref.get();",
         1, "ESCRITURA A LA NUBE FUERA DE LA PUERTA"),
    # 2. CONTROL POSITIVO DE D-33: el manejador de inicio de sesion vuelve a
    #    escribir por su cuenta, como hacia antes de este ciclo. Si esto no se
    #    pusiera rojo, el arreglo no estaria medido por nada.
    # Ancla REDISENADA en el 01-07: la linea del arranque paso de un booleano a
    # un VEREDICTO. El sabotaje es el mismo: colar una escritura propia.
    Caso("el manejador de inicio de sesion vuelve a escribir por su cuenta", INDEX,
         "    const lectura = await d.leerNube();",
         "    const refColada = userDocRef();\n"
         "    if (refColada) await refColada.set(buildSyncPayload().payload);\n"
         "    const lectura = await d.leerNube();",
         1, "ESCRITURA A LA NUBE FUERA DE LA PUERTA"),
    # 4. El juez deja de mirar si el paquete esta incompleto (D-34, lado juez).
    Caso("el juez deja de mirar si el paquete esta incompleto", INDEX,
         "  if (incompleto.length) {",
         "  if (false) {",
         1, "esperaba incompleto"),
    # 5. `buildSyncPayload` recupera un catch vacio (D-34, lado censo).
    Caso("buildSyncPayload recupera un catch vacio", INDEX,
         "      if (raw) portfolioData[p.id] = JSON.parse(raw);\n    } catch (e) { incompleto.push(clave); }",
         "      if (raw) portfolioData[p.id] = JSON.parse(raw);\n    } catch (e) {}",
         1, "CATCH VACIO EN EL CAMINO DE SUBIDA"),
    # 6. El mapa del indicador deja de ser cerrado y lo desconocido sale verde.
    Caso("un resultado desconocido vuelve a pintar verde", INDEX,
         "  if (resultado === 'auth')      return 'auth';\n  return 'error';",
         "  if (resultado === 'auth')      return 'auth';\n  return 'ok';",
         1, "AC-3 un resultado desconocido da ROJO"),
    # 7. El `catch` del manejador vuelve a declararse verde, que es como D-31
    #    tapaba a D-33 mientras ocurria. Sin la extraccion de la tarea 1(d) no
    #    habia oraculo posible y declararlo mordiente habria sido 5.1 con
    #    uniforme de test.
    Caso("el fallo del inicio de sesion vuelve a declararse verde", INDEX,
         "    console.error('alIniciarSesion:', e);\n    resultado = 'error';",
         "    console.error('alIniciarSesion:', e);\n    resultado = 'ok';",
         1, "AC-3 una lectura de nube que LANZA no acaba en verde"),
    # 8. EL ESLABON PRODUCTOR de D-34. El catch NO queda vacio (asi el censo no
    #    lo ve): simplemente deja de NOMBRAR la clave. Sin esta fila, los casos
    #    4 y 5 pasan aunque la marca no se ponga nunca.
    Caso("el productor deja de nombrar la clave que no pudo leer", INDEX,
         "      if (raw) historyData[p.id] = JSON.parse(raw);\n    } catch (e) { incompleto.push(clave); }",
         "      if (raw) historyData[p.id] = JSON.parse(raw);\n    } catch (e) { void clave; }",
         1, "AC-2 el paquete nombra la clave de HIST"),
    # 9. El manejador deja de pasar por `estadoSync`. Cubrir el mecanismo no
    #    cubre su CABLEADO: sin esta fila, el caso 6 mide la funcion pura y
    #    nadie mide que alguien la llame.
    Caso("el manejador deja de pasar por estadoSync", INDEX,
         "  const aviso = estadoSync(resultado);",
         "  const aviso = resultado;",
         1, "AC-3 un aviso desconocido pasa por estadoSync"),
    # ── Hallazgos de la revision adversaria del propio ciclo 01-04. Cada uno
    #    es un mutante que SOBREVIVIO a la puerta entera. Un sabotaje manual de
    #    ayer es una anecdota fechada; esto es lo que lo demuestra manana.
    # 10. La guarda de activos sustituida por un PROXY sobre el nombre del
    #     estado de la nube. Sobrevivia porque el fixture ataba `activos` al
    #     nombre: ahora hay filas mixtas que lo matan.
    Caso("la guarda de activos se sustituye por un proxy del estado de la nube", INDEX,
         "  if (!estado.hayActivosLocales && (nube.activos || 0) > 0) {",
         "  if (!estado.hayActivosLocales && nube.estado === 'con-datos') {",
         1, "esperaba ok, obtuve activos"),
    # 11-13. LA TUBERIA entre el productor y el juez. El productor tenia su
    #     control y el juez el suyo, y cortar el cable de en medio sobrevivia.
    Caso("se corta el cable que lleva la marca de paquete incompleto", INDEX,
         "    incompleto: construido.incompleto\n  });",
         "    incompleto: []\n  });",
         1, "AC-2 con el paquete incompleto NO escribe"),
    Caso("se corta el cable que lleva el cerrojo del libro", INDEX,
         "    libroIlegible: d.cerrojo(),",
         "    libroIlegible: false,",
         1, "AC-1 con el cerrojo puesto NO escribe"),
    Caso("se corta el cable que lleva si hay activos locales", INDEX,
         "    hayActivosLocales: d.activos(),",
         "    hayActivosLocales: true,",
         1, "AC-1 sin activos locales y con la nube llena NO escribe"),
    # 14. El manejador deja de PINTAR el indicador. El valor de retorno seguia
    #     siendo correcto, asi que sin el espia esto sobrevivia (5.6).
    Caso("el manejador deja de pintar el indicador", INDEX,
         "  const aviso = estadoSync(resultado);\n  setSyncUI(aviso, motivoFinal);",
         "  const aviso = estadoSync(resultado);",
         1, "AC-3 y además PINTA el indicador"),
    # 15. EL CABLEADO ASINCRONO. Sin el `await`, la suite del manejador deja de
    #     ejercer y la puerta sale VERDE Y SORDA. Medido: con el await quitado,
    #     el sabotaje 9 dejaba de morder. Cubrir el mecanismo no cubre su cable.
    # Ancla REDISENADA en el 01-07. Quitar el `await` de `ejercida` ya no produce
    # este mensaje: con las suites nuevas, las promesas sueltas se pisan el
    # estado y el proceso muere antes de imprimirlo. Se separa en DOS casos, que
    # miden dos cosas distintas:
    #   (a) el guardian `ejercida` en persona: una suite que no ejerce nada;
    #   (b) la red nueva contra promesas sin manejar, que antes daba rc=1 MUDO.
    Caso("una suite asincrona no llega a ejercer ni un control", INDEX,
         "    await ejercida('pruebasTuberiaDeSubida', () => pruebasTuberiaDeSubida(contado));",
         "    await ejercida('pruebasTuberiaDeSubida', () => { pruebasTuberiaDeSubida(contado); });",
         1, "pruebasTuberiaDeSubida no ejerci\u00f3 ni un control"),
    Caso("se pierde el await que cablea las suites asincronas", INDEX,
         "    const antes = ejercidos;\n    await fn();",
         "    const antes = ejercidos;\n    fn();",
         1, "no ejerci\u00f3 ni un control"),
    # La red nueva contra promesas SIN MANEJAR. Antes una promesa suelta mataba
    # el proceso con rc=1 y sin una palabra: un rojo sin nombre.
    Caso("una promesa suelta mata el proceso sin decir por que", INDEX,
         "function pruebasIndicador(check) {",
         "function pruebasIndicador(check) {\n"
         "  Promise.reject(new Error('promesa suelta de sabotaje'));",
         2, "una promesa quedo sin manejar"),
    # ── Controles del ciclo 01-05: la vara de medir. ────────────────────────
    # N1/N2. Una foto sellada MALFORMADA tiene que decir "no pude medir" con su
    #     nombre, no reventar con un traceback y rc=1 disfrazado de hallazgo del
    #     codigo. El ancla deja el JSON valido a proposito: se quiere una foto
    #     con la CLAVE de tipo equivocado, no un fichero que no parsea (eso ya
    #     lo cazaba el `except` de lectura).
    Caso("la foto de funcsize tiene 'excede' del tipo equivocado", BASELINE,
         '"excede": {', '"excede": null,\n  "_sabotaje": {',
         2, "la clave 'excede' es NoneType"),
    Caso("la foto de emptycatch tiene 'motivos' del tipo equivocado", CATCHES,
         '"motivos": {', '"motivos": null,\n  "_sabotaje": {',
         2, "la clave 'motivos' es NoneType"),
    Caso("deriva: se afloja la vara de medir", FUNCSIZE,
         "'umbral_lineas': 60,", "'umbral_lineas': 500,",
         3, "DERIVA"),
    # ── Controles del ciclo 01-06: la capa de AVISO (D-38). ────────────────
    # Hasta este ciclo NINGUNO de estos mutantes moria: la puerta entera salia
    # rc=0 con un fallo de guardado pintado en VERDE.
    #
    # A. Los dos PINTORES, ejecutados de verdad sobre un DOM observable.
    Caso("el pintor del guardado usa el mismo color para el fallo", INDEX,
         "el.style.color = ok ? 'var(--green)' : 'var(--red)';",
         "el.style.color = 'var(--green)';",
         1, "AC-1 los colores de fallo y de \u00e9xito son DISTINTOS"),
    Caso("el aviso se pinta INVISIBLE", INDEX,
         "  el.style.opacity = '1';", "  el.style.opacity = '0';",
         1, "AC-1 el aviso de fallo queda VISIBLE"),
    Caso("el fallo dura lo mismo que el exito", INDEX,
         "ok ? 1800 : 5000);", "1800);",
         1, "AC-2 las dos duraciones difieren"),
    # El CRUCE (5.5): sin cancelar el anterior, el apagado del "Guardado OK"
    # borraria a los 1,8 s el aviso de error que acaba de sustituirlo.
    Caso("el pintor deja de cancelar el temporizador anterior", INDEX,
         "  clearTimeout(indicadorTimer);\n  indicadorTimer =", "  indicadorTimer =",
         1, "AC-2 la segunda pintura cancel\u00f3 el temporizador ANTERIOR"),
    # El MUTANTE VECINO que destapo la revision adversaria: cancelar OTRA
    # variable satisface "cancelo algo". Por eso el aserto exige el id EXACTO.
    Caso("el pintor cancela OTRO temporizador, no el suyo", INDEX,
         "  clearTimeout(indicadorTimer);\n  indicadorTimer =",
         "  clearTimeout(saveTimer);\n  indicadorTimer =",
         1, "AC-2 la segunda pintura cancel\u00f3 el temporizador ANTERIOR"),
    Caso("la rama de ERROR del indicador de sync se pinta en verde", INDEX,
         "    dot.style.background = '#e74c3c';\n    dot.title = 'No se pudo sincronizar';",
         "    dot.style.background = '#27ae60';\n    dot.title = 'Sincronizado';",
         1, "AC-3 exactamente UNO pinta el verde de sincronizado"),
    # B. La familia que el borrador del plan dejaba viva (R-1): el AVISO del
    #    juez. Reproducido antes del ciclo: salia rc=0 y "Autopruebas OK".
    Caso("un rechazo por vaciado se etiqueta como TODO BIEN", INDEX,
         "    return { subir: false, aviso: 'pendiente', clave: 'vaciaria',",
         "    return { subir: false, aviso: 'ok', clave: 'vaciaria',",
         1, "AC-4 matriz"),
    # C. La red por CANAL y la red por RECEPTOR de tools/avisos.py.
    Caso("un aviso de consola se degrada a informativo", INDEX,
         "  else console.error('No se sincroniza: el guardado local fall\u00f3.');",
         "  else console.warn('No se sincroniza: el guardado local fall\u00f3.');",
         1, "la capa de aviso ha cambiado sin que la foto lo sepa"),
    Caso("aparece un aviso NUEVO sin sellar", INDEX,
         "function schedSave(mensajeExito) {",
         "function schedSave(mensajeExito) {\n  console.warn('aviso nuevo sin sellar');",
         1, "aviso NUEVO o CAMBIADO"),
    Caso("alguien pinta el aviso desde FUERA de los pintores", INDEX,
         "function schedSave(mensajeExito) {",
         "function schedSave(mensajeExito) {\n  const x = document.getElementById"
         "('save-indicator'); if (x) x.style.color = 'var(--green)';",
         1, "fuera de los pintores"),
    Caso("deriva: cambia el ambito del censo de avisos", AVISOS,
         "'cortes': ['runSelfTests'],", "'cortes': [],",
         3, "DERIVA"),
    Caso("la foto de avisos tiene 'motivos' del tipo equivocado", BASELINE_AVISOS,
         '"motivos": {', '"motivos": null,\n  "_sabotaje": {',
         2, "la clave 'motivos' es NoneType"),
    # D. Mutantes de ARNES. Estos NO miden producto: miden el instrumento con el
    #    que se mide el producto, y son el control positivo de los asertos del
    #    AC-0 y del AC-6, que no tienen trozo de producto que revertir.
    Caso("ARNES: la ventana de pintura pierde su finally", INDEX,
         "  try { return fn(v); } finally { v.cerrar(); }",
         "  const r = fn(v); v.cerrar(); return r;",
         1, "AC-0 y aun as\u00ed restaur\u00f3 getElementById"),
    Caso("ARNES: el reloj falso deja de dar identificadores unicos", INDEX,
         "sig++; v.programaciones.push({ id: sig, fn: fn, ms: ms }); return sig;",
         "v.programaciones.push({ id: sig, fn: fn, ms: ms }); return sig;",
         1, "AC-2 con identificadores distintos"),
    # Ancla ESTABLE a proposito: no la expresion regular (que ya cambio una vez
    # y dejo tres mutadores mudos), sino la linea del fallo cerrado.
    Caso("ARNES: el derivador de identificadores no encuentra ninguno", RUNSELFTESTS,
         "    if not ids:\n", "    ids = []\n    if not ids:\n",
         2, "no derive ningun id del marcado"),
    # R-3: vigilar solo el conjunto VACIO no basta. El pintor hace
    # `if (!el) return`, asi que un conjunto INCOMPLETO de origen lo dejaria
    # irse de vacio y en verde (5.15).
    Caso("ARNES: al derivador le falta JUSTO el identificador del aviso", RUNSELFTESTS,
         "    if not ids:\n",
         "    ids = [i for i in ids if i != 'save-indicator']\n    if not ids:\n",
         2, "no tiene identificadores que los pintores usan de verdad: save-indicator"),
    # ── Lo que destaparon los TRES brazos adversarios del 01-06. ───────────
    # Cada uno de estos salia rc=0 y "Autopruebas OK" con el ciclo ya escrito,
    # re-verificado a mano sobre copia aislada antes de aceptarlo.
    #
    # El peor: los colores INTERCAMBIADOS. El aserto pedia que fueran DISTINTOS
    # y nunca CUALES, asi que pintar el fallo en VERDE lo satisfacia -- que es
    # literalmente el dano que da nombre a D-38. Mi oraculo heredo mi punto
    # ciego (5.8), en el ciclo que existe para cerrar ese agujero.
    Caso("los colores del pintor del guardado, INTERCAMBIADOS", INDEX,
         "el.style.color = ok ? 'var(--green)' : 'var(--red)';",
         "el.style.color = ok ? 'var(--red)' : 'var(--green)';",
         1, "AC-1 el fallo se pinta con el color de PELIGRO"),
    Caso("el ERROR de sincronizacion pintado NARANJA en vez de rojo", INDEX,
         "    dot.style.background = '#e74c3c';\n    dot.title = 'No se pudo sincronizar';",
         "    dot.style.background = '#e67e22';\n    dot.title = 'No se pudo sincronizar';",
         1, "AC-3 el estado error pinta SU color"),
    Caso("el aviso dura 2 milisegundos: invisible para el operador", INDEX,
         "ok ? 1800 : 5000);", "ok ? 1 : 2);",
         1, "AC-2 el aviso de \u00e9xito dura lo bastante para leerse"),
    # 5.1 con uniforme: el comentario lo llamaba "MECANISMO explicito" y el
    # aserto pasaba con el mecanismo BORRADO, porque `cedido` ya era false.
    Caso("ARNES: se borra el mecanismo que detecta la cesion de control", INDEX,
         "  Promise.resolve().then(() => { v.cedido = true; });\n", "",
         1, "AC-0 y el detector REACCIONA cuando s\u00ed se cede el control"),
    # El ambito del censo escapaba por las dependencias INYECTADAS y por el
    # codigo suelto del arranque: nueve avisos reales del camino de la fase
    # quedaban fuera y un aviso sembrado ahi salia verde.
    Caso("aviso NUEVO sembrado en el guardado por sincronizacion", INDEX,
         "  } else if (!saveOpsAll(entrante)) {",
         "  } else if (console.warn('aviso sembrado en sync'), !saveOpsAll(entrante)) {",
         1, "aviso NUEVO o CAMBIADO"),
    # Degradar a un canal NO censado (`console.log`) hace DESAPARECER el aviso.
    # Antes salia rotulado como mejora y con el comando de resellado debajo:
    # el instrumento dirigia la mano del operador a amnistiar el silencio.
    Caso("aviso del ARRANQUE degradado a un canal no censado", INDEX,
         "      console.error('Operaciones antiguas ilegibles en la cartera '",
         "      console.log('Operaciones antiguas ilegibles en la cartera '",
         1, "han DESAPARECIDO avisos que la foto sellaba"),
    # ── Controles del ciclo 01-07: la BAJADA de la nube y los SUMIDEROS. ───
    # A. Cada arreglo, revertido POR SEPARADO, tiene que matar su propia prueba.
    #    Los ocho se re-verificaron a mano sobre una COPIA aislada antes de
    #    cablearlos aqui (CLAUDE.md 3.4: el brazo trabaja sobre copia).
    #
    # D-45 en persona: el desempate del arranque miraba SOLO los activos, asi
    # que un dispositivo con libro y sin activos aceptaba cualquier documento
    # por viejo que fuera, y la pantalla quedaba en VERDE.
    Caso("D-45: el desempate vuelve a mirar solo los activos", INDEX,
         "  const hayQueProteger = tieneOperaciones(local.ops) || !!local.hayActivosLocales;",
         "  const hayQueProteger = !!local.hayActivosLocales;",
         1, "AC-1 con LIBRO local y documento más viejo, NO se aplica"),
    # La fila SIMETRICA. Sin ella, cerrar D-45 por el lado del libro habria
    # abierto el mismo agujero por el lado de los activos (5.16).
    Caso("el desempate vuelve a mirar solo el libro", INDEX,
         "  const hayQueProteger = tieneOperaciones(local.ops) || !!local.hayActivosLocales;",
         "  const hayQueProteger = tieneOperaciones(local.ops);",
         1, "AC-1 con ACTIVOS locales y documento más viejo, tampoco se aplica"),
    # El hallazgo 2 de la revision adversaria del plan: sin conservar la marca
    # de tiempo al aplicar, `localSaved` volvia a 0 y TODO documento parecia mas
    # nuevo. La rama que cierra D-45 no habria disparado nunca en la app real: el
    # control habria pasado con el dano vivo (5.10).
    Caso("el reloj del sync vuelve a ponerse a cero al aplicar", INDEX,
         ",\n                                                  savedAt: Number(data.savedAt) || 0 }));",
         " }));",
         1, "AC-3 la marca de tiempo del documento SOBREVIVE al aplicar"),
    # El hallazgo 1: la bajada devolvia el mismo valor tanto si aplicaba como si
    # rechazaba, y el arranque lo traducia a VERDE. Cerrar solo la bajada habria
    # dejado la pantalla mintiendo en el escenario exacto de la ficha (5.5).
    Caso("el arranque vuelve a repintar VERDE encima del rechazo", INDEX,
         "      ? lectura\n      : await d.subir('inicio de sesión');",
         "      ? { aviso: 'ok', motivo: 'ok' }\n      : await d.subir('inicio de sesión');",
         1, "AC-4 un rechazo de la bajada NO acaba en verde"),
    # El SEGUNDO camino de bajada. Cerrar solo el del arranque habria sido el
    # caso disfrazado de clase: la escucha en vivo tenia su desempate aparte.
    Caso("la escucha en vivo deja de consultar al juez", INDEX,
         "    if (!decision.aplicar) {",
         "    if (false) {",
         1, "AC-2 la escucha EN VIVO tampoco aplica una nube más vieja"),
    # D-27. Ancla con la linea de la firma: `const okOps  = saveOpsAll(ops);`
    # aparece TAMBIEN en `guardarTodo`, y sin la firma el banco casaria de mas
    # y no sabria cual esta midiendo.
    Caso("D-27: el borrado de operacion vuelve a tirar el resultado del libro", INDEX,
         "function persistOps() {\n  const okOps  = saveOpsAll(ops);",
         "function persistOps() {\n  saveOpsAll(ops);\n  const okOps  = true;",
         1, "AC-7 un libro que no se guarda NO se anuncia en verde"),
    Caso("D-29: el interruptor de objetivos vuelve a subir siempre", INDEX,
         "  if (saveMeta()) {",
         "  if (saveMeta() || true) {",
         1, "AC-7 el interruptor NO sube si la lista de carteras no se guardó"),
    # D-46: el CRUCE que no medía nadie. Antes de este ciclo, quitar `okMeta`
    # dejaba la puerta ENTERA en rc=0 y, con la cuota llena, "Guardado OK" en
    # verde Y subida a la nube.
    Caso("D-46: el veredicto del guardado deja de mirar la lista de carteras", INDEX,
         "  const todoBien = okRows && okOps && okMeta;",
         "  const todoBien = okRows && okOps;",
         1, "AC-6 con SÓLO la lista de carteras rota, el guardado dice que no"),
    # B. El instrumento NUEVO, tools/sumideros.py. Un control que nunca se ha
    #    visto rojo no se ha visto.
    Caso("aparece un sumidero de SUBIDA nuevo sin sellar", INDEX,
         "function isMobile() {",
         "function isMobile() {\n  schedulePush();",
         1, "sumidero NUEVO, sin cobertura sellada"),
    # La direccion CONTRARIA, que es la mitad que este instrumento no hereda de
    # funcsize: una boca de aviso que se CIERRA es el silencio de la fase.
    Caso("desaparece una boca de aviso del guardado", INDEX,
         "  showSaveIndicator(todoBien ? 'Guardado ✓' : 'No se pudo guardar', todoBien);\n"
         "  if (!todoBien) console.error('El guardado de las operaciones falló: no se anuncia éxito.');\n",
         "",
         1, "ha DESAPARECIDO una boca de aviso"),
    Caso("la foto de sumideros tiene 'motivos' del tipo equivocado", BASELINE_SUMIDEROS,
         '"motivos": {', '"motivos": null,\n  "_sabotaje": {',
         2, "sumideros: la foto sellada"),
    Caso("la foto de sumideros no parsea", BASELINE_SUMIDEROS,
         None, "{esto no es json",
         2, "la foto sellada no se puede leer"),
    # Un receptor sellado que ya no existe es un sumidero que dejo de medirse.
    # Callarlo seria vigilar una ficcion.
    Caso("un sumidero sellado ya no existe en el codigo", SUMIDEROS,
         "        'schedulePush': 'subir',",
         "        'schedulePush': 'subir',\n        'noExisteJamas': 'subir',",
         2, "sumideros sellados que ya no existen"),
    Caso("deriva: se afloja la direccion de la comparacion de sumideros", SUMIDEROS,
         "'direccion': {'subir': 'dominacion', 'anunciar': 'ambas',",
         "'direccion': {'subir': 'dominacion', 'anunciar': 'dominacion',",
         3, "DERIVA (rc=3): sumideros del dano"),
    # ── Lo que destaparon los CINCO brazos adversarios del 01-07. ─────────
    # Cada uno de estos salia rc=0 con el ciclo ya escrito y la puerta VERDE, y
    # se re-verifico a mano sobre copia aislada antes de aceptarlo.
    #
    # EL PEOR: hacer inyectable una funcion crea POR CONSTRUCCION un cableado
    # por defecto que corre en el navegador y que ninguna prueba toca, porque
    # todas inyectan el suyo. Con este mutante D-45 volvia ENTERA a produccion.
    Caso("el cableado por defecto de la bajada deja de ver el libro", INDEX,
         "           aplicar: applySyncPayload, ops: () => ops,",
         "           aplicar: applySyncPayload, ops: () => [],",
         1, "AC-2 el cableado de la bajada lee EL libro de verdad"),
    Caso("el cableado por defecto deja de leer la marca de tiempo", INDEX,
         "  return { ref: userDocRef(), leerMeta: () => localStorage.getItem(META_KEY),",
         "  return { ref: userDocRef(), leerMeta: () => null,",
         1, "AC-2 y lee LA clave de META de verdad"),
    Caso("el cableado por defecto deja de pintar", INDEX,
         "           activos: hasRealLocalData, pintar: setSyncUI };",
         "           activos: hasRealLocalData, pintar: () => {} };",
         1, "AC-2 y pinta con setSyncUI"),
    Caso("el cableado del arranque deja de subir por la puerta unica", INDEX,
         "  return { leerNube: pullFromFirestore, subir: subirALaNube,",
         "  return { leerNube: pullFromFirestore, subir: async () => ({ aviso: 'ok' }),",
         1, "AC-4 y sube por la puerta única"),
    # El estado de MIGRACION: el dia del despliegue TODOS los dispositivos ya
    # sincronizados tienen META sin marca de tiempo (D-30). Sin esta rama, el
    # arreglo de D-45 no protegia a nadie en su primer arranque: control en
    # verde y dano vivo (5.10).
    Caso("con el reloj local desconocido se vuelve a aplicar cualquier cosa", INDEX,
         "  if (!localSaved || !remoto) {",
         "  if (false) {",
         1, "AC-2 sin marca de tiempo local NO se aplica nada"),
    # El empate: ahora que lo local adopta la marca del documento aplicado, el
    # empate es el estado NORMAL tras sincronizar. Con `>=` el primer snapshot
    # de la escucha reaplicaba el documento y se comia la edicion sin guardar.
    Caso("el desempate vuelve a aceptar el empate", INDEX,
         "  if (remoto > localSaved) {",
         "  if (remoto >= localSaved) {",
         1, "AC-1 un empate NO se aplica"),
    # El campo del veredicto que nadie afirmaba. Con el, el arranque trata un
    # rechazo como «no hay nada arriba» y SUBE encima de la nube.
    Caso("la bajada miente sobre si llego a leer la nube", INDEX,
         "  return { sincronizado: true, aplicado: aplicado, aviso: decision.aviso,",
         "  return { sincronizado: false, aplicado: aplicado, aviso: decision.aviso,",
         1, "AC-4 un rechazo SÍ leyó la nube: sincronizado es true"),
    # El AVISO de las ramas que SI aplican: pantalla mintiendo en la direccion
    # contraria (verde que se queda naranja para siempre).
    Caso("el camino feliz de la bajada se anuncia como pendiente", INDEX,
         "    return { aplicar: true, utilizable: true, aviso: 'ok', clave: 'nube-mas-nueva',",
         "    return { aplicar: true, utilizable: true, aviso: 'pendiente', clave: 'nube-mas-nueva',",
         1, "AC-1 y el camino feliz se anuncia en verde"),
    # El fallo CERRADO del reloj: el aviso estaba sellado por el censo, pero el
    # EFECTO de la guarda no lo medía nadie (5.6).
    Caso("con META ilegible el arranque adivina que lo local es del ano cero", INDEX,
         "    return { sincronizado: false, aplicado: false, aviso: 'error',\n"
         "             clave: 'meta-ilegible', motivo: 'la marca de tiempo local no se pudo leer' };",
         "    localSaved = 0;",
         1, "AC-2 y el aviso es de error, no verde"),
    Caso("con META ilegible la escucha en vivo sigue adelante", INDEX,
         "      setSyncUI(estadoSync('error'));\n      return;",
         "      setSyncUI(estadoSync('error'));",
         1, "AC-2 y lo pinta como error, no en verde"),
    # Los dos caminos tienen que coincidir tambien en lo que el operador MIRA.
    Caso("la escucha en vivo rechaza sin pintar nada", INDEX,
         "      console.warn('[SYNC] cambio de la nube NO aplicado:', decision.motivo);\n"
         "      setSyncUI(estadoSync(decision.aviso), decision.motivo);",
         "      console.warn('[SYNC] cambio de la nube NO aplicado:', decision.motivo);",
         1, "AC-4 un rechazo en vivo también pinta el aviso del veredicto"),
    # D-54. El naranja afirmaba UNA causa y lo alcanzan OCHO veredictos. Visto en
    # PRODUCCION el 2026-09-05: el operador, con 90 operaciones, leyo «este
    # dispositivo no tiene operaciones». Los TRES eslabones llevan mutante propio
    # porque revertir uno solo dejaba los otros verdes: medido, revertir los dos
    # llamantes con el pintor intacto daba rc=0 (5.6, el cable no es el mecanismo).
    Caso("el naranja vuelve a afirmar una causa fija", INDEX,
         "    status.textContent = textoPendiente(motivo);",
         "    status.textContent = 'Cambios sin subir: este dispositivo no tiene "
         "operaciones y no se pisa el libro de la nube.';",
         1, "D-54 el PINTOR usa el motivo del veredicto"),
    Caso("la bajada se come el motivo de su veredicto", INDEX,
         "  d.pintar(estadoSync(decision.aviso), decision.motivo);",
         "  d.pintar(estadoSync(decision.aviso));",
         1, "D-54 y le pasa al pintor el MOTIVO de su veredicto"),
    Caso("el arranque se come el motivo antes de pintar", INDEX,
         "  setSyncUI(aviso, motivoFinal);",
         "  setSyncUI(aviso);",
         1, "D-54 y el arranque NO se come el motivo"),
    # Y el caso del motivo AUSENTE: sin esto, «fallar cerrado en la pantalla»
    # seria un comentario. Inventarse una causa cuando no la hay es el mismo
    # defecto en su otra mitad.
    Caso("sin motivo, el texto se inventa una causa", INDEX,
         "  return m ? 'Cambios sin subir (' + m + '). ' + base\n"
         "           : 'Cambios sin subir. ' + base;",
         "  return 'Cambios sin subir (este dispositivo no tiene operaciones). ' + base;",
         1, "D-54 sin motivo"),
    Caso("un cambio de la nube entra al disco y la pantalla no se entera", INDEX,
         "    applySyncPayload(data);\n    repintarTrasSync();",
         "    applySyncPayload(data);",
         1, "AC-2 y AHÍ sí repinta la pantalla"),
    # La guarda `utilizable`, ejercida sobre la funcion ENTERA y no sobre el
    # juez aislado.
    Caso("la bajada deja de distinguir un documento inutilizable", INDEX,
         "  if (!decision.utilizable) {",
         "  if (false) {",
         1, "AC-2 un documento sin carteras no cuenta como sincronizado"),
    # El `|| 0` del reloj, afirmado por su VALOR y no solo por un ancla.
    Caso("el reloj se sella con la hora actual en vez de con la del documento", INDEX,
         "savedAt: Number(data.savedAt) || 0 }));",
         "savedAt: Number(data.savedAt) || Date.now() }));",
         1, "AC-3 un documento SIN marca deja el reloj local en cero"),
    # D-27 cerrada por la CLASE: el panel de importacion tenia su PROPIO anuncio
    # de exito, mas grande que el indicador, y lo pintaba en verde pasara lo que
    # pasara -- despues de haber vaciado la importacion pendiente.
    Caso("persistOps deja de devolver su veredicto al panel de importacion", INDEX,
         "  render();\n  // DEVUELVE el veredicto",
         "  render();\n  return true;\n  // DEVUELVE el veredicto",
         1, "AC-7 y devuelve false para que el panel de importación no mienta"),
    # Los efectos laterales que el arnes stubea: sin CONTARLOS, borrarlos del
    # producto salia verde.
    Caso("borrar una operacion deja de propagarla a la cartera", INDEX,
         "  const okOps  = saveOpsAll(ops);\n  syncAllPortfoliosFromOps();",
         "  const okOps  = saveOpsAll(ops);",
         1, "AC-7 y propaga el libro a la cartera"),
    Caso("borrar una operacion deja de actualizar la foto del mes", INDEX,
         "  autoSnapshot();   // la foto del mes refleja la cartera ya actualizada",
         "  ",
         1, "AC-7 y actualiza la foto del mes"),
    # ── Los instrumentos, saboteados a ELLOS (5.7). ────────────────────────
    # Una llamada opcional es una llamada DIRECTA por nombre: dejarla fuera del
    # censo era una ceguera NO declarada.
    Caso("un sumidero de subida abierto con llamada opcional `?.()`", INDEX,
         "function isMobile() {",
         "function isMobile() {\n  schedulePush?.();",
         1, "sumidero NUEVO, sin cobertura sellada"),
    # El sumidero del ARRANQUE: la funcion de subida pasada como VALOR.
    Caso("aparece un sumidero de subida pasado como referencia", INDEX,
         "function isMobile() {",
         "function isMobile() {\n  const colado = subirALaNube;\n  return !!colado;",
         1, "sumidero NUEVO, sin cobertura sellada"),
    # El MOTIVO, cableado: antes era prosa y un sumidero sellado con el marcador
    # de relleno pasaba verde para siempre (5.1 dentro del propio instrumento).
    Caso("un sumidero sellado se queda sin motivo escrito", BASELINE_SUMIDEROS,
         '"guardarTodo|subir|schedulePush": "La subida del guardado completo',
         '"guardarTodo|subir|schedulePush": "SIN MOTIVO ESCRITO — escribelo. La subida',
         2, "marcador de relleno"),
    Caso("la foto de sumideros se queda sin motivos de golpe", BASELINE_SUMIDEROS,
         '  "motivos": {', '  "motivos": {},\n  "motivos_apartados": {',
         2, "SIN motivo escrito"),
    # El `--update` de sumideros se niega a aflojar: hasta ahora solo tenia caso
    # permanente el de funcsize, y una reproduccion manual es una anecdota
    # fechada (4.5.6).
    Caso("deriva: se afloja la direccion de referencia de sumideros", SUMIDEROS,
         "'subir-referencia': 'dominacion', 'anunciar-referencia': 'dominacion'},",
         "'subir-referencia': 'ambas', 'anunciar-referencia': 'dominacion'},",
         3, "DERIVA (rc=3): sumideros del dano"),
    # cloudwrites: las dos regresiones que destapo el brazo del aparato.
    #     El ancla del multi-declarador. Con la expresion anterior --que barria
    #     desde la palabra clave-- se ligaba `basura`, que no es referencia de
    #     nada, y NUNCA `refColada`: la escritura quedaba sin que la mirara
    #     ninguna red, y la guarda de vacuidad seguia satisfecha con basura.
    #     `userDocRef()` da null sin sesion, asi que el `if` no ejecuta nada.
    Caso("cloudwrites liga el declarador equivocado y deja la escritura sin ver", INDEX,
         "  const d = deps || depsDeBajada();",
         "  const basura = 0, refColada = userDocRef();\n"
         "  if (refColada) await refColada.update({ colado: 1 });\n"
         "  const d = deps || depsDeBajada();",
         1, "ESCRITURA A LA NUBE FUERA DE LA PUERTA"),
    Caso("no se puede medir: index.html vacio", INDEX,
         None, "",
         2, "INSTRUMENTO ROTO"),
]


def main():
    fallos = []
    h0 = hash_arbol()

    # CONTROL DE VACUIDAD. Sin el, una puerta siempre-roja aprobaria este banco.
    rc, salida = puerta()
    if rc != VERDE_INTERIOR:
        if rc == 0:
            print("CONTROL DE VACUIDAD FALLIDO: la puerta interior devuelve 0.")
            print("   Deberia devolver 4 ('verde, pero el banco no corrio'). Un 0 ahi")
            print("   es una puerta que sale VERDE con el banco apagado (D-40).")
        else:
            print(f"CONTROL DE VACUIDAD FALLIDO: la puerta ya esta roja SIN sabotaje "
                  f"(rc={rc}, esperaba {VERDE_INTERIOR}).")
            print("   Nada de lo que siga significaria nada.")
        print(salida)
        return 2
    print(f"  OK    control de vacuidad: sin sabotaje, la puerta interior da "
          f"rc={VERDE_INTERIOR} (verde con el banco omitido)")

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
        print("  OK    --check no escribe en la foto sellada (funcsize)")

    antes = hashlib.sha256(BASELINE_AVISOS.read_bytes()).hexdigest()
    subprocess.run([sys.executable, str(AVISOS), '--check'],
                   capture_output=True, text=True, check=False, cwd=ROOT)
    if hashlib.sha256(BASELINE_AVISOS.read_bytes()).hexdigest() != antes:
        print("  NO MUERDE: avisos --check ha ESCRITO en su foto sellada")
        fallos.append("avisos --check escribe")

    else:
        print("  OK    --check no escribe en la foto sellada (avisos)")

    antes = hashlib.sha256(BASELINE_SUMIDEROS.read_bytes()).hexdigest()
    subprocess.run([sys.executable, str(SUMIDEROS), '--check'],
                   capture_output=True, text=True, check=False, cwd=ROOT)
    if hashlib.sha256(BASELINE_SUMIDEROS.read_bytes()).hexdigest() != antes:
        print("  NO MUERDE: sumideros --check ha ESCRITO en su foto sellada")
        fallos.append("sumideros --check escribe")
    else:
        print("  OK    --check no escribe en la foto sellada (sumideros)")

    antes = hashlib.sha256(CATCHES.read_bytes()).hexdigest()
    subprocess.run([sys.executable, str(EMPTYCATCH), '--check'],
                   capture_output=True, text=True, check=False, cwd=ROOT)
    if hashlib.sha256(CATCHES.read_bytes()).hexdigest() != antes:
        print("  NO MUERDE: emptycatch --check ha ESCRITO en su foto sellada")
        fallos.append("emptycatch --check escribe")
    else:
        print("  OK    --check no escribe en la foto sellada (emptycatch)")

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

    # ── Ciclo 01-05: controles que no caben como Caso, y por que. ──────────

    # (a) CONTROL POSITIVO del rc=4. El control de vacuidad de arriba exige que
    #     la puerta interior devuelva 4. Hay que demostrar que ESE control muere
    #     si el arreglo se revierte: si no, pasaria con y sin el (CLAUDE.md 5.9).
    #     No cabe como Caso porque un Caso compara el rc de la puerta, y aqui lo
    #     que se mide es justamente que la puerta deja de distinguirse.
    original = VERIFY.read_bytes()
    # El MODO se guarda con el contenido. Restaurar por os.replace desde un
    # temporal recien creado dejaba la puerta SIN bit de ejecucion, que es la
    # misma clase de fallo que este ciclo arreglo en el enganche: un fichero
    # que sigue ahi y ya no ejecuta nada.
    modo_original = VERIFY.stat().st_mode
    try:
        sustituir_unico_mismo_largo(VERIFY, "\n  exit 4\n", "\n  exit 0\n")
        rc, _ = puerta()
        if rc == VERDE_INTERIOR:
            print("  NO MUERDE: la puerta interior sigue dando 4 con el `exit 4` quitado; "
                  "el sabotaje no llego")
            fallos.append("el estimulo del rc=4 no llego")
        elif rc != 0:
            print(f"  NO MUERDE: esperaba que la puerta interior cayera a 0, dio rc={rc}")
            fallos.append("control positivo del rc=4")
        else:
            print("  OK    control positivo: sin el `exit 4`, la puerta interior vuelve "
                  "a dar 0 y la vacuidad lo caza")
    finally:
        # Restauracion ATOMICA: escribir en un temporal del mismo directorio y
        # renombrar, para que la puerta nunca quede a medio escribir. Queda una
        # ventana entre la mutacion y esta linea si el proceso muere de forma
        # que no ejecute el `finally`; NO se tapa con un comentario que prometa
        # un freno: quien lo caza es el control de vacuidad de la proxima
        # corrida, que ve la puerta interior en 0 y lo dice con esas palabras.
        # Restauracion EN EL MISMO INODO, no por `os.replace`. El bash padre
        # que esta ejecutando este mismo fichero conserva un descriptor abierto
        # sobre el inodo ORIGINAL: un renombrado le deja leyendo los bytes
        # MUTADOS el resto de la corrida, y `hash_arbol()` --que lee por RUTA--
        # informaria del arbol como limpio. La mutacion es de la misma longitud
        # (lo afirma `sustituir_unico_mismo_largo`), asi que devolver los bytes
        # originales tampoco mueve nada de lo que el padre aun no ha leido.
        with open(VERIFY, 'r+b') as f:
            f.write(original)
            f.truncate(len(original))
            f.flush()
            os.fsync(f.fileno())
        os.chmod(VERIFY, modo_original)

    # (b) Los tres desenlaces de hookcheck, SOBRE COPIAS. No se mutila el
    #     enganche instalado: cuando la puerta corre desde el pre-push, borrarlo
    #     o reescribirlo seria pisar el script que se esta ejecutando. Lo que
    #     mide el enganche REAL es el paso de la puerta (y el caso N3, que
    #     mutila el instalador, que si es seguro tocar).
    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp)
        inst, hook = d / 'install-hooks.sh', d / 'pre-push'
        def hk(h, i):
            r = subprocess.run([sys.executable, str(HOOKCHECK), '--hook', str(h),
                                '--installer', str(i)],
                               capture_output=True, text=True, check=False, cwd=ROOT)
            return r.returncode, r.stdout + r.stderr

        def sano():
            """Deja la copia EXACTAMENTE como la deberia dejar el instalador.

            El contenido se DERIVA del instalador con el mismo extractor que usa
            `hookcheck`, no del enganche instalado en esta maquina. Leer el
            instalado hacia que el banco reventara con un traceback -- y rc=1,
            o sea rotulado como fallo del CODIGO -- en una maquina donde el
            enganche no existe todavia, que es justo el caso que este ciclo
            existe para cazar.
            """
            inst.write_bytes(INSTALLHOOKS.read_bytes())
            try:
                cuerpo = hookcheck.esperado(INSTALLHOOKS)
            except SystemExit as e:
                raise AssertionError(
                    "no pude derivar el enganche esperado del instalador "
                    f"(hookcheck salio con {e.code}). El defecto esta en el BANCO "
                    "o en el instalador, no en el comprobador.") from None
            hook.write_text(cuerpo, encoding='utf-8')
            hook.chmod(0o755)

        # Control de VACUIDAD de este bloque: una copia sana tiene que salir
        # VERDE. Sin el, un comprobador siempre-rojo pasaria los cuatro casos
        # de abajo y pareceria perfecto.
        sano()
        rc, salida = hk(hook, inst)
        if rc != 0:
            print(f"  NO MUERDE: hookcheck da rc={rc} sobre una copia SANA; "
                  "nada de lo que sigue significa nada")
            fallos.append("hookcheck vacuidad")
        else:
            print("  OK    control de vacuidad: hookcheck verde sobre una copia sana")

        def sin_bit():
            hook.chmod(0o644)

        def distinto():
            hook.write_text(hook.read_text(encoding='utf-8') + "colado\n",
                            encoding='utf-8')

        def sin_heredoc():
            inst.write_text(
                INSTALLHOOKS.read_text(encoding='utf-8').replace("<<'HOOK'", "<<'OTRO'"),
                encoding='utf-8')

        def sin_unset():
            """El enganche deja de limpiar VERIFY_INNER: la SEGUNDA capa de D-40.

            Se mutila el INSTALADOR de la copia y se compara contra el enganche
            REAL: si alguien quitara esa linea, el comprobador lo cantaria como
            DISTINTO en la proxima puerta. No cabe como Caso porque hookcheck ya
            no corre en la puerta interior, y no se toca el enganche instalado
            porque mutarlo mientras el propio enganche corre seria pisar el
            script en marcha.
            """
            texto = INSTALLHOOKS.read_text(encoding='utf-8')
            if texto.count("unset VERIFY_INNER\n") != 1:
                raise AssertionError(
                    "ancla no unica: 'unset VERIFY_INNER' no aparece exactamente "
                    "una vez en install-hooks.sh. El defecto esta en el BANCO.")
            inst.write_text(texto.replace("unset VERIFY_INNER\n", ""), encoding='utf-8')

        for etiqueta, rc_esp, txt_esp, prepara in (
            ("AUSENTE", 1, "ENGANCHE AUSENTE", lambda: hook.unlink()),
            ("NO EJECUTABLE", 1, "ENGANCHE NO EJECUTABLE", sin_bit),
            ("DISTINTO", 1, "ENGANCHE DISTINTO", distinto),
            ("FORMA (el instalador cambio de forma)", 2, "INSTRUMENTO ROTO", sin_heredoc),
            ("ILEGIBLE (no puedo leer el instalador)", 2, "INSTRUMENTO ROTO",
             lambda: inst.chmod(0o000)),
            ("el enganche deja de limpiar VERIFY_INNER", 1, "ENGANCHE DISTINTO", sin_unset),
        ):
            try:
                sano()
                prepara()
            except AssertionError as e:
                print(f"  BANCO ROTO: hookcheck {etiqueta} — {e}")
                fallos.append(f"hookcheck {etiqueta} (banco)")
                continue
            rc, salida = hk(hook, inst)
            inst.chmod(0o644)
            if rc != rc_esp or txt_esp not in salida:
                print(f"  NO MUERDE: hookcheck {etiqueta} — esperaba rc={rc_esp} y "
                      f"{txt_esp!r}, dio rc={rc}")
                fallos.append(f"hookcheck {etiqueta}")
            else:
                print(f"  OK    muerde: hookcheck distingue {etiqueta} (rc={rc})")

    # El hash del arbol mira el CONTENIDO, no el modo. Un fichero que sigue
    # ahi byte a byte y ya no ejecuta nada es la misma clase de fallo que el
    # enganche sin permiso, y el hash lo daba por identico. Medido: la
    # restauracion atomica del control positivo de arriba perdia este bit.
    for ejecutable in (VERIFY, INSTALLHOOKS):
        if not os.access(ejecutable, os.X_OK):
            print(f"  ARBOL SUCIO: {ejecutable.name} ha perdido el bit de ejecucion")
            fallos.append(f"{ejecutable.name} sin bit de ejecucion")
    if not fallos or all('bit de ejecucion' not in f for f in fallos):
        print("  OK    la puerta y el instalador siguen siendo ejecutables")

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
