# Acta del ciclo 01-07 — «Cerrar la bajada de la nube»

**Fase 1 · Guardado que no miente.** APPLY: `42ee677` (2026-09-01). Verificación en navegador,
arreglo de D-54 y cierre: 2026-09-05 (`4d3dde3`, `8087530`, `4b9bf4e`, `892d936`, `493d635`).

**Deudas que cierra:** D-45, D-46, D-27, D-29, D-30, D-54.
**Deudas que abre:** D-48 a D-53 (del APPLY), D-55, D-56, D-57 (de la verificación y del cierre).

---

## Qué se construyó

Un solo juez, `decidirBajada`, gobierna **los dos caminos** por los que la nube entra: el arranque y
la escucha en vivo, que hasta ahora tenía su propio desempate escrito aparte. «Hay datos que
proteger» pasa a sumar **dos** primitivos —el libro de operaciones, que era lo que faltaba, y los
activos, que era lo único que se miraba—. `hasRealLocalData` conserva su semántica porque alimenta
además la guarda de activos de la subida: unificarla la habría apagado.

Tres cosas más hicieron falta para que el cierre no fuera **ficticio**:

- el reloj del sync deja de borrarse al aplicar (D-30, cruce de boundary de Fase 3 **declarado**);
- la rama del **reloj desconocido**, sin la cual el arreglo no habría protegido a nadie el día del
  despliegue, porque todo dispositivo ya sincronizado llega con la marca de tiempo borrada;
- la bajada devuelve un **veredicto**, no un booleano que colapsaba «aplicado» y «rechazado», y el
  arranque ya no repinta verde encima.

Instrumento nuevo `tools/sumideros.py`, cableado a la puerta: foto sellada de por dónde sale el daño
al mundo —subir y anunciar éxito—, con el motivo de cada entrada **cableado**, no decorativo.

Y, ya en la verificación, el arreglo de **D-54**: el aviso naranja compone su texto a partir del
**motivo del veredicto** en vez de afirmar una causa fija.

## Reconciliación de los criterios de aceptación

| AC | Resultado | Evidencia |
|---|---|---|
| **AC-1** un solo juez para el desempate, sin tocar el de activos | **PASS** | los dos caminos llaman a `decidirBajada`; `hasRealLocalData` intacta. Mutante propio: «la escucha en vivo deja de consultar al juez» |
| **AC-2** una nube más vieja no empobrece el libro por ningún camino | **PASS** | ejercido con dependencias inyectadas sobre las funciones reales, no sólo el juez puro |
| **AC-3** el reloj del sync deja de ponerse a cero | **PASS** | con control que falla si la marca vuelve a perderse |
| **AC-4** el arranque no queda verde tras un rechazo | **PASS** | espía sobre el pintor; el mutante «el arranque vuelve a repintar VERDE encima del rechazo» da rc=1 |
| **AC-5** los sumideros sellados y el instrumento muerde | **PASS** | `tools/sumideros.py` en la puerta, con rc=1/2/3 distinguibles y control de vacuidad |
| **AC-6** el cruce «falla sólo la lista de carteras» tiene oráculo | **PASS** | color afirmado por VALOR y subidas espiadas reasignando el lanzador |
| **AC-7** los dos sitios que producían el daño, cerrados | **PASS** | y un tercero que destapó la revisión: el panel de importación tenía su propio anuncio de éxito, más grande que el indicador, que se pintaba en verde pasara lo que pasara |
| **AC-8** todo control nuevo se ha visto ROJO | **PASS** | banco de sabotaje: **118 mutantes** mordiendo en la corrida del 2026-09-05, y el árbol idéntico antes y después |
| **AC-9** visto en el navegador real | **PASS** | acta propia: `01-07-VERIFICACION-NAVEGADOR.md`, nueve de nueve |

## Lo que la verificación en navegador añadió, y no estaba en el plan

**El plan daba el checkpoint humano por trámite de confirmación. No lo fue: encontró un defecto de
correctness antes de llegar al primer punto de la lista.**

Nada más abrir la app desplegada, el operador leyó «Cambios sin subir: este dispositivo **no tiene
operaciones**» con **90 operaciones** en el dispositivo. La causa se **demostró** en su consola
(`savedAt` → `undefined`, o sea la rama del reloj desconocido) en vez de suponerse.

- El **comportamiento** era el previsto y querido (D-50): sin desempate posible y con datos que
  proteger, no se aplica la nube y se avisa.
- El **texto** era un defecto: el naranja lo alcanzan **ocho** veredictos distintos del producto y
  afirmaba uno solo. Y el propio ciclo lo había agravado: antes eran **cuatro** claves, y una de las
  cuatro nuevas es la que ve **todo dispositivo ya sincronizado** el día del despliegue. Pasó de
  texto raramente falso a texto universal el día del estreno.

Se arregló dentro del ciclo, por la **clase**: el texto sale del veredicto, y sin motivo no se
inventa causa.

## El hallazgo del cierre: cubrir el mecanismo no cubre su cable

La primera versión de las pruebas de D-54 cubría el **pintor** y parecía completa. Revertidos los
dos llamantes **dejando el pintor intacto**, la suite entera seguía en verde (`rc=0`): el arreglo
podía desconectarse sin que nada se pusiera rojo (§5.6). Se añadió `pruebasCableDelMotivo`, que
ejerce la bajada y el arranque **enteros** y espía el segundo argumento.

Controles positivos, con su mensaje literal:

| Revertido | rc | Mensaje |
|---|---|---|
| el pintor | **1** | `D-54 el PINTOR usa el motivo del veredicto: esperaba true, obtuve false` (y tres más) |
| la bajada | **1** | `D-54 y le pasa al pintor el MOTIVO de su veredicto: … obtuve undefined` |
| el arranque | **1** | `D-54 y el arranque NO se come el motivo: … obtuve undefined` |

Cuatro sabotajes permanentes en el banco, uno por eslabón más el del motivo ausente: *un control
positivo de hoy es una anécdota fechada.*

**Y la puerta cazó tres sabotajes YA EXISTENTES que dejaron de morder** porque el cambio movió sus
anclas: `rc=1` con el mensaje «CONTROLES QUE NO MUERDEN (3)», en vez de pasar en verde. Reanclados.

## Verificación final

`tools/verify.sh` → **rc=0**, once pasos, por las **dos** variantes (manual y enganche `pre-push`).
`index.html` con la misma huella antes y después de medir (`9459b0fc…`).

## Desviaciones respecto al plan

1. **El ciclo no terminó en el APPLY.** El plan preveía verificar y cerrar; la verificación abrió un
   arreglo de correctness (D-54) que se ejecutó dentro del mismo ciclo, con su despliegue y su
   segunda pasada de navegador. **No se difirió**, porque §3.4 prohíbe entrar en UNIFY con un
   hallazgo de correctness sin atender, y porque el ciclo lo había agravado.
2. **La comprobación final salió mejor de lo pedido.** Se pidió pintar el naranja con un motivo
   inyectado; el arranque repintó **el suyo, el real**, con las dos marcas de tiempo y «89
   operaciones locales que proteger». Demuestra el camino completo en producción, no el pintor
   aislado.
3. **Nota de proceso:** el despliegue se hizo con autorización explícita del operador («haz lo que
   creas correcto» tras preguntarle por el push). Se deja escrito porque en el 01-06 se dio por
   autorizado algo que no lo estaba.

## Lo que este ciclo NO cubre, dicho por escrito

- **D-56**: dos de los cuatro llamantes pasan el motivo **sin control que lo mate**. La pantalla dice
  hoy la verdad en los cuatro caminos; falta el guardián que lo mantenga mañana.
- **D-18**: el aviso **rojo del guardado local fallido** sigue sin verse nunca en un navegador.
- **D-57** y **D-51**: la política de sincronización —quién gana y quién publica— es Fase 3.
