---
phase: 01-guardado-fiable
plan: 03
type: summary
closed: 2026-08-30
commits: ["96c7a3e"]
---

# Acta del ciclo 01-03 — «El cerrojo del libro ilegible»

> Un SUMMARY es un ACTA: se escribe una vez y se entierra. Las deudas de este ciclo **no** viven
> aquí, viven en `.paul/DEUDAS.md` (D-23, D-24, D-25, D-26), que es la lista viva.

## 1. Qué se cerró y por qué ahora

El cerrojo `opsIlegible`, que impide escribir encima de un libro de operaciones que no parsea, se
levantaba **antes** de confirmar que la reparación se había escrito. Era el único defecto de
correctness que impedía cerrar la Fase 1, y lo encontró el brazo de radio de impacto de la
transición del 2026-08-30 (`01-TRANSICION.md` §5), no una prueba: **el cruce de las dos
condiciones —«libro local ilegible» × «nube sin operaciones»— no lo medía nada**. Cada una tenía
su prueba y su mutante por separado; su intersección, ninguno (`CLAUDE.md` §5.5).

Registrarlo como deuda habría blanqueado la fase como «hecha» con el mecanismo de protección
desarmado dentro. Se arregló.

## 2. Reconciliación de los criterios de aceptación

| AC | Veredicto | Evidencia |
|---|---|---|
| **AC-1** Una nube vacía NO repara un libro ilegible | **PASS** | `pruebasCerrojoIlegible`, tres afirmaciones independientes (el blob sigue byte a byte, el cerrojo sigue puesto, se emitió **ese** aviso). Mutantes «el cerrojo vuelve a levantarse antes de reparar» y «una nube vacía vuelve a contar como reparación», ambos rc=1 con el texto `AC-1 el blob ilegible sigue en disco byte a byte` |
| **AC-2** Una nube con operaciones SÍ repara, y sólo entonces se levanta | **PASS** | medición **directa** de `repararLibroIlegible` (ver §4). Mutantes «la reparación buena NO levanta el cerrojo» (rc=1, `AC-2 y baja el cerrojo ella misma, sin releer el disco`) y «la reparación vuelve a pasar por la puerta y no puede escribir» (rc=1) |
| **AC-3** Si la escritura de reparación falla, el cerrojo se queda puesto | **PASS** | `pruebasReparacionFallida` con `setItem` que lanza. Mutante «la reparación levanta el cerrojo aunque la escritura falle», rc=1, texto `AC-3 el cerrojo sigue puesto tras la escritura fallida` |
| **AC-4** Las autopruebas nuevas no tocan los datos reales | **PASS** | arnés de `pruebasSincronizacion` (foto y restauración **por valor**, clave a clave) + centinelas de `tools/run_selftests.py`, que viven **fuera** de la suite. Verificado camino a camino por el brazo de falsos verdes, incluido que `pruebasReparacionFallida` repone `setItem` y `console.error` por todos los caminos. Confirmado además en el navegador real (§7) |
| **AC-5** El formato ANTIGUO también repara | **PASS** | `pruebasCerrojoIlegible`, bloque `opsData`. Mutante «el formato antiguo vuelve a reparar por la puerta», rc=1, texto `AC-5 el formato antiguo también escribe la reparación` |

## 3. Qué se construyó

- **`escribirOpsAll`** — la escritura cruda del libro, que **no** consulta el cerrojo.
- **`saveOpsAll`** — sigue siendo la puerta: si el cerrojo está puesto, avisa y devuelve `false`;
  si no, delega. Se troceó en vez de darle un parámetro «bypass», que la habría convertido en su
  propia excepción.
- **`repararLibroIlegible`** — escribe primero y **sólo baja el cerrojo si la escritura confirma**.
  Deja constancia en la consola de la reparación exitosa (ver §5, hallazgo G6-3).
- **Rama moderna de `applySyncPayload` reordenada**: la guarda de no-vaciado sigue siendo la
  primera; después el cruce del cerrojo, que con una nube sin operaciones **no repara y lo dice**.
- **Rama del formato antiguo**: también repara, y ahora mira el resultado en vez de tirarlo.
  Cierra la **clase**, no el caso (`CLAUDE.md` §5.15): un dispositivo sin actualizar no habría
  podido levantar el cerrojo jamás, porque `loadOpsAll` lo re-marcaba y `saveOpsAll` se negaba.
- **Tres funciones de autoprueba nuevas**: `pruebasCerrojoIlegible`, `pruebasReparacionFallida` y
  `pruebasPrecedenciaDeGuardas`, más el auxiliar `opsEnDisco`.
- **Diez controles positivos nuevos** en `tools/sabotage.py`, y **tres anclas rediseñadas** porque
  el arreglo las hizo desaparecer.

`applySyncPayload` pasó de 43 a 50 líneas: por debajo del presupuesto de 60, sin trocear y sin
amnistía. `funcsize.py --check` rc=0, «las mismas 12 funciones que sella la foto».

## 4. El hallazgo del propio aparato de medición

**Un sabotaje no mordió a la primera, y el defecto estaba en la prueba, no en el arreglo.**

El mutante «la reparación buena NO levanta el cerrojo» pasaba la batería entera. Causa:
`applySyncPayload` termina en `ops = loadOpsAll()`, que **vuelve a decidir el cerrojo leyendo el
disco ya reparado**. El check «y sólo entonces se levanta el cerrojo» pasaba con y sin el arreglo:
no medía la reparación, medía la relectura. Es `CLAUDE.md` §5.8 —el oráculo hereda los puntos
ciegos de quien lo escribe— y **sólo apareció porque el sabotaje se ejecutó de verdad**.

Corregido midiendo `repararLibroIlegible` **a solas**, sin pasar por la relectura. Los checks
que quedan detrás de un `applySyncPayload` se han anotado en el código como redundantes: se
conservan porque documentan el estado esperado, no porque protejan.

## 5. Los tres brazos de revisión + G6

Los cuatro **COMPLETARON** con veredicto explícito. Ninguno mutó el árbol (prohibición por nombre
en el prompt: `checkout`, `restore`, `stash`, `reset`, escrituras).

### Brazo 1 — correctness del reordenamiento (Fable)
- **F1 «ningún camino levanta el cerrojo sin escritura confirmada»: CONFIRMADA.** Censo completo
  de las asignaciones de `opsIlegible` del fichero, no sólo las del diff, incluido
  `migrateOpsToGlobal` y el arranque.
- **F2 «ningún camino lo deja puesto tras una reparación buena»: CONFIRMADA.**
- **F3 «las dos ramas quedaron simétricas»: REFUTADA.** → **D-24**. La moderna decide con el
  cerrojo de memoria; la antigua lo re-deriva del disco. Si el libro se corrompe **después** de
  cargar la app, la moderna lo pisa **sin copia de rescate**. Anterior al ciclo; diferido con
  motivo escrito, atado a la Fase 3.
- Limpieza: la rama antigua tiraba el resultado de la reparación → **arreglado**. Asimetría de
  avisos con una nube antigua vacía → anotada dentro de D-24.

### Brazo 2 — falsos verdes (Fable)
- **F1 «cada check pasaría con el arreglo y moriría sin él»: REFUTADA**, tres casos reales:
  - el contador de «se avisó de que no había con qué reparar» casaba con **cualquier**
    `console.error`, y la relectura final emite uno siempre → **arreglado exigiendo el mensaje**;
  - «el fallo de reparación se registra» lo satisfacía el rechazo del `saveOpsAll` de la línea
    anterior → **arreglado reordenando**, el check va antes de tocar la puerta;
  - «el guardado sigue negándose» no distinguía «me negué por el cerrojo» de «no pude escribir»,
    porque la escritura estaba rota a propósito → **arreglado sacándolo del `try`**.
- **F2 «ninguna aserción casa de más»: REFUTADA en parte.** `parseOpsBlob(...).length` **lanzaba**
  si la reparación regresaba: el hallazgo habría salido por el canal de **«instrumento roto»
  (rc=2)** en vez del de hallazgo (rc=1), tapándolo. Es la trampa de §4.3 que este repo ya pagó el
  2026-08-29 → **arreglado con `opsEnDisco()`**, que devuelve `'ilegible'` en vez de lanzar.
- **F3 «no tocan los datos reales del operador»: CONFIRMADA**, verificada camino a camino.

### Brazo 3 — calidad del oráculo (Fable)
- **F1 literal CONFIRMADA** (los mutantes no caen todos en la misma rama), **pero refutada como
  garantía de cobertura: 3 de 6 piezas del arreglo no tenían control positivo propio.**
  - la reparación podría volver a pasar por la puerta (bloqueo permanente del libro) → **mutante
    añadido**;
  - la rama del formato antiguo nunca se había visto roja → **mutante añadido**;
  - la **precedencia** de las dos guardas no la medía nada → ver abajo.
- **F2 «el caso rediseñado sigue midiendo lo mismo»: CONFIRMADA.**
- **F3 «ningún ancla frágil o ambigua»: CONFIRMADA en lo que importa** — las seis son únicas hoy,
  y una rotura sale como **«BANCO ROTO»**, nunca como «no muerde» ni como verde.
- Limpieza: los textos esperados eran laxos (`"AC-1"` casa con cualquier fallo de ese apartado,
  incluso de otro ciclo) → **endurecidos al nombre completo del check**.

### G6 — revisión ligera del diff
- **La precedencia de las guardas seguía sin control positivo.** Mi primer intento de mutante
  **estaba mal construido**: movía el aviso junto con la guarda, así que seguía sonando y el caso
  salía «NO MUERDE». Reconstruido invirtiendo de verdad el orden de las dos ramas, generando el
  texto desde el propio fichero para no transcribirlo a mano. Muerde con rc=1.
  El caso que ya existía **no** lo cubría: quita la guarda (presencia), no la reordena
  (precedencia) — §5.11, presencia ≠ precedencia.
- **El aviso de reparación EXITOSA se había perdido** con el reordenamiento: los dos caminos de
  fallo avisaban y el de éxito no dejaba rastro, y por D-23 la consola es hoy el único canal que
  existe → **restituido, con su check y su mutante propio** (§5.6: cubrir el mecanismo no cubre
  su aviso).
- Una reparación descarta en silencio lo tecleado con el cerrojo puesto → **D-25**.
- `funciones_vistas` es una cifra sellada que `--check` no compara; estuvo en **153 cuando el
  fichero tenía 162** y la puerta seguía verde → **D-26**.

## 6. Salida literal de la puerta

`bash tools/verify.sh` → **rc=0**, con el árbol limpio y en exclusiva:

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

`python3 tools/sabotage.py` → **rc=0**, «Todos los controles de la puerta muerden»,
**30 controles**, `arbol identico antes y despues (22aebc22e683)`.

Los diez del 01-03, con su rc literal:

```
  OK    muerde: el cerrojo vuelve a levantarse antes de reparar (rc=1)
  OK    muerde: una nube vacia vuelve a contar como reparacion (rc=1)
  OK    muerde: la reparacion levanta el cerrojo aunque la escritura falle (rc=1)
  OK    muerde: la reparacion buena NO levanta el cerrojo (rc=1)
  OK    muerde: la reparacion vuelve a pasar por la puerta y no puede escribir (rc=1)
  OK    muerde: el formato antiguo vuelve a reparar por la puerta (rc=1)
  OK    muerde: se invierte la PRECEDENCIA de las dos guardas del cruce (rc=1)
  OK    muerde: la reparacion buena deja de dejar constancia (rc=1)
  OK    muerde: saveOpsAll deja de consultar el cerrojo (rc=1)
  OK    muerde: el sync vuelve a deduplicar por huella y se come operaciones (rc=1)   [ancla rediseñada]
```

**Las dos variantes verificadas** (`CLAUDE.md` §4.2): a mano, y el enganche `pre-push`, que
imprimió `pre-push: abriendo la puerta…` y la misma lista en verde antes de dejar salir el push.

## 7. Verificación en el navegador real

Sobre `https://californiakid91.github.io/food/` con `96c7a3e` publicado. Confirmado **antes** de
mirar nada que Pages servía la versión nueva: huella `661acd6b17aed4808c9d8367a2cd72b4`, idéntica
a la local (el primer intento devolvió la anterior; se reintentó hasta que coincidió).

| Punto | Resultado |
|---|---|
| El navegador tiene el código nuevo (`typeof repararLibroIlegible === 'function'`) | **PASS** |
| `?selftest=1` imprime «✅ Autopruebas OK» | **PASS** |
| Operaciones y carteras idénticas antes y después de `?selftest=1` | **PASS** — **90 operaciones y 4 carteras**, contadas por el operador en la consola leyendo `balance-ops` y `balance-meta-v2` directamente del almacenamiento, antes y después de la corrida. Las mismas cifras que el 01-02, así que el ciclo tampoco movió nada entre medias. Éste es el fallo que estuvo vivo en producción —decir «OK» mientras borraba—, y por eso «no borró» y «dijo OK» se comprueban por separado |

## 8. Desviaciones respecto al PLAN

| Desviación | Motivo |
|---|---|
| El plan pedía **cinco** sabotajes nuevos y **dos** anclas rediseñadas; salieron **diez** y **tres** | Los brazos de revisión encontraron tres piezas del arreglo sin control positivo (la escritura cruda, la rama antigua, la precedencia) y un aviso sin mutante. Se añadieron en vez de diferirse: un control que no se ha visto rojo no se ha visto |
| El plan no contemplaba tocar las pruebas ya escritas | Cuatro checks pasaban con y sin el arreglo. Arreglar el oráculo era condición para que los AC significasen algo |
| Se restituyó un `console.warn` que el reordenamiento había eliminado | No estaba en el plan porque el plan no vio que lo eliminaba. §5.6 |
| No se troceó `applySyncPayload` | El plan lo preveía **sólo si** cruzaba las 60 líneas. Quedó en 50; trocear sin necesidad habría sido deriva |

## 9. Lo que este ciclo NO hizo (scope limits respetados)

No fusiona `ops` locales con los de la nube (Fase 3). No construye salida de interfaz para un
cerrojo atascado (Fase 5). No cierra D-01, D-15, D-18, D-21 ni D-22. No toca los cuatro `catch`
vacíos restantes. No verifica si `firestore.rules` está desplegado. **No cierra la Fase 1**: eso
exige repetir la transición completa sobre el diff resultante.

Boundaries respetadas: `vaciariaElLibro`, `tieneOperaciones` y `opsDelDocumento` intactos —este
ciclo los **usa**; `rescatarOpsIlegible`, `dedupeOps`, `opFingerprint`, `parseNum` y familia,
intactos; `index.html` sigue siendo un fichero único sin build ni dependencias nuevas.

## 10. Decisiones tomadas

| Decisión | Motivo |
|---|---|
| Trocear `saveOpsAll` en vez de darle un parámetro «bypass» | Un «bypass» convierte a la puerta en su propia excepción, y la excepción acaba usándose por comodidad |
| La reparación llama a la escritura **cruda**, no a la puerta | Si pasara por la puerta, con el cerrojo puesto no podría escribir jamás: bloqueo permanente. Tiene mutante propio desde este ciclo |
| Cerrar la CLASE: el formato antiguo también repara | Cerrar sólo el caso moderno dejaba el mismo defecto vivo por el otro camino (§5.15) |
| Los checks enmascarados por la relectura se conservan **anotados**, no se borran | Documentan el estado esperado; borrarlos perdería la intención. Lo que no se hace es confiar en ellos |
| Los cuatro hallazgos de correctness ajenos al ciclo se difieren **por escrito**, no se arreglan aquí | Arreglar D-24 exige releer el disco en cada guardado y cambiar el contrato de `escribirOpsAll` recién fijado; D-26 exige cambiar qué compara `--check`, que el propio instrumento declara **deriva (rc=3)**. Hacerlo dentro de un ciclo que va de otra cosa sería mover la vara sin plan |
