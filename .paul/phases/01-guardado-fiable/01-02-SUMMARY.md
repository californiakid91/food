---
phase: 01-guardado-fiable
plan: 02
subsystem: sync
tags: [firestore, localStorage, dedupe, ids, guards]

requires:
  - phase: 01-01
    provides: guardado honesto y carga incondicional del libro de operaciones
provides:
  - identificadores de operación sin colisión dentro de un extracto
  - deduplicación de sincronización por identificador Y huella (`dedupeOpsById`)
  - guardas simétricas de no-vaciado del libro (`vaciariaElLibro` + `opsDelDocumento`)
affects: [03-sync-que-fusiona, 04-correccion-fiscal-fifo]

tech-stack:
  added: []
  patterns:
    - "Un único juez para dos guardas simétricas, no el mismo criterio escrito dos veces"
    - "Fallar CERRADO cuando no se puede leer la nube; se ve en naranja, no en verde"
    - "Los controles que vigilan a las autopruebas viven en el arnés, fuera de la suite"

key-files:
  created: []
  modified: [index.html, tools/run_selftests.py, tools/sabotage.py, .paul/DEUDAS.md]

key-decisions:
  - "Un único juez para las dos guardas de no-vaciado"
  - "Fallar CERRADO si no se puede leer la nube"
  - "Los controles de las autopruebas viven en el ARNÉS, no dentro de la suite"
  - "Anchura fija de 6 caracteres en el contador, con invariante que la vigila"

patterns-established:
  - "Toda guarda nueva nace con su sabotaje que demuestra que muerde"
  - "El límite aceptado a propósito se anota en DEUDAS.md, no se esconde"

completed: 2026-08-30
duration: —
---

# Fase 01 Plan 02: Sincronización que no destruye · ACTA

**La sincronización ya no puede fundir dos operaciones distintas en una ni vaciar el libro de
operaciones de toda la flota de dispositivos.**

## Criterios de aceptación

Medidos con `tools/verify.sh` ejecutado fresco sobre `e0beab9`, árbol limpio antes y después
(0 ficheros modificados en ambos extremos). **rc=0.**

| AC | Descripción | Estado | Evidencia |
|----|-------------|--------|-----------|
| AC-1 | Los identificadores no colisionan dentro de un extracto | **PASS** | 6 invariantes en `runSelfTests()`: 500 identificadores en ráfaga sin repetidos, monotonía temporal, anchura constante. Sabotajes `los identificadores vuelven a poder chocar` (rc=1) y `el identificador puede cambiar de anchura` (rc=1) |
| AC-2 | Dos operaciones idénticas del mismo día sobreviven a la sincronización | **PASS** | 16 invariantes, incluido uno **extremo a extremo** sobre `applySyncPayload`, no sólo sobre `dedupeOpsById`. Sabotaje `el sync vuelve a deduplicar por huella y se come operaciones` (rc=1) |
| AC-3 | El formato antiguo sigue consolidándose | **PASS** | 7 invariantes; `dedupeOps` por huella sigue vivo y ejercido en el camino `opsData`. Sabotaje `la guarda de subida vuelve a ser ciega al formato antiguo` (rc=1) |
| AC-4 | Nadie vacía el libro de nadie | **PASS** | 18 invariantes sobre `vaciariaElLibro` y `opsDelDocumento`, más dos que afirman que **la misma función** se usa en las dos guardas. Sabotajes `se quita la guarda de no-vaciado al aplicar` y `...al subir` (rc=1 ambos) |

**47 invariantes** etiquetados por AC, de una suite total de 57. Cada guarda del ciclo tiene su
sabotaje que la ha visto roja con rc y mensaje literales.

## Salida de la puerta

```
PUERTA — food
  OK    index.html presente y no vacio
  OK    sintaxis de index.html
  OK    autopruebas (runSelfTests)
  OK    trinquete de tamano de funciones
  OK    banco de sabotaje (los controles muerden)
  OK    lint de tools/
VERDE — todo ejercido y en verde.
```

Banco de sabotaje: **26 controles**, todos mordiendo. Incluye el control de vacuidad (sin
sabotaje la puerta está verde), el de orden del veredicto (un hallazgo real da rc=1, no rc=2),
el de deriva (rc=3), el de instrumento roto (rc=2) y el de árbol idéntico antes y después.

## Qué se construyó

| Tarea | Qué hace | Commit |
|---|---|---|
| Task 1: Identificadores que no chocan | Contador monotónico de anchura fija (6 caracteres) entre la marca de tiempo y el azar. Medido antes: el 10,2 % de los extractos de 100 operaciones traía al menos una colisión | `77f8cef` |
| Task 2: Deduplicar por identificador Y huella | `dedupeOpsById` para la rama `data.opsAll`. `dedupeOps` por huella se queda intacto para la migración y el formato antiguo, con el porqué escrito en el código | `77f8cef` |
| Task 3: Nadie vacía el libro de nadie | `vaciariaElLibro` (juez único) + `opsDelDocumento` (lectura única del documento), cableados a las DOS guardas: la de subir y la de aplicar | `77f8cef` |
| Arreglos de la revisión del diff | Ocho hallazgos, ver abajo | `56795eb` |

## Boundaries — respetados

- `dedupeOps` y `opFingerprint`: **definiciones intactas**. Comprobado en el diff: lo único que
  cambió a su alrededor es un comentario que explica por qué conviven los dos criterios, y la
  sustitución del uso en la rama `opsAll` (que es exactamente lo que pedía la Task 2).
- Formato de los identificadores ya guardados: no se migra ninguno.
- `buildSyncPayload`, resolución por `savedAt`, `computeFifo`, `exportTaxExcel`, `parseNum` /
  `numIn` / `parseLooseNum`: sin tocar.
- Sin dependencias nuevas ni build system. `index.html` sigue siendo un fichero único.

## Desviaciones del plan

Ninguna tarea se desvió. Lo que **no estaba en el plan** son los ocho arreglos que destapó la
revisión del diff, todos aplicados en `56795eb`:

| # | Qué era | Cómo se cerró |
|---|---|---|
| 1 | `?selftest=1` **borraba el libro real del usuario y las carteras**, e imprimía «✅ Autopruebas OK» | Arreglado + control en el arnés (fuera de la suite) + sabotaje |
| 2 | La guarda de subida era ciega al formato antiguo de la nube | Arreglado + invariante + sabotaje |
| 3 | La lectura de la nube rompía el push sin conexión | Falla **cerrado** y se ve → deuda **D-17** |
| 4 | Al omitir el push, el indicador seguía en verde | Estado naranja «Cambios sin subir» → deuda **D-16** |
| 5 | La comprobación de restauración contaba claves, no valores | Arreglado + sabotaje |
| 6 | La guarda de subida sólo estaba probada por presencia, no por precedencia | Deuda **D-15**, afinada |
| 7 | El contador podía desbordar su anchura e invertir el orden del FIFO | Anchura fija 6 + invariante de anchura |
| 8 | Las deudas estaban sin commitear | Commiteadas |

**El más caro (el 1) no era de este ciclo:** venía del 01-01, había pasado su revisión, y estaba
vivo en producción. Lo destapó revisar el diff que lo *extendía*.

Al poner el banco al día, **dos sabotajes no mordían**: uno saboteaba la aserción en vez del
mecanismo, y otro apuntaba a un invariante que no existía. Otra vez la misma lección: *cuando el
trabajo mecánico sale limpio, el defecto está en el instrumento que lo mide.*

## Brazos de revisión

- **G6 · `/code-review` del diff del ciclo (correctness):** ejecutado. **8 hallazgos**, todos los
  de correctness arreglados en `56795eb`; tres límites conocidos diferidos por escrito a
  `.paul/DEUDAS.md` (D-15, D-16, D-17). Ningún hallazgo de correctness quedó sin atender.
- **G7 · CRG blast-radius** y **G8 · `/security-review`:** son brazos **de fase**, no de ciclo.
  Corresponden a la transición de la Fase 1, no a este acta.

## Deudas nuevas

Subidas a `.paul/DEUDAS.md` en el mismo commit que las originó, con su origen citado:

- **D-15** · La guarda de subida está comprobada por presencia, no por precedencia (afinada).
- **D-16** · La guarda de subida deja de sincronizar los activos, no sólo el libro.
- **D-17** · Sin conexión y sin caché, un dispositivo sin operaciones no sube nada.

## Lo que este acta NO puede afirmar

`verify.sh` ejerce funciones puras en node sobre un DOM de mentira. **No prueba la interfaz ni
Firestore.** Nadie ha abierto todavía este ciclo en un navegador, y este ciclo toca el camino que
escribe los datos reales.

Además, y esto es lo urgente: **el fallo nº 1 sigue vivo en producción.** Abrir
`https://californiakid91.github.io/food/?selftest=1` en la versión desplegada borra el libro de
operaciones y las carteras. Está arreglado en local pero **sin desplegar**. No abrir esa dirección
con `?selftest=1` hasta que se haga push.

## Pendiente antes de cerrar la fase

1. `git push` (el enganche `pre-push` vuelve a correr la puerta).
2. Verificación a mano en la app desplegada, **recargando dos veces** (el service worker sirve la
   versión anterior en la primera): guardar y ver el punto verde; confirmar que el estado naranja
   **no** aparece en uso normal; `?selftest=1` debe decir OK **y** dejar los datos intactos.
3. Heredada del 01-01 y todavía sin comprobar en el navegador: que el aviso de guardado salga en
   **rojo** cuando el guardado falla.

---
*Fase: 01-guardado-fiable, Plan: 02*
*Cerrado: 2026-08-30*
