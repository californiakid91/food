# Project State

## Project Reference

See: .paul/PROJECT.md (updated 2026-08-29)

**Core value:** Llevar al día tus carteras con precios manuales y sacar de ahí una declaración de la renta correcta, sin backend propio.
**Current focus:** v0.1 Datos fiables — Fase 1 "Guardado que no miente"

## Current Position

Milestone: v0.1 Datos fiables (v0.1.0)
Phase: 1 of 6 (Guardado que no miente) — **ABIERTA**. El ciclo **01-07 está CERRADO**; la fase no se
ha vuelto a medir contra el código desde entonces.
Plan: 01-07 **ejecutado, verificado en navegador y cerrado** (2026-09-05).
Status: **UNIFY hecho.** Acta en `01-07-SUMMARY.md`. Cierra D-45, D-46, D-27, D-29, D-30 y D-54.
Abre D-48 a D-53, D-55, D-56 y D-57. Siguen abiertas D-42, D-43, D-44, D-47 y D-03 (a re-medir).
Last activity: 2026-09-05 — **cierre del 01-07**. El APPLY estaba commiteado desde el 2026-09-01 sin
acta y con este documento diciendo todavía «plan esperando aprobación»: **el estado mentía sobre el
propio proceso**, y se descubrió al retomar comparando con `git log`.

**Lo que hay que recordar de este ciclo:**

1. **El checkpoint humano NO fue un trámite.** Encontró un defecto de correctness **antes** del
   primer punto de la lista: el operador abrió la app con 90 operaciones y leyó «este dispositivo
   **no tiene operaciones**». El comportamiento era el previsto (D-50); el TEXTO mentía (D-54).
2. **El ciclo había agravado ese texto sin verlo.** El naranja lo alcanzaban cuatro veredictos y
   pasó a ocho; una de las claves nuevas es la que ve **todo dispositivo ya sincronizado** el día
   del despliegue. Un texto raramente falso se volvió universal el día del estreno.
3. **Cubrir el mecanismo no cubre su cable (§5.6), medido otra vez.** Las pruebas del pintor de
   D-54 estaban completas en apariencia; revertidos los dos llamantes con el pintor intacto, la
   suite entera seguía en **rc=0**. El arreglo podía desconectarse sin que nada se pusiera rojo.
4. **La puerta cazó tres sabotajes suyos que dejaron de morder** porque el cambio movió sus anclas:
   `rc=1` con «CONTROLES QUE NO MUERDEN (3)», no un verde.
5. **La comprobación final la hizo la app sola y salió mejor que la pedida:** se pidió inyectar un
   motivo y el arranque repintó el REAL, con «89 operaciones locales que proteger» — la cifra
   exacta del libro tras el borrado de la propia verificación.

Progress:
- Milestone: [█░░░░░░░░░] 14% (1 de 7 fases, contando la 0)
- Phase: [██████████] 7 ciclos cerrados. **Falta la QUINTA transición**: medir la fase contra el
  código. Las cuatro anteriores cambiaron el resultado las cuatro veces.

## Loop Position

Current loop state:
```
PLAN ──▶ APPLY ──▶ UNIFY
  ✓        ✓        ✓     [01-07 cerrado el 2026-09-05.
                            Siguiente: QUINTA transición de fase — medir la Fase 1
                            contra el código, antes de preguntar nada]
```

Ciclos 01-01 a 01-07: cerrados, cada uno con su acta. Sus CUATRO transiciones midieron la meta
contra el código y **las cuatro cambiaron el resultado**. `PLAN == SUMMARY` habría cerrado la fase
las cuatro veces.

## Performance Metrics

**Velocity:**
- Total plans completed: 7
- Average duration: —
- Total execution time: —

**By Phase:**

| Phase | Plans | Total Time | Avg/Plan |
|-------|-------|------------|----------|
| 00-hotfix-decimal | 1/1 | — | — |
| 01-guardado-fiable | 6/6 | — | — |

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
| El enfoque del 01-06 lo decide una DIALÉCTICA, no yo solo | 01-06 PLAN | Diseño abierto con dos precedentes propios del repo en contra (01-04 dice «quien decide no hace E/S» Y dice «extraer para poder EJECUTARLO en node»). Dos posturas, dos rondas. Gana ejecutar el pintor real: la mitad «decisión» ya existe y está medida; lo que nunca ha ejecutado ningún test es el pintor |
| El arnés observable devuelve `null` para todo id que no exista en `index.html` | 01-06 PLAN | Un DOM de mentira permisivo fabrica una clase de falsos verdes que el navegador no tiene: una errata en un identificador pasaría verde fuera del navegador y no pintaría nada en pantalla (§5.3). El conjunto se deriva del fichero, no se enumera |
| El `aviso` del juez de subida entra en la matriz: la familia que el borrador dejaba viva | 01-06 PLAN | Re-verificado a mano: hoy un rechazo por vaciado etiquetado «todo bien» sale rc=0 y «✅ Autopruebas OK». Cerrar los dos pintores y llamarlo «la clase» habría sido §5.10 con acta, y ya pasó en el borrador del 01-05 |
| El `try/finally` del reloj falso es BLOQUEANTE, no buena práctica | 01-06 PLAN | Sin él, un aserto que lance deja `setTimeout` sustituido para toda la vida de la página y el temporizador que guarda queda capturado: el ciclo contra el borrado silencioso habría dejado de guardar en silencio. Lleva mutante propio, o el control nunca se habrá visto rojo |
| La red se cierra por RECEPTOR, no por una lista de canales | 01-06 PLAN | El borrador enumeraba «los dos pintores» y heredaba un ámbito de consola sellado a mano, que deja fuera HOY el arranque y las ventanas emergentes de sesión. Un guardián de deriva caza a quien QUITE una entrada, pero un conjunto incompleto DE ORIGEN le es invisible (§5.15) |
| Se retira la cifra «nueve mutantes» de todo criterio de éxito | 01-06 PLAN | Nunca se enumeraron: el brazo B los reportó y sólo se re-verificó el representativo. Un criterio que cita una cifra sin artefacto no se puede marcar PASS con evidencia. Lo contrastable es el censo derivado |
| El ámbito del censo de avisos se mide ENTERO y se exime por NOMBRE | 01-06 | Se intentó acotar dos veces y las dos perdió avisos reales: con ocho raíces a mano escapaban nueve del camino de la fase; con raíces derivadas y cierre transitivo se perdió `guardarTodo`, que sólo se alcanza como ARGUMENTO de un temporizador. Un cierre transitivo sobre JS tiene más formas de escaparse de las que uno puede enumerar. El instrumento MIDE; quien EXIME es el criterio |
| Un aviso que DESAPARECE es un HALLAZGO, no una mejora | 01-06 | Degradar un `console.error` del arranque a `console.log` salía rotulado «ha desaparecido» **con el comando de resellado debajo**: el instrumento dirigía la mano del operador a amnistiar el silencio (§4.4). Aquí la dirección buena no es «menos»: una boca que se cierra ES el daño de esta fase. Por eso NO compara por dominación, al revés que `funcsize` y `emptycatch` |
| Los colores se afirman por su VALOR, no por «que sean distintos» | 01-06 | «Distintos» lo satisface INTERCAMBIARLOS, o sea pintar el fallo en verde: `rc=0` y «✅ Autopruebas OK». Mi oráculo heredó mi punto ciego dentro del ciclo escrito para cerrar ese agujero (§5.8) |
| El censo entra más ancho que el alcance del plan, y se dice | 01-06 | El plan excluía los avisos que no son de guardado ni de arranque. Con ámbito plano sí entran, y se sellan con su motivo uno a uno. Recortar el ámbito para que cuadrara con el plan habría sido meterle juicio al instrumento, y un instrumento con juicio dentro se dobla |
| Los diez hallazgos de los brazos se arreglan DENTRO del ciclo, ninguno se difiere | 01-06 | Seis eran huecos del propio aparato de medición y cuatro correctness en las herramientas. Pasar a UNIFY con uno sin atender lo habría blanqueado como «hecho» (§3.4) |
| La CUARTA transición tampoco cierra la FASE 1: abre el ciclo 01-07 | Fase 1 transición 4 | Los tres objetivos del alcance están en PASS y el aparato de medición resistió entero, pero la META no: al arrancar sin activos, una nube más vieja empobrece el libro con la pantalla en VERDE. Ficharlo como deuda lo blanquearía como «fase hecha» (§5.10) — misma decisión que en las tres transiciones anteriores |
| T4-1 es Fase 1 aunque el ROADMAP lo listara en la Fase 3 | Fase 1 transición 4 | El ROADMAP pone «`hasRealLocalData()` debe mirar `ops`» en el alcance de la Fase 3, pero el daño es pérdida de libro en el ARRANQUE con estado tranquilizador —la meta literal de la Fase 1— y **no exige fusionar**: basta que el predicado cuente el libro. Es la misma asimetría que el 01-04 cerró en el otro lado (§5.16). La fusión por `id` sí se queda en la Fase 3 |
| D-15 se CIERRA re-midiéndola, no heredando el acta del 01-04 | Fase 1 transición 4 | Su ficha se contradecía a sí misma desde la tercera transición. Se volvió a mutar `subirALaNube` para ignorar el veredicto del juez: `rc=1`. El 01-04 la había cerrado sin que nadie lo anotara. Una medición commiteada no se hereda (§7) |
| D-27, D-29 y D-46 van JUNTAS al 01-07: son la misma familia | Fase 1 transición 4 | La invariante «un fallo de guardado no se anuncia como éxito y no se sincroniza» existe dentro de `guardarTodo` y no en los demás caminos. Arreglar sólo el cruce de META repetiría el defecto por los otros seis llamantes: se cierra la CLASE (§5.15) |
| La prohibición a los brazos se escribe por lo que EJECUTAN, no por lo que editan | Fase 1 transición 4 | Un brazo corrió el banco de sabotaje sobre el árbol real para re-derivar una cifra; el banco muta `index.html` en vivo, y al detenerlo lo dejó sucio. No desobedeció ni una palabra. Regla nueva en `CLAUDE.md` §3.4: todo brazo trabaja sobre COPIA y sobre el árbol real sólo LEE |
| El enfoque del 01-07 lo decide una DIALÉCTICA, y ésta rechaza las DOS posturas | 01-07 PLAN | Ni censo de llamantes (nace con ~10 exenciones por nombre: la lista blanca de §5.15, y mide un proxy sintáctico §5.11) ni refactor de doce sitios (toca flujos con `prompt`/`confirm` que la puerta no ve, y cierra «por construcción» sin artefacto §5.1). Gana vigilar los SUMIDEROS: el daño no es «booleano descartado», es ANUNCIAR VERDE y SUBIR, y esas salidas son pocas y derivables del código |
| El cierre de D-45 exige arreglar el reloj del sync, y eso CRUZA un boundary de Fase 3 | 01-07 PLAN | Al aplicar, la marca de tiempo se pierde: tras el primer sync todo documento parece más nuevo y la rama que cierra D-45 no dispara nunca. Sin esto el cierre sería ficticio —control verde, daño vivo, §5.10—. Se cruza el boundary y se dice en voz alta; la SEMÁNTICA DE FUSIÓN sigue entera en la Fase 3 |
| `hasRealLocalData` NO se unifica: conserva su semántica de activos | 01-07 PLAN | Alimenta dos preguntas distintas de `decidirSubida`, y una es la guarda de activos del 01-04. Convertirla en el predicado combinado la habría apagado, dejando que una subida machaque los activos de la nube — invisible a la puerta, porque la matriz recibe los booleanos ya inyectados. El «predicado único» se reformula como «los dos jueces consumen los mismos primitivos» |
| El juez de bajada gobierna los DOS caminos, no sólo el del arranque | 01-07 PLAN | La escucha en vivo tiene su propio desempate escrito aparte: es literalmente el segundo predicado que el ciclo existe para eliminar. Cerrar sólo uno habría sido el caso disfrazado de clase |
| El instrumento sella una HUELLA y promete menos, en vez de prometer lo indecidible | 01-07 PLAN | «¿Está esta llamada gobernada por un veredicto?» no se decide estáticamente sobre JS: o se atribuye por función contenedora —presencia, no precedencia (§5.11)— o se sella la huella. Se sella, y el criterio se rebaja a «ningún sumidero nuevo nace sin que alguien lo mire». Un instrumento con juicio dentro se dobla (§9) |
| Un criterio que no puede MORIR no es criterio | 01-07 PLAN | El borrador marcaba el predicado único con un `grep` de nombres, que es una aserción de nombre satisfecha por accidente (§5.8) y que revertir el arreglo no mata. Se sustituye por controles de comportamiento sobre los dos caminos, y el plan exige nombrar por escrito todo arreglo que no pueda tener control positivo |
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
| ~~**D-38 · la capa de AVISO no tiene oráculo**~~ | **RESUELTA** en el ciclo 01-06 (2026-08-31) | Cerrada por la CLASE: los dos pintores se EJECUTAN, color por su valor, visibilidad y duración; el `aviso` del juez en las 84 filas; `tools/avisos.py` cableado a la puerta con dos redes disjuntas. Acta: `01-06-SUMMARY.md` |
| **D-44 · el censo de avisos es ESTÁTICO y exime `runSelfTests` a mano** | Ceguera **declarada**, no un falso verde: presencia ≠ precedencia, la red por receptor sólo ve literales, y hay un corte escrito a mano | Ficha completa en `.paul/DEUDAS.md`. Se reabre si aparece un `getElementById` calculado sobre un elemento de aviso, un canal de aviso nuevo, o **un segundo corte** |
| ~~**El ciclo 01-06 no se ha visto en un NAVEGADOR**~~ | **RESUELTO** el 2026-08-31: desplegado (`7b6115a..685b44b`) y mirado en la app real | Acta: `01-06-VERIFICACION-NAVEGADOR.md`. Cuatro puntos en PASS, incluido **que guardar sigue funcionando después de las autopruebas**. Queda sin reportar el estado del indicador de sync |
| **D-45 · al arrancar, una nube MÁS VIEJA empobrece el libro y la pantalla queda en VERDE** | **Abre el ciclo 01-07.** Es la meta literal de la fase, viva: pérdida de libro en el arranque con estado tranquilizador. La puerta entera sale `rc=0` sobre el código con el defecto | Ciclo 01-07: un solo juez para las dos direcciones de «¿hay datos locales que proteger?», con oráculo que ejerza el desempate de `pullFromFirestore` |
| **D-46 · el cruce «sólo falla el guardado de la lista de carteras» no tiene oráculo** | **Abre el ciclo 01-07.** Quitar `okMeta` del veredicto deja la puerta en `rc=0` y VERDE; con la cuota llena, «Guardado ✓» en verde Y subida a la nube | Ciclo 01-07: un control que falle **sólo** `saveMeta` y exija `false`, rojo y cero subidas. Junto con D-27 y D-29, que son la misma familia |
| **D-47 · sin volcado al cerrar la pestaña: ventana de 600 ms** | Pérdida sin fallo declarado; **no abre ciclo por sí sola** | Se decide aparte. El arreglo natural es volcar en `pagehide` |
| ~~**D-15 · la guarda de subida comprobada por presencia, no por precedencia**~~ | **CERRADA** el 2026-09-01, re-midiéndola | Ignorar el veredicto del juez en `subirALaNube` da `rc=1`. La cerró el 01-04 sin anotarlo |
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

### Cuarta pasada — ciclo 01-06, `685b44b`, 2026-08-31

Misma disciplina que las tres anteriores: confirmado ANTES de mirar nada que Pages servía la
versión nueva (huella `66e6dd20e9ec76163a332a06f5ef2598`, idéntica a la local; **los dos primeros
intentos devolvieron todavía la anterior**, `4ff3b0ba…`).

Antes de pedirle nada al operador se midió el diff **por funciones**: 12 nuevas y 4 cambiadas,
**todas de pruebas o del arnés**; **cero funciones del producto tocadas**, y las **139 sentencias
de primer nivel idénticas** a las de la versión ya verificada. Acota el riesgo; no sustituye a
mirar.

| Punto | Resultado | Evidencia |
|---|---|---|
| El navegador tiene el código nuevo | **PASS** | `typeof abrirVentanaDePintura === 'function'` en consola |
| `?selftest=1` imprime «✅ Autopruebas OK» | **PASS** | leído en la consola |
| `?selftest=1` deja los datos intactos | **PASS** | **90 operaciones y 5 carteras**, contadas en las DOS consolas, antes y después. **Cifras anotadas** |
| **Guardar sigue funcionando DESPUÉS de las autopruebas** | **PASS** | el operador cambió un valor y el guardado funcionó. Es el control de R-2 en el sitio real: sin el `try/finally` del reloj falso, la página habría dejado de guardar en silencio |
| El estado del indicador de sincronización tras las pruebas | **NO REPORTADO** | no se marca PASS: no se hereda de que el resto fuera bien |
| El aviso rojo del GUARDADO LOCAL fallido | **NO COMPROBADO** | sigue siendo **D-18**, por decisión del operador. Exige agotar el almacenamiento con 90 operaciones reales delante |

Las carteras son 5 y no 4 porque el operador añadió una antes de empezar. El invariante no es la
cifra absoluta sino que **sea la misma antes y después**, y lo es.
Detalle y comandos exactos en `01-06-VERIFICACION-NAVEGADOR.md`.

**Nota de proceso:** el despliegue **no se autorizó**. El asistente preguntó si empujaba y tomó por
un sí una respuesta que no lo era. Queda escrito en vez de callado.

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

Last session: 2026-09-05
Stopped at: **ciclo 01-07 CERRADO**, desplegado y verificado dos veces en el navegador real. Árbol
limpio; `index.html` en `9459b0fc3b40a50a38d0c506fec2b862`; puerta en **rc=0** por las dos variantes.

**Aviso para quien retome:** al empezar esta sesión, este documento decía «PLAN 01-07 esperando
aprobación, sin ejecutar» cuando el APPLY llevaba cuatro días commiteado. **El estado mintió sobre
el proceso mismo**, y sólo se vio comparando con `git log`. Antes de creerse este documento, mírense
los commits.

Next action: **QUINTA transición de fase** — medir los objetivos de la Fase 1 **contra el código**,
con brazos disjuntos que trabajen sobre COPIA y sobre el árbol real sólo LEAN. No cerrar por conteo
de actas: `PLAN == SUMMARY` ha disparado en falso las cuatro veces anteriores, y las cuatro
mediciones cambiaron el resultado.
Resume file: .paul/phases/01-guardado-fiable/01-07-SUMMARY.md

---
*STATE.md — Updated after every significant action*
