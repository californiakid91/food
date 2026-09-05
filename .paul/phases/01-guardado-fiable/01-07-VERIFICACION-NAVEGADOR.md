# Verificación en navegador — ciclo 01-07

**Estado: COMPLETA** (2026-09-05). Los nueve puntos en PASS, uno con observación (O-1).
Un hallazgo de correctness encontrado ANTES de empezar la lista: **D-54**.

## Preparación (hecha por el asistente, 2026-09-05)

| Paso | Resultado |
|---|---|
| Puerta manual `tools/verify.sh` | **rc=0**, once pasos en verde |
| `index.html` idéntico antes y después de la puerta | `5b3807ddb7edf1f8bd7959bda7773901` en ambas |
| Push a `origin/main` | `685b44b..42ee677`, con el enganche `pre-push` ejerciendo la puerta otra vez (rc=0) |
| Pages sirve la versión nueva | **SÍ**. Huella descargada `5b3807ddb7edf1f8bd7959bda7773901`, idéntica a la local. Los **dos primeros intentos** devolvieron todavía la anterior (`66e6dd20…`) |

Se confirma la huella ANTES de mirar la pantalla, como en las cuatro pasadas previas.

## Puntos a ejercer — AC-9

URL: `https://californiakid91.github.io/food/` — **recargar dos veces** (el service worker
sirve la versión anterior en la primera).

| # | Punto | Cómo | Resultado | Evidencia |
|---|---|---|---|---|
| 1 | El navegador tiene el código nuevo | en consola: `typeof decidirBajada === 'function'` | **PASS** | devolvió `true`. Comprobado por una función NUEVA, no por el aspecto de la pantalla |
| 2 | Recuento ANTES | en consola: `JSON.parse(localStorage.getItem('balance-ops')).length` y carteras en pantalla | **ANOTADO** | **90 operaciones y 5 carteras**. Las MISMAS cifras que la pasada del 01-06 |
| 3 | `?selftest=1` imprime «✅ Autopruebas OK» | abrir con el parámetro y leer la consola | **PASS** | leído en la consola por el operador |
| 4 | Recuento DESPUÉS, idéntico | mismo comando que el punto 2 | **PASS** | **90 operaciones y 5 carteras**, idénticas al punto 2. Cifras ANOTADAS, no heredadas de un «ok» |
| 5 | Guardar sigue funcionando tras las autopruebas | cambiar un valor **en la misma carga** que ejecutó `?selftest=1` | **PASS** | «Guardado» con tick **VERDE** arriba. Es el control de R-2 en el sitio real: sin el `try/finally` del reloj falso, la página habría dejado de guardar en silencio el resto de la sesión |
| 6 | Alta de cartera | crear una cartera nueva | **PASS** | creada «sin problema» según el operador. El total pasa de 5 a **6 carteras**: la cifra cambia porque el operador la cambió, no por un fallo |
| 7 | Borrado de operación | botón rojo `×` de una fila del historial (`deleteOp`) — uno de los dos sitios operados este ciclo | **PASS** | el recuento bajó de **90 a 89**, leído en `localStorage` DESPUÉS del gesto. El borrado llegó al libro, no sólo a la pantalla. Aviso mostrado: no reportado |
| 8 | Interruptor de objetivos | casilla «Con % objetivo» (`onUseTargetsToggle`) — el otro sitio operado | **PASS con observación** | marcado y desmarcado sin error. **No pinta nada** en el camino de éxito: es lo escrito (sólo avisa si `saveMeta()` falla). Persistencia comprobada aparte. Ver O-1 |
| 9 | **Estado del indicador de sincronización** | mirar el puntito y decir su color | **VERDE**, REPORTADO explícitamente | tras los gestos, el puntito está en verde. El naranja del arranque (D-50) se deshizo solo al guardar, como estaba previsto. **Es la primera pasada en que este punto se reporta**: en el 01-06 quedó sin reportar |

El punto 9 va aparte y se reporta **explícitamente**: quedó sin reportar en la pasada del 01-06 y
no se hereda de que el resto fuera bien.

## Lo que esta pasada NO comprueba

- El aviso ROJO del **guardado local** fallido: sigue siendo **D-18**. Exige agotar el
  almacenamiento del navegador con el libro real delante.


## Hallazgo en el punto 0 — antes de empezar la lista

Al abrir la app desplegada, **lo primero** que apareció fue el naranja «Cambios sin subir: este
dispositivo **no tiene operaciones** y no se pisa el libro de la nube», en un dispositivo con **90
operaciones**. El operador preguntó si era normal.

**Causa DEMOSTRADA, no supuesta.** En la consola del dispositivo del operador:

```
JSON.parse(localStorage.getItem('balance-meta-v2')||'{}').savedAt   →   undefined
```

Sin marca de tiempo local, `decidirBajada` entra por la rama `reloj-desconocido`: hay datos que
proteger y no hay desempate posible, así que **no aplica** el documento y avisa. Es **D-50**, el
coste declarado del ciclo, y es el comportamiento QUERIDO: quedarse quieto y decirlo, antes que
dejar ganar a la nube y empobrecer el libro en verde.

| Parte | Veredicto |
|---|---|
| **Comportamiento** (no aplicar, avisar en naranja, no perder nada) | **CORRECTO y previsto** — D-50 |
| **Texto del aviso** | **DEFECTO** — atribuye una causa falsa: **D-54** |

El texto es un hallazgo de correctness y se arregla dentro de este ciclo. El comportamiento no se
toca.

**El despliegue no pierde datos**, y el estado se deshace solo en cuanto el operador guarde algo una
vez: eso vuelve a poner el reloj local en hora.


## O-1 · Observación del operador: el interruptor de objetivos no confirma nada

**Lo que vio:** «marco y desmarco y no pasa nada con el puntito, pero al cambiar de cartera es
cuando parece que se sincroniza».

**Contrastado con el código** (`onUseTargetsToggle`, `index.html`): es el comportamiento escrito.
El camino de ÉXITO guarda, programa la subida y **no pinta nada**; sólo hay aviso en el camino de
FALLO («No se pudo guardar»). Y el puntito no cambia porque ya estaba verde: verde → verde no se ve.

**Lo que sí queda como asimetría de la capa de aviso:** `guardarTodo` confirma con «Guardado ✓» y
este camino, que también modifica los datos del operador, **calla**. No se pierde nada; la app
confirma en un sitio y no en otro para acciones del mismo tipo. Se ficha, no se arregla aquí.

**No se da por bueno sin medirlo:** «no pasa nada» podría ser «guardó en silencio» o «no guardó».
Se pidió la comprobación de persistencia en `localStorage` en vez de suponerla. Con la casilla
marcada, el disco devuelve `{id:'p1779839499052qkfo', name:'🤖 Robótica', useTargets: true}`:
**guardó en silencio**. Queda fichado como **D-55**.

## Resultado de la pasada

**Nueve de nueve en PASS**, uno con observación. Lo que esta pasada demuestra que las pruebas fuera
del navegador no demostraban:

- las autopruebas se ejecutan en el navegador real **sin tocar el libro** (90 → 90, cifras anotadas);
- **guardar sigue funcionando después de ellas**, en la misma carga de página;
- los **dos sitios operados por el ciclo** funcionan sobre datos reales: el borrado bajó el libro de
  90 a 89 en disco, y el interruptor persistió su cambio;
- el **naranja del arranque se deshace solo** al guardar una vez, como D-50 predecía;
- el indicador de sincronización acabó en **VERDE**, y esta vez se reporta.

Lo que NO demuestra, y se dice: el aviso **rojo del guardado local fallido** sigue sin verse nunca
en un navegador (**D-18**), porque exige agotar el almacenamiento con el libro real delante.
