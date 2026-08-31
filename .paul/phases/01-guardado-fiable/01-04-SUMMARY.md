---
phase: 01-guardado-fiable
plan: 04
subsystem: sync
tags: [firestore, guardado, no-vaciado, sabotaje, trinquete]
requires:
  - phase: 01-02
    provides: el juez único de no-vaciado (`vaciariaElLibro` / `tieneOperaciones` / `opsDelDocumento`)
  - phase: 01-03
    provides: el contrato del cerrojo del libro ilegible (`opsIlegible` / `repararLibroIlegible`)
provides:
  - una única puerta de escritura a la nube (`subirALaNube`) decidida por una función pura (`decidirSubida`)
  - el manejador de inicio de sesión extraído y ejecutable fuera del navegador (`alIniciarSesion`)
  - dos instrumentos nuevos cableados a la puerta: `tools/cloudwrites.py` y `tools/emptycatch.py`
affects: [fase-3-sincronia, fase-2-backup]
tech-stack:
  added: []
  patterns:
    - "Juez único puro + E/S tonta: quien decide no toca la red ni el DOM"
    - "Tri-estado explícito para la nube en vez de booleano"
    - "Dos redes disjuntas para cerrar una clase (por receptor y por método)"
key-files:
  created: [tools/cloudwrites.py, tools/emptycatch.py, .paul/baseline-catches.json]
  modified: [index.html, tools/funcsize.py, tools/verify.sh, tools/sabotage.py, tools/run_selftests.py, .paul/baseline-funcs.json, .paul/DEUDAS.md]
key-decisions:
  - "La nube es un tri-estado más un cuarto caso: colapsarlo en booleano ERA el defecto D-33"
  - "Fallo cerrado SIMÉTRICO: vale para las operaciones y también para los activos"
  - "El verde sólo se alcanza por `estadoSync`; cero llamadas literales `setSyncUI('ok')`"
  - "Se cruza el boundary de `funcsize.py` para compartir el localizador en vez de copiarlo"
patterns-established:
  - "Sabotaje del eslabón PRODUCTOR, no sólo del consumidor"
  - "Sabotaje del CABLE entre dos piezas ya medidas por separado"
duration: ~2h30
started: 2026-08-30T14:00:00Z
completed: 2026-08-30T16:23:00Z
---

# Fase 01 · Plan 04: Una sola puerta de subida — Acta

**Las tres escrituras al documento de Firestore pasan a ser UNA, decidida por una función pura
que falla cerrado cuando no puede mirar; y dos instrumentos nuevos ponen la puerta roja si
aparece una cuarta.**

## Qué se cerraba y por qué

La meta de la Fase 1 es *«que ningún fallo de guardado ni de arranque pueda borrar el libro de
operaciones en silencio»*. La segunda transición de la fase la midió contra el código y encontró
que la meta **fallaba**: había tres escrituras a la nube y sólo dos pasaban por la guarda de
no-vaciado. La tercera vivía en el manejador de inicio de sesión, se recorría también cuando la
lectura de la nube **fallaba** —su `catch` devolvía `false`, indistinguible de «arriba no hay
nada»— y subía un libro vacío encima de uno completo **con el indicador en verde**.

Ficharlo como deuda lo habría blanqueado como «fase hecha». Se arregló.

## Resultados de los criterios de aceptación

Todas las cifras de esta tabla son **posteriores** al último cambio que las afecta: se
re-derivaron en este UNIFY, con el árbol en exclusiva (`HEAD^{tree}` =
`5870b9a53d56939119b647e9b64425e550ee7fb6`, idéntico antes y después de medir, y
`git status` vacío).

| Criterio | Estado | Evidencia re-medida en UNIFY |
|---|---|---|
| **AC-1** · Una sola puerta, decidida por función pura que falla cerrado | **PASS** | Exactamente **dos** `.set(` en `index.html`: `ref.set(construido.payload)` dentro de `subirALaNube` (`index.html:3205`) y `map.set` del gráfico (`3730`). Los dos caminos preguntan a `decidirSubida` (`3120`). La matriz recorre **84 combinaciones** y exige el **motivo**, no sólo el booleano |
| **AC-2** · Nadie sube un paquete que no pudo construir entero | **PASS** | `buildSyncPayload` devuelve las claves que falló; las autopruebas imprimen `subida omitida (prueba): paquete incompleto: balance-rows-7` desde una clave corrupta sembrada **en el arnés**, no sintética |
| **AC-3** · El indicador nunca dice verde sin resultado que lo justifique | **PASS** | `grep -c "setSyncUI('ok')" index.html` → **0**. `estadoSync` (`3154`) es un mapa cerrado: lo desconocido da rojo |
| **AC-4** · La clase de escrituras cerrada, dos redes disjuntas | **PASS** | `tools/cloudwrites.py` rc=0: «1 escritura a la nube, dentro de `subirALaNube`; 1 referencia de Firestore vigilada; 0 verdes escritos a mano». Fallo cerrado comprobado en copia con `index.html` vacío: **rc=2, «INSTRUMENTO ROTO: … esta vacio»** |
| **AC-5** · El censo de `catch` vacíos es un control, no un grep | **PASS** | `tools/emptycatch.py --check` rc=0 contra `.paul/baseline-catches.json`, que nombra los tolerados uno a uno. Mismo fallo cerrado rc=2 con el fichero vacío. El banco demuestra que `--check` **no escribe** |
| **AC-6** · Cada control nuevo se ha visto rojo, y el estímulo llegó | **PASS** | `tools/sabotage.py` rc=0 con **44 casos mordiendo**, **15 de este ciclo**, más el control de vacuidad en verde y el control de árbol idéntico. Cifra re-contada en UNIFY (`grep -c 'muerde:'`) |
| **AC-7** · El coste del arreglo queda escrito | **PASS** | **D-35** en `.paul/DEUDAS.md`: «un paquete incompleto bloquea TODAS las subidas y no hay salida en pantalla», con qué la reabre |

## La puerta, por sus DOS variantes

| Variante | Resultado |
|---|---|
| Manual — `bash tools/verify.sh` redirigido a fichero, rc capturado | **rc=0**, «VERDE — todo ejercido y en verde» |
| Automática — el enganche `pre-push` invocado directamente | **rc=0** |
| Comparación byte a byte de las dos salidas | **Idénticas** salvo la línea de anuncio del propio enganche (`pre-push: abriendo la puerta…`) |

La lista de la puerta tiene ahora **ocho pasos**, dos de ellos nuevos de este ciclo (**puerta
única de escritura a la nube** y **censo de `catch` vacíos**), colocados **antes** del banco de
sabotaje y **fuera** de cualquier interruptor.

## Lo que encontró la revisión adversaria de este ciclo — y está arreglado

Cuatro brazos disjuntos, con la **frase a demoler** en vez de «el código a revisar», y prohibición
explícita y por nombre de mutar nada. El de *correctness* no pudo demoler su frase. Los otros tres
**sí**, con mutantes ejecutados que sobrevivían a la puerta entera. Los tres eran bloqueantes y se
arreglaron antes de este UNIFY; cada uno dejó su **test permanente**, que hoy vuelve a morder:

1. **El fixture de la matriz ataba el contenido de la nube a su nombre de estado.** Una guarda
   falsa que mirase sólo el nombre pasaba las filas y la puerta entera. Hay filas mixtas y el
   sabotaje *«la guarda de activos se sustituye por un proxy del estado de la nube»*.
2. **El CABLE entre el productor de la marca «incompleto» y el juez no lo medía nadie.** Los dos
   extremos tenían control; cortarlos por el medio sobrevivía a todo. `subirALaNube` acepta
   dependencias inyectables y hay el sabotaje *«se corta el cable que lleva la marca de paquete
   incompleto»* (más los gemelos del cerrojo y de los activos locales).
3. **Volver `runSelfTests` asíncrona la había sacado del trinquete de tamaño sin poner nada
   rojo.** El ámbito sellado pasa a incluir `async function` (**semántica v2**, foto resellada a
   propósito) y `onScreenshotPicked` queda fichada en D-09.

Además, dos huecos del propio aparato de medición: **un `await` perdido dejaba una suite entera
sin ejercer y la puerta salía verde y sorda** (hoy hay sabotaje propio), y el interruptor
`VERIFY_INNER` saltaba el banco **en silencio** — ahora lo AVISA por pantalla. Se borró un
`VERIFY_DEGRADED` que el script anunciaba en un comentario y que **ninguna rama leía**: era
§5.1 en estado puro, un freno que sólo existía escrito.

## Qué se construyó

| Fichero | Cambio | Para qué |
|---|---|---|
| `index.html` | Modificado (+574/−…) | `decidirSubida`, `estadoSync`, `subirALaNube`, `alIniciarSesion` extraída y ejecutable, `buildSyncPayload` nombra lo que no pudo leer |
| `tools/cloudwrites.py` | **Creado** (205 líneas) | Dos redes disjuntas: por receptor de Firestore y por método `.set(`. Más el censo de verdes escritos a mano |
| `tools/emptycatch.py` | **Creado** (228 líneas) | Censo de `catch` vacíos contra foto sellada; cuenta las dos variantes; cero tolerados en el camino de subida |
| `.paul/baseline-catches.json` | **Creado** | Nombra uno a uno los `catch` vacíos tolerados, con su motivo |
| `tools/funcsize.py` | Modificado | Se extrae `localizar_funciones(js)` para compartirla en vez de duplicar el escáner; ámbito ampliado a `async function` |
| `tools/verify.sh` | Modificado | Dos pasos nuevos en la lista ÚNICA; el interruptor `VERIFY_INNER` ahora avisa |
| `tools/sabotage.py` | Modificado | 15 casos nuevos; re-anclado el caso que apuntaba a código que este ciclo eliminó |
| `tools/run_selftests.py` | Modificado | El arnés siembra una clave corrupta real para medir el eslabón PRODUCTOR |
| `.paul/DEUDAS.md` | Modificado | D-33, D-34 y D-31 cerradas con evidencia; D-35, D-36 y D-37 abiertas |

## Decisiones tomadas

| Decisión | Por qué |
|---|---|
| La nube es un **tri-estado** (`con-datos` / `vacía` / `ilegible`) más un cuarto caso (`no-consultada`) | Colapsarlo en un booleano era exactamente el defecto de D-33 |
| El fallo cerrado es **simétrico**: vale para las operaciones y para los **activos** | La asimetría entre los dos predicados ERA el defecto (§5.16). El cruce «ops sí · activos no · nube ilegible» hoy tiene fila propia con nombre propio |
| Un **cerrojo puesto no es un libro vacío**: entra como entrada propia del juez | Subir `opsAll: []` con `savedAt` fresco mientras el libro real duerme ilegible sería el mismo daño por otra puerta |
| D-31 se cierra por la **CLASE**: cero llamadas literales `setSyncUI('ok')` | La ficha nombraba un `catch`, pero había dos miembros más vivos: el callback de error vacío del `onSnapshot` y el verde incondicional del arranque |
| Se **cruza** el boundary de `funcsize.py`, dicho en voz alta | La alternativa era un segundo escáner, y dos escáneres se desincronizan a la primera. Prueba de que no cambió lo que mide: `--check` verde sin resellar |
| Se resella la foto del trinquete con **semántica v2** a propósito | Ampliar el ámbito a `async function` cambia la regla de medida; el instrumento lo declara DERIVA (rc=3) y por eso el resellado es una decisión escrita, no un trámite |

## Desviaciones respecto al plan

| Desviación | Motivo |
|---|---|
| El plan pedía **ocho** sabotajes nuevos; hay **quince** | Los tres hallazgos bloqueantes de la revisión adversaria y sus gemelos (cables del cerrojo y de los activos, `await` perdido) exigieron control propio cada uno |
| El plan pedía los cuatro veredictos «con su identificador de ejecución»; **no existe un fichero de veredictos** | Los hallazgos y su resolución están en el mensaje del commit `21e1edb` y, sobre todo, **en el código: cada uno tiene su sabotaje mordiendo hoy**. Se declara la desviación en vez de decir que el requisito se cumplió |
| El plan no preveía tocar el interruptor `VERIFY_INNER` ni borrar el `VERIFY_DEGRADED` fantasma | Salieron del brazo de *cableado*: un banco que se salta en silencio y un freno que sólo existe en un comentario son falsos verdes, y arreglarlos era correctness |

## Deudas — al libro, no a esta acta

Cerradas con evidencia: **D-33**, **D-34**, **D-31**.
Abiertas por este ciclo: **D-35** (la subida bloqueada por paquete incompleto no tiene salida en
la interfaz), **D-36** (el veredicto de las autopruebas puede imprimirse antes que sus fallos),
**D-37** (cambiar de cuenta de Google en el mismo navegador sube el libro de la anterior).
`onScreenshotPicked` añadida a **D-09**.

Fichas completas en `.paul/DEUDAS.md`, que es la lista viva.

## Lo que este ciclo NO cierra

- **La FASE 1 sigue abierta.** El cierre de un ciclo nunca autoriza el de una fase (§7). La fase
  se cierra midiendo su meta contra el código, en una transición aparte.
- **Nada de esto se ha visto en un navegador.** El commit está en local, **dos por delante** de
  `origin/main`: no está desplegado. La puerta ejerce las funciones puras en node sobre un DOM de
  mentira y **no prueba la interfaz** — y este ciclo añade un estado visual nuevo (el punto ROJO
  «No se pudo sincronizar»). Una sonda verde nunca supera a un intento real (§7 bis).
- D-18 (aviso ROJO de guardado), D-22 (el grafo que no ve `index.html`), D-26 (`funciones_vistas`)
  siguen abiertas por decisión del plan.

---
*Fase: 01-guardado-fiable · Plan: 04*
*Cerrado: 2026-08-31*

---

## ERRATA — añadida el 2026-08-31 por la TERCERA transición de la Fase 1

**«15 sabotajes de este ciclo» es falso: son 14.** El total (44 casos mordiendo) sí es correcto.
Re-derivado: `git show 96c7a3e:tools/sabotage.py | grep -c '    Caso('` → **30**, hoy **44**, y
sólo `21e1edb` tocó el fichero; ningún caso anterior desapareció. El método de re-conteo que este
acta declara (`grep -c 'muerde:'`) sólo puede producir el 44 — **el 15 no se re-derivó de nada**.
Un acta no se reescribe, así que la cifra queda arriba con esta errata al pie.
Detalle: `01-TRANSICION-3.md`, hallazgo T3-6.
