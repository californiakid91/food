# Project State

## Project Reference

See: .paul/PROJECT.md (updated 2026-08-29)

**Core value:** Llevar al día tus carteras con precios manuales y sacar de ahí una declaración de la renta correcta, sin backend propio.
**Current focus:** v0.1 Datos fiables — Fase 1 "Guardado que no miente"

## Current Position

Milestone: v0.1 Datos fiables (v0.1.0)
Phase: 1 of 6 (Guardado que no miente) — en curso
Planes: 01-01 CERRADO (`dd13e42` + `86ad865` + `80d523f`); 01-02 CERRADO (`77f8cef` +
`56795eb` + acta)
Status: los DOS ciclos cerrados, DESPLEGADO (`feb643b`) y VERIFICADO en el navegador real.
Pendiente sólo la transición de fase (brazos G7/CRG y G8/security-review)
Last activity: 2026-08-30 — push (`feb643b`, puerta verde en el pre-push) + verificación manual
en la app desplegada: 3 de 4 puntos confirmados; el 4º sube al libro como D-18

Progress:
- Milestone: [█░░░░░░░░░] 14% (1 de 7 fases, contando la 0)
- Phase: [█████████░] 95% (ciclos cerrados, desplegado y verificado; falta la transición de fase)

## Loop Position

Current loop state:
```
PLAN ──▶ APPLY ──▶ UNIFY
  ✓        ✓        ✓     [01-02 cerrado. Fase 1 pendiente de despliegue + navegador]
```

## Performance Metrics

**Velocity:**
- Total plans completed: 3
- Average duration: —
- Total execution time: —

**By Phase:**

| Phase | Plans | Total Time | Avg/Plan |
|-------|-------|------------|----------|
| 00-hotfix-decimal | 1/1 | — | — |
| 01-guardado-fiable | 2/2 | — | — |

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
| Un único juez para las dos guardas de no-vaciado | 01-02 | `vaciariaElLibro` + `opsDelDocumento`: la misma función en los dos lados, no el mismo criterio escrito dos veces |
| Fallar CERRADO si no se puede leer la nube | 01-02 | Se prefiere perder sincronía a perder el libro; y se ve en naranja, no en verde |
| Los controles de las autopruebas viven en el ARNÉS | 01-02 | Uno dentro de la suite sería juez y parte; el de datos reales está en `run_selftests.py` |
| Cerrar el ciclo 01-02 sin cerrar la FASE 1 | 01-02 UNIFY | Los 3 objetivos del scope están en el código, medidos uno a uno; pero ningún eslabón se ha visto en un navegador y nada está desplegado. Una sonda verde no supera a un intento real |

### Deferred Issues

**Las deudas viven ahora en `.paul/DEUDAS.md`** (D-01 a D-11), que es la lista viva que se lee al
arrancar cada sesión. Esta tabla ya no se mantiene: duplicarla sería tener dos fuentes de verdad.

### Blockers/Concerns

| Blocker | Impact | Resolution Path |
|---------|--------|-----------------|
| Ninguno | — | Los dos blockers anteriores (sin desplegar, sin ver en navegador) se cerraron el 2026-08-30, ver «Verificación manual» |

## Verificación manual de la Fase 1 — app desplegada, 2026-08-30

Hecha sobre `https://californiakid91.github.io/food/` con `feb643b` publicado. Confirmado antes de
empezar que Pages servía la versión nueva (huella del fichero descargado idéntica a la local) y que
el navegador del operador la tenía cargada (`typeof dedupeOpsById === 'function'` en consola, no
por el aspecto de la pantalla).

| Punto | Resultado | Evidencia |
|---|---|---|
| Aviso verde «Guardado ✓» al guardar | **PASS** | visto en pantalla por el operador |
| El naranja «Cambios sin subir» NO sale en uso normal | **PASS** | el puntito quedó verde |
| `?selftest=1` deja los datos intactos | **PASS** | **90 operaciones y 4 carteras, idénticas antes y después**, contadas en consola. Es el fallo que estaba vivo en producción |
| `?selftest=1` imprime «✅ Autopruebas OK» | **PASS** | leído en la consola del navegador |
| El aviso sale en ROJO cuando el guardado falla | **NO COMPROBADO** | → **D-18**. Exige agotar el almacenamiento del navegador; no se improvisó con 90 operaciones reales delante |

Los dos últimos se comprobaron por separado a propósito: el fallo original consistía justamente en
imprimir «OK» **mientras** borraba, así que «no borró» y «dijo OK» son afirmaciones independientes.

## Boundaries (Active)

Del PLAN 01-02 (siguiente):

- `dedupeOps` / `opFingerprint` intactos: los necesitan `migrateOpsToGlobal` y el formato antiguo `opsData`
- `parseNum` / `numIn` / `parseLooseNum` no se tocan (Fase 0)
- `buildSyncPayload` y la resolución por `savedAt` son Fase 3; `computeFifo` y `exportTaxExcel`, Fase 4

Permanentes del proyecto:

- `index.html` sigue siendo un fichero único sin build system ni dependencias nuevas
- No reintroducir la obtención automática de precios

## Session Continuity

Last session: 2026-08-30
Stopped at: Fase 1 desplegada y verificada en el navegador real. La fase sigue formalmente
abierta: falta su transición, que es donde corren los dos brazos de revisión DE FASE.
Next action: transición de la Fase 1 — G7 (CRG blast-radius) y G8 (`/security-review`) sobre el
diff de la fase, evolución de PROJECT.md y ROADMAP.md, y commit de cierre. Empezar con contexto
limpio.
Resume file: .paul/phases/01-guardado-fiable/01-02-SUMMARY.md

---
*STATE.md — Updated after every significant action*
