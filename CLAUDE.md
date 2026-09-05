# Normas de trabajo — food

> Adaptación al proyecto `food` de la doctrina de proceso y verificación traída de otro
> proyecto el 2026-08-29. Son normas de PROCESO. Donde el original decía «la puerta», «el
> instrumento» o «el criterio de parada», aquí ya está sustituido por lo que existe de verdad
> en este repositorio.
>
> **Todas estas reglas nacieron de un fallo real y medido.** No son teoría. Cada una evitó, o
> habría evitado, que algo se diera por bueno sin serlo.

**Qué es este proyecto:** una PWA personal de carteras de inversión, un único `index.html`
servido desde GitHub Pages, sincronizado con Firestore. De sus datos sale la declaración de la
renta. Contexto completo en `.paul/PROJECT.md`.

---

## 0. La regla madre

> **Nada se marca como hecho sin validación. Se prueba, y se enseña la prueba.**

Corolarios que se aplican sin excepción:

- **El silencio nunca es «limpio».** Un pase que no pudo ejecutarse AVISA (`DEGRADADO`). Si no
  avisó y no aplicaba, calla. Lo que no puede hacer es parecer verde.
- **Un pase que no se ejecuta no avisa de nada.** Un instrumento que existe pero que no dispara
  ningún objetivo **no existe**.
- **Confianza no es evidencia.** «Debería funcionar» no es un resultado; ejecutar y leer la
  salida, sí.

---

## 1. El loop: PLAN → APPLY → UNIFY

**Obligatorio y en ese orden. Nunca se salta UNIFY.**

| Fase | Qué es | Salida |
|---|---|---|
| **PLAN** | Se escribe qué se va a hacer, con criterios de aceptación verificables | `.paul/phases/NN-nombre/NN-PP-PLAN.md` |
| **APPLY** | Se ejecuta tarea a tarea, con verificación por tarea | código + evidencia |
| **UNIFY** | Se reconcilia lo planeado contra lo real y se cierra | `NN-PP-SUMMARY.md` + estado actualizado |

**Reglas del loop:**

- Se arranca directo en `/paul:plan`. No hay fase de discusión previa por defecto.
- **Parar tras cada UNIFY.** No encadenar ciclos en la misma sesión: escribir el handoff y
  limpiar contexto.
- Un ciclo sin `SUMMARY` es un ciclo que no ocurrió.
- **El cierre de un CICLO nunca autoriza el cierre de una FASE.** Ver §7.

---

## 2. PLAN — cómo se escribe

Un PLAN sin criterios verificables es una intención, no un plan.

### Estructura mínima

1. **Objetivo**: qué se cierra y por qué AHORA (qué está bloqueado mientras no se haga).
2. **Criterios de aceptación (AC)** en formato Given/When/Then. Cada uno debe poder
   contestarse con un artefacto, no con una opinión.
3. **Tareas** con acción, comando de verificación y criterio de hecho.
4. **Boundaries — DO NOT CHANGE**: ficheros o invariantes intocables, con su motivo.
5. **Scope limits — lo que este ciclo NO hace**, enumerado. Evita que el alcance crezca solo.

### Normas de planificación

- **Revisión adversaria de todo PLAN, siempre.** Un modelo distinto del que escribió el plan lo
  ataca antes de ejecutarlo. Aquí: el plan lo escribe Opus, lo ataca Fable.
- **Diseño abierto** (hay varias soluciones plausibles y ninguna obvia) ⇒ **debate estructurado
  con dos posturas opuestas, mínimo 2 rondas, ANTES de fijar el enfoque** (`/dialectic`).
  No lo decide un solo modelo en solitario.
- **Los dos brazos de revisión miden cosas DISJUNTAS.** Medido: un brazo de datos sobre un plan
  dio 0 falsedades, y un brazo adversario sobre ESE MISMO plan encontró 4 agujeros, 2 graves.
  Un solo brazo lo habría aprobado.
- **Da la FRASE a demoler, no «el código a revisar».** Un revisor al que se le pide «refuta esta
  afirmación concreta» encuentra cosas que uno genérico no.
- **Un panel que refuta TODO sesga hacia el falso negativo.** Pide veredictos, no destrucción.
- **Dos revisores CIEGOS que coinciden NO se corroboran**: si comparten el mismo punto de
  partida, comparten el mismo punto ciego.

---

## 3. APPLY — el bucle Ejecutar/Cualificar

Por cada tarea, en este orden:

### 3.1 EJECUTAR

Localizar el sitio exacto antes de editar (búsqueda estructural, no leer ficheros enteros).
Si la tarea llama a una librería externa, **confirmar la API vigente antes de escribir la
llamada**, no de memoria.

> Nota local: `smart_search` NO indexa el JS inline de `index.html` (devuelve 0 símbolos).
> Aquí la búsqueda estructural es `grep` dirigido sobre el fichero. No es una excusa para
> leerlo entero.

### 3.2 REPORTAR ESTADO — honestamente

| Estado | Cuándo | Qué pasa |
|---|---|---|
| **DONE** | completo, sin dudas | cualificación estándar |
| **DONE_WITH_CONCERNS** | completo, pero con dudas concretas | la cualificación ataca primero esas dudas |
| **NEEDS_CONTEXT** | falta información que no está en el plan | se para y se pregunta |
| **BLOCKED** | impedimento estructural | se para, se dice qué se intentó y qué desbloquea |

> **Nunca producir en silencio trabajo del que dudas.** Fingir seguridad produce trabajo que
> falla en la verificación o, peor, en producción.

### 3.3 CUALIFICAR

> **Tu informe sobre tu propio trabajo es optimista por construcción. Fíate de la salida, no de
> tu recuerdo de haberla producido.**

1. **Re-leer el output real.** Abrir los ficheros, no recordarlos.
2. **Ejecutar el comando de verificación FRESCO.** Una verificación rancia no es verificación.
3. **Comparar contra la especificación Y contra el AC**, línea a línea.
4. Puntuar: **PASS** · **GAP** (falta algo) · **DRIFT** (hace algo distinto).
5. Si GAP o DRIFT: arreglar y volver a cualificar. Máximo 3 vueltas; a la cuarta, escalar.

### Frenos mentales

| Si estás pensando… | Para. En su lugar… |
|---|---|
| «ya debería funcionar» | ejecuta `tools/verify.sh` y lee la salida |
| «esto ya lo comprobé» | compruébalo otra vez, fresco |
| «está bastante cerca» | compara contra el AC palabra por palabra |
| «los tests pasan» | compara TAMBIÉN contra la especificación |
| «es una desviación menor» | escríbela; las menores se acumulan en deriva |

### 3.4 Revisión del diff — BLOQUEANTE

Antes de cerrar APPLY, **revisión del diff del ciclo, siempre, con señal de salida inequívoca**.
Nunca una revisión que pueda fallar en silencio: confirma que completó, o decláralo DEGRADADO.

- Correctness ⇒ se arregla ahora.
- Limpieza ⇒ se aplica si es barata, o se difiere **por escrito** con su motivo, en el libro de
  deudas.
- **Prohibido pasar a UNIFY con un hallazgo de correctness sin atender**: eso lo blanquea como
  «hecho».
- **Los brazos de revisión LEEN. Prohíbeles mutar EXPLÍCITAMENTE Y POR NOMBRE en el prompt**
  (nada de `checkout`/`restore`/`stash`/`reset`/escrituras). Medido: un revisor destruyó
  cableado sin commitear e invalidó cifras ya comunicadas.
- **Aquí MEDIR MUTA: prohibir «no edites» NO basta.** `tools/sabotage.py` —y por tanto
  `tools/verify.sh`, que lo incluye— reescribe `index.html` en vivo para demostrar que los
  controles muerden. Medido en la cuarta transición: un brazo que sólo quería **re-derivar una
  cifra publicada** corrió el banco sobre el árbol real, lo dejó mutado mientras otro brazo medía,
  y al detenerlo murió a mitad de un sabotaje dejando el fichero sucio. **No desobedeció ni una
  palabra de su prohibición.**
  👉 Regla: **todo brazo trabaja sobre una COPIA; sobre el árbol real sólo LEE.** La prohibición se
  escribe por lo que el brazo EJECUTA, no sólo por lo que edita. Y se le exige comparar la huella
  del original al empezar y al terminar: ese control es el que lo destapó.
- **Y la copia tampoco basta: el DIRECTORIO DE TRABAJO también se escribe.** Medido en la quinta
  transición: los cinco brazos trabajaron sobre copia y `index.html` no se tocó, pero un proceso
  lanzado en segundo plano arrancó con el directorio reseteado al repositorio real y dejó dos
  ficheros suyos dentro. **Nadie desobedeció.**
  👉 Regla: todo script de un brazo **fija su directorio de trabajo de forma absoluta y lo afirma
  antes de escribir nada**. Y el control que lo destapó vuelve a ser el mismo: comparar el estado
  del árbol al empezar y al terminar.
- **Un brazo puede reportar VIVO un mutante que muere.** Medido en la quinta transición: uno de los
  hallazgos principales resultó falso al re-verificarlo, y la distinción que quedaba en pie era
  otra —el defecto estaba en lo que se PINTA, no en lo que se DEVUELVE—. Aceptarlo sin medir habría
  fichado un defecto inexistente y descrito mal el real.
  👉 Regla: **todo hallazgo decisivo se re-verifica a mano antes de ficharlo**, con la unicidad del
  ancla afirmada. Si el ancla no es única, el defecto es del banco (§5.4), no del código.
- Brazos **disjuntos**, uno por dimensión: correctness · falsos verdes · calidad del oráculo ·
  cableado · documentos-contra-evidencia.

> Dato real: en un ciclo, esta revisión encontró **5 defectos reales sobre un diff que ya tenía
> 20 sabotajes superados, 21 tests verdes y la puerta en verde**. Los 5 estaban en código recién
> escrito, y los 2 peores eran **huecos del propio aparato de medición**.

---

## 4. La doctrina de verificación

### 4.1 Todo instrumento nace CABLEADO

- **Todo script nace conectado a un objetivo ejecutable en el MISMO commit.** Un script huérfano
  es un script que nadie ejecuta.
- **Toda comprobación cara nace incremental.**
- Si el modelo repite el mismo juicio por tercera vez, **falta un script**. El trabajo a la
  máquina, no al modelo.
- **El veredicto de toda puerta es un exit code**, no una opinión.

### 4.2 La puerta

**Aquí la puerta es `tools/verify.sh`.** Es el único objetivo agregado que ejerce todo:

1. `index.html` presente y no vacío
2. sintaxis del `<script>` inline (`tools/check_syntax.py`)
3. autopruebas del propio código, ejecutadas de verdad en node (`tools/run_selftests.py`)
4. trinquete de tamaño de funciones (`tools/funcsize.py --check`)
5. puerta única de escritura a la nube (`tools/cloudwrites.py`)
6. censo de `catch` vacíos (`tools/emptycatch.py`)
7. capa de aviso: censo y receptores (`tools/avisos.py`)
8. sumideros del daño —subir y anunciar— (`tools/sumideros.py`)
9. banco de sabotaje: demuestra que los anteriores muerden (`tools/sabotage.py`)
10. enganche `pre-push` instalado y al día (`tools/hookcheck.py`)
11. higiene de `tools/` (ruff)

> **Esta lista se desactualizó sola.** Decía seis pasos cuando la puerta ejercía once, y lo
> descubrió la quinta transición. Es la trampa de §9 aplicada a un documento: una lista copiada a
> mano envejece al siguiente commit. **Lo que manda es la salida de `verify.sh`**; si esta lista y
> ella no coinciden, la equivocada es ésta.

Reglas:

- Correr «las autopruebas» **no es la puerta**. La puerta es `tools/verify.sh`.
- Las comprobaciones caras viven en **UNA sola lista compartida** — la de `verify.sh` — para que
  la variante automática no pueda ejercer menos que la manual. Dos listas se desincronizan a la
  primera.
- La variante automática es el enganche `pre-push`, que se instala con `tools/install-hooks.sh`
  y **llama al mismo `verify.sh`**. Los hooks no viajan en el repo: en una máquina nueva hay que
  volver a instalarlo.
- **Verifica AMBAS variantes.** Medido en otro proyecto: mover una diana dejó la automática sin
  ella mientras la manual seguía verde, y los tres vigilantes del ciclo seguían verdes porque
  todos miraban la manual.
- La salida degradada debe ser **RUIDOSA**: el resumen dice DEGRADADO, nunca ✅.
- Las comprobaciones nuevas van **FUERA** de cualquier interruptor de degradado.

### 4.3 Exit codes NOMINALES

> **«rc≠0» no vale como criterio.** Un traceback sin capturar también da rc≠0, así que un control
> que sólo mire el rc pasa **con y sin** el manejo de errores. Se exige el MENSAJE, no sólo el rc.

| rc | Significado |
|---|---|
| 0 | verde |
| 1 | hallazgo real (regresión / trinquete flojo) |
| 2 | **instrumento roto**: no pudo medir |
| 3 | **deriva**: cambió la regla de medida, la foto ya no es comparable |

**Fallar CERRADO**: fichero que no parsea, que no decodifica, que falta, `node` ausente ⇒ **rc=2
con nombre**, jamás «0 hallazgos». Cero hallazgos y «no pude medir» son cosas distintas y no
pueden compartir salida.

**El orden del veredicto es una decisión.** Medido aquí el 2026-08-29: con un invariante roto, la
puerta devolvía rc=2 («instrumento roto») porque el banco de sabotaje no podía medir con la
puerta ya roja. El aviso tapaba el hallazgo real y mandaba a mirar las herramientas en vez del
código. Arreglado: si algo anterior está rojo, el banco se **omite ruidosamente** y gana el
mensaje del hallazgo. Hay un test permanente que lo vuelve a demostrar.

### 4.4 Trinquetes (baselines) — cómo se hacen bien

**Aquí el trinquete es `tools/funcsize.py` contra `.paul/baseline-funcs.json`.**

- **`--check` NUNCA escribe.** Comprobado con un hash en el banco de sabotaje.
- **`--update` distingue APRETAR de AFLOJAR.** Se niega a sellar un empeoramiento sin `--amnesty`,
  y lo enumera uno por uno. **Apretar cuesta un comando; aflojar cuesta decirlo en voz alta y
  queda en el diff.**
- **La foto sella la SEMÁNTICA, no sólo las cifras** (umbral, ámbito, métrica, versión). Si la
  regla de medida cambia ⇒ **rc=3**, con mensaje propio y **sin imprimir el comando de
  re-sellado**. Sin esto: aflojas la vara, desaparecen hallazgos, el trinquete lo canta como
  «mejora», te ofrece sellar, y **queda verde para siempre**.
- **La huella es un MULTICONJUNTO**, no un conteo ni un conjunto. Un conteo total es un control
  de paridad: arreglar uno aquí y romper otro allá deja el mismo número y sale verde.
- **Sin número de línea en la huella**: reordenar el fichero movería todo y el instrumento sería
  inservible.
- **Si la métrica es parte de la clave, compara por DOMINACIÓN, no por igualdad.** Con igualdad,
  cada mejora se clasifica como «regresión» y la amnistía se vuelve rutina — que es
  `--no-verify` con otro nombre.
- **Ante un delta mixto gana el mensaje de EMPEORAMIENTO.** Si gana el de «mejora», el
  instrumento imprime el comando de sellado, el operador obedece, y **el empeoramiento queda
  amnistiado dentro**. Los dos casos dan rc≠0, así que ningún sabotaje que mire sólo el rc lo
  caza: **el defecto vive en el MENSAJE, que es lo que dirige la mano**.
- **Declara las cegueras en la cabecera del instrumento.** Las de `funcsize.py` están escritas
  ahí: no ve funciones flecha, ni métodos de objeto, ni closures anidadas.

### 4.5 Sabotaje: la única prueba de que un control muerde

**Aquí el banco es `tools/sabotage.py`**, cableado como paso de la puerta.

Por cada control nuevo:

1. **Sabotéalo y observa el rojo.** Un control que nunca se ha visto rojo no se ha visto.
2. **Transcribe el rc literal y el mensaje**, no «falla correctamente».
3. **Incluye el control de VACUIDAD**: sin sabotaje ⇒ verde. Sin él, un instrumento
   siempre-rojo pasa todos los demás sabotajes.
4. **Aplica y REVIERTE**, con hash del árbol antes y después.
5. **El sabotaje afirma la UNICIDAD DE SU ANCLA antes de mutar.** Si el patrón no casa, el
   defecto está en el banco, y el banco debe decirlo en vez de reportar «no muerde».
6. **Y deja un TEST PERMANENTE.** *Un sabotaje manual de hoy es una anécdota fechada; lo que lo
   vuelve a demostrar mañana es un test.*

---

## 5. Las trampas medidas — el catálogo

> Cada una costó tiempo real. Léelas antes de escribir un control.

### 5.1 Escribir en un comentario que existe un freno NO lo cablea
**Reincidente.** Un comentario que dice «esto lo comprueba el vigilante X» **no comprueba nada**
si el vigilante X no existe. Y cuanto mejor conoces la trampa, **más convincente es el comentario
que sustituye a la comprobación**.
👉 Pregunta obligatoria: **«¿qué artefacto lo vuelve a demostrar mañana?»** Y si el comentario
apunta a un test, **abre el test**.

### 5.2 Un control que se ejecuta DENTRO de lo que mide es incondicional
Si tu control corre dentro de la misma suite que la sonda lanza, toda pasada mutada sale roja
**por el arnés**, y el instrumento certifica sus garantías pase lo que pase.
👉 El control corre **fuera**, como subproceso.

### 5.3 Tu banco puede estar midiendo OTRO árbol y decirlo en verde
Una copia sin su entorno mide otra cosa. Y **la configuración se busca HACIA ARRIBA**: un fichero
de config huérfano en un directorio PADRE secuestra la corrida.
👉 **Control de fidelidad ANTES de medir**: reproduce la foto esperada **clave por clave** y
**aborta** si no casa. El síntoma de este fallo es **una cifra rara, no un error**.

### 5.4 Un meta-instrumento falla INVENTANDO agujeros, no ignorándolos
**Reincidente.** Antes de creerte un «no reacciona», **demuestra que el estímulo LLEGÓ**.
👉 Caso real: un banco reportó «los vigilantes no muerden»; el sabotaje **nunca se había
aplicado** porque el patrón de búsqueda no casó. El defecto estaba en el banco.
👉 Regla: **el sabotaje afirma la unicidad de su ancla antes de mutar**, y se verifica el efecto
por un camino independiente.

### 5.5 Dos condiciones medidas POR SEPARADO no son la matriz medida
Cada guarda tenía su test y su mutante, y **el CRUCE de dos de ellas no lo medía nada**:
reordenarlas rompía el comportamiento y pasaba todos los tests y todos los mutantes.

### 5.6 Cubrir el MECANISMO no cubre su AVISO
Una alarma necesita **su propio mutante**. Si no, el mecanismo tiene control y el log que lo
delata puede degradarse a INFO sin poner nada en rojo.

### 5.7 Antes de creerte un control de mutantes, sabotéalo a ÉL
Dos agujeros reales del instrumento: el runner devolvía un código de «éxito» ante un
identificador de test **inexistente**, y eso contaba como «mutante muerto». Y el hash vigilaba el
**fuente**, no lo que el intérprete **ejecutó**.

### 5.8 Tu propio oráculo hereda tus puntos ciegos
**La reincidencia número uno.** Sólo un adversario **EJECUTANDO** los encuentra. Tres modos:
- **ENUMERAR donde había que DESCUBRIR** — comprobar una lista fija donde había que derivarla del
  artefacto real. *(Por esto `run_selftests.py` carga el `<script>` entero en un DOM de mentira en
  vez de extraer una lista fija de funciones.)*
- **CASAR DE MÁS** — aserciones por subcadena que se satisfacen por accidente. Caso real: buscar
  `\btest\b` casaba con `ops-test`, así que borrar la suite del agregado dejaba el control verde.
- **MUTAR SÓLO DENTRO DE LA RAMA QUE YA MIRAS** — *si todos tus mutantes están dentro del `if`,
  tu oráculo no mide el arreglo: mide su cuerpo.*

### 5.9 Un test escrito PARA un arreglo puede pasar CON y SIN él
Sólo el **control positivo** lo destapa: revierte el arreglo y comprueba que el test **muere**.
👉 **La inyección debe caer donde el error PROPAGA.** Los caminos «best-effort» (colas de avisos,
telemetría) están hechos para tragar errores: un fallo inyectado ahí certifica pase lo que pase.

### 5.10 Detectar ≠ prevenir
La mitigación debe atacar la **categoría del daño**. Un hallazgo cerrado con la categoría
equivocada es **peor que uno abierto**: nadie vuelve a mirarlo.

### 5.11 Un guard rojo puede señalar su PROXY roto, no la invariante
Cuando un control se pone rojo al MOVER código sin romper nada, sospecha del proxy. Pero
acertar eso no basta: extender el control por **vecindad** donde tocaba por **ruta** afloja la
puerta. **Presencia ≠ precedencia.**

### 5.12 Un test de «la firma es estable» sin RELOJ FALSO no mide nada
Dio verde con el sabotaje puesto: las dos pasadas caían en el mismo segundo.

### 5.13 El árbol EN EXCLUSIVA
**Reincidente.** Una sonda en paralelo da alarmas falsas. Nada corriendo a la vez sobre el árbol,
y **hash antes y después de toda medición que comuniques**.

### 5.14 La tubería se come el código de salida
`comando | tail` devuelve el rc del `tail`, no el del comando. Redirige a fichero y captura el rc.
👉 Familia: **`diff` entre dos ficheros inexistentes devuelve éxito**. Cualquier comparación debe
**afirmar primero que sus entradas existen y no están vacías**.

### 5.15 Una LISTA BLANCA sólo protege de lo que ya conoce
Y **el guardián de deriva no puede avisarlo**: compara el conjunto sellado con el actual, así que
caza a quien QUITE una entrada, pero **un conjunto incompleto DE ORIGEN le es invisible**.
👉 Cierra **la clase, no el caso**: deriva la lista del entorno real y exige cobertura total.

### 5.16 Dos predicados sobre el mismo conjunto tienen que ser el MISMO predicado
Caso real: la guarda usaba «existe» y el ámbito usaba «es un fichero». Un directorio con el
nombre del fichero burlaba la guarda entera. **La asimetría ERA el defecto.**

### 5.17 Escribir la lección NO la evita
**Reincidente.** Sólo un **control positivo que se ejecuta** la evita.
👉 Y: *cuando el trabajo mecánico sale limpio, el defecto está en el instrumento que lo mide.*

---

## 6. UNIFY — cerrar el loop

1. Reconciliar AC por AC: **PASS/FAIL con su evidencia**, no con una afirmación.
2. Escribir el `SUMMARY`: qué se construyó, resultados de los AC, salida de la verificación,
   resultado de los brazos de revisión, **desviaciones con su motivo**, decisiones tomadas.
3. Actualizar el estado en **TODOS** los sitios donde vive: `.paul/STATE.md`, `.paul/ROADMAP.md`,
   `.paul/PROJECT.md` y `.paul/paul.json`. No en uno.
4. **Las deudas van al LIBRO DE DEUDAS (`.paul/DEUDAS.md`), no al SUMMARY.** Ver §8.
5. Commitear.

---

## 7. Cierre de FASE — por MEDICIÓN, nunca por conteo

> ### 🔴 `PLAN == SUMMARY` NO ES EL DISPARADOR DE CIERRE.
> Ha disparado en falso 18 veces. Que haya tantas actas como planes no dice nada sobre si el
> trabajo está hecho.

**El disparador es medir los objetivos de la fase CONTRA EL CÓDIGO, antes de preguntar nada.**

- «¿Existe el artefacto que este objetivo debía producir?» → compruébalo con un comando.
- **Medir cambia el resultado.** Caso real: una deuda estaba mal clasificada y tenía un freno
  roto; sólo se vio al medir. Otro: una cifra publicada («17 pendientes») era **16** porque un
  ciclo posterior la había movido.
- **Al transicionar, mide el código — no le creas al libro de deudas NI a una medición ya
  commiteada.** Un «✅ comprobado» puede haber mirado la mitad del mecanismo.
  👉 Antes de heredar una medición, pregunta: **«¿qué eslabón NO miró?»**
- **Enumerar no es reclamar.** Listar lo que hiciste no demuestra que cubra lo que hacía falta.
- **Una sonda verde nunca supera a un intento real.** Aquí: las autopruebas en node no sustituyen
  a abrir la app desplegada. Ver §7 bis.
- **Re-deriva la cifra DESPUÉS del cambio que la afecta, y deja el script en el repo.**
  Reincidente: una cifra medida al planificar ya era otra al terminar el APPLY.

### 7 bis. Lo que la puerta NO puede ver — específico de este proyecto

`verify.sh` ejerce las funciones puras en node sobre un DOM de mentira. **No prueba la interfaz.**
Antes de dar por buena una fase que toque la pantalla, hay que abrir
`https://californiakid91.github.io/food/` y mirarlo, **recargando dos veces** (el service worker
sirve la versión anterior en la primera). Y `?selftest=1` ejecuta los invariantes en el navegador
real, que no es lo mismo que ejecutarlos en node.

---

## 8. El libro de deudas — única fuente de verdad

**Aquí el libro es `.paul/DEUDAS.md`.**

- **Un SUMMARY es un ACTA**: se escribe una vez y se entierra. **Un libro de deudas es una LISTA
  VIVA** que se lee al arrancar cada sesión.
- **Toda deuda diferida en un UNIFY sube al libro en el MISMO commit, con su origen citado.**
- **Si una deuda sólo existe en un SUMMARY, es como si no existiera.**
- Cada ficha: qué es, cómo se midió, estado, y **qué la reabre**.
- Deja constancia de las resoluciones en el estado **sin que te lo pidan**.

---

## 9. Higiene del código

> **Adaptación deliberada.** El original exige que el código nuevo aterrice en módulos hoja y
> nunca engorde un monolito. Aquí **el monolito es el producto**: `index.html` tiene que poder
> servirse tal cual desde Pages, sin build. Así que la regla se sustituye por su equivalente
> medible dentro de un fichero único, con cifras derivadas del código real: mediana 8 líneas,
> p90 39, máximo 449.
>
> **El recuento vigente NO se copia aquí a propósito.** Vive en `.paul/baseline-funcs.json`, que
> se resella con el instrumento. Una cifra copiada a mano en un documento queda desfasada al
> siguiente cambio y luego se cita como si fuera cierta — pasó con esta misma línea el
> 2026-08-29: decía 146 cuando ya eran 151.

- **Presupuesto: ninguna función nueva pasa de 60 líneas.** Es holgado sobre el p90 real (39) y
  lo vigila `tools/funcsize.py`, cableado a la puerta.
- **Las funciones que ya lo exceden son deuda declarada, nombrada una a una** en
  `.paul/baseline-funcs.json` y en `.paul/DEUDAS.md`. Sólo pueden encoger.
- **Toda función pura nueva nace con su invariante en `runSelfTests()`**, en el mismo commit.
  Es lo más parecido a un «módulo hoja» que admite este proyecto: código sin DOM, verificable
  fuera del navegador.
- **Al trocear, el criterio de parada se declara con SUJETO EXPLÍCITO.** *Un criterio de parada
  sin sujeto acaba midiéndose sobre lo que conviene, y nadie lo nota en ocho cortes.*
- Las **exenciones se nombran una a una** (función, tamaño, motivo). Nunca una regla que exima
  categorías enteras: **el instrumento MIDE; quien EXIME es el criterio.** Un instrumento con
  juicio dentro es un instrumento que se dobla.

---

## 10. Ritual de cierre de toda tarea

**Dos pasos, sin que el operador los pida:**

**(A) Commit-checkpoint.** Lo que se pierde sin commit no es el fichero: es **la trazabilidad** —
por qué esas cifras, qué se refutó, qué se aceptó.
> *El commit no es la celebración del final: es el arnés durante el camino.*

**(B) Recomendar limpiar el contexto.** Limpiar es el default.
- **Prohibido ofrecer «¿seguimos?» sobre un contexto grande.**
- La pregunta que decide: **«¿qué necesita el paso siguiente que no esté ya en un fichero?»**
  Si la respuesta no es «nada», el arreglo **no es resumir: es escribirlo y entonces limpiar**.
  Un resumen es lossy y propaga cifras rancias.

---

## 11. Cómo hablar con el operador

- **Cero jerga.** Explicar en lenguaje simple **qué hacemos, por qué y qué conseguimos**.
- **No mostrar código ni diffs en el chat.** Describir el cambio por su **efecto**, no por su
  implementación.
- **Toda la profundidad técnica va a los ficheros** (planes, actas, comentarios del código): ahí
  no se pierde nunca, sólo se saca del chat. **El chat es simple; los ficheros, completos.**
- **Reportar con fidelidad**: si algo falló, decirlo con su salida; si se saltó un paso, decirlo;
  si está hecho y verificado, decirlo sin rodeos.
- **Corregir sin ceremonia**: enmienda lo que cambie una decisión del operador y sigue. Sin
  disculpas largas ni recuento de errores.
- **Preguntar sólo lo que cambia el trabajo.** Las rutinas no se consultan; lo irreversible, sí.
- El operador escribe en español. Todo —chat, planes, actas, comentarios del código— va en
  español.

---

## 12. Checklist de bolsillo

Antes de decir que algo está hecho:

- [ ] ¿Ejecuté `tools/verify.sh` y **leí** la salida, o me fío de mi recuerdo?
- [ ] ¿Este control se ha visto **rojo** alguna vez? ¿Con qué rc y qué mensaje?
- [ ] ¿Pasaría este test **sin** el arreglo? (revierte y compruébalo)
- [ ] ¿Hay algún comentario que **afirme** un control? ¿Existe ese control? Ábrelo.
- [ ] ¿El instrumento puede fallar y salir **verde**? ¿Qué pasa si no puede medir?
- [ ] ¿Estoy midiendo el árbol que creo? ¿El árbol está limpio (`git status`)?
- [ ] Si dije «no reacciona»: ¿demostré que **el estímulo llegó**?
- [ ] ¿Comparé entradas que **existen y no están vacías**?
- [ ] ¿La cifra que voy a publicar es **posterior** al cambio que la afecta?
- [ ] ¿Este script está **cableado** a `verify.sh`?
- [ ] ¿Las deudas están en `.paul/DEUDAS.md`, no sólo en el acta?
- [ ] ¿Estoy cerrando una fase por **conteo de actas** en vez de por medición?
- [ ] Si toqué la pantalla: ¿lo he **abierto en el navegador**, recargando dos veces?
