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

### Active (In Progress)

Ninguno — listo para planificar la Fase 1.

### Planned (Next)

- [ ] Fase 1 — Guardado que no miente (carga incondicional de `ops`, errores visibles, dedupe por `id`)
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
- Los cambios se validan a mano: no hay CI

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

## Success Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Autopruebas en verde antes de cada despliegue | 100% | round-trip decimal | On track |
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
*Last updated: 2026-08-29*
