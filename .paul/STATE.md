# Project State

## Project Reference

See: .paul/PROJECT.md (updated 2026-08-29)

**Core value:** Llevar al día tus carteras con precios manuales y sacar de ahí una declaración de la renta correcta, sin backend propio.
**Current focus:** v0.1 Datos fiables — Fase 1 "Guardado que no miente"

## Current Position

Milestone: v0.1 Datos fiables (v0.1.0)
Phase: 1 of 6 (Guardado que no miente)
Plan: 0 of 3 in current phase
Status: Ready to plan
Last activity: 2026-08-29 — Fase 0 desplegada (`69f728e`), PAUL inicializado desde la auditoría Fable

Progress:
- Milestone: [█░░░░░░░░░] 14% (1 de 7 fases, contando la 0)
- Phase: [░░░░░░░░░░] 0%

## Loop Position

Current loop state:
```
PLAN ──▶ APPLY ──▶ UNIFY
  ○        ○        ○     [Ready for first PLAN]
```

## Performance Metrics

**Velocity:**
- Total plans completed: 1
- Average duration: —
- Total execution time: —

**By Phase:**

| Phase | Plans | Total Time | Avg/Plan |
|-------|-------|------------|----------|
| 00-hotfix-decimal | 1/1 | — | — |
| 01-guardado-fiable | 0/3 | — | — |

## Accumulated Context

### Decisions

| Decision | Phase | Impact |
|----------|-------|--------|
| Bug de la coma como Fase 0 fuera del ciclo | Fase 0 | Ya desplegado; el resto va por PLAN→APPLY→UNIFY |
| Fiscal antes que UX | Roadmap | Fases 3-4 antes que la 5 |
| Autopruebas con `?selftest=1`, sin build system | Fase 0 | Cada fase añade su invariante a `runSelfTests()` |
| Sin SonarQube ni audit enterprise | Init | No se crea `.paul/config.md` |

### Deferred Issues

| Issue | Origin | Effort | Revisit |
|-------|--------|--------|---------|
| Confirmar si los dividendos del OCR de Revolut llegan brutos o netos de retención | Auditoría 2026-08-29 | S | Con una captura real, antes de la Fase 6 |
| El documento único de Firestore crece hacia el límite de 1 MB por los snapshots | Auditoría 2026-08-29 | M | Cuando el payload pase de ~500 KB |
| Borrar el Worker de Cloudflare en su dashboard | Memoria previa | S | Junto a la limpieza de `worker.js` (Fase 6) |

### Blockers/Concerns

| Blocker | Impact | Resolution Path |
|---------|--------|-----------------|
| Ninguno | — | — |

## Boundaries (Active)

Sin PLAN activo todavía. Protecciones permanentes del proyecto:

- `index.html` sigue siendo un fichero único sin build system ni dependencias nuevas
- `parseLooseNum` conserva su heurística de miles: es el camino del OCR
- No reintroducir la obtención automática de precios

## Session Continuity

Last session: 2026-08-29
Stopped at: Fase 0 desplegada y PAUL inicializado con el roadmap de la auditoría
Next action: `/paul:plan` para la Fase 1 "Guardado que no miente"
Resume context: el backlog completo con citas de línea está en la memoria `food-audit-2026-08-29`

---
*STATE.md — Updated after every significant action*
