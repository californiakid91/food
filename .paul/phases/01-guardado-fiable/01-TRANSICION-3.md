# Fase 1 — TERCERA transición · medición contra el código

**Fecha:** 2026-08-31 · **Revisión medida:** `f9949e8` (HEAD), árbol limpio
**Huella de `index.html`:** `4ff3b0ba79afa7ca1d479ea1525ad51d` — la misma que sirve Pages
**Árbol en exclusiva:** `HEAD^{tree}` = `dbd46d97beca95ea8252276a503df9350e0e1b29`, idéntico antes
y después de toda medición. Ningún proceso concurrente sobre el árbol.

## Veredicto

> ## 🔴 La FASE 1 **NO** cierra. Abre el ciclo **01-05**.

Los tres objetivos del ALCANCE están en el código y verificados. La **META** no: el aparato de
medición **no cubre la capa de aviso**, y la meta de esta fase dice literalmente «**en silencio**».
Un guardado que falla y se pinta VERDE es, para el operador, exactamente el mismo daño que la
fase existe para impedir — y hoy ese cambio pasa la puerta entera sin que nada se ponga rojo.

Es la **tercera vez consecutiva** que medir cambia el resultado: la primera abrió el 01-03, la
segunda destapó D-33 y abrió el 01-04, y ésta abre el 01-05. `PLAN == SUMMARY` habría cerrado la
fase las tres veces.

## Método

G7 (radio de impacto) sigue **DEGRADADO** — `code-review-graph` no ve el JS dentro de un `.html`
(**D-22**). Se sustituyó por **cuatro brazos adversarios disjuntos**, cada uno con **una frase
concreta que demoler** y con prohibición explícita y nominal de mutar el árbol
(`checkout`/`restore`/`stash`/`reset`/`clean`/`commit`/escrituras/`sed -i`); los que necesitaban
mutar trabajaron sobre copias en el scratchpad.

| Brazo | Frase a demoler | Resultado |
|---|---|---|
| A · caminos de pérdida | «no existe camino que empobrezca el libro sin que se vea» | DEMOLIDA (redescubre **D-01**, ya fichada) |
| B · calidad del oráculo | «toda guarda de la meta tiene un mutante que muere» | **DEMOLIDA — 9 supervivientes** |
| C · cableado e instrumentos | «todo control está cableado y ninguno falla en verde» | DEMOLIDA (3 hallazgos) |
| D · documentos contra evidencia | «lo que dicen los documentos sobre el código es cierto» | DEMOLIDA (6 hallazgos) |

**Los cuatro midieron cosas distintas y los cuatro encontraron algo distinto.** Ninguno solo
habría bastado: el de documentos no vio un mutante y el del oráculo no vio una cifra falsa.

## Los tres objetivos del ALCANCE — PASS

| Objetivo | Resultado | Evidencia (medida hoy, no citada) |
|---|---|---|
| Cargar `ops` incondicionalmente al arrancar, fuera del `if` de META | **PASS** | `ops = loadOpsAll()` es la **primera** sentencia de `initPortfolios`, antes del `try` de META |
| Los `catch` vacíos de guardado avisan en la UI en vez de decir «Guardado ✓» | **PASS (mecanismo)** · **FAIL (oráculo)** | las tres funciones devuelven booleano y `guardarTodo` sólo canta victoria si las tres van bien, pinta rojo si no y **se niega a subir**. Pero el pintado en sí no lo mide nadie → hallazgo T3-1 |
| `applySyncPayload` deduplica por `id`, nunca por huella | **PASS** | usa `dedupeOpsById`; el camino del formato antiguo conserva `dedupeOps` a propósito |

## La puerta

`tools/verify.sh` ejecutada fresca al empezar: **rc=0**, ocho pasos, «VERDE — todo ejercido y en
verde», árbol idéntico antes y después.

## Hallazgos

### 🔴 T3-1 · La capa de AVISO no tiene oráculo: nueve mutantes sobreviven a la puerta entera
**Verificado por mí sobre copia aislada.** Sustituir en `showSaveIndicator` el color condicional
por un verde fijo —o sea, **pintar en VERDE un guardado que ha fallado**— deja la puerta en
`rc=0` y «VERDE — todo ejercido y en verde», con el banco de sabotaje ejecutado y en OK.

Por qué no se ve: `tools/dom_stub.js` devuelve `null` en `getElementById`, así que el **cuerpo**
de `showSaveIndicator` es código muerto en node; y las autopruebas lo sustituyen por un espía, o
sea que miden que **los llamantes pasan `ok=false`**, nunca qué hace la función con ese `false`.
Los sabotajes existentes mutan a los llamantes. Es §5.6 en estado puro: **el mecanismo tiene
control, su aviso no**.

Las otras ocho supervivencias reportadas por el brazo B (no re-verificadas una a una por mí, sí
la representativa) caen en tres familias: el color y la duración del aviso local; el `aviso` que
devuelve `decidirSubida` en sus ramas de rechazo (la matriz de 84 filas comprueba `clave` y
`subir`, **nunca `aviso`**, y `cloudwrites.py` sólo prohíbe el literal `setSyncUI('ok')`, no un
`estadoSync('ok')` alimentado por el juez); y tres mensajes de consola degradables a informativos
sin que ningún espía los mire.

### 🔴 T3-2 · Los trinquetes revientan con `rc=1` y traceback en vez de fallar CERRADO
**Verificado por mí.** Con `"excede": null` en la foto (JSON válido, y su propio chequeo de forma
lo acepta porque valida la **clave** pero no el **tipo**), `funcsize.py --check` muere con
`TypeError: 'NoneType' object is not iterable` y **rc=1**. La puerta lo rotula entonces
«FALLO trinquete de tamaño de funciones → HALLAZGOS (rc=1)»: **un instrumento roto sale
clasificado como código que ha engordado**, y manda a mirar el sitio equivocado. Es exactamente
lo que `CLAUDE.md` §4.3 prohíbe. Mismo agujero de clase en `emptycatch.py`.

### 🟠 T3-3 · `VERIFY_INNER=1` deja la puerta en `rc=0` con el banco sin correr
**Verificado por mí.** Imprime «OMITIDO banco de sabotaje» y «VERDE, PERO EL BANCO NO CORRIÓ»,
pero **sale con 0**. El enganche `pre-push` hereda el entorno y sólo bloquea con rc≠0: esa
variable exportada en un perfil deja pasar todos los push con el banco apagado, para siempre.
El veredicto de una puerta es un exit code, no una línea de texto que alguien tiene que leer.

### 🟠 T3-4 · Nada vigila que el enganche `pre-push` exista ni que esté al día
Hoy el instalado es byte a byte el del instalador (comprobado por el brazo C), pero **ningún paso
lo comprueba**. En una máquina nueva la variante automática sencillamente no existe, y nada se
pone rojo. Es la definición del propio proyecto de instrumento no cableado.

### 🟠 T3-5 · La foto del trinquete nació desfasada dentro del commit que la selló
**Verificado por mí.** `.paul/baseline-funcs.json` dice `funciones_vistas: 186`; hoy se derivan
**190** sobre un `index.html` que **no ha cambiado ni una línea** desde el sellado
(`git diff 21e1edb..HEAD -- index.html` vacío). `--check` sale verde porque esa cifra no se
compara — que es **D-26**, correctamente abierta. Pero desmiente la línea de la cabecera de
`DEUDAS.md` que promete que las cifras de instrumento «las vuelve a derivar un script».

### 🟠 T3-6 · Cifras y estado desfasados en los documentos
**Verificado por mí:**
- «**15 sabotajes de este ciclo**» (en `01-04-SUMMARY.md`, `STATE.md` y `ROADMAP.md`) **son 14**:
  el banco tenía 30 en `96c7a3e` y tiene 44 hoy, y sólo `21e1edb` lo tocó. El total (44) sí es
  correcto. El «15» no se re-derivó de nada — es la trampa de §9 con el acta declarando lo
  contrario.
- `PROJECT.md` sigue afirmando «los tres primeros están desplegados y verificados en el navegador
  real; **el 01-04 no**» — **falso desde ayer**. §6 exige actualizar el estado en TODOS los
  sitios; se actualizó en `STATE.md` y no aquí.
- `ROADMAP.md` se contradice dentro de su propio fichero: la tabla dice «3 ciclos cerrados» y el
  detalle, sesenta líneas más abajo, dice cuatro. **Reincidente**: la transición anterior ya
  corrigió este mismo defecto en esta misma tabla.

### 🟡 T3-7 · Dos fichas describen mecanismos que ya no existen
`D-15` sitúa la guarda «dentro de `schedulePush`» y afirma que cerrarla exige «un doble de
Firestore y autopruebas asíncronas, que hoy no existen»: las tres cosas son falsas hoy —el 01-04
trajo el doble y las autopruebas asíncronas—, y su propio disparador de reapertura se cumplió sin
que nadie la revisara. `D-03` describe el fallo de `set()` «con el indicador de sync en verde»,
cuando el 01-04 cerró justo esa mitad. Ninguna se cierra a ciegas: se **re-miden y se reescriben**.

### ⚪ Lo que el brazo A encontró y NO abre ciclo: es D-01, y es Fase 3
Un dispositivo rezagado con 2 operaciones puede pisar una nube de 500 y, por rebote, el libro
local del otro dispositivo, sin un solo aviso: la guarda `vaciariaElLibro` protege del **vacío**,
no del **truncamiento**. Es real y es grave, pero **ya está fichado como D-01** y es literalmente
la meta declarada de la **Fase 3** («que abrir la app en otro dispositivo no pueda borrar
operaciones importadas en el primero»). La meta de la Fase 1 habla de fallos de **guardado y
arranque**. Se anota su agravante —`applySyncPayload` escribe META **sin `savedAt`** (D-30), lo
que pone el reloj a cero y hace aceptable cualquier documento por viejo que sea— y se deja donde
le toca. Meterlo aquí sería mover la vara de la fase a mitad de partido.

## Lo que resistió — para que esto no sea un panel que refuta todo

- El **núcleo** de las seis guardas muerde: invertir `vaciariaElLibro`, quitar la carga
  incondicional de `ops`, quitar `opsIlegible = true`, hacer que `saveOpsAll` devuelva `true` o
  escriba con el cerrojo puesto — todos mueren con control positivo. El estímulo llega.
- Fallo cerrado real donde se comprobó: `node` ausente, foto ausente, JSON corrupto y patrón que
  no casa dan **rc=2 con mensaje propio**, provocados uno a uno.
- `--check` **no escribe**: garantizado por hash dentro del banco, no por confianza.
- El trinquete distingue apretar de aflojar, se niega a sellar un empeoramiento sin amnistía, y
  ante deriva de semántica da rc=3 sin ofrecer el comando de resellado.
- Los cierres de **D-33, D-34 y D-31** aguantan: exactamente una escritura a Firestore dentro de
  `subirALaNube`, cero `setSyncUI('ok')` literales, cinco `catch` vacíos y ninguno en el camino de
  subida, los dos instrumentos cableados como pasos 5 y 6, y la matriz recorriendo 84 filas.
- La única tubería del repo captura el rc antes de entubar.

## Qué abre el ciclo 01-05

**Objetivo:** que la capa de AVISO deje de ser el punto ciego del aparato de medición, y que los
instrumentos no puedan romperse y salir clasificados como hallazgo de código.

1. Dar oráculo al **cuerpo** de `showSaveIndicator` y al `aviso` de `decidirSubida` — hoy sólo se
   miden sus llamantes y su `clave`. Cerrar la **clase**, no los nueve casos.
2. `funcsize.py` y `emptycatch.py`: validar **tipo** además de clave, y envolver la comparación
   para que un instrumento roto salga **rc=2 con nombre**, nunca rc=1.
3. `VERIFY_INNER=1` con todo verde debe salir con **rc≠0**, o el enganche debe limpiarlo del
   entorno.
4. Un paso que compruebe que el enganche `pre-push` existe y coincide con su instalador.

**Fuera de alcance del 01-05:** el truncamiento por sync (D-01/D-30, Fase 3), el resellado de
`funciones_vistas` (D-26), y el rediseño de lo que compara `--check`.

## Correcciones aplicadas en este mismo commit

«15 sabotajes» → **14** donde estaba citado; `PROJECT.md` puesto al día con el despliegue y la
verificación en navegador del 01-04; la fila de la tabla de `ROADMAP.md` corregida a cuatro ciclos.
Las fichas D-15 y D-03 se marcan **A RE-MEDIR**, no se cierran.
