# Handoff — ciclo 01-02, APPLY terminado, UNIFY pendiente

Fecha: 2026-08-29. Escrito porque el operador tenía que irse, no porque hubiera un problema.

## Dónde está esto exactamente

- **Fase 1** «Guardado que no miente». Plan `01-02` **ejecutado y revisado**, **sin acta** y
  **sin desplegar**.
- Commits: `77f8cef` (las tres tareas del plan) y `56795eb` (los arreglos de la revisión del diff).
- Árbol limpio. `tools/verify.sh` en **rc=0**, con **26 controles de sabotaje** en verde.
- **NO se ha hecho push.** Es deliberado, ver abajo.

## Lo primero al volver: decidir el push

Hay dos cosas en tensión y la decisión es del operador:

1. **A favor de desplegar ya:** `56795eb` arregla un fallo que está VIVO en producción. Abrir
   `https://californiakid91.github.io/food/?selftest=1` en el navegador **borraba el libro de
   operaciones y la lista de carteras**, imprimiendo «✅ Autopruebas OK». Reproducido ejecutando,
   no razonado. Mientras no se despliegue, ese `?selftest=1` sigue siendo peligroso: **no lo
   abras en producción hasta desplegar.**
2. **A favor de esperar:** este ciclo toca el camino que escribe los datos reales
   (sincronización) y **nadie lo ha abierto todavía en un navegador**. La puerta ejerce funciones
   puras en node; no prueba la interfaz ni Firestore.

Recomendación: `git push` (el enganche `pre-push` vuelve a correr la puerta), y acto seguido la
verificación manual de abajo, sin dejarla para otro día.

> Si la máquina es nueva, el enganche no viaja en el repo: `tools/install-hooks.sh`.

## Verificación manual que se debe (recargar DOS veces, el service worker sirve la anterior)

De este ciclo:
- Guardar algo y ver el punto **verde** «Sincronizado».
- El estado **naranja** «Cambios sin subir» es nuevo. Se ve cuando el dispositivo no tiene
  operaciones y la nube sí. Difícil de provocar a mano; basta con confirmar que en uso normal
  **no** aparece.
- `?selftest=1` en el navegador real: tiene que decir «✅ Autopruebas OK» **y** dejar los datos
  intactos. Hacerlo sólo DESPUÉS de desplegar.

Heredada del 01-01 y todavía pendiente:
- Que el aviso de guardado salga en rojo cuando el guardado falla.

## Qué hizo el ciclo

1. **Identificadores que no chocan.** Contador monotónico de ancho fijo (6 caracteres), detrás de
   la marca de tiempo y delante del azar. Medido antes: el 10,2 % de los extractos de 100
   operaciones traía una colisión.
2. **La sincronización ya no funde dos compras iguales.** `dedupeOpsById` exige identificador Y
   huella. El criterio por huella sola se queda en la migración y en el formato antiguo.
3. **Nadie vacía el libro de nadie.** Un único juez, `vaciariaElLibro`, más una única lectura del
   documento, `opsDelDocumento`, cableados a las DOS guardas: la de subir y la de aplicar.

## Lo que encontró la revisión del diff (todo arreglado en `56795eb`)

| # | Qué era | Estado |
|---|---|---|
| 1 | `?selftest=1` borraba el libro real del usuario y decía OK | arreglado + control en el arnés + sabotaje |
| 2 | La guarda de subida era ciega al formato antiguo de la nube | arreglado + invariante + sabotaje |
| 3 | La lectura de la nube rompía el push sin conexión | falla CERRADO y se ve → **D-17** |
| 4 | Al omitir el push el punto seguía verde | estado naranja nuevo → **D-16** |
| 5 | La comprobación de restauración contaba claves, no valores | arreglado + sabotaje |
| 6 | La guarda de subida sólo está probada por presencia | **D-15**, afinada |
| 7 | El contador podía desbordar su anchura e invertir el FIFO | ancho 6 + invariante de anchura |
| 8 | Las deudas estaban sin commitear | commiteadas |

**Dos lecciones nuevas, las dos sobre el aparato de medición, no sobre el código:**

- El fallo más caro del ciclo (el 1) **no era del ciclo**: venía del 01-01, había pasado su
  revisión, y estaba vivo. Lo destapó revisar el diff que lo *extendía*.
- Al poner el banco al día, **dos sabotajes no mordían**: uno porque saboteaba la aserción en vez
  del mecanismo, y otro porque no existía el invariante que debía matar. Otra vez: *cuando el
  trabajo mecánico sale limpio, el defecto está en el instrumento*.

## Siguiente acción concreta

`/paul:unify .paul/phases/01-guardado-fiable/01-02-PLAN.md`

Los 4 AC del plan están en PASS con autopruebas ejecutables y sabotaje que las respalda. El acta
tiene que recoger, además de los AC, las desviaciones: los siete arreglos de la revisión que no
estaban en el plan, y las tres deudas nuevas (D-15 afinada, D-16, D-17).

**No hace falta nada de la conversación anterior:** todo está en los commits, en
`.paul/DEUDAS.md` y en este fichero. Limpiar contexto antes de seguir.
