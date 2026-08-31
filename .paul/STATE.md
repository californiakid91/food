# Project State

## Project Reference

See: .paul/PROJECT.md (updated 2026-08-29)

**Core value:** Llevar al día tus carteras con precios manuales y sacar de ahí una declaración de la renta correcta, sin backend propio.
**Current focus:** v0.1 Datos fiables — Fase 1 "Guardado que no miente"

## Current Position

Milestone: v0.1 Datos fiables (v0.1.0)
Phase: 1 of 6 (Guardado que no miente) — **ABIERTA; su TERCERA transición NO la cerró**
Planes: 01-01, 01-02, 01-03, **01-04** y **01-05** CERRADOS. El 01-04 desplegado y visto en el
navegador (`e2e8f86`); el **01-05** (`4e81e6c`) es instrumental y **no toca `index.html`**, por lo
que no necesita navegador. **01-06 pendiente de planificar**: cierra D-38 ENTERA y es lo único que
queda para poder intentar la cuarta transición.
Status: los TRES objetivos del ALCANCE siguen en PASS. La **META no**: dice «en silencio», y el
aparato de medición **no cubre la capa de aviso** — pintar en VERDE un guardado que ha fallado deja
la puerta entera en `rc=0`, y nueve mutantes de esa capa sobreviven (**D-38**). Los otros tres
huecos del aparato de medición **ya no están**: el 01-05 cerró **D-39** (los trinquetes fallan
CERRADO), **D-40** (la puerta no puede salir verde con el banco apagado, ni por rc ni por entorno)
y **D-41** (el enganche `pre-push`, vigilado). Abiertas D-38 (bloquea la fase), D-42 y D-43;
D-15 y D-03 marcadas A RE-MEDIR.
Last activity: 2026-08-31 — **UNIFY del ciclo 01-05**, la vara de medir (`4e81e6c`). Los siete AC
en PASS, cada uno **re-medido en esta sesión** y no heredado del APPLY: rc y mensajes literales
transcritos en el acta. Puerta VERDE fresca por **sus dos variantes, y con salida idéntica**
(`bash tools/verify.sh` → rc=0; y con `VERIFY_INNER=1` **exportado**, el enganche `pre-push` ejerció
igualmente los nueve pasos, banco incluido). Banco rc=0, 61 controles verdes, **11 nuevos**, árbol
idéntico antes y después (`39474868af25`). `index.html` intacto byte a byte y ninguna foto
resellada. El UNIFY abrió **D-43** al leer los mutadores uno a uno. Acta: `01-05-SUMMARY.md`.
Actividad anterior: 2026-08-31 — **TERCERA TRANSICIÓN de la Fase 1**. Árbol en exclusiva
(`HEAD^{tree}` = `dbd46d97beca95ea8252276a503df9350e0e1b29`, idéntico antes y después; huella de
`index.html` `4ff3b0ba79afa7ca1d479ea1525ad51d`, la misma que sirve Pages). Puerta VERDE fresca
(`rc=0`, ocho pasos) ANTES de medir. G7 sigue DEGRADADO (D-22) y se sustituyó por **cuatro brazos
adversarios disjuntos**, cada uno con una FRASE concreta que demoler y prohibición nominal de
mutar el árbol: **los cuatro la demolieron, y cada uno encontró algo que ninguno de los otros
vio**. Los hallazgos decisivos fueron **re-verificados a mano** por el orquestador sobre copias
aisladas. Acta: `01-TRANSICION-3.md`.
Actividad anterior: 2026-08-31 — despliegue y verificación en el navegador del 01-04 (`e2e8f86`,
`f9949e8`): verde en uso normal, «✅ Autopruebas OK» sin tocar datos, y los estados NARANJA y ROJO
vistos por primera vez en un navegador.
Y antes: 2026-08-31 — UNIFY del ciclo 01-04, puerta verde por sus dos variantes.

Progress:
- Milestone: [█░░░░░░░░░] 14% (1 de 7 fases, contando la 0)
- Phase: [████████░░] 83% (5 de 6 ciclos cerrados; queda el 01-06, que cierra D-38 y desbloquea la fase)

## Loop Position

Current loop state:
```
PLAN ──▶ APPLY ──▶ UNIFY
  ✓        ✓        ✓     [01-05 cerrado — listo para planificar el 01-06]
```

Ciclos 01-01 a 01-05: cerrados, cada uno con su acta. La
fase NO está cerrada. Su TERCERA transición (2026-08-31) midió la meta contra el código y **volvió
a cambiar el resultado, por tercera vez consecutiva**: la primera abrió el 01-03, la segunda
destapó D-33 y abrió el 01-04, y ésta abre el 01-05. `PLAN == SUMMARY` habría cerrado la fase las
tres veces.

## Performance Metrics

**Velocity:**
- Total plans completed: 6
- Average duration: —
- Total execution time: —

**By Phase:**

| Phase | Plans | Total Time | Avg/Plan |
|-------|-------|------------|----------|
| 00-hotfix-decimal | 1/1 | — | — |
| 01-guardado-fiable | 5/6 | — | — |

## Accumulated Context

### Decisions

| Decision | Phase | Impact |
|----------|-------|--------|
| Bug de la coma como Fase 0 fuera del ciclo | Fase 0 | Ya desplegado; el resto va por PLAN→APPLY→UNIFY |
| Fiscal antes que UX | Roadmap | Fases 3-4 antes que la 5 |
| Autopruebas con `?selftest=1`, sin build system | Fase 0 | Cada fase añade su invariante a `runSelfTests()` |
| Sin SonarQube ni audit enterprise | Init | No se crea `.paul/config.md` |
| Adoptada la doctrina de `CLAUDE.md` | 2026-08-29 | Todo PLAN lleva revisión adversaria; nada se cierra sin la puerta en verde |
| La puerta es `tools/verify.sh` | 2026-08-29 | Enganchada a `pre-push`; 16 controles con sabotaje que demuestra que muerden |
| Ninguna cifra medida se copia a los documentos | 01-01 | Vive sólo en la foto sellada; se desactualizó dos veces el mismo día |
| No sellar con amnistía al estrenar el trinquete | 01-01 | Se trocea la función; aflojar la vara el primer día haría rutina la amnistía |
| Un único juez para las dos guardas de no-vaciado | 01-02 | `vaciariaElLibro` + `opsDelDocumento`: la misma función en los dos lados, no el mismo criterio escrito dos veces |
| Fallar CERRADO si no se puede leer la nube | 01-02 | Se prefiere perder sincronía a perder el libro; y se ve en naranja, no en verde |
| Los controles de las autopruebas viven en el ARNÉS | 01-02 | Uno dentro de la suite sería juez y parte; el de datos reales está en `run_selftests.py` |
| La transición de fase abre el ciclo 01-03 en vez de cerrar la fase | Fase 1 transición | El brazo de radio de impacto encontró un cruce sin medir que deja escribir un libro vacío sobre uno ilegible. Registrarlo como deuda lo blanquearía como «fase hecha»; se arregla |
| G7 se declara DEGRADADO y se sustituye, no se salta | Fase 1 transición | `code-review-graph` no parsea el JS inline de un `.html`: 0 nodos de `index.html`. Un verde suyo sobre esta fase sería un falso verde |
| El arreglo del cerrojo cierra la CLASE, no el caso: la rama del formato antiguo también repara | 01-03 PLAN | La revisión adversaria vio que un dispositivo sin actualizar no podría reparar nunca, porque `loadOpsAll` re-marca el cerrojo y `saveOpsAll` se niega. Cerrar sólo `opsAll` habría dejado el mismo defecto vivo por el otro camino (§5.15) |
| El coste del arreglo se registra como deuda en vez de esconderse | 01-03 PLAN | El arreglo convierte un caso recuperable-con-pérdida-acotada en un bloqueo silencioso indefinido. Es mejor para el dato y peor para el operador; se dice por escrito o no existe |
| La reparación llama a la escritura CRUDA, no a la puerta | 01-03 | Si pasara por `saveOpsAll`, con el cerrojo puesto no podría escribir jamás: el libro quedaría bloqueado para siempre. Desde este ciclo tiene mutante propio |
| Los checks enmascarados por la relectura se ANOTAN, no se borran | 01-03 | `applySyncPayload` termina releyendo el disco, así que varios checks del cerrojo pasan con y sin el arreglo. Documentan el estado esperado; lo que no se hace es confiar en ellos. Lo que mide de verdad es la llamada directa a `repararLibroIlegible` |
| Los cuatro hallazgos de correctness ajenos al ciclo se difieren por escrito | 01-03 UNIFY | D-24 exige releer el disco en cada guardado y cambiar el contrato de `escribirOpsAll` recién fijado; D-26 exige cambiar qué compara `--check`, que el instrumento declara DERIVA (rc=3). Rediseñar la pieza recién puesta dentro de un ciclo que va de otra cosa es mover la vara sin plan |
| Cerrar el ciclo 01-02 sin cerrar la FASE 1 | 01-02 UNIFY | Los 3 objetivos del scope están en el código, medidos uno a uno; pero ningún eslabón se ha visto en un navegador y nada está desplegado. Una sonda verde no supera a un intento real |
| La segunda transición tampoco cierra la FASE 1: abre el ciclo 01-04 | Fase 1 transición 2 | Los tres objetivos del alcance están en PASS, pero la META no: la guarda de no-vaciado cubre dos de las tres escrituras a la nube. Es la misma forma del defecto que abrió el 01-03. Ficharlo como deuda lo blanquearía como «fase hecha» (§5.10) |
| El 01-04 cierra la CLASE, no los dos casos | Fase 1 transición 2 | Enumerar a mano las tres escrituras repetiría el defecto: una lista blanca sólo protege de lo que ya conoce (§5.15). El conjunto se deriva del código y hace falta un control que muerda si aparece una cuarta |
| Los números de línea del libro de deudas se declaran NO fiables en vez de actualizarse | Fase 1 transición 2 | La auditoría encontró casi todas desfasadas. Corregirlas una a una las deja mal otra vez mañana — es la trampa de §9. Se cierra la clase: para localizar código se usa el NOMBRE y `grep` |
| El juez de subida falla CERRADO también cuando no puede mirar los ACTIVOS | 01-04 PLAN | La revisión adversaria destapó un cruce sin medir: libro con operaciones, sin activos, y la lectura de la nube fallando. Hoy no sube por accidente —la excepción aborta el push—; la primera versión del plan lo habría convertido en «subir». El fallo cerrado estaba escrito para las operaciones y no para los activos: **la asimetría ERA el defecto** (§5.16) |
| La nube es un TRI-ESTADO, no un booleano | 01-04 PLAN | «Leída y vacía», «ilegible» y «no consultada» son tres cosas distintas. Colapsarlas en un booleano pierde exactamente la distinción que causó D-33 |
| El censo de escrituras usa DOS redes disjuntas, no una regla más lista | 01-04 PLAN | La regla «descartar receptores ligados a `new Map`/`new Set`» aplicada a `.add(` daba falso rojo con `root.classList.add`, y arreglarlo por nombre habría sido la lista blanca que la propia ficha D-33 prohíbe. Se derivan los enlaces a referencias de Firestore (red A) Y se vigila el método (red B): cazan fallos distintos |
| El manejador de inicio de sesión se extrae para poder EJECUTARLO en node | 01-04 PLAN | Hoy es una flecha anónima que ni siquiera se registra fuera del navegador. Sin extraerlo, el sabotaje de su aviso no tenía oráculo posible y declararlo mordiente habría sido §5.1 con uniforme de test |
| El sabotaje del eslabón PRODUCTOR es obligatorio, no opcional | 01-04 PLAN | Los sabotajes del juez y del censo pasan los dos aunque la marca de «paquete incompleto» no se ponga NUNCA. La inyección tiene que caer donde el error PROPAGA (§5.9): una clave corrupta sembrada en el arnés |
| D-31 se cierra por la CLASE: cero llamadas literales `setSyncUI('ok')` | 01-04 PLAN | La ficha nombraba un `catch`, pero había dos miembros más vivos —el callback de error vacío del `onSnapshot` y el verde incondicional del arranque—. Cerrar sólo el caso habría sido §5.10 en pequeño |
| Se cruzan dos boundaries y se dice en voz alta | 01-04 PLAN | `buildSyncPayload` (sólo su manejo de errores) y `funcsize.py` (extraer el localizador de funciones para no tener dos escáneres). Un boundary cruzado sin decirlo es deriva; dicho, es una decisión |
| El coste del arreglo se ficha como deuda antes de construirlo | 01-04 PLAN | Rechazar la subida por un paquete incompleto deja el libro sin copia en la nube mientras dure el fallo, sin salida en la interfaz. Es el gemelo de D-23. Mejor para el dato y peor para el operador: se escribe o no existe |
| Cuatro brazos adversarios disjuntos sustituyen a G7, que sigue ciego | Fase 1 transición 2 | El de seguridad no encontró nada y el de objetivos encontró el hallazgo que paró la fase. Brazos que miden lo mismo se corroboran en su punto ciego; éstos midieron cosas distintas |
| El fallo cerrado del juez es SIMÉTRICO: operaciones y activos | 01-04 | La asimetría entre los dos predicados ERA el defecto (§5.16). El cruce «ops sí · activos no · nube ilegible» tiene fila propia en la matriz y sabotaje propio |
| Se cruza el boundary de `funcsize.py` y se dice en voz alta | 01-04 | Copiar el escáner habría dado dos escáneres que se desincronizan a la primera. Prueba de que sigue midiendo igual: `--check` verde sin resellar |
| El trinquete se resella con semántica v2 a propósito (ámbito ampliado a `async function`) | 01-04 | Volver `runSelfTests` asíncrona la había sacado del trinquete SIN que nada se pusiera rojo. Cambiar la regla de medida es DERIVA (rc=3): el resellado es una decisión escrita, no un trámite |
| Los tres hallazgos de la revisión adversaria se arreglan dentro del ciclo, no se difieren | 01-04 | Eran correctness y eran huecos del propio aparato de medición: un fixture que ataba el contenido de la nube a su nombre, un CABLE sin medir entre dos piezas ya medidas, y un `await` perdido que dejaba una suite sin ejercer con la puerta verde y sorda |
| El interruptor `VERIFY_INNER` pasa a AVISAR, y se borra un `VERIFY_DEGRADED` fantasma | 01-04 | Un banco que se salta en silencio es un falso verde; y el `VERIFY_DEGRADED` sólo existía en un comentario que ninguna rama leía — §5.1 en estado puro |
| La TERCERA transición tampoco cierra la FASE 1: abre el ciclo 01-05 | Fase 1 transición 3 | Los tres objetivos del alcance están en PASS, pero la META no: la meta dice «en silencio» y la capa de AVISO no tiene oráculo. Un guardado fallido pintado en verde pasa la puerta entera. Ficharlo como deuda lo blanquearía como «fase hecha» (§5.10) — misma decisión que en las dos transiciones anteriores |
| Un fallo pintado en VERDE cuenta como borrado en silencio | Fase 1 transición 3 | Es la lectura literal de la meta. Si sólo se exigiera el MECANISMO, la fase cerraría con nueve mutantes vivos en la capa que el operador realmente mira |
| El truncamiento por sync NO entra en el 01-05: es D-01 y es Fase 3 | Fase 1 transición 3 | El brazo de caminos de pérdida redescubrió que un dispositivo rezagado pisa una nube rica sin aviso. Es real y grave, pero ya está fichado y es la meta declarada de la Fase 3. La meta de la Fase 1 habla de guardado y ARRANQUE. Meterlo aquí sería mover la vara a mitad de partido |
| El acta del 01-04 no se reescribe: se le pone ERRATA al pie | Fase 1 transición 3 | Un SUMMARY es un acta y se entierra (§8). La cifra falsa («15 sabotajes», son 14) queda donde estaba, con la corrección y su re-derivación debajo. Los documentos VIVOS (STATE, ROADMAP) sí se corrigen en su sitio |
| El rc=4 y el `unset` del enganche son DOS capas, no una | 01-05 | El rc arregla el contrato («ese verde no existe»); el `unset` arregla el entorno («el enganche no lo hereda»). Con una sola, el agujero de D-40 sigue abierto por el otro lado |
| El contrato del código de salida se cambia en el MISMO commit que su consumidor vivo | 01-05 | `sabotage.py::puerta()` corre la puerta con `VERIFY_INNER=1` y su control de vacuidad exige que esa corrida sea verde. Cambiarlo sin tocar al consumidor **mataba el banco entero**. Con control positivo: revertido el `exit 4`, la vacuidad lo caza |
| El vigilante del enganche va DESPUÉS del banco y FUERA de la corrida interior | 01-05 | Cablearlo antes dejaba al banco sin correr en cualquier máquina sin el enganche instalado — o sea, en un CI. Mide la MÁQUINA, no el código |
| `hookcheck` deriva lo esperado del heredoc del INSTALADOR, no de una copia pegada | 01-05 | Una copia pegada en el comprobador se desincroniza a la primera, y entonces vigila una ficción. Y si no encuentra el heredoc: rc=2, nunca «coinciden» |
| Toda foto sellada corrupta imprime su REMEDIO | 01-05 | Una foto ilegible bloqueaba también el resellado: el operador quedaba sin salida. Un rc=2 sin salida es un callejón |
| `comparar_o_roto` se deja sin oráculo a propósito y se ficha como D-42 | 01-05 | Quitarlo devolvería el rc=1 con traceback en cuanto alguien añada una clave sin validar, que es justo D-39. Red declarada, deuda escrita |
| `index.html` intacto y cero fotos reselladas son EVIDENCIA, no ausencia de trabajo | 01-05 | Son la prueba de que el ciclo cambió cómo FALLAN los instrumentos, no qué MIDEN. Si una foto hubiera necesitado resellado, sería deriva (rc=3) |
| Los hallazgos de los brazos se re-verifican a mano antes de aceptarlos | Fase 1 transición 3 | Un brazo puede inventar agujeros (§5.4). Los cuatro decisivos se reprodujeron con comando propio sobre copias aisladas; el resto se marca explícitamente como no re-verificado |

### Deferred Issues

**Las deudas viven ahora en `.paul/DEUDAS.md`** (D-01 a D-11), que es la lista viva que se lee al
arrancar cada sesión. Esta tabla ya no se mantiene: duplicarla sería tener dos fuentes de verdad.

### Blockers/Concerns

| Blocker | Impact | Resolution Path |
|---------|--------|-----------------|
| ~~El cerrojo del libro ilegible se levanta antes de confirmar la reparación~~ | **RESUELTO** en el ciclo 01-03 (`96c7a3e`) | Arreglado, con autoprueba del cruce y diez controles positivos. Acta: `01-03-SUMMARY.md` |
| ~~La FASE 1 no se ha medido contra el código después del 01-03~~ | **RESUELTO**: medida el 2026-08-30 sobre `69f728e..HEAD` | Acta: `01-TRANSICION-2.md`. La medición cambió el resultado: destapó D-33 |
| ~~**D-33** · una tercera escritura a la nube esquiva la guarda de no-vaciado~~ | **RESUELTO** en el ciclo 01-04 (`21e1edb`) | Cerrada por la CLASE: una sola escritura, dos redes disjuntas cableadas a la puerta, control positivo en el banco. Acta: `01-04-SUMMARY.md` |
| ~~**El ciclo 01-04 no se ha visto en un navegador**~~ | **RESUELTO** el 2026-08-31: desplegado (`9ca21ee..e2e8f86`) y mirado en la app real | Acta: `01-04-VERIFICACION-NAVEGADOR.md`. Seis de siete puntos en PASS, incluido el ROJO nuevo. Queda el recuento final sin cifra |
| ~~**La FASE 1 no se ha medido contra el código después del 01-04**~~ | **RESUELTO** el 2026-08-31 | Acta: `01-TRANSICION-3.md`. Medir volvió a cambiar el resultado: la fase NO cierra |
| ~~**D-39 · los trinquetes fallan ABIERTO con traceback**~~ | **RESUELTA** en el ciclo 01-05 (`4e81e6c`) | `cargar_baseline()` valida el TIPO de cada clave en los dos instrumentos, incluidas las que sólo lee `--update`. rc=2 con nombre, clave y remedio. Dos sabotajes propios |
| ~~**D-40 · `VERIFY_INNER=1` deja la puerta en rc=0 sin banco**~~ | **RESUELTA** en el ciclo 01-05 (`4e81e6c`) | Dos capas: la variante interior devuelve **rc=4** (verde sólo para el banco, y dicho en la cabecera), y el enganche **limpia** la variable. Verificado con la variable exportada: el push ejerció los nueve pasos |
| ~~**D-41 · nada vigila el enganche `pre-push`**~~ | **RESUELTA** en el ciclo 01-05 (`4e81e6c`) | `tools/hookcheck.py`, cableado como paso de la puerta, con seis desenlaces distinguibles y control de vacuidad |
| **D-38 · la capa de AVISO no tiene oráculo** | Nueve mutantes sobreviven a la puerta entera; un guardado fallido pintado en VERDE sale «VERDE — todo ejercido y en verde». **Bloquea el cierre de la Fase 1** | Ciclo **01-06**: las tres familias de mutantes **y los DOS pintores que deciden** (`showSaveIndicator` y `setSyncUI`), con reloj falso para la duración. La CLASE entera, no seis de nueve |
| **D-39 · los trinquetes fallan ABIERTO con traceback** | Un instrumento roto sale rotulado como «el código ha engordado» y manda a mirar el sitio equivocado (§4.3) | Ciclo 01-05: validar tipos en `cargar_baseline` y envolver la comparación para dar rc=2 con nombre |
| **D-40 · `VERIFY_INNER=1` deja la puerta en rc=0 sin banco** | El enganche hereda el entorno: esa variable exportada deja pasar todos los push con el banco apagado | Ciclo 01-05: rc≠0 en esa variante, o el enganche limpia la variable |
| **D-41 · nada vigila el enganche `pre-push`** | En una máquina nueva la variante automática no existe y nada se pone rojo | Ciclo 01-05: un paso que compare el instalado con su instalador |
| G7 (radio de impacto) no ve `index.html` | La transición de fase no tiene instrumento propio; hoy se hace a mano | D-22. Se cierra cuando el grafo indexe el `<script>`, o cuando el sustituto sea un script del repo cableado a la puerta |

## Verificación manual de la Fase 1 — app desplegada, 2026-08-30

Hecha sobre `https://californiakid91.github.io/food/` con `feb643b` publicado. Confirmado antes de
empezar que Pages servía la versión nueva (huella del fichero descargado idéntica a la local) y que
el navegador del operador la tenía cargada (`typeof dedupeOpsById === 'function'` en consola, no
por el aspecto de la pantalla).

| Punto | Resultado | Evidencia |
|---|---|---|
| Aviso verde «Guardado ✓» al guardar | **PASS** | visto en pantalla por el operador |
| El naranja «Cambios sin subir» NO sale en uso normal | **PASS** | el puntito quedó verde |
| `?selftest=1` deja los datos intactos | **PASS** | **90 operaciones y 4 carteras, idénticas antes y después**, contadas en consola. Es el fallo que estaba vivo en producción |
| `?selftest=1` imprime «✅ Autopruebas OK» | **PASS** | leído en la consola del navegador |
| El aviso sale en ROJO cuando el guardado falla | **NO COMPROBADO** | → **D-18**. Exige agotar el almacenamiento del navegador; no se improvisó con 90 operaciones reales delante |

Los dos últimos se comprobaron por separado a propósito: el fallo original consistía justamente en
imprimir «OK» **mientras** borraba, así que «no borró» y «dijo OK» son afirmaciones independientes.

### Segunda pasada — ciclo 01-03, `96c7a3e`, 2026-08-30

Misma disciplina: confirmado antes de mirar nada que Pages servía la versión nueva (huella
`661acd6b17aed4808c9d8367a2cd72b4`, idéntica a la local; el primer intento devolvió la anterior).

| Punto | Resultado | Evidencia |
|---|---|---|
| El navegador tiene el código nuevo | **PASS** | `typeof repararLibroIlegible === 'function'` en consola |
| `?selftest=1` imprime «✅ Autopruebas OK» | **PASS** | leído en la consola |
| `?selftest=1` deja los datos intactos | **PASS** | **90 operaciones y 4 carteras**, leídas de `balance-ops` y `balance-meta-v2` antes y después. Las mismas que en la pasada anterior |
| El aviso sale en ROJO cuando el guardado falla | **NO COMPROBADO** | sigue siendo **D-18**; el 01-03 no lo tocó |

### Tercera pasada — ciclo 01-04, `e2e8f86`, 2026-08-31

Misma disciplina que las dos anteriores: confirmado ANTES de mirar nada que Pages servía la
versión nueva (huella `4ff3b0ba79afa7ca1d479ea1525ad51d`, idéntica a la local; los dos primeros
intentos devolvieron todavía la anterior, `661acd6b…`).

| Punto | Resultado | Evidencia |
|---|---|---|
| El navegador tiene el código nuevo | **PASS** | `typeof decidirSubida === 'function'` en consola |
| Verde en uso normal | **PASS** | visto en pantalla por el operador |
| `?selftest=1` imprime «✅ Autopruebas OK» | **PASS** | leído en la consola |
| `?selftest=1` deja los datos intactos | **PASS** | contado por el operador antes y después; **sin cifra anotada** esta vez |
| NARANJA «Cambios sin subir» | **PASS** | provocado con un cerrojo de mentira; `aviso: 'pendiente'` |
| **ROJO «No se pudo sincronizar»** | **PASS** | provocado con una escritura que rechaza; `aviso: 'error'`. **Primera vez que este estado se ve en un navegador** |
| El aviso rojo del GUARDADO LOCAL fallido | **NO COMPROBADO** | sigue siendo **D-18**: es otro aviso, y exige agotar el almacenamiento del navegador |

Los dos estados de fallo se provocaron inyectando dependencias falsas, no rompiendo nada real:
**ninguna de las dos pruebas escribe en la nube**. Detalle y comandos exactos en
`01-04-VERIFICACION-NAVEGADOR.md`, para que la próxima pasada no tenga que redescubrirlos.

## Boundaries (Active)

Del PLAN 01-04 (ya ejecutado; se mantienen como invariantes vivos):

- **Exactamente una** escritura a Firestore en `index.html`, dentro de `subirALaNube`. Lo vigilan
  dos redes disjuntas en `tools/cloudwrites.py`, cableadas a la puerta
- **Cero** llamadas literales `setSyncUI('ok')`: el verde sólo se alcanza por `estadoSync`
- `decidirSubida` es pura y no toca red ni DOM: quien decide no hace E/S
- Cero `catch` vacíos en el camino de subida; los tolerados fuera de él están **nombrados uno a
  uno** en `.paul/baseline-catches.json`

Del PLAN 01-03 y anteriores (siguen vivos):

- `vaciariaElLibro` / `tieneOperaciones` / `opsDelDocumento` intactos: son el juez único del 01-02,
  y el 01-04 los **usa** desde un sitio más sin reescribir su criterio
- `repararLibroIlegible` / `rescatarOpsIlegible` / `escribirOpsAll`: contrato fijado en el 01-03.
  `opsIlegible` se **lee** como entrada del juez de subida; no cambia quién lo pone ni quién lo quita
- `dedupeOps` / `opFingerprint` / `dedupeOpsById` intactos
- `parseNum` / `numIn` / `parseLooseNum` no se tocan (Fase 0)
- La semántica de fusión de `buildSyncPayload` y la resolución por `savedAt` siguen siendo Fase 3
  (el 01-04 tocó **sólo** su manejo de errores); `computeFifo` y `exportTaxExcel`, Fase 4

Permanentes del proyecto:

- `index.html` sigue siendo un fichero único sin build system ni dependencias nuevas
- No reintroducir la obtención automática de precios

## Session Continuity

Last session: 2026-08-31
Stopped at: **UNIFY del ciclo 01-05 cerrado.** Los siete AC en PASS, **re-medidos en esta sesión**
con el árbol limpio (`1bd8d35b…`), no heredados del APPLY: los rc y los mensajes literales están
transcritos en el acta. Lo que más importa de este ciclo: la puerta con la que se va a medir el
01-06 ya no puede salir verde sin ejercerse, ni confundir un instrumento roto con un hallazgo del
código, ni suponer que la variante automática existe.

Este UNIFY **cambió algo al medir**, como los tres anteriores: leyendo los seis mutadores nuevos
uno a uno contra el texto del AC-7 apareció **D-43** — un mutador sustituye texto sin afirmar que
su ancla sea única. No es un falso verde (falla ruidosamente), pero es una desviación nominal del
AC y está escrita en el libro en este mismo commit.

**Sin desplegar, y comprobado que no importa:** el local va 5 commits por delante de `origin/main`
(en `7b6115a`), pero el `index.html` de HEAD es **el mismo blob** que el de `origin/main`
(`a2ed63a9…`): Pages sirve exactamente el código verificado en el navegador. Lo pendiente de
empujar son actas y herramientas.

Next action: `/paul:plan 01-06` — la capa de aviso ENTERA (D-38). Es lo único que queda para poder
intentar la CUARTA transición de la Fase 1. Recordar: el 01-06 **sí** exige verificación en el
navegador (§7 bis), porque cambia lo que el operador ve cuando algo falla.
Resume file: .paul/phases/01-guardado-fiable/01-05-SUMMARY.md

---
*STATE.md — Updated after every significant action*
