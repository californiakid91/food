# Libro de deudas — food

> **Lista VIVA, no un acta.** Se lee al arrancar cada sesión. Toda deuda diferida en un UNIFY sube
> aquí en el MISMO commit, con su origen citado. Si una deuda sólo existe en un SUMMARY, es como
> si no existiera. Norma completa en `CLAUDE.md` §8.
>
> Cada ficha dice: **qué es · cómo se midió · estado · qué la reabre.**

**CUARTA TRANSICIÓN de la Fase 1 (2026-09-01): la fase NO cierra, abre el ciclo 01-07.** Cuatro
brazos adversarios disjuntos; por primera vez uno —el del aparato de medición— **no demolió su
frase**, y por primera vez **ninguna cifra publicada era falsa**. Pero la META sigue sin cumplirse:
al arrancar, una nube más vieja empobrece el libro con la pantalla en verde (**D-45**), y quitar la
lista de carteras del veredicto de guardado deja la puerta en `rc=0` (**D-46**). Se cerró **D-15**
re-midiéndola en vez de heredarla. Acta: `.paul/phases/01-guardado-fiable/01-TRANSICION-4.md`.

Último ciclo cerrado: **01-06** (2026-08-31), la capa de aviso. **Cerró D-38** por la clase y
abrió **D-44**. Los TRES brazos adversarios del diff demolieron el ciclo ya escrito, cada uno
viendo algo que los otros dos no: diez hallazgos, el peor de ellos **un fallo de guardado pintado
en VERDE que salía `rc=0`** dentro del ciclo escrito para impedirlo.
Acta: `.paul/phases/01-guardado-fiable/01-06-SUMMARY.md`.

Ciclo anterior: **01-05** (2026-08-31), la vara de medir. Cerró **D-39, D-40 y D-41**,
abrió **D-42** (y **D-43** al cerrarlo) y re-midió **D-26** (186 sellado vs **190** derivadas: se ha vuelto a desfasar y la
puerta sigue verde). La revisión adversaria del diff destapó **dos falsos verdes del propio
arreglo** —un enganche sin bit de ejecución que git ignora dejando pasar el push, y suponer
`.git/hooks` con `core.hooksPath` puesto— y **un daño colateral**: cablear el vigilante del
enganche antes del banco dejaba sin correr el banco en cualquier máquina sin instalar.
Acta: `.paul/phases/01-guardado-fiable/01-05-SUMMARY.md`.

Última medición contra el código: **2026-08-31**, **TERCERA transición de la Fase 1**
(cuatro brazos adversarios disjuntos: caminos de pérdida, calidad del oráculo, cableado, y
documentos contra evidencia). Abrió **D-38, D-39, D-40 y D-41**, marcó **D-15 y D-03 a
re-medir**, y **NO cerró la fase**: acta `.paul/phases/01-guardado-fiable/01-TRANSICION-3.md`.
La revisión adversaria del PLAN 01-05 (2026-08-31) amplió **D-38** con un segundo pintor que
decide (`setSyncUI`) y con el reloj de la duración, y partió el trabajo en dos ciclos: **01-05**
(instrumental) y **01-06** (la capa de aviso entera).
Medición anterior: **2026-08-30**, ciclo **01-04** (cuatro brazos adversarios
disjuntos —correctness, falsos verdes, calidad del oráculo y cableado— sobre el diff del ciclo).
Cerró D-33, D-34 y D-31; abrió D-35, D-36 y D-37, y añadió `onScreenshotPicked` a D-09. Acta del
ciclo: `.paul/phases/01-guardado-fiable/01-04-SUMMARY.md`. La medición anterior (SEGUNDA
transición de la Fase 1) está en `.paul/phases/01-guardado-fiable/01-TRANSICION-2.md`.
D-12 y D-13 vienen de la revisión adversaria del plan 01-01, no de la auditoría inicial.

> ### ⚠️ Los números de línea de este libro son de la revisión en que se MIDIÓ, no de HEAD.
> `index.html` crece en cada ciclo y las citas de línea se desfasan al día siguiente: la auditoría
> de documentos del 2026-08-30 encontró que **casi todas** las de este fichero ya apuntaban mal.
> Se cierra la CLASE en vez del caso (`CLAUDE.md` §5.15): **para localizar el código se usa el
> NOMBRE de la función y `grep`, nunca el número de línea.** Las cifras derivadas de instrumentos
> (tamaños de función, controles de sabotaje, hashes) sí son fiables **cuando un script las
> vuelve a derivar**. Las copiadas a mano, no — y **`funciones_vistas` de `baseline-funcs.json`
> es una de las copiadas a mano**: dice 186 y hoy se derivan 190 sobre un `index.html` que no ha
> cambiado desde el sellado. Es munición de **D-26**, no una cifra fiable.

---

## Abiertas — riesgo de pérdida de datos

### D-45 · Al arrancar, una nube MÁS VIEJA empobrece el libro y la pantalla queda en VERDE
- **Qué es:** `pullFromFirestore` decide si el documento de la nube gana con
  `if (!hasRealLocalData() || (data.savedAt || 0) >= localSaved)`. `hasRealLocalData()` mira **sólo
  los activos** (`rows`) de cada cartera; **nunca el libro de operaciones**. Un operador que lo
  tenga todo vendido —activos vacíos, libro fiscal rico, que es cuando el libro más importa— cae en
  la primera rama, la comparación de fechas se desactiva y **cualquier** documento de la nube gana,
  por viejo que sea. `vaciariaElLibro` sólo bloquea el caso vacío, así que una nube rancia con una
  operación sustituye a un libro local de tres. Y al terminar, el punto de sync se pinta en VERDE.
- **Cómo se midió:** brazo de caminos de pérdida de la CUARTA transición (2026-09-01), reproducido
  sobre copia aislada: `ANTES ops 3 / DESPUÉS ops 1`, con la nube declarando un `savedAt` de 1000
  frente a un local de 2000000000000. La puerta entera sobre esa copia: **`rc=0`, VERDE**.
- **Por qué es Fase 1 y no Fase 3:** el ROADMAP lista este arreglo en el alcance de la Fase 3, pero
  el daño es **pérdida de libro en el ARRANQUE con estado tranquilizador**, que es la meta literal
  de la Fase 1, y **no exige fusionar**: basta que el predicado cuente el libro. Es además la misma
  asimetría que el 01-04 cerró en el otro lado (§5.16): el juez de subida `decidirSubida` ya mira
  las dos cosas —`tieneOperaciones` **y** `hayActivosLocales`—; el camino de bajada se quedó con el
  predicado viejo. **La asimetría ES el defecto.** Fusionar `ops` por `id` sigue siendo Fase 3.
- **Estado:** abierta. **Abre el ciclo 01-07.**
- **Qué la reabre:** nada la cierra sola. Se cierra cuando las dos direcciones usen el MISMO juez
  para «¿hay datos locales que proteger?», con un control que ejerza el desempate de
  `pullFromFirestore` y muerda si vuelve a mirar sólo los activos.

### D-46 · El cruce «sólo falla el guardado de la lista de carteras» no tiene oráculo
- **Qué es:** `guardarTodo` sólo canta victoria si las tres escrituras van bien
  (`todoBien = okRows && okOps && okMeta`). Quitar `okMeta` de esa conjunción —o sea, dejar de
  mirar si la lista de carteras se guardó— **deja la puerta entera en `rc=0` y VERDE**. Si
  `localStorage.setItem(META_KEY, …)` falla por cuota, el operador ve «Guardado ✓» en verde y
  además se sube a la nube.
- **Cómo se midió:** brazo del oráculo de la CUARTA transición (2026-09-01), **re-verificado a
  mano** sobre copia aislada con unicidad de ancla afirmada antes de mutar y estímulo demostrado en
  el fichero: `bash tools/verify.sh` → `rc=0`, diez pasos, «VERDE — todo ejercido y en verde».
  Escapa porque `pruebasFalloDeEscritura` inyecta su fallo parcial siempre en `saveOpsAll`, nunca
  en `saveMeta` a solas: los tres sumandos tienen control por separado y **el CRUCE no lo mide
  nadie** (`CLAUDE.md` §5.5).
- **Estado:** abierta. **Abre el ciclo 01-07**, junto con **D-27** y **D-29**, que son la misma
  familia: la invariante «un fallo de guardado no se anuncia como éxito y no se sincroniza» existe
  en un sitio y no en los demás.
- **Qué la reabre:** nada la cierra sola. Se cierra con un control que haga fallar **únicamente**
  `saveMeta` y exija `guardarTodo() === false`, aviso en rojo y cero subidas.

### D-47 · No hay volcado al cerrar la pestaña: una ventana de 600 ms sin guardar
- **Qué es:** apuntar una operación llama a `schedSave()`, que aplaza el guardado 600 ms. **No
  existe ningún manejador `beforeunload`, `pagehide` ni `visibilitychange` en todo `index.html`**
  (grep: cero resultados). Cerrar la pestaña dentro de esa ventana pierde la operación que el
  operador ya ha visto en pantalla.
- **Cómo se midió:** brazo de caminos de pérdida de la CUARTA transición (2026-09-01): tras
  `schedSave()`, memoria = 1 operación, disco = 0.
- **Estado:** abierta. **No abre ciclo por sí sola:** es pérdida sin fallo declarado —el guardado no
  llegó a intentarse, así que no hay nada que avisar— y su arreglo es independiente del resto.
- **Qué la reabre:** nada; se decide aparte. El arreglo natural es volcar en `pagehide`.

### D-35 · Un paquete incompleto bloquea TODAS las subidas y no hay salida en pantalla
- **Qué es:** desde el ciclo 01-04, si una sola clave del almacenamiento no se puede leer o
  parsear, `buildSyncPayload` marca el paquete como incompleto y **la subida se rechaza entera**,
  incluido el libro de operaciones. Mientras dure el fallo el dispositivo queda sin copia en la
  nube, y **no hay ninguna salida en la interfaz**: el operador ve el punto en rojo con «No se
  pudo sincronizar» y nada más. Es el gemelo exacto de **D-23**: mejor para el dato y peor para el
  operador. La primera versión del PLAN 01-04 afirmaba que el arreglo «no introduce un modo de
  fallo nuevo peor»; era falso, y lo destapó la revisión adversaria del plan.
- **Cómo se midió:** razonado sobre el código y ejercido en las autopruebas
  (`pruebasTuberiaDeSubida`: con el paquete incompleto no se escribe). **No reproducido con un
  almacenamiento corrupto real en el navegador.**
- **Estado:** ABIERTA y aceptada a sabiendas. Rechazar es lo correcto para el dato: `ref.set`
  reemplaza el documento entero, así que subir un paquete a medias borra de la nube lo que falte.
- **Qué la reabre:** nada la cierra sola. Se cierra cuando la pantalla diga QUÉ clave falló y
  ofrezca una salida sin abrir la consola. Es Fase 5 (interfaz) y arrastra a D-18 y a D-23: las
  tres son el mismo agujero —un bloqueo correcto que el operador no puede ni ver ni resolver—.

### D-36 · El veredicto de las autopruebas puede imprimirse antes que sus fallos
- **Qué es:** `runSelfTests` es asíncrona desde el 01-04. Si una suite quedara sin `await`, sus
  checks llegarían por microtarea **después** del mensaje de veredicto pero antes del código de
  salida: la consola imprimiría «✅ Autopruebas OK» y el proceso saldría con rc=1 **sin listar ni
  un fallo**, mandando a mirar a ciegas.
- **Cómo se midió:** brazo adversario de falsos verdes del ciclo 01-04 (2026-08-30), ejecutado en
  una copia del repo, 3 corridas de 3.
- **Estado:** ABIERTA, pero acotada. El `await` que falta lo caza ahora un control propio (una
  suite que no ejerce ni un solo check es una suite que no corrió) y su sabotaje. Lo que queda sin
  cerrar es la carrera del MENSAJE, no la del veredicto: el rc siempre es correcto.
- **Qué la reabre:** se cierra cuando el veredicto se calcule y se imprima después de haber
  drenado todas las promesas, o cuando `check` deje de poder ejecutarse tras el resumen.

### D-37 · Cambiar de cuenta de Google en el mismo navegador sube el libro de la cuenta anterior
- **Qué es:** los datos locales no están separados por usuario. Si se cierra sesión con la cuenta
  A y se entra con la B en el mismo navegador, el libro de A sigue en el almacenamiento local y el
  juez de subida lo aprueba —ninguno de los dos lados está vacío— y lo escribe en el documento
  de B.
- **Cómo se midió:** brazo adversario de correctness del ciclo 01-04 (2026-08-30), leyendo el
  código. **No reproducido.**
- **Estado:** ABIERTA, prioridad baja: la app es personal y de un solo usuario. Se ficha porque no
  estaba dicho en ningún sitio, y porque el juez de subida no puede protegerla — el problema es
  que las claves de almacenamiento no llevan el identificador de la cuenta.
- **Qué la reabre:** que se use la app con más de una cuenta, o que se comparta el dispositivo.

### D-39 · Los trinquetes revientan con `rc=1` y traceback en vez de fallar CERRADO
- **Qué es:** `cargar_baseline()` de `tools/funcsize.py` valida que la clave `excede` exista, pero
  no su TIPO. Con `"excede": null` (JSON válido y aceptado por su propio chequeo de forma),
  `--check` muere con `TypeError: 'NoneType' object is not iterable` y **rc=1**. La puerta lo
  rotula entonces «FALLO trinquete de tamaño de funciones → HALLAZGOS (rc=1)»: **un instrumento
  roto sale clasificado como código que ha engordado**, y manda a mirar el sitio equivocado.
  Mismo agujero de clase en `tools/emptycatch.py` (`tolerados` sin validar tipo, y `--update`
  leyendo `['motivos']` sin validarlo).
- **Cómo se midió:** TERCERA transición (2026-08-31), brazo de cableado; **re-verificado a mano**
  por el orquestador sobre copia aislada: rc obtenido **1**, rc debido **2**.
- **Estado:** **CERRADA** en el ciclo **01-05** (2026-08-31). `cargar_baseline()` de los dos
  instrumentos valida ahora **el TIPO de cada clave**, y `emptycatch` valida además `motivos`, que
  sólo lee `--update`: antes `--check` salía **VERDE** con una foto que `--update` no podía leer —
  la forma que validaba el chequeo no era la forma que el instrumento necesita (§5.16). Rojo
  literal reproducido antes y después:
  - antes: `TypeError: 'NoneType' object is not iterable` + **rc=1**, rotulado por la puerta como
    «el monolito ha engordado»
  - después: `rc=2 INSTRUMENTO ROTO: funcsize: la foto sellada baseline-funcs.json: la clave
    'excede' es NoneType, se esperaba un objeto` + **rc=2**
  Dos sabotajes permanentes en el banco (uno por instrumento). El `except` de la comparación es
  **estrecho a propósito**: comprobado que un hallazgo real sigue en **rc=1** (`EL MONOLITO HA
  ENGORDADO`, `CATCH VACIO EN EL CAMINO DE SUBIDA`), no tapado por el aviso.
- **Qué la reabre:** cualquier instrumento nuevo que lea una foto sellada sin validar sus tipos.

### D-40 · `VERIFY_INNER=1` deja la puerta en `rc=0` con el banco de sabotaje sin correr
- **Qué es:** con esa variable puesta, `verify.sh` imprime «OMITIDO banco de sabotaje» y «VERDE,
  PERO EL BANCO NO CORRIÓ», pero **sale con 0**. El enganche `pre-push` hereda el entorno y sólo
  bloquea con rc≠0: esa variable exportada en un perfil, un wrapper o un CI deja pasar todos los
  push con el banco apagado, indefinidamente. **El veredicto de una puerta es un exit code, no una
  línea de texto que alguien tiene que leer** (§4.1).
- **Cómo se midió:** TERCERA transición (2026-08-31); **re-verificado a mano**: `VERIFY_INNER=1
  bash tools/verify.sh` sobre copia aislada → `rc=0`.
- **Estado:** **CERRADA** en el ciclo **01-05** (2026-08-31), con **las DOS capas, no una**:
  1. La puerta corrida con `VERIFY_INNER=1` devuelve ahora **rc=4** («verde, pero el banco no
     corrió»), nunca 0. Un 4 es verde para **un solo consumidor**, `sabotage.py::puerta()`; para
     el operador y para el enganche es no-verde. La tabla de códigos está escrita en la cabecera
     de `verify.sh`.
  2. El enganche **limpia la variable** (`unset VERIFY_INNER`) antes de llamar a la puerta, así
     que un perfil contaminado no la hereda.
  Con una sola capa el agujero seguía abierto por el otro lado. **Medido con la variable
  exportada:** a mano `rc=4`; por el enganche, puerta COMPLETA con el banco corrido, `rc=0` con
  código sano y **`rc=1` PUSH BLOQUEADO** con una regresión real.
  Cambiar este contrato tenía un **consumidor vivo**: el control de vacuidad del banco exigía que
  esa corrida fuera verde. Se cambió el consumidor en el mismo commit, y hay **control positivo**:
  revertido el `exit 4`, la puerta interior vuelve a dar 0 y la vacuidad lo caza.
- **Qué la reabre:** cualquier interruptor nuevo que reduzca lo que se ejerce sin cambiar el rc.

### D-41 · Nada vigila que el enganche `pre-push` exista ni que esté al día
- **Qué es:** la variante automática de la puerta es el enganche que instala
  `tools/install-hooks.sh`. Hoy el instalado es byte a byte el del instalador, pero **ningún paso
  de la puerta lo comprueba**. En una máquina nueva la variante automática sencillamente no
  existe, y nada se pone rojo; si el instalador cambia, el instalado queda rancio en silencio. Es
  la definición del propio proyecto de instrumento no cableado (§4.1), y el escenario exacto que
  §4.2 manda vigilar: «verifica AMBAS variantes».
- **Cómo se midió:** TERCERA transición (2026-08-31), brazo de cableado: comparó el enganche
  instalado contra el heredoc del instalador (idénticos) y comprobó que ni `verify.sh` ni
  `sabotage.py` lo miran.
- **Estado:** **CERRADA** en el ciclo **01-05** (2026-08-31) con `tools/hookcheck.py`, cableado
  como paso de la puerta. Distingue **seis desenlaces**, cada uno con su sabotaje sobre copias:
  **AUSENTE** · **NO EJECUTABLE** · **DISTINTO** · **FORMA** (el instalador cambió de forma, rc=2)
  · **ILEGIBLE** (rc=2) · y el positivo de que el enganche siga limpiando `VERIFY_INNER`. Más un
  **control de vacuidad**: sobre una copia sana, verde.
  El contenido esperado se **deriva del instalador** (se extrae su heredoc), no de una copia
  pegada en el comprobador: dos copias se desincronizan a la primera.
  **La revisión adversaria del diff destapó dos falsos verdes de este mismo arreglo**, los dos
  reproducidos a mano en un repo de usar y tirar antes de creérselos:
  - un enganche **sin bit de ejecución** hace que git lo **ignore** (avisa con un `hint:`
    silenciable) y **el push sale con rc=0** — la variante automática muerta con el fichero ahí;
  - suponer `.git/hooks` es falso con `core.hooksPath` puesto o en un `git worktree`: el enganche
    se ignora entero. Ahora la ruta **se le pregunta a git** (`git rev-parse --git-path hooks`),
    en el comprobador **y** en el instalador.
- **Nota de diseño:** el paso va **después del banco y fuera de la corrida interior**, a propósito.
  Mide la MÁQUINA, no el código. Cableado antes, un clon recién hecho o un CI ponía la puerta en
  rojo por el enganche y **el banco no llegaba a correr**: en esa máquina nada demostraba que
  ninguno de los otros controles muerde. Lo destapó la revisión del diff.
- **Qué la reabre:** que aparezca otro enganche de git sin su fila en `hookcheck.py` (la lista de
  enganches es enumerada, no derivada), o que el instalador cambie de forma sin reinstalar.

### D-42 · `comparar_o_roto` es una red SIN ORÁCULO: pasa con y sin ella
- **Qué es:** el envoltorio que hace fallar cerrado la comparación de los dos trinquetes es hoy
  **inalcanzable por construcción**. `cargar_baseline()` ya valida los tipos de todo lo que le
  llega, así que `comparar` no puede lanzar ninguna de las excepciones que captura. Los dos
  sabotajes de la foto malformada **miden la validación, no el envoltorio**: dan el mismo rc y el
  mismo mensaje con él y sin él. Es §5.9 en pequeño, y está **escrito en su propio docstring** en
  vez de contarse como control medido.
- **Cómo se midió:** revisión adversaria del diff del ciclo 01-05 (2026-08-31), hallazgo #3,
  reproducido revirtiendo las dos llamadas a `comparar(...)` a pelo: mensaje y rc **idénticos**.
- **Estado:** ABIERTA, y **deliberadamente no se arregla ahora**. Quitarlo devolvería el rc=1 con
  traceback en cuanto alguien añada una clave sin validarla, que es justo D-39. Se queda como red
  declarada.
- **Qué la reabre:** que se añada a una foto sellada una clave que `cargar_baseline` no valide;
  entonces el envoltorio pasa a ser alcanzable y hay que darle sabotaje propio.

### D-43 · Un mutador del banco sustituye texto SIN afirmar que su ancla sea única
- **Qué es:** de los seis mutadores del bloque de `hookcheck` en `tools/sabotage.py`, cinco no
  necesitan ancla (borran el fichero, le quitan el bit de ejecución, le añaden una línea, le
  cambian los permisos) y `sin_unset` **sí** afirma la unicidad de la suya. El sexto,
  `sin_heredoc`, sustituye `<<'HOOK'` **sin afirmar que aparezca exactamente una vez**. La doctrina
  lo exige explícitamente (§4.5.5 y §5.4): el sabotaje afirma la unicidad de su ancla **antes** de
  mutar, porque un meta-instrumento falla inventando agujeros, no ignorándolos.
- **Cómo se midió:** UNIFY del ciclo 01-05 (2026-08-31), leyendo los seis mutadores uno a uno
  contra el texto del AC-7 del propio plan, que dice «cada caso afirma la UNICIDAD DE SU ANCLA
  antes de mutar».
- **Estado:** ABIERTA, y **no es un falso verde**: si el ancla dejara de casar, la copia quedaría
  intacta, `hookcheck` daría rc=0 en vez del rc=2 esperado y el caso gritaría **NO MUERDE**. O sea
  que falla **ruidosamente**, que es la propiedad que importa. Es una desviación **nominal** del
  AC-7, escrita en vez de callada, no un agujero medido.
- **Qué la reabre:** que `install-hooks.sh` pase a contener más de un heredoc, momento en el que el
  mutador mutaría los dos y el caso dejaría de medir lo que dice medir. Se cierra con dos líneas:
  la misma afirmación que ya tiene `sin_unset`.

### D-44 · El censo de avisos es ESTÁTICO y su ámbito se exime a mano
- **Qué es:** `tools/avisos.py` mide leyendo el texto de `index.html`, no ejecutándolo. De ahí
  salen tres cegueras, escritas también en la cabecera del propio instrumento:
  1. **Presencia no es precedencia (§5.11).** Un literal escrito dentro de una CADENA cuenta como
     cobertura. Los comentarios sí se borran antes de medir, así que un comentario no cuela.
  2. **La red por RECEPTOR sólo ve `getElementById` con un literal.** Un `getElementById(variable)`
     que acabara resolviendo a un elemento de aviso le es invisible. No se cierra por lista blanca
     de variables porque el fichero tiene decenas de identificadores compuestos legítimos
     (`'bar-' + id`), y una lista blanca sólo protege de lo que ya conoce.
  3. **El ámbito exime `runSelfTests` a mano.** Es el único CORTE, nombrado con su motivo (sus
     avisos son el veredicto de la propia suite, y ya tienen juez: el código de salida de la
     puerta). Quitarlo o cambiarlo es DERIVA (rc=3).
- **Cómo se midió:** revisión adversaria del diff del 01-06 (2026-08-31), **dos brazos disjuntos
  llegaron al mismo sitio por caminos distintos**, y el hallazgo se re-verificó a mano sobre copia
  aislada. El ámbito se intentó acotar **dos veces** y las dos perdió avisos reales:
  - con **ocho raíces escritas a mano**, escapaban **nueve avisos** del camino de la fase
    (`applySyncPayload` ×5, `pullFromFirestore`, `listenFirestore`, `repararLibroIlegible`,
    `migrateOpsToGlobal`): sembrar un aviso nuevo en el guardado por sincronización daba `rc=0`;
  - con **raíces derivadas y cierre transitivo**, se perdió **`guardarTodo`** —el guardado en
    persona— porque sólo se alcanza como ARGUMENTO (`setTimeout(guardarTodo, 600)`).
  Un cierre transitivo sobre JavaScript tiene más formas de escaparse de las que uno puede
  enumerar. **Por eso hoy se mide TODO el `<script>` y se exime por nombre**: el instrumento MIDE,
  y quien EXIME es el criterio.
- **Consecuencia aceptada:** el censo incluye avisos que NO son de guardado ni de arranque (borrar
  carteras y operaciones, vaciar activos, el texto reconocido de una captura). No se excluyen: se
  sellan con su motivo. Es más ancho que el alcance declarado del ciclo 01-06, **en la dirección
  segura**, y se dice por escrito en vez de recortarlo.
- **Estado:** ABIERTA como ceguera declarada. **No es un falso verde**: es un límite del método,
  escrito en la cabecera del instrumento y aquí, no un agujero que se descubra mañana.
- **Qué la reabre:** que aparezca en `index.html` un `getElementById` con identificador calculado
  que resuelva a un elemento de aviso; que un aviso se emita por un canal que no sea
  `console.error`, `console.warn`, `alert` ni `confirm`; o que haga falta un segundo CORTE — el
  segundo corte es la señal de que el criterio está empezando a doblarse.

### D-01 · El sync reemplaza el libro de operaciones en vez de fusionarlo
- **Qué es:** `applySyncPayload` sustituye `ops` entero por lo que venga de la nube, con
  last-write-wins por un único `savedAt` de documento. Importar operaciones en el móvil sin red y
  abrir luego el portátil puede borrarlas sin aviso.
- **Cómo se midió:** lectura del código en la auditoría del 2026-08-29 (`index.html:2874`,
  `2911`). **No reproducido en vivo**: el comportamiento de Firestore con escrituras encoladas
  offline está razonado sobre la semántica documentada de `set()`, no observado.
- **Estado:** planificada como Fase 3 del roadmap. Depende de tener backup antes (D-02).
  **Cota parcial YA PUESTA** en el ciclo 01-02 (`77f8cef`): un único juez, `vaciariaElLibro`,
  cablea las dos guardas e impide el caso destructivo en los dos sentidos. La fusión real sigue
  siendo Fase 3. Ojo: la guarda de subida omite el push ENTERO, así que mientras el libro local
  esté vacío y la nube tenga operaciones, los cambios de activos tampoco suben. Es deliberado —
  fusionar es Fase 3— pero no es gratis.
- **Qué la reabre:** cualquier cambio en `buildSyncPayload`/`applySyncPayload` antes de la Fase 3.

### D-02 · No existe copia de seguridad fuera de Firestore
- **Qué es:** todo el estado vive en localStorage y en un único documento de Firestore que se
  pisan mutuamente. No hay exportación ni restauración.
- **Cómo se midió:** búsqueda de código de backup/restore en `index.html` — no hay ninguno.
- **Estado:** planificada como Fase 2. Arrastrada desde 2026-05-30.
- **Qué la reabre:** nada; está en cola.

### D-03 · El documento de Firestore crece hacia el límite de 1 MB

> **⚠️ A RE-MEDIR (2026-08-31, tercera transición).** La mitad del daño que describe —«el fallo
> de `set()` falla en silencio mientras el indicador sigue verde»— la cerró el ciclo 01-04, y se
> vio el ROJO en el navegador el 2026-08-31. El núcleo (el documento hacia 1 MB, el tamaño del
> paquete jamás medido) sigue abierto. Detalle: `01-TRANSICION-3.md`, hallazgo T3-7.
- **Qué es:** `buildSyncPayload` mete todos los snapshots mensuales de todos los activos en UN
  documento. Firestore corta en 1 MB, y el fallo de `set()` sólo hace `console.error`
  (`index.html:2945`) mientras el indicador de sync sigue verde.
- **Cómo se midió:** lectura del código. **El tamaño real del payload NO se ha medido nunca.**
- **Estado:** abierta, sin fase asignada.
- **Qué la reabre:** medir el payload. Si pasa de ~500 KB, sube a fase propia.

### D-13 · Las ramas de legado siguen colapsando compras idénticas del mismo día
- **Qué es:** `dedupeOps` por huella, que se conserva en `migrateOpsToGlobal` y en la rama `opsData`,
  no distingue dos compras legítimamente idénticas del mismo día dentro de la misma cartera.
- **Cómo se midió:** lectura del código, confirmada por la revisión adversaria del 2026-08-29
  (`index.html:988`, `1010`, `2877`).
- **Estado:** **límite aceptado a propósito**, vigente desde el ciclo 01-02 (`77f8cef`). La
  migración corre una sola vez y `opsData` sólo llega de un dispositivo sin actualizar. La rama
  moderna (`opsAll`) ya NO tiene este problema: deduplica por identificador Y huella, con
  autoprueba y sabotaje permanentes.
- **Qué la reabre:** que aparezca un dispositivo antiguo sincronizando de verdad, o que la migración
  tenga que volver a correr.

### D-18 · Que el aviso de guardado se PINTE de rojo no lo ejerce nadie
- **Qué es:** cuando el guardado falla, la app debe avisar en rojo en vez de decir «Guardado ✓».
  La DECISIÓN de avisar como error está cubierta: los invariantes sustituyen `showSaveIndicator`
  y comprueban que recibe `ok === false`, incluido el camino de éxito PARCIAL (los activos se
  guardan y el libro no). Lo que nadie ejerce es el último eslabón, dentro del cuerpo de
  `showSaveIndicator`: `el.style.color = ok ? 'var(--green)' : 'var(--red)'`. Al interceptar la
  función, el invariante nunca corre su cuerpo. Es exactamente la trampa de `CLAUDE.md` §5.6:
  cubrir el mecanismo no cubre su aviso.
- **Cómo se midió:** verificación manual de la Fase 1 en la app desplegada, 2026-08-30. Tres de
  los cuatro puntos se confirmaron en el navegador real (aviso verde al guardar; el naranja no
  aparece en uso normal; `?selftest=1` deja los datos intactos — 90 operaciones y 4 carteras,
  idénticas antes y después). El cuarto NO se comprobó: provocar un fallo real de guardado exige
  agotar el almacenamiento del navegador, y no se improvisó con 90 operaciones reales delante.
- **Estado:** abierto y acotado. Riesgo bajo —es un operador ternario de una línea— pero el
  eslabón no está ejercido y no se blanquea como comprobado. Hereda del ciclo 01-01, donde el
  aviso rojo se construyó y nunca se vio en pantalla.
- **NO la cierra la verificación del 2026-08-31.** Ese día se vio en el navegador el punto ROJO
  «No se pudo sincronizar», y es **otro indicador**: ése es `setSyncUI`, el de la SUBIDA a la nube,
  y se provoca inyectando una escritura que rechaza (receta en `01-04-VERIFICACION-NAVEGADOR.md`).
  D-18 habla del cuerpo de `showSaveIndicator`, el aviso del GUARDADO LOCAL. Confundirlos cerraría
  la ficha con la categoría equivocada, que es peor que dejarla abierta (§5.10).
- **Qué la reabre:** cualquier cambio en `showSaveIndicator` o en el tema de colores; y se cierra
  cuando exista una forma segura y repetible de provocar un fallo de guardado real.

### D-16 · La guarda de subida deja de sincronizar los activos, no sólo el libro
- **Qué es:** cuando la guarda salta, `schedulePush` abandona el push ENTERO. Mientras el libro
  local esté vacío y la nube tenga operaciones, tampoco suben carteras, activos, histórico ni
  precios. Es deliberado —fusionar es Fase 3— pero no es gratis: un usuario que borre todas sus
  operaciones a propósito deja de sincronizar lo demás indefinidamente.
- **Cómo se midió:** revisión del diff del ciclo 01-02, sobre `77f8cef`.
- **Estado:** aceptado a propósito, ya NO en silencio: desde este ciclo el indicador se pone
  naranja («Cambios sin subir») en vez de quedarse verde, que era el defecto de verdad.
- **Qué la reabre:** la Fase 3, que al fusionar libros hace innecesaria la guarda entera.

### D-17 · Sin conexión y sin caché, un dispositivo sin operaciones no sube nada
- **Qué es:** la guarda de subida necesita leer la nube, y `enablePersistence` es best-effort
  (falla con varias pestañas abiertas y en navegadores que no lo soportan). Sin caché y sin red, esa
  lectura falla. Se ha decidido fallar CERRADO: no se sube y se avisa en naranja.
- **Cómo se midió:** revisión del diff del ciclo 01-02. El comentario del propio código ya advertía
  de esto para las transacciones; la guarda nueva reintrodujo una lectura en ese camino.
- **Estado:** abierto y acotado. Sólo afecta a dispositivos SIN operaciones locales; el usuario con
  libro sigue subiendo directo, sin lectura previa. Se elige perder sincronía antes que perder el
  libro.
- **Qué la reabre:** que el modo avión se vuelva un caso de uso principal, o la Fase 3.

### D-19 · La lectura previa a subir puede contestarla la caché, no el servidor
- **Qué es:** antes de subir, un dispositivo con el libro local vacío pregunta a la nube si está
  vacía (`ref.get()` en `schedulePush`). Firestore tiene la persistencia activada
  (`db.enablePersistence({ synchronizeTabs: true })`), así que esa lectura puede resolverse desde
  la caché local. Con una caché anticuada, el dispositivo A cree que la nube sigue vacía, la
  guarda le deja pasar, y el `set()` machaca las operaciones que el dispositivo B ya había subido.
  La guarda hermana ya falla CERRADO cuando la lectura RECHAZA (D-17); lo que no cubre es que la
  lectura RESPONDA, y responda algo rancio.
- **Cómo se midió:** brazo de seguridad de la transición de la Fase 1, 2026-08-30, sobre el diff
  `69f728e..abe5e80`. Verificado en el código: la persistencia se habilita en `index.html:2855` y
  la lectura de la guarda no pasa `{ source: 'server' }`.
- **Estado:** abierto y acotado. **No es una regresión**: antes de esta fase no había guarda
  ninguna y ese dispositivo machacaba la nube SIEMPRE. Es el residuo que la guarda no alcanza.
  El arreglo obvio —forzar lectura de servidor— reintroduce y agrava D-17: sin red esa lectura
  rechaza y el dispositivo deja de sincronizar. El equilibrio pertenece a la Fase 3, que sustituye
  la guarda entera por una fusión y ya no necesita preguntar quién gana.
- **Qué la reabre:** la Fase 3; o que aparezca un caso real de dos dispositivos con la caché
  desincronizada.

### D-20 · El payload de la nube sólo está validado en el bloque del libro
- **Qué es:** el ciclo 01-02 blindó el tramo de `opsAll` de `applySyncPayload` (comprueba que sea
  un array, tolera entradas nulas). El tramo anterior, el de `portfolioData`, sigue sin validar:
  un documento con `portfolioData: { "1": null }` lanza una excepción al leer `pd.nextId` cuando
  `portfolios`, `currentPortId` y `nextId` YA se han reasignado a los valores de la nube y parte
  de las claves de activos ya se han escrito. Queda un estado a medias en memoria y en disco. Y un
  `nextId` no numérico deja `nextId = NaN`, con lo que todas las filas nuevas nacen con
  identificador `NaN`.
- **Cómo se midió:** brazo de seguridad de la transición de la Fase 1, 2026-08-30. Preexistente:
  el diff de la fase no tocó ese tramo.
- **Estado:** abierto. Zona ligada: una operación con campos absurdos que pase `dedupeOpsById`
  llega hasta el cálculo del FIFO —base de la renta— sin validación de forma.
- **Qué la reabre:** la Fase 3 reescribe `applySyncPayload`; la Fase 4 toca el FIFO. Lo que llegue
  antes.

### D-21 · La migración del formato antiguo con el libro ilegible no la ejerce nadie
- **Qué es:** `migrateOpsToGlobal` convierte el formato antiguo por cartera al libro único. El
  ciclo 01-01 le añadió un camino nuevo —saltar la cartera ilegible y rescatar su contenido— que
  ninguna autoprueba ejecuta. Es un camino de UNA SOLA OPORTUNIDAD: corre en la primera apertura
  tras actualizar un dispositivo viejo, y si pierde o duplica operaciones históricas no hay
  segunda ocasión de notarlo.
- **Cómo se midió:** brazo de radio de impacto de la transición de la Fase 1, 2026-08-30.
  `grep -n "migrateOpsToGlobal(" index.html` devuelve sólo su definición (1075) y su único
  llamante de producción (3420): cero llamantes en la zona de autopruebas.
- **Estado:** abierto. La función entera tiene llamante de producción, así que no es código
  muerto; lo que no está ejercido es su rama nueva.
- **Qué la reabre:** que se toque `migrateOpsToGlobal` o el formato antiguo `opsData`; y se cierra
  con una autoprueba que siembre una cartera antigua con blob ilegible.

### D-25 · Una reparación desde la nube descarta en silencio lo tecleado con el cerrojo puesto
- **Qué es:** con el cerrojo puesto, `saveOpsAll` lleva rato negándose, así que todo lo que el
  operador haya apuntado desde que abrió la app vive **sólo en memoria y en la pantalla**. Cuando
  llega de la nube un documento con operaciones, la reparación escribe **únicamente la lista de la
  nube** y el `loadOpsAll` final sustituye la memoria por ella: lo tecleado desaparece de la
  pantalla y del disco **sin ningún aviso**. La guarda de no-vaciado no protege aquí, porque la
  nube no viene vacía.
- **Cómo se midió:** revisión ligera del diff del ciclo 01-03 (2026-08-30). **No es una regresión**:
  el código anterior al ciclo también pisaba. Lo que cambia es que ahora sabemos que existe.
- **Estado:** ABIERTA, diferida por escrito. Es la misma familia que **D-01** (el sync reemplaza en
  vez de fusionar) y se cierra con ella en la Fase 3: fusionar local y nube es exactamente lo que
  este ciclo declaró fuera de alcance. Distinta de **D-23**, que se dispara al recargar; ésta se
  dispara al sincronizar. `pruebasPrecedenciaDeGuardas` construye justo ese estado (cerrojo puesto
  + memoria poblada) pero sólo ejercita la mitad de la nube vacía.
- **Qué la reabre:** nada la cierra sola. Si la Fase 3 fusiona y esta ficha sigue abierta, es que
  la fusión no cubrió el caso del cerrojo puesto.

### D-24 · La rama moderna del sync decide el cerrojo con memoria rancia y puede pisar un blob ilegible sin rescatarlo
- **Qué es:** `applySyncPayload` decide por `opsIlegible` **en memoria**, que sólo es tan fresco
  como la última `loadOpsAll()`. Si el libro se corrompe en disco **después** de que la app haya
  cargado (otra pestaña, corrupción del almacenamiento), la rama moderna cree que el cerrojo está
  bajado y `saveOpsAll` **pisa el blob corrupto sin hacerle copia de rescate**. La rama del formato
  antiguo NO tiene el problema: llama a `loadOpsAll()` dentro, así que re-deriva el cerrojo del
  disco y sí rescata. Mismo estado de disco, resultado distinto según el formato del payload.
  Arrastra dos asimetrías menores de aviso: una nube en formato antiguo vacía no emite ni el
  `[SYNC] libro recibido vacío` ni el «no llega nada con que repararlo»; calla donde la moderna
  es ruidosa.
- **Cómo se midió:** brazo adversario de correctness sobre el diff del ciclo 01-03 (2026-08-30),
  censando **todas** las asignaciones de `opsIlegible` del fichero, no sólo las del diff. Es un
  defecto **anterior al ciclo**: el 01-03 no lo introdujo, lo destapó al preguntarse si las dos
  ramas eran simétricas. **No reproducido en vivo**: exige corromper el almacenamiento entre la
  carga y la sincronización.
- **Estado:** ABIERTA, diferida por escrito. Cerrarla exige releer el disco antes de escribir —en
  cada guardado, no sólo en el sync— o mover el rescate dentro de la escritura cruda. Las dos
  opciones cambian el coste de `schedSave` y el contrato de `escribirOpsAll`, que este ciclo
  acababa de fijar; hacerlo aquí sería rediseñar la pieza recién puesta sin plan. Va con **D-01**
  (Fase 3), que ya tiene que revisar la semántica entera de `applySyncPayload`.
- **Qué la reabre:** nada la cierra sola. La frase «las dos ramas son simétricas» queda REFUTADA
  y no debe volver a escribirse hasta que exista una prueba que la sostenga. Si alguien afirma la
  simetría en un acta o un comentario, esta ficha es la refutación.

### D-23 · El cerrojo del libro ilegible no tiene salida visible para el operador
- **Qué es:** el ciclo 01-03 arregló que el cerrojo `opsIlegible` se levantase antes de confirmar
  la reparación. El precio es que ahora, con el libro local ilegible y una nube **vacía o
  ausente**, el cerrojo queda puesto **indefinidamente**: nada fuera de `loadOpsAll` y
  `repararLibroIlegible` lo baja, no hay interfaz para resolverlo, y el único aviso es un
  `console.error` que el usuario no ve. Y encadena: `saveOpsAll` devuelve `false` → `guardarTodo`
  devuelve `false` → no hay subida → **las operaciones nuevas viven sólo en memoria y se pierden
  al recargar**. Antes del ciclo, ese mismo caso se «resolvía» escribiendo `[]` encima con la copia
  de rescate a salvo: un reinicio con pérdida acotada. Ahora es un bloqueo silencioso. Es mejor
  para el dato y peor para el operador, y por eso se escribe en vez de esconderse.
- **Cómo se midió:** leyendo el código en la revisión adversaria del PLAN 01-03 (2026-08-30). Lo
  encontró Fable atacando la frase «el arreglo no empeora nada»; no salió de ejecutar nada.
- **Estado:** ABIERTA y aceptada a sabiendas. Construir la salida en pantalla es UX (Fase 5) y
  arrastraría a **D-18**, así que el ciclo 01-03 la declaró fuera de alcance por escrito.
  **Salida manual mientras tanto:** en las herramientas del navegador, comprobar primero que
  existe una clave `balance-ops-rescate-*` con el contenido original y **sólo entonces** borrar la
  clave `balance-ops`; al recargar, `loadOpsAll` leerá «no hay nada» en vez de «ilegible» y bajará
  el cerrojo. Ligada a **D-18** (el aviso en rojo no se pinta en ninguna prueba), a **D-15** y,
  desde el 01-04, a **D-35**: son la misma familia —un bloqueo correcto para el dato que el
  operador no puede ni ver ni resolver—. **Revisada en el 01-04 y NO cambia de forma:** el cerrojo
  pasó a ser entrada explícita del juez de subida (`libroIlegible`), lo que hace el bloqueo más
  visible en el código y le añade un aviso naranja en pantalla, pero **no le da salida**. Sigue
  igual de abierta y por el mismo motivo.
- **Qué la reabre:** nada la cierra sola. Se cierra cuando exista un aviso en pantalla que diga al
  operador que el libro está bloqueado y le ofrezca la salida sin abrir la consola. Si alguien
  quita el `if (opsIlegible)` de `saveOpsAll` para «desatascarlo», el sabotaje «saveOpsAll deja de
  consultar el cerrojo» se pone rojo: esta deuda se paga con interfaz, no aflojando el cerrojo.

### D-27 · `persistOps` canta «Guardado ✓» antes de saber si el libro entró
- **Qué es:** `persistOps` —el camino de borrar una operación y el de confirmar una importación—
  llama a `saveOpsAll(ops)` **ignorando su booleano**, luego a `saveRows()`, que pinta «Guardado ✓»
  en VERDE por su cuenta. Con el cerrojo puesto (D-23) o el almacenamiento lleno, la pantalla dice
  que se guardó mientras el libro NO se guardó. El `schedSave()` posterior lo corrige a rojo ~600 ms
  después. Es exactamente la mentira que el objetivo OBJ-2 de la fase prohibía, en un llamante que
  ninguna prueba ejerce.
- **Cómo se midió:** brazo de radio de impacto de la segunda transición (2026-08-30).
  `grep -n "persistOps(" index.html` da dos llamantes de producción y **cero** en la zona de
  autopruebas. Las pruebas de fallo de escritura ejercen `saveRows` y `guardarTodo` por separado,
  nunca esta secuencia — el CRUCE no lo mide nadie (`CLAUDE.md` §5.5).
- **Estado:** abierta. Severidad menor (se autocorrige), pero matiza **D-23**: su ficha dice que el
  único aviso es un `console.error`; en realidad al editar sí sale el rojo, **precedido de un verde
  mentiroso**. La experiencia no es muda, es contradictoria.
- **Qué la reabre:** nada la cierra sola. Se cierra cuando `persistOps` decida el aviso al final,
  como hace `guardarTodo`, y una autoprueba ejerza el cruce.

### D-28 · La migración del formato antiguo se declara exitosa aunque su escritura falle
- **Qué es:** la Fase 1 cambió el contrato de `saveOpsAll`, que ahora devuelve `false` si no pudo
  escribir. `migrateOpsToGlobal` **ignora ese booleano** y devuelve `migrated: true` igualmente. Si
  la escritura falla, el arranque hace `ops = loadOpsAll()` → `[]` y el `schedSave()` siguiente
  puede sellar un libro vacío —una escritura pequeña sí cabe donde no cabía la grande—. A partir de
  ahí la clave ya no está ausente, la migración devuelve `migrated: false` **para siempre**, y las
  operaciones históricas quedan varadas en las claves antiguas. Es un camino de **una sola
  oportunidad**.
- **Cómo se midió:** brazo de radio de impacto de la segunda transición (2026-08-30), censando los
  llamantes de `saveOpsAll` tras el cambio de contrato. El dato no se destruye —las claves antiguas
  sobreviven— pero sale del libro vivo sin más rastro que la consola. **No reproducido en vivo:**
  exige la cuota agotada justo en la primera apertura tras actualizar.
- **Estado:** abierta. Distinta de **D-21**, que ficha la rama ilegible sin ejercer, no este
  contrato roto.
- **Qué la reabre:** nada la cierra sola. El arreglo es propagar el booleano al resultado; hace
  falta además una autoprueba que falle la escritura y exija `migrated: false`.

### D-29 · La invariante «si el guardado local falló, no se sube» sólo la respeta `guardarTodo`
- **Qué es:** la fase estableció que un guardado local fallido no debe sincronizarse: subir lo que
  hay en memoria machacaría la copia buena de la nube. Esa regla vive **sólo dentro de
  `guardarTodo`**. Seis llamantes de `saveMeta` ignoran su booleano, y uno de ellos
  (`onUseTargetsToggle`) hace `saveMeta(); schedulePush();` seguido: con `saveMeta` fallido, sube
  igualmente. La asimetría ES el defecto (`CLAUDE.md` §5.16).
- **Cómo se midió:** brazos de radio de impacto y de objetivos de la segunda transición
  (2026-08-30). `grep -n "saveMeta()" index.html` da el llamante de `guardarTodo` —que sí lo
  comprueba— y seis que lo ignoran.
- **Estado:** abierta. **No es una regresión**: esos llamantes ya empujaban así antes de la fase.
  Lo que la fase hizo fue crear la invariante y dejarla asimétrica.
- **Qué la reabre:** nada la cierra sola. Se cierra cuando la decisión de subir dependa del
  resultado del guardado en TODOS los caminos, no sólo en uno.

### D-30 · `applySyncPayload` escribe META sin `savedAt`
- **Qué es:** tras aplicar un documento de la nube, `applySyncPayload` reescribe META **sin el
  campo `savedAt`**. La siguiente lectura calcula `localSaved = 0`, con lo que cualquier snapshot
  posterior se considera más nuevo y se vuelve a aplicar. Amplifica **D-01** y **D-24**.
- **Cómo se midió:** brazo de objetivos de la segunda transición (2026-08-30), leyendo el objeto
  que se serializa al final de `applySyncPayload` y comparándolo con el que escribe `saveMeta`,
  que sí lleva `savedAt`. Otra asimetría entre dos escrituras de la misma clave.
- **Estado:** abierta. El ROADMAP ya lo tenía en el alcance de la **Fase 3** («`applySyncPayload`
  debe guardar META con su `savedAt`»); esta ficha lo saca del roadmap y lo pone en la lista viva,
  que es lo que se lee al arrancar.
- **Qué la reabre:** nada; va con la Fase 3.

---

## Abiertas — corrección fiscal

### D-04 · El orden de operaciones del mismo día lo decide el azar
- **Qué es:** el desempate del FIFO es lexicográfico por `id`, y `genOpId` lleva un sufijo
  aleatorio, así que una compra y una venta del mismo día pueden procesarse al revés.
- **Cómo se midió:** lectura del código (`index.html:1015`, `1042`).
- **Estado:** Fase 4, plan 04-01. **Reducida a medias, sin querer, por el ciclo 01-02**
  (`77f8cef`): los identificadores NUEVOS llevan un contador de ancho fijo delante del azar, así
  que entre ellos el desempate ya es el orden de entrada, no el azar. Pero esto NO cierra la deuda:
  (a) los identificadores YA guardados siguen siendo aleatorios y son los del histórico fiscal;
  (b) el orden de entrada tampoco es necesariamente el orden real de las operaciones dentro del
  día. Sigue haciendo falta un criterio explícito, que es lo que hace la Fase 4.
- **Qué la reabre:** nada; está en cola. Debe cerrarse antes de la próxima campaña de la renta.

### D-05 · No existe el tipo de operación «split»
- **Qué es:** un split contable dejaría el FIFO mal para siempre.
- **Cómo se midió:** búsqueda de `split` en `index.html` — cero resultados.
- **Estado:** Fase 4, plan 04-03.
- **Qué la reabre:** que el bróker haga un split antes de que se implemente.

### D-06 · La regla de los dos meses del IRPF no se avisa
- **Qué es:** una pérdida con recompra de valores homogéneos en ±2 meses no es deducible ese año.
  El Excel la declara como pérdida sin marca.
- **Cómo se midió:** lectura de `exportTaxExcel`.
- **Estado:** Fase 4, plan 04-04. **Pendiente de investigar** la redacción exacta de la norma y
  qué cuenta como valor homogéneo.
- **Qué la reabre:** nada; está en cola.

### D-07 · El tipo de cambio puede caer al de hoy
- **Qué es:** si a una operación le falta el cambio congelado, `opFx` usa el spot actual o un
  1,08 fijo. El mismo Excel da cifras distintas según el día que se genere.
- **Cómo se midió:** lectura del código (`index.html:1020`, `2703`).
- **Estado:** Fase 4, plan 04-02.
- **Qué la reabre:** nada; está en cola.

### D-08 · No se sabe si los dividendos del OCR llegan brutos o netos
- **Qué es:** el Excel avisa de revisar la retención, pero nadie ha confirmado qué importe extrae
  realmente `parseRevolutStatement` de un extracto de verdad.
- **Cómo se midió:** no se ha medido. **Requiere una captura real del operador.**
- **Estado:** abierta, bloqueada por falta de dato.
- **Qué la reabre:** que el operador comparta una captura con dividendos.

---

## Abiertas — tamaño del código

### D-09 · Trece funciones por encima del presupuesto de 60 líneas
- **Qué es:** deuda de tamaño declarada y congelada. Sólo pueden encoger; ninguna función nueva
  puede unirse a la lista.
- **Cómo se midió:** `tools/funcsize.py`, re-medido el 2026-08-29 tras el plan 01-01. La cifra de
  funciones vistas vive sólo en `.paul/baseline-funcs.json`, porque copiarla aquí la desactualiza
  al siguiente ciclo — ya pasó dos veces el mismo día. Los trece tamaños de abajo sí se citan porque están congelados:
  si cambiaran, el trinquete se pondría rojo. Exenciones nombradas una a una:

  | Función | Líneas | Motivo de la exención |
  |---|---|---|
  | `exportTaxExcel` | 449 | genera el Excel del IRPF entero; trocearla toca la Fase 4 |
  | `calcRebalance` | 141 | cálculo del rebalanceo; se toca en la Fase 6 |
  | `renderTable` | 132 | pintado principal de activos; se toca en la Fase 5 |
  | `drawBar` | 132 | gráfico de barras en canvas |
  | `parseRevolutTrade` | 117 | parseo de extractos, con muchos casos límite |
  | `renderGlobalPosition` | 110 | cabecera global |
  | `renderOps` | 102 | tabla de operaciones; se toca en la Fase 5 |
  | `parseRevolutStatement` | 96 | parseo de extractos |
  | `renderImportPreview` | 83 | previsualización de importación |
  | `refreshRowDerived` | 80 | recálculo incremental de una fila |
  | `drawPie` | 75 | gráfico de tarta en canvas |
  | `drawGlobalSpark` | 66 | sparkline global |
  | `onScreenshotPicked` | 67 | OCR de capturas de pantalla; se toca en la Fase 5 |

- **Estado:** congelada. El trinquete impide que empeore.
- **Añadida el 2026-08-30 (ciclo 01-04): `onScreenshotPicked`, 67 líneas.** No es código nuevo:
  ya excedía, pero el trinquete **no la veía** porque es una `async function` y su ámbito sólo
  cubría `function NOMBRE(`. El ciclo 01-04 amplió el ámbito (semántica versión 1 → 2, es un
  APRIETE de la vara) y apareció. Lo destapó el banco de sabotaje, no el razonamiento: al volver
  `runSelfTests` asíncrona, el mutante «el monolito engorda» dejó de morder porque la función
  había salido de la medida. **Sellarla sin nombrarla aquí habría sido aflojar en silencio**, y lo
  cazó el brazo adversario de cableado del propio ciclo.
- **Qué la reabre:** tocar cualquiera de esas funciones en su fase correspondiente — es la
  ocasión de bajarla del listado. Y si aparece una decimocuarta, el trinquete se pone rojo.

### D-26 · `funciones_vistas` es una cifra sellada que nadie vuelve a derivar
- **Qué es:** `tools/funcsize.py` **escribe** `funciones_vistas` en la foto al hacer `--update` y
  no la lee nunca; `--check` la ignora por completo. Es una cifra en un fichero que parece medida
  y no vigila nada. Es la misma trampa que `CLAUDE.md` §9 describe para los recuentos copiados a
  mano en un documento: se desfasan y luego se citan como si fueran ciertos.
- **Cómo se midió:** revisión ligera del diff del 01-03 (2026-08-30). En la revisión `bbb0e9c` la
  foto decía **153** cuando `index.html` tenía **162** funciones de primer nivel, **y la puerta
  estaba verde**. El resellado de este ciclo la deja en 168, que hoy sí casa; nada impide que se
  vuelva a desfasar.
- **Estado:** ABIERTA. No se toca en el 01-03: cambiar qué compara `--check` es cambiar la regla de
  medida, y eso el propio instrumento lo declara **deriva (rc=3)**. Hacerlo dentro de un ciclo que
  va de otra cosa sería mover la vara sin plan. Ligada a **D-10** y **D-14**, que son las otras
  cegueras declaradas del mismo instrumento.
- **Medición nueva, 2026-08-31 (ciclo 01-05):** la foto sella **186** y el código tiene **190**.
  Ya se ha vuelto a desfasar, como decía la ficha, **y la puerta sigue verde**. Se derivó de
  rebote al comprobar el remedio del mensaje de foto corrupta: borrar la foto y resellar produce
  un fichero que difiere del original **exactamente en esa cifra**. No se resella: el 01-05 tiene
  esto en sus límites de alcance por escrito, y resellar aquí escondería la munición de D-26.
- **Qué la reabre:** nada la cierra sola. Se cierra cuando `--check` compare la cifra —y entonces
  hace falta su sabotaje: desfasarla a mano tiene que poner la puerta roja.

### D-10 · El trinquete de tamaño no ve funciones flecha
- **Qué es:** `funcsize.py` sólo ve `function NOMBRE(...)` de primer nivel. Una función de 300
  líneas escrita como `const f = () => {…}` le es invisible.
- **Cómo se midió:** ceguera declarada a propósito en la cabecera del propio instrumento.
- **Estado:** abierta y **declarada**, no descubierta. Un límite declarado es un límite; uno
  descubierto después es un agujero.
- **Qué la reabre:** que aparezca código nuevo escrito con funciones flecha grandes.

### D-14 · La distinción entre una regex y una división es heurística
- **Qué es:** para contar llaves, `funcsize.py` decide si una barra abre una expresión regular
  mirando el carácter anterior. Es lo que hace cualquier tokenizador sin gramática completa, y
  puede equivocarse con construcciones raras.
- **Cómo se midió:** la revisión de falsos verdes del 2026-08-29 construyó el caso `throw /}/;`
  —JavaScript válido— y demostró que el instrumento medía una función de 85 líneas como si
  tuviera 2, **en silencio y sin dar rc=2**. Se añadieron `throw`, `yield` y `await` a la lista, y
  hay un sabotaje permanente que mete esa función y exige que el instrumento la vea.
- **Estado:** el caso conocido está cerrado; la clase (heurística sin gramática) sigue abierta.
- **Qué la reabre:** cualquier otra palabra clave tras la que una barra abra regex. Si aparece,
  se añade a la lista y se le pone su sabotaje.

---

## Abiertas — limpieza

### D-22 · El instrumento de radio de impacto no ve el producto
- **Qué es:** el brazo G7 de la transición de fase es `code-review-graph`, que construye un grafo
  del código y calcula el alcance de un cambio. **No parsea el JavaScript inline de un `.html`**,
  así que `index.html` —que ES el producto— no entra en su grafo. Corre, tarda, da rc=0 y presenta
  un panel de ahorro de tokens sobre un análisis que no ha mirado el fichero que la fase cambió.
  Es un instrumento que existe y no dispara ningún objetivo: por `CLAUDE.md` §0, no existe.
- **Cómo se midió:** transición de la Fase 1, 2026-08-30. Tras `code-review-graph build`, el grafo
  tiene 49 nodos repartidos en 10 ficheros y **ninguno es `index.html`** (consultado directamente
  contra `.code-review-graph/graph.db`, agrupando por `file_path`). `detect-changes --base 69f728e`
  reporta «25 funciones cambiadas» y «Untested: roto, main, noop, el, k», que son nombres de
  `tools/` y `sync.py`, no del producto. Es la misma ceguera que ya tenía `smart_search`.
- **Estado:** abierto. G7 queda declarado **DEGRADADO** y sustituido, en esta transición, por un
  análisis de radio de impacto hecho con grep dirigido por un revisor adversario; ese sustituto
  encontró seis huecos de cobertura reales, así que el brazo no se saltó, se reemplazó.
- **Qué la reabre:** nada la cierra por sí sola. Se cierra cuando el grafo indexe el `<script>` de
  `index.html`, o cuando el sustituto por grep se convierta en un script del repo cableado a la
  puerta —que es lo que exige `CLAUDE.md` §4.1 si el juicio se repite por tercera vez.

### D-32 · Las copias de rescate del libro no tienen tope ni caducidad
- **Qué es:** `rescatarOpsIlegible` guarda el blob ilegible en una clave `balance-ops-rescate-<marca
  de tiempo>` para no perderlo. Deduplica por contenido exacto, pero nada limita cuántas copias se
  acumulan si el contenido cambia cada vez (corrupción parcial repetida). Es un riesgo de agotar la
  cuota del navegador, que a su vez es la causa de varios de los fallos de guardado que esta misma
  fase intenta hacer visibles.
- **Cómo se midió:** brazo de seguridad de la segunda transición de la Fase 1 (2026-08-30).
  Severidad BAJA: el dato que se guarda es el que ya estaba en local, no dato externo, y no hay vía
  de explotación por un tercero.
- **Estado:** abierta. Es deuda de limpieza, no de pérdida de datos: la red de rescate existe
  precisamente para no perder nada.
- **Qué la reabre:** nada; se cierra cuando el rescate conserve las N últimas copias en vez de
  todas. Va bien con la copia rotativa de la **Fase 2**, que ya tiene que resolver ese mismo
  problema.

### D-11 · `worker.js` es un proxy obsoleto
- **Qué es:** proxy de precios de Yahoo, sin uso desde que se quitó la obtención automática de
  precios.
- **Cómo se midió:** confirmado en la auditoría del 2026-08-29.
- **Estado:** Fase 6, plan 06-04. Incluye borrar también el Worker en el panel de Cloudflare.
- **Qué la reabre:** nada; está en cola.

---

## Cerradas en la CUARTA transición (2026-09-01)

### D-15 · La guarda de subida está comprobada por presencia, no por precedencia — CERRADA 2026-09-01
- **Qué era:** la guarda que impide subir un libro vacío se comprobaba sólo por PRESENCIA: los
  sabotajes demostraban que `schedulePush` **llamaba** al juez, no que su veredicto se respetara ni
  que corriera ANTES del `set()`. Medido en el 01-02: `if (false && vaciariaElLibro(...))` dejaba
  la puerta verde.
- **Cómo se cerró:** el ciclo **01-04** reescribió la zona entera —una sola puerta de subida,
  `subirALaNube`, gobernada por el juez puro `decidirSubida`— y cerró la deuda **sin que nadie lo
  anotara**. La cuarta transición (2026-09-01) lo re-midió en vez de heredarlo, sobre copia
  aislada y con el ancla afirmada única antes de mutar:
  `if (!decision.subir)` → `if (false && !decision.subir)` en `subirALaNube` da
  **`rc=1`, «FALLO autopruebas (runSelfTests)», «HALLAZGOS (rc=1)»**.
  Ignorar el veredicto del juez MUERDE. Presencia **y** precedencia están ejercidas.
- **Estado:** **CERRADA**. La ficha se cierra citando la medición de hoy, no el acta del 01-04:
  una medición commiteada no se hereda (`CLAUDE.md` §7).
- **Qué la reabre:** que el camino de subida vuelva a tener más de una salida, o que la Fase 3
  reescriba la zona sin traerse su arnés.

---

## Cerradas en el ciclo 01-06 (2026-08-31)

### D-38 · La capa de AVISO no tiene oráculo: nueve mutantes sobreviven a la puerta entera
- **Qué es:** el aparato de medición cubre el MECANISMO de las guardas pero no su AVISO. Sustituir
  en `showSaveIndicator` el color condicional por un verde fijo —o sea, **pintar en VERDE un
  guardado que ha fallado**— deja `tools/verify.sh` en `rc=0` y «VERDE — todo ejercido y en
  verde», con el banco de sabotaje ejecutado y en OK. Otras ocho mutaciones de la misma capa
  sobreviven igual: la duración del aviso de error, el `aviso` que devuelve `decidirSubida` en sus
  ramas de rechazo, y tres mensajes de consola degradables a informativos. Es **§5.6**: el
  mecanismo tiene control, su aviso no.
- **Por qué es invisible hoy:** `tools/dom_stub.js` devuelve `null` en `getElementById`, así que el
  CUERPO de `showSaveIndicator` es código muerto en node; las autopruebas lo sustituyen por un
  espía, o sea que miden que los llamantes pasan `ok=false`, nunca qué hace la función con ese
  `false`. La matriz de 84 filas comprueba `clave` y `subir`, **nunca `aviso`**. Y
  `cloudwrites.py` prohíbe el literal `setSyncUI('ok')`, no un `estadoSync('ok')` alimentado por
  el juez — D-31 cerró el caso literal, no esta clase.
- **Cómo se midió:** TERCERA transición de la Fase 1 (2026-08-31), brazo adversario del oráculo
  sobre una copia aislada; el mutante representativo **re-verificado a mano** por el orquestador:
  `bash tools/verify.sh` → `rc=0`. Control positivo del arnés hecho: invertir `vaciariaElLibro`
  SÍ muere (rc=2), o sea que el estímulo llega y el oráculo muerde cuando puede.
- **Segundo pintor que DECIDE, destapado por la revisión adversaria del PLAN 01-05 (2026-08-31):**
  `setSyncUI` lleva dentro toda la cascada de estados con sus colores. Mutar su rama de error para
  pintar el verde `#27ae60` es literalmente «un fallo de sincronización pintado en verde» —el daño
  que da nombre al ciclo— y **hoy no lo mide nada**: la matriz comprueba el `aviso` que DEVUELVE el
  juez, no lo que el pintor HACE con él, y `cloudwrites.py` sólo prohíbe el literal
  `setSyncUI('ok')`. El arreglo tiene que cortar por el mismo sitio en los DOS pintores.
- **La duración no vive en el elemento:** vive en el `setTimeout` del aviso. Un espía que registre
  lo escrito en el elemento **no puede leerla**, así que ese mutante exige un reloj falso (§5.12),
  no un espía de pantalla.
- **Estado:** **CERRADA** en el ciclo **01-06** (2026-08-31), por la CLASE y no por los casos.
  Lo que la cierra, cada pieza con su mutante en `tools/sabotage.py`:
  - **Los dos pintores se EJECUTAN de verdad** sobre un DOM observable con reloj falso, dentro de
    una ventana que se retira en un `finally` idempotente. Ya no se les sustituye por espías, que
    era el agujero. Se afirma el color **por su valor**, la **visibilidad** y la **duración**.
  - **El `aviso` del juez de subida** entra en las 84 filas de la matriz, con oráculo escrito
    aparte: ninguna rama de rechazo puede devolver el aviso de éxito.
  - **`tools/avisos.py`**, cableado a la puerta, con dos redes disjuntas: por RECEPTOR (nadie toca
    los elementos del aviso fuera de los pintores) y por CANAL (los **34** avisos al operador
    sellados con su nivel y su prefijo literal, cada uno con su motivo escrito).
- **Lo que costó cerrarla de verdad:** el ciclo se dio por hecho una vez y **los tres brazos
  adversarios lo demolieron**, cada uno viendo algo que los otros dos no. El peor hallazgo:
  los asertos exigían que los colores de éxito y de fallo fueran **DISTINTOS**, nunca **CUÁLES**,
  así que **intercambiarlos —el fallo pintado en VERDE— salía `rc=0` y «✅ Autopruebas OK»**. Es
  literalmente el daño que nombra esta ficha, vivo dentro del ciclo escrito para matarlo: mi
  oráculo heredó mi punto ciego (§5.8). Otros tres del mismo grupo: el error de sincronización en
  naranja, un aviso de **2 milisegundos**, y el detector de cesión de control pasando con el
  mecanismo **borrado** (§5.1).
- **Qué la reabre:** que aparezca cualquier aviso al operador sin entrada sellada en
  `.paul/baseline-avisos.json`, o cualquier propiedad del aviso que el operador MIRA —color,
  texto, visibilidad, duración, nivel— sin un mutante que la mate. **No basta con que exista un
  aserto: tiene que haberse visto rojo.**

---

## Cerradas en el ciclo 01-04 (2026-08-30)

### D-33 · Una tercera escritura a la nube esquivaba la guarda de no-vaciado — CERRADA 2026-08-30
- **Qué era:** tres escrituras al documento de Firestore y sólo dos pasaban por el juez. La
  tercera vivía en el manejador de inicio de sesión y se recorría también cuando la lectura de la
  nube **fallaba**, porque su `catch` devolvía `false`, indistinguible de «arriba no hay nada».
- **Cómo se cerró (ciclo 01-04):** se cerró la CLASE, no los tres casos. Ahora existe **una sola
  función con una escritura a la nube** (`subirALaNube`), quien decide es la función pura
  `decidirSubida`, y la nube es un **tri-estado explícito** (`con-datos` / `vacia` / `ilegible`)
  más un cuarto caso (`no-consultada`): la distinción que se perdía al colapsarla en un booleano
  es exactamente la que causaba el daño. El juez **falla CERRADO de forma simétrica**: si para
  decidir hace falta mirar la nube y no se pudo mirar, no se sube — para las operaciones **y**
  para los activos.
- **Qué lo demuestra mañana:** `tools/cloudwrites.py`, cableado como paso de `tools/verify.sh` en
  el mismo commit, con **dos redes disjuntas** (por el receptor y por el método) que se ponen
  rojas si aparece una CUARTA escritura. No es una lista blanca: los enlaces a Firestore se
  DERIVAN del código, y el instrumento da rc=2 si no consigue derivar ninguno. Más los sabotajes
  «aparece una cuarta escritura a la nube fuera de la puerta» y «el manejador de inicio de sesión
  vuelve a escribir por su cuenta» (control positivo literal de esta ficha), y las 84 filas de la
  matriz de `decidirSubida`.

### D-34 · Dos `catch` vacíos en la función que construye lo que se sube — CERRADA 2026-08-30
- **Qué era:** `buildSyncPayload` se tragaba con `catch {}` el fallo de leer una cartera, la
  omitía del paquete, y como `ref.set` **reemplaza el documento entero**, la borraba de la nube.
- **Cómo se cerró (ciclo 01-04):** `buildSyncPayload` devuelve `{ payload, incompleto }` y NOMBRA
  las claves que no pudo leer; la subida se rechaza con ese motivo y el indicador no se pone
  verde. Decisión declarada: un fallo en el histórico bloquea igual que uno en los activos, porque
  el histórico **no es reconstruible** y omitirlo lo borraría de la nube.
- **Qué lo demuestra mañana:** `tools/emptycatch.py`, cableado a la puerta, con foto sellada que
  **nombra uno a uno** los `catch` vacíos tolerados y **cero tolerados en el camino de subida**.
  Cuenta las DOS variantes (`catch (e) {}` y `catch {}`): contar sólo una ERA el defecto. Más tres
  sabotajes: el del censo, el del **eslabón productor** (una clave corrupta sembrada en el
  almacenamiento, que exige que el paquete la nombre) y el del **cable** entre productor y juez.
- **Corrección de una cifra publicada:** el censo del acta anterior decía 6 `catch` vacíos. Con el
  instrumento —que además ignora los que sólo aparecen en comentarios— la cifra real es **5**, y
  vive en `.paul/baseline-catches.json`, no copiada aquí.

### D-31 · El indicador de sincronía se pintaba VERDE después de un error — CERRADA 2026-08-30
- **Qué era:** el `catch` del manejador de inicio de sesión hacía `console.error` y después ponía
  el punto en verde. Era la fábrica de silencio que hacía invisible a D-33.
- **Cómo se cerró (ciclo 01-04): por la CLASE, no por el caso.** La ficha nombraba un `catch`,
  pero había **dos miembros más vivos**: el callback de error del `onSnapshot` era `() => {}` —el
  escucha moría y el punto seguía verde— y el arranque pintaba verde incondicionalmente,
  borrando un naranja o un rojo legítimos. Hoy hay **cero llamadas literales** que pinten verde:
  el verde sólo se alcanza por `estadoSync(resultado)`, un mapa CERRADO donde lo desconocido da
  ROJO. Se añadió el estado `error` al indicador, con mensaje propio: reutilizar el de
  autenticación habría mentido sobre la causa.
- **Qué lo demuestra mañana:** la comprobación del aviso en `tools/cloudwrites.py` (cero verdes
  escritos a mano), y tres sabotajes: «un resultado desconocido vuelve a pintar verde», «el fallo
  del inicio de sesión vuelve a declararse verde» y «el manejador deja de pintar el indicador»
  —este último porque el valor de retorno seguía siendo correcto y nadie miraba si además se
  pintaba: cubrir el mecanismo no cubre su cableado.

---

## Cerradas ANTES de este ciclo

### D-00 · Un número tecleado con coma se multiplicaba por mil — CERRADA 2026-08-29
- **Qué era:** `parseNum` aplicaba una heurística de miles y leía `0,123` como `123`. Afectaba a
  títulos, precios y a la edición de operaciones importadas, o sea al FIFO y al Excel del IRPF.
- **Cómo se midió:** reproducido ejecutando el código real fuera del navegador antes de tocarlo.
- **Cómo se cerró:** revisión `69f728e`. En la entrada de teclado el último separador es el
  decimal; la heurística de miles se quedó sólo en el camino del OCR.
- **Qué la reabriría:** el invariante está en `runSelfTests()` y hay un sabotaje permanente que
  lo verifica. Si `tools/sabotage.py` deja de morder ahí, esta deuda vuelve a estar abierta.

### D-12 · Los identificadores de operación colisionaban dentro de un extracto — CERRADA 2026-08-29
- **Qué era:** `genOpId` mezclaba la marca de tiempo con tres caracteres aleatorios, y un extracto
  entero se importa dentro del mismo milisegundo: sólo 46.656 valores distinguían las operaciones.
- **Cómo se midió:** ejecutando el generador real, 2026-08-29: **10,2 % de los extractos de 100
  operaciones tenía al menos una colisión**. El sufijo aleatorio sí tenía siempre 3 caracteres
  (200.000 muestras); la causa era el problema del cumpleaños, no la longitud.
- **Cómo se cerró:** ciclo 01-02 (`77f8cef`). Un contador monotónico de ancho fijo, detrás de la
  marca de tiempo y delante del azar, hace imposible que dos llamadas coincidan. El ancho es fijo
  porque el identificador es el desempate al ordenar el FIFO.
- **Residuo conocido:** los identificadores ya guardados NO se migran, así que las colisiones
  históricas siguen en disco. Por eso la deduplicación del sync exige identificador **Y** huella:
  una colisión de fábrica no puede comerse una operación legítima.
- **Qué la reabriría:** hay autoprueba (mil ráfagas de 500 identificadores) con su control positivo
  —el generador viejo tiene que seguir colisionando— y un sabotaje permanente. Si `tools/sabotage.py`
  deja de morder en «los identificadores vuelven a poder chocar», esta deuda vuelve a estar abierta.
