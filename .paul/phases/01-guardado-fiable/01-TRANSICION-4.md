# Fase 1 — CUARTA transición · medición contra el código

**Fecha:** 2026-09-01 · **Revisión medida:** `571659c` (HEAD), árbol limpio
**Huella de `index.html`:** `66e6dd20e9ec76163a332a06f5ef2598` — la misma que sirve Pages
(comprobado con `curl -s https://californiakid91.github.io/food/ | md5sum`)
**Árbol:** `HEAD^{tree}` = `23c169f1d866e15ff2d56fc10035c731a74bacfe`, idéntico al empezar y al
terminar. **Con una interrupción real de la exclusividad, documentada abajo en «Nota de proceso».**

## Veredicto

> ## 🔴 La FASE 1 **NO** cierra. Abre el ciclo **01-07**.

Los tres objetivos del ALCANCE están en el código y verificados. La **META** no. La meta dice
«ningún fallo de guardado ni de **arranque** puede borrar el libro **en silencio**», y hay un
camino de arranque, reproducido, que **empobrece el libro y deja la pantalla en verde**.

Es la **cuarta vez consecutiva** que medir cambia el resultado: la primera abrió el 01-03, la
segunda destapó D-33 y abrió el 01-04, la tercera abrió el 01-05 y el 01-06, y ésta abre el 01-07.
`PLAN == SUMMARY` habría cerrado la fase las cuatro veces.

## Método

G7 (radio de impacto) sigue **DEGRADADO** — `code-review-graph` no ve el JS dentro de un `.html`
(**D-22**). Se sustituyó por **cuatro brazos adversarios disjuntos**, cada uno con **una frase
concreta que demoler**, con prohibición explícita y nominal de mutar el árbol.

| Brazo | Frase a demoler | Resultado |
|---|---|---|
| A · caminos de pérdida | «ningún fallo de guardado ni de arranque empobrece el libro sin que el operador se entere» | **DEMOLIDA — 1 grave reproducido** |
| B · calidad del oráculo | «toda guarda de la meta tiene un mutante que muere» | **DEMOLIDA — 1 superviviente de 17** |
| C · cableado e instrumentos | «los diez pasos están cableados, ninguno falla en verde, las dos variantes ejercen lo mismo» | **RESISTE** |
| D · documentos contra evidencia | «lo que los documentos afirman sobre el código es cierto y toda cifra se re-deriva» | DEMOLIDA (3 defectos de forma, **cero cifras falsas**) |

**Novedad respecto a las tres transiciones anteriores:** por primera vez un brazo **no demuele su
frase**. El brazo C intentó cinco roturas concretas del aparato de medición y ninguna cedió. Y por
primera vez **ninguna cifra publicada es falsa**: las cuatro que el brazo D re-derivó en fresco
—74 controles del banco, 34 avisos censados, diez pasos de la puerta, y la huella de lo desplegado—
dieron exactamente lo que dicen los documentos. En la tercera transición había tres cifras falsas.

## Los tres objetivos del ALCANCE — PASS

| Objetivo | Resultado | Evidencia (medida hoy, no citada) |
|---|---|---|
| Cargar `ops` incondicionalmente al arrancar, fuera del `if` de META | **PASS** | `ops = loadOpsAll()` es la primera sentencia de `initPortfolios` (`index.html:3388`), antes del `try` de META |
| Los `catch` vacíos de guardado avisan en la UI en vez de decir «Guardado ✓» | **PASS (mecanismo y oráculo)** | `guardarTodo` (`index.html:3348`) sólo canta victoria si las tres escrituras van bien; desde el 01-06 el pintado se **ejecuta** y se lee su color por VALOR. Con una salvedad: ver T4-2 |
| `applySyncPayload` deduplica por `id`, nunca por huella | **PASS** | `dedupeOpsById` en la rama del formato nuevo (`index.html:3010`); la rama del formato antiguo conserva `dedupeOps` a propósito (decisión del 01-03) |

## La puerta

`tools/verify.sh` ejecutada fresca al empezar: **rc=0**, **diez pasos**, «VERDE — todo ejercido y
en verde», árbol idéntico antes y después.

## Hallazgos

### 🔴 T4-1 · Al arrancar, una nube MÁS VIEJA empobrece el libro y la pantalla queda en VERDE
**Reproducido por el brazo A y re-verificado por mí leyendo el código.**

`pullFromFirestore` (`index.html:3095`) decide si aplicar el documento de la nube así:

```
if (!hasRealLocalData() || (data.savedAt || 0) >= localSaved) applySyncPayload(data);
setSyncUI(estadoSync('ok'));
```

`hasRealLocalData()` (`index.html:3073`) mira **sólo los activos** (`rows`) de cada cartera.
**Nunca mira el libro de operaciones.** Así que un operador que lo tenga todo vendido —activos
vacíos, libro fiscal rico, que es justo cuando el libro más importa— cae en `!hasRealLocalData()`,
la comparación de fechas se desactiva, y **cualquier** documento de la nube gana, por viejo que
sea. Dentro, `vaciariaElLibro` sólo bloquea el caso **vacío**: una nube rancia con una operación
sustituye a un libro local de tres. Y `pullFromFirestore` remata pintando el punto de sync en
verde.

Reproducción del brazo A (`node repro_pull.js`, rc=0) sobre copia aislada:

```
ANTES  | ops en memoria: 3 | en disco: 3 | savedAt local: 2000000000000
pull devolvio: true
DESPUES| ops en memoria: 1 | en disco: 1 | nube savedAt: 1000
```

**Por qué es Fase 1 y no Fase 3.** El ROADMAP lista «`hasRealLocalData()` debe mirar `ops`, no
sólo `rows`» dentro del alcance de la Fase 3, y podría alegarse que le toca allí. No:

- El daño es **pérdida de libro en el ARRANQUE, con estado tranquilizador**, que es la meta
  literal de esta fase. D-01 se dejó para la Fase 3 en la transición anterior porque es la
  dirección contraria (subida de un rezagado) y porque exige **fusionar**. Éste no exige fusionar:
  basta que el predicado «¿hay datos locales que proteger?» cuente el libro.
- Es la **misma asimetría que el ciclo 01-04 arregló en el otro lado** (§5.16). El juez de subida,
  `decidirSubida` (`index.html:3134`), ya mira **las dos cosas**: `!tieneOperaciones(...)` **y**
  `!hayActivosLocales`. El camino de bajada se quedó con el predicado viejo, que sólo mira activos.
  **La asimetría entre los dos predicados ES el defecto**, exactamente como en el 01-04.
- Es §5.11 además: un proxy («¿hay algo local?») medido sobre los activos donde el objeto protegido
  por la fase es el libro.

**La puerta no lo ve:** `tools/verify.sh` sobre la copia con el defecto sale **rc=0** y VERDE.
Ninguna autoprueba ejerce el desempate de `pullFromFirestore`; los controles de `hayActivosLocales`
cubren sólo la subida.

Lo que **NO** entra por aquí: fusionar `ops` por `id` en `applySyncPayload` sigue siendo Fase 3.
Aquí se cierra la asimetría del predicado, no la semántica de fusión.

### 🔴 T4-2 · El cruce «sólo falla el guardado de la lista de carteras» no tiene oráculo
**Reproducido por el brazo B y RE-VERIFICADO POR MÍ sobre copia aislada, con unicidad de ancla
afirmada antes de mutar y estímulo demostrado en el fichero.**

Mutación aplicada en `index.html:3352`:

```
- const todoBien = okRows && okOps && okMeta;
+ const todoBien = okRows && okOps;
```

`bash tools/verify.sh` → **`rc=0`**, diez pasos OK, «VERDE — todo ejercido y en verde».

Por qué escapa: las autopruebas SÍ ejercen `guardarTodo` con un fallo parcial
(`pruebasFalloDeEscritura`, `index.html:4886`), pero el fallo parcial que inyectan cae siempre en
`saveOpsAll`, **nunca en `saveMeta` a solas**. Es §5.5 literal: los tres sumandos tienen control por
separado y **el cruce no lo mide nadie**.

Consecuencia real: si `localStorage.setItem(META_KEY, …)` falla —cuota llena—, el operador ve
«Guardado ✓» **en verde**, y además `schedulePush()` sube a la nube. Un fallo de guardado que el
operador no ve: la meta literal de esta fase.

Lo cierra un caso que haga fallar **únicamente** `saveMeta` y exija `guardarTodo() === false` y
aviso en rojo.

### 🟠 T4-3 · El cerrojo del libro ilegible es MUDO en la interfaz durante el arranque
**Reproducido por el brazo A.** Con `balance-ops` corrupto, `loadOpsAll` rescata y pone el cerrojo,
y sólo lo cuenta por `console.error`. Sin sesión, el operador abre la app, ve el libro vacío y el
punto de sync en su estado normal, sin explicación. **Ya está fichado como D-23**; esta transición
lo re-mide y confirma que sigue vivo, y añade el detalle de que en el arranque no se emite **ningún**
aviso de interfaz (lista de avisos vacía durante el arranque, medido).

### 🟡 T4-4 · No hay volcado al cerrar la pestaña: ventana de 600 ms
**Reproducido por el brazo A.** `schedSave()` aplaza el guardado 600 ms, y **no existe ningún
manejador `beforeunload` / `pagehide` / `visibilitychange` en todo `index.html`** (grep: cero
resultados). Cerrar la pestaña dentro de esa ventana pierde la operación que el operador acaba de
ver en pantalla. Se ficha como **D-47**; no abre ciclo por sí solo: es pérdida sin fallo declarado
—el guardado no llegó a intentarse— y su arreglo es independiente del resto.

### 🟡 T4-5 · Tres defectos de FORMA en los documentos (ninguna cifra falsa)
Medidos por el brazo D:
- **D-15** se contradice dentro de su propia ficha: la caja de aviso de la tercera transición dice
  que tres de sus afirmaciones son falsas hoy, y el cuerpo, tres líneas más abajo, las sigue
  afirmando («que hoy no existen»). Se marcó A RE-MEDIR y nunca se re-midió. **Re-medida hoy: ver
  abajo, se CIERRA con evidencia.**
- **D-38** figura como `Estado: CERRADA` pero su ficha vive bajo el epígrafe
  `## Abiertas — riesgo de pérdida de datos`. Leída por sección dice abierta; leída por su campo,
  cerrada.
- **D-09** dice «los doce tamaños de abajo» cuando la tabla tiene **trece** filas desde que entró
  `onScreenshotPicked`.

Los tres se corrigen en este mismo commit.

## Lo que resistió — para que esto no sea un panel que refuta todo

- **El aparato de medición aguantó entero.** El brazo C intentó cinco roturas concretas y ninguna
  cedió: no consiguió que una deriva de semántica imprimiera el comando de resellado (los tres
  trinquetes callan), ni que un delta mixto dirigiera la mano al sellado (gana el empeoramiento),
  ni colar `VERIFY_INNER` por el enganche (la segunda capa lo limpia), ni que un `rc=2` de
  instrumento tapara un hallazgo `rc=1` (el orden del veredicto lo impide), ni encontrar un script
  huérfano o un control que sólo exista en un comentario.
- **Fallo cerrado, reproducido uno a uno:** `index.html` ausente o vacío, `node` ausente, foto con
  un tipo equivocado, foto corrupta, instalador sin su heredoc ⇒ **rc=2 con nombre y con remedio**,
  en los ocho instrumentos.
- **Las dos variantes ejercen lo mismo**: el enganche instalado es byte a byte el del instalador y
  llama al mismo `verify.sh`; con `VERIFY_INNER=1` **exportado**, el enganche corrió la puerta
  entera, banco incluido.
- **16 de 17 mutaciones del brazo B murieron**, incluidas las cuatro que más importan: colores del
  aviso intercambiados, error de sync pintado de verde, carga de `ops` condicional, y `await`
  perdido en la escritura a la nube.
- **Cero cifras falsas** en los documentos, por primera vez en las cuatro transiciones.

## Deudas re-medidas — no heredadas

### D-15 · **SE CIERRA**, con evidencia de hoy
La ficha decía que la guarda de subida está «comprobada por presencia, no por precedencia»: que
poner `if (false && vaciariaElLibro(...))` dejaba la puerta verde. **Re-medido hoy** sobre copia
aislada, con el ancla afirmada única antes de mutar, en el código que dejó el 01-04:

```
- if (!decision.subir) {
+ if (false && !decision.subir) {
```

`bash tools/verify.sh` → **`rc=1`**, «FALLO autopruebas (runSelfTests)», «HALLAZGOS (rc=1)».

Ignorar el veredicto del juez en el camino de subida **muerde**. El ciclo 01-04 cerró esta deuda
al reescribir la zona, y nadie lo anotó. Presencia **y** precedencia están ejercidas. Se cierra
citando esta medición, no el acta del 01-04.

### D-42, D-43, D-44 · siguen siendo cegueras ACOTADAS y declaradas
Medidas por el brazo C: D-42 sigue sin oráculo pero ninguna clave nueva sin validar la reabre;
D-43 sigue sin afirmar unicidad de su ancla, y hoy hay exactamente **un** heredoc en el instalador,
así que la ceguera sigue acotada y fallaría ruidosamente; D-44 conserva sus tres cegueras escritas
en la cabecera de `avisos.py` y en la semántica sellada, y quitar el corte de `runSelfTests` da
deriva `rc=3`, reproducido.

### D-27 y D-29 · siguen vivas, re-medidas hoy
- **D-27**: `persistOps` (`index.html:2208`) sigue llamando a `saveOpsAll(ops)` **ignorando su
  booleano** y luego a `saveRows()`, que pinta «Guardado ✓» en verde por su cuenta. El rojo llega
  ~600 ms después. Verde mentiroso corto, pero verde mentiroso.
- **D-29**: `grep -n "saveMeta()"` da **seis** llamantes que ignoran el booleano, además del de
  `guardarTodo` que sí lo comprueba. Uno de ellos, `onUseTargetsToggle` (`index.html:4197`), hace
  `saveMeta(); schedulePush();` seguido: con META fallido, sube igual.

Las dos son de la **misma familia que T4-2** y por eso van al ciclo 01-07 juntas: la invariante
«si el guardado local falló, ni se anuncia éxito ni se sube» existe en un sitio y no en los demás.

## Nota de proceso — la exclusividad del árbol se rompió, y por qué

**Un brazo de revisión ejecutó `tools/sabotage.py` sobre el repositorio REAL.** El banco muta
`index.html` en vivo para demostrar que los controles muerden, así que el árbol quedó con una
mutación viva mientras otro brazo medía. Al detener a los agentes, el banco murió a mitad de un
sabotaje y **dejó el fichero mutado**.

Detectado por el brazo B, que compara la huella al empezar y al terminar — el control funcionó.
Restaurado con `git checkout -- index.html` y verificado byte a byte contra HEAD
(`66e6dd20e9ec76163a332a06f5ef2598`). **No se perdió nada**: no había trabajo sin commitear. Los
brazos C y D se relanzaron desde cero sobre copias.

**La lección, que es nueva y va a `CLAUDE.md`:** prohibir «no edites el árbol» **no basta**. En
este repositorio **medir muta**: correr la puerta o el banco reescribe `index.html` como parte de
su funcionamiento normal. Un brazo que sólo quería re-derivar una cifra publicada acabó saboteando
el repositorio real sin desobedecer ni una palabra de su prohibición. La regla correcta es que
**todo brazo de revisión trabaja sobre una copia, y sobre el árbol real sólo LEE**.

## Qué abre el ciclo 01-07

**Objetivo:** que la invariante «un fallo de guardado no se anuncia como éxito y no se sincroniza»
valga en **todos** los caminos, y que el arranque no pueda empobrecer el libro por mirar el proxy
equivocado.

1. **T4-1** — cerrar la asimetría del predicado: quien decide si la nube gana al arrancar tiene que
   contar el libro, no sólo los activos. Cerrar la **clase** (un solo juez para las dos
   direcciones), no el caso. Con oráculo que ejerza el desempate de `pullFromFirestore`.
2. **T4-2** — un control que haga fallar **sólo** el guardado de la lista de carteras y exija que
   `guardarTodo` diga que no, avise en rojo y no suba.
3. **D-27 y D-29** — que el anuncio y la decisión de subir dependan del resultado del guardado en
   todos los llamantes, no en uno. Es la misma clase que el punto 2.

**Fuera de alcance del 01-07:** la fusión de `ops` por `id` y el `savedAt` por sección (D-01, D-30,
Fase 3); el aviso en pantalla del cerrojo (D-23) y el volcado al cerrar la pestaña (D-47), que se
fichan y se deciden aparte; y el resellado de `funciones_vistas` (D-26).

## Correcciones aplicadas en este mismo commit

- **D-15 CERRADA** con la medición de hoy transcrita en su ficha.
- **D-38** movida a una sección de cerradas, para que su ubicación deje de contradecir su estado.
- **D-09**: «los doce tamaños» → «los trece tamaños».
- Fichas nuevas: **D-45** (T4-1), **D-46** (T4-2), **D-47** (T4-4).
- `CLAUDE.md` §3.4: la regla nueva sobre los brazos de revisión y el árbol.
