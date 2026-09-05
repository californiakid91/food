# food

## What This Is

PWA personal de gestión de carteras de inversión, servida como un único `index.html` estático desde GitHub Pages y sincronizada con Firestore. Registra carteras y activos con precios introducidos a mano (EUR/USD con conversión), importa operaciones desde capturas de pantalla del bróker vía OCR, mantiene un libro global de operaciones, calcula el FIFO fiscal y exporta el Excel para la declaración de la renta española.

## Core Value

Llevar al día tus carteras con precios manuales y sacar de ahí una declaración de la renta correcta, sin depender de ningún servicio de precios ni de un backend propio.

## Current State

| Attribute | Value |
|-----------|-------|
| Type | Application |
| Version | 0.0.0 |
| Status | Production (uso personal diario) |
| Last Updated | 2026-08-29 |

**Production URLs:**
- https://californiakid91.github.io/food/ — la app

## Requirements

### Core Features

- Carteras con activos, precios manuales y conversión USD→EUR
- Objetivos de % por cartera (toggle) y cálculo de rebalanceo
- Importación de operaciones desde capturas del bróker vía OCR
- Libro global de operaciones a nivel de cuenta + FIFO continuo multi-ejercicio
- Exportación del Excel para el IRPF español
- Snapshots mensuales automáticos y gráficos en canvas; modo avión

### Validated (Shipped)

- [x] Corrección del separador decimal en la entrada manual (`parseNum`) — `69f728e`, 2026-08-29
- [x] `runSelfTests()` con `?selftest=1` cubriendo el round-trip `parseNum`/`numIn` — `69f728e`
- [x] Puerta de verificación `tools/verify.sh` con códigos de salida nominales, banco de sabotaje y enganche `pre-push` — 2026-08-29
- [x] Trinquete de tamaño de funciones sellado sobre el código real — 2026-08-29

### Active (In Progress)

**Fase 1 — Guardado que no miente.** **Seis ciclos cerrados.** Los cuatro primeros: 01-01 (arranque y guardado honestos),
01-02 (sincronización que no destruye), 01-03 (el cerrojo del libro ilegible, `96c7a3e`) y **01-04**
(una sola puerta de subida, `21e1edb`). **Los cuatro están desplegados y verificados en el
navegador real**; el 01-04 el 2026-08-31 (`e2e8f86`), con sus estados naranja y rojo vistos por
primera vez en la app.

El 01-04 cerró el hallazgo que paró la fase en su segunda transición: había tres escrituras a
Firestore y sólo dos pasaban por la guarda de no-vaciado. Ahora hay **una**, decidida por una
función pura que falla cerrado —de forma simétrica para operaciones y activos— cuando no puede
mirar la nube, y dos instrumentos nuevos ponen la puerta roja si aparece otra.

El **01-05** (`4e81e6c`, 2026-08-31) es el quinto ciclo cerrado y **no toca la app**: arregla la
vara de medir antes de medir con ella. Los trinquetes ya no pueden reventar y salir rotulados como
«el código ha engordado»; la puerta ya no puede terminar en verde con el banco de sabotaje apagado,
ni por su código de salida ni por un entorno contaminado; y la variante automática (el enganche
`pre-push`) está vigilada en vez de supuesta. Por eso no necesita verificación en navegador — y por
eso el 01-06 sí la necesitará.

El **01-06** (2026-08-31) es el sexto y último ciclo, y **cierra D-38**: la capa de aviso ya tiene
oráculo. Los dos pintores —el del guardado y el de la sincronización— **se ejecutan de verdad** por
primera vez, sobre un DOM observable con reloj falso, y se lee lo que hacen: el texto, el color
**por su valor**, la visibilidad y cuánto dura el aviso. Un instrumento nuevo, `tools/avisos.py`,
sella los 34 avisos al operador con su nivel y su mensaje, y vigila que nadie pinte esos elementos
por su cuenta.

Lo que hay que recordar de ese ciclo: **se dio por hecho una vez y estaba mal**. La puerta ya
estaba verde cuando tres revisiones adversarias independientes encontraron diez cosas, ninguna de
ellas vista por más de una. La peor: los asertos pedían que los colores de éxito y de fallo fueran
*distintos*, nunca *cuáles*, así que **intercambiarlos —el fallo de guardado pintado en verde—
pasaba la puerta entera**. Era exactamente el daño que el ciclo existía para impedir.

El 01-06 se desplegó y **se miró en el navegador** el 2026-08-31: 90 operaciones y 5 carteras
idénticas antes y después de las autopruebas, y guardar siguió funcionando después de ejecutarlas.

**La CUARTA medición de la fase contra el código se hizo el 2026-09-01, y la fase sigue abierta.**
Por primera vez el aparato de medición aguantó entero —el brazo que lo atacó no consiguió romperlo
por ninguno de los cinco caminos que intentó— y por primera vez ninguna cifra publicada era falsa.
Lo que impide cerrar ya no son huecos del instrumental, sino **dos defectos del producto**, los dos
con la misma forma: una **asimetría** entre dos caminos que deberían juzgar igual.

El primero: cuando la app arranca y decide si los datos de la nube ganan a los locales, mira **sólo
los activos** y nunca el libro de operaciones. Un operador que lo tenga todo vendido —sin activos,
pero con el libro fiscal entero— hace que **cualquier copia de la nube gane, por vieja que sea**, y
la pantalla se queda en verde. El mismo juicio, en la dirección contraria (al subir), ya mira las
dos cosas desde el 01-04.

El segundo: el guardado exige que las tres escrituras vayan bien, pero **nadie comprueba el caso en
que falle sólo la lista de carteras**. Quitar esa condición del veredicto pasa la puerta entera en
verde. Con el almacenamiento lleno, el operador vería «Guardado ✓» y además se subiría a la nube.

Los dos abren el ciclo **01-07**. Las cuatro mediciones de esta fase han cambiado el resultado al
hacerlas; contar actas la habría cerrado las cuatro veces.

**El ciclo 01-07 cerró los dos el 2026-09-05**, y se vio dos veces en el navegador real. Un solo
juez gobierna ahora las dos direcciones por las que entra la nube, y «hay datos que proteger» suma
el libro además de los activos. El checkpoint humano no fue un trámite: nada más abrir la app, el
operador leyó «este dispositivo **no tiene operaciones**» con noventa delante. El comportamiento
era el correcto; el TEXTO mentía, y el propio ciclo lo había agravado. Se arregló dentro del mismo
ciclo: el aviso compone su causa a partir del veredicto, y sin motivo no se inventa ninguna.

**La QUINTA medición se hizo el 2026-09-05, y la fase SIGUE abierta.** Cinco brazos adversarios,
cada uno sobre su propia copia del proyecto, y los cinco encontraron algo que ninguno de los otros
vio. Lo que impide cerrar es, otra vez, un defecto del producto, y esta vez el daño no está en el
dispositivo sino **en la nube**:

Cuando la app arranca y la nube trae un libro **más grande de lo que cabe** en el almacenamiento
del navegador, el libro **no se guarda** —eso ya se sabía y se avisa por consola— pero el reloj
interno **sí se adelanta**, como si hubiera llegado. A partir de ahí el dispositivo se cree al día.
En cuanto el operador toca cualquier cosa, sube su libro pequeño **encima del grande**: en la
prueba, la nube pasó de 42 operaciones a 2, con «Guardado ✓» y el punto en verde. Como de la nube
sale la declaración de la renta, la pérdida es la que más importa.

Y junto a eso, un hueco de medición del mismo tamaño: **nadie comprueba lo que la app PINTA cuando
la sincronización falla**. Las pruebas cuentan si se escribió o no en la nube; el operador, en
cambio, mira la pantalla. Pintar verde sobre una subida fallida pasa la verificación entera.

Los dos abren el ciclo **01-08**. **Las cinco mediciones de esta fase han cambiado el resultado al
hacerlas**; contar actas la habría cerrado las cinco veces.

### Planned (Next)

- [ ] Fase 2 — Backup/restore JSON
- [ ] Fase 3 — Sync que fusiona en vez de reemplazar
- [ ] Fase 4 — Corrección fiscal del FIFO
- [ ] Fase 5 — UX del uso diario
- [ ] Fase 6 — Extras de valor

### Out of Scope

- Framework, build system o backend propio — el valor está en que siga siendo un HTML único desplegable en Pages
- Obtención automática de precios (se retiró a propósito; `worker.js` quedó obsoleto y se borra en la Fase 6)
- Envío mensual del Excel por email — descartado el 2026-08-04, no reproponer

## Target Users

**Primary:** el propio autor, usuario único.
- Opera en Revolut, con títulos fraccionarios y multi-divisa (EUR/USD)
- Usa la app a diario desde el móvil (PWA) y ocasionalmente desde el PC
- El output crítico es anual: la declaración de la renta

## Context

**Technical Context:**
`index.html` de ~4.500 líneas con todo el JS inline, sin tests ni build. Firebase Auth + Firestore para sync (un único documento por usuario), service worker para modo avión, GitHub Pages para el despliegue. `sync.py` sincroniza fuera de la app; `worker.js` es un proxy de Yahoo ya obsoleto.

## Constraints

### Technical Constraints

- Un solo fichero `index.html` sin build system: nada de imports, bundlers ni dependencias nuevas
- Todo el estado viaja en UN documento de Firestore (límite de 1 MB; los snapshots mensuales lo engordan)
- iOS/PWA no ejecuta nada en segundo plano
- No hay CI: la puerta es local (`tools/verify.sh` + enganche `pre-push`, que hay que reinstalar en cada máquina con `tools/install-hooks.sh`)

### Business Constraints

- La Fase 4 (FIFO/IRPF) debe estar cerrada antes de la próxima campaña de la renta
- Usuario único: los conflictos de sync son entre dispositivos propios, no entre personas

## Key Decisions

| Decision | Rationale | Date | Status |
|----------|-----------|------|--------|
| Atacar el backlog completo de la auditoría con estructura PAUL | 16 hallazgos con dependencias entre sí; hacen falta fases | 2026-08-29 | Active |
| Bug de la coma decimal como Fase 0 fuera del ciclo | Estaba corrompiendo datos en producción | 2026-08-29 | Active |
| Fiscal antes que UX | El dato del que sale la renta pesa más que la comodidad diaria | 2026-08-29 | Active |
| Sin SonarQube ni audit enterprise | Proyecto personal de un fichero; no aportan | 2026-08-29 | Active |
| Autopruebas con `?selftest=1` en vez de framework de tests | Blinda invariantes sin introducir build system | 2026-08-29 | Active |
| Adoptada la doctrina de proceso y verificación en `CLAUDE.md` | Traída de otro proyecto del operador; cada regla nació de un fallo real medido | 2026-08-29 | Active |
| La puerta es `tools/verify.sh`, enganchada a `pre-push` | Un instrumento que no dispara ningún objetivo no existe | 2026-08-29 | Active |
| §9 adaptada: presupuesto por función (60 líneas), no módulos hoja | El monolito es el producto: `index.html` debe servirse tal cual | 2026-08-29 | Active |
| Las deudas viven en `.paul/DEUDAS.md`, no en las actas | Una deuda que sólo existe en un SUMMARY es como si no existiera | 2026-08-29 | Active |

## Success Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| La puerta (`tools/verify.sh`) en verde antes de cada push | 100% | enganchada a pre-push | On track |
| Controles de la puerta con sabotaje que demuestra que muerden | 100% | todos (cifra viva en la salida de `tools/sabotage.py`; no se copia aquí) | Achieved |
| Invariantes cubiertos por `runSelfTests()` | 4 (decimal, FIFO, año fiscal, sync) | 1 | On track |
| Escenarios de pérdida de datos abiertos | 0 | 4 (ops sin cargar, dedupe, sync, sin backup) | At risk |
| Riesgos fiscales conocidos sin resolver | 0 | 4 (orden intradía, split, 2 meses, opFx) | At risk |

## Tech Stack / Tools

| Layer | Technology | Notes |
|-------|------------|-------|
| App | HTML + JS inline, sin build | Un único `index.html` |
| Persistencia local | localStorage | Fuente de verdad en el dispositivo |
| Sync | Firebase Auth + Firestore | Un documento por usuario, last-write-wins |
| Hosting | GitHub Pages | Despliegue por `git push` a `main` |
| Offline | Service worker (`sw.js`) | Recargar 2× para ver una versión nueva |
| OCR | Parseo propio de extractos y posiciones | `parseLooseNum`, `parseRevolutStatement` |
| FX | Frankfurter + `FX_FALLBACK` | Cambio congelado por operación |

## Links

| Resource | URL |
|----------|-----|
| Repository | https://github.com/californiakid91/food |
| Production | https://californiakid91.github.io/food/ |
| Autopruebas | https://californiakid91.github.io/food/?selftest=1 (ver consola) |

---
*PROJECT.md — Updated when requirements or context change*
*Last updated: 2026-09-05*
