# Verificación en NAVEGADOR — ciclo 01-08

**Fecha:** 2026-09-06 · **Commit publicado:** `c106225` · **App:** https://californiakid91.github.io/food/

La puerta `tools/verify.sh` ejerce las funciones puras en node sobre un DOM de mentira. **No prueba
la interfaz.** Este ciclo toca pantalla, así que sin esta pasada no está verificado (§7 bis).

## Antes de mirar nada: ¿estoy mirando la versión que creo?

Dos comprobaciones independientes, en este orden, ANTES de pedirle nada al operador:

1. **Lo que sirve Pages es el fichero de este ciclo.** Descargado y comparado por **huella**, no por
   aspecto: `64e6e29462fc48b4d7876b14bf514b07`, idéntica a la local. Los **dos primeros intentos
   devolvieron todavía la anterior** (`9459b0fc…`), como en las cuatro pasadas anteriores; coincidió
   al tercero. Re-confirmado después por una segunda descarga independiente.
2. **El navegador del operador tiene el código nuevo**, afirmado por una FUNCIÓN y no por el aspecto
   de la pantalla: `typeof soltarFreno` → `"function"`. `soltarFreno` **nace en este ciclo**, así que
   es prueba de identidad: la versión anterior no puede satisfacerla.

## Resultados

| Punto | Resultado | Evidencia |
|---|---|---|
| El navegador tiene el código nuevo | **PASS** | `typeof soltarFreno === 'function'` en consola |
| `?selftest=1` imprime «✅ Autopruebas OK» | **PASS** | leído en la consola del operador |
| `?selftest=1` deja los datos INTACTOS | **PASS** | **89 operaciones**, `JSON.parse(localStorage.getItem('balance-ops')).length` → `89`, la misma cifra que el propio log de sincronización contaba mientras las pruebas corrían. **Cifra anotada** |
| Guardar sigue funcionando DESPUÉS de las autopruebas | **PASS** | el operador cambió un valor en la pestaña normal y el aviso salió en **VERDE** |
| **El aviso del camino de nube nombra su CAUSA y sus CIFRAS** | **PASS** | `sync-status.textContent` → `'Cambios sin subir (documento NO más nuevo (1788726184823 <= 1788726184823) con 89 operaciones locales que proteger). Tus datos siguen guardados en este dispositivo.'` Es lo que el ciclo construyó, visto en el navegador real: no un color desnudo |
| El juez de bajada protege el libro por los DOS caminos | **PASS** | Consola: `[SYNC] documento de la nube NO aplicado: …` desde `pullFromFirestore` (arranque, vía `alIniciarSesion`) **y** `[SYNC] cambio de la nube NO aplicado: …` desde la escucha en vivo. Dos caminos, un solo criterio |
| **El puntito queda NARANJA sin haber nada pendiente** | **HALLAZGO — D-67 confirmada** | ver abajo |
| El aviso ROJO del guardado local fallido | **NO COMPROBADO** | sigue siendo **D-18**. Exige agotar el almacenamiento del navegador con 89 operaciones reales delante |
| El NARANJA del freno de la nube (`nube-pendiente`) | **NO COMPROBADO** | exige un libro entrante que no quepa. No se improvisa contra los datos reales del operador; se puede provocar con dependencias falsas como en la tercera pasada |

## El hallazgo: D-67, ahora medida donde importa

`sync-dot.title` → `'Cambios sin subir'`, con **las dos marcas de tiempo idénticas**
(`1788726184823 <= 1788726184823`). Nube y dispositivo están al día: **no hay nada pendiente de
subir**, y aun así el operador ve naranja. Aparece por los dos caminos, así que no es del arranque.

La ficha de D-67 decía «reproducida ejecutando, **no re-verificada por el orquestador**». Ahora está
confirmada **en la app desplegada, leída de la consola del operador**. Sube de prioridad: un aviso
que salta tras cada sincronización correcta **enseña a ignorar el único aviso que hay**, que es lo
contrario de la meta de esta fase.

**Distinción que la medición deja clara, y que importa para no arreglar lo que no es:** lo que falla
es el **VEREDICTO del empate**, no la capa que lo pinta. La capa de aviso —lo que este ciclo
construyó— funciona: nombra su causa y sus cifras. D-67 es del juez.

## Veredicto

**El ciclo 01-08 está verificado en el navegador.** Cinco puntos en PASS, dos no comprobados y
declarados como tales (no heredados de que el resto fuera bien), y un hallazgo que **no es una
regresión de este ciclo**: es una avería preexistente que esta pasada convirtió de sospecha en
medición.
