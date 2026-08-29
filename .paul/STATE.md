# Project State

## Project Reference

See: .paul/PROJECT.md (updated 2026-08-29)

**Core value:** Llevar al día tus carteras con precios manuales y sacar de ahí una declaración de la renta correcta, sin backend propio.
**Current focus:** v0.1 Datos fiables — Fase 1 "Guardado que no miente"

## Current Position

Milestone: v0.1 Datos fiables (v0.1.0)
Phase: 1 of 6 (Guardado que no miente) — en curso
Planes: 01-01 CERRADO (`dd13e42` + `86ad865`); 01-02 planificado, sin ejecutar
Status: ciclo 01-01 cerrado; listo para planificar/ejecutar 01-02
Last activity: 2026-08-29 — UNIFY de 01-01: 4 AC en PASS, 8 defectos de la revisión arreglados

Progress:
- Milestone: [█░░░░░░░░░] 14% (1 de 7 fases, contando la 0)
- Phase: [█████░░░░░] 50% (01-01 de 2 planes)

## Loop Position

Current loop state:
```
PLAN ──▶ APPLY ──▶ UNIFY
  ✓        ✓        ✓     [01-01 cerrado — listo para el siguiente PLAN]
```

## Performance Metrics

**Velocity:**
- Total plans completed: 2
- Average duration: —
- Total execution time: —

**By Phase:**

| Phase | Plans | Total Time | Avg/Plan |
|-------|-------|------------|----------|
| 00-hotfix-decimal | 1/1 | — | — |
| 01-guardado-fiable | 1/2 | — | — |

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

### Deferred Issues

**Las deudas viven ahora en `.paul/DEUDAS.md`** (D-01 a D-11), que es la lista viva que se lee al
arrancar cada sesión. Esta tabla ya no se mantiene: duplicarla sería tener dos fuentes de verdad.

### Blockers/Concerns

| Blocker | Impact | Resolution Path |
|---------|--------|-----------------|
| Ninguno | — | — |

## Boundaries (Active)

Del PLAN 01-02 (siguiente):

- `dedupeOps` / `opFingerprint` intactos: los necesitan `migrateOpsToGlobal` y el formato antiguo `opsData`
- `parseNum` / `numIn` / `parseLooseNum` no se tocan (Fase 0)
- `buildSyncPayload` y la resolución por `savedAt` son Fase 3; `computeFifo` y `exportTaxExcel`, Fase 4

Permanentes del proyecto:

- `index.html` sigue siendo un fichero único sin build system ni dependencias nuevas
- No reintroducir la obtención automática de precios

## Session Continuity

Last session: 2026-08-29
Stopped at: Ciclo 01-01 cerrado con su acta
Next action: Verificar a mano en la app desplegada (recargando dos veces) que el aviso de guardado
  se comporta; luego `/paul:apply .paul/phases/01-guardado-fiable/01-02-PLAN.md`
Resume file: .paul/phases/01-guardado-fiable/01-01-SUMMARY.md

---
*STATE.md — Updated after every significant action*
