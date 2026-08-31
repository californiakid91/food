#!/usr/bin/env bash
# Instala el enganche de git que dispara LA PUERTA antes de cada push.
# Los hooks no viajan en el repo, asi que esto se vuelve a correr en cada
# maquina. Llama al MISMO tools/verify.sh que se usa a mano: una sola lista,
# para que la variante automatica no pueda ejercer menos que la manual.
#
# El directorio de enganches se le PREGUNTA A GIT en vez de suponer
# `.git/hooks`: con `core.hooksPath` puesto, o en un `git worktree` (donde
# `.git` es un fichero y no un directorio), instalar en `.git/hooks` deja el
# enganche donde git no lo va a mirar nunca. Medido el 2026-08-31: con
# core.hooksPath desviado, un pre-push ejecutable que devuelve 1 se ignora y
# el push sale con rc=0.
set -euo pipefail
cd "$(dirname "$0")/.."
HOOKS="$(git rev-parse --git-path hooks)"
mkdir -p "$HOOKS"
cat > "$HOOKS/pre-push" <<'HOOK'
#!/usr/bin/env bash
# Generado por tools/install-hooks.sh — no editar a mano.
echo "pre-push: abriendo la puerta…"
# SEGUNDA CAPA contra el entorno contaminado. verify.sh ya no devuelve 0 con
# VERIFY_INNER=1 (devuelve 4, que no es verde para nadie salvo el banco), pero
# el enganche HEREDA el entorno del operador: si esa variable quedara exportada
# en un perfil, el push correria una puerta con el banco apagado. Aqui se
# limpia antes de llamar, asi que ni siquiera llega. Son dos capas a proposito:
# con una sola, el agujero sigue abierto por el otro lado.
unset VERIFY_INNER
"$(git rev-parse --show-toplevel)/tools/verify.sh"
rc=$?
if [ $rc -ne 0 ]; then
  echo
  echo "PUSH BLOQUEADO (rc=$rc). Nada sale a produccion sin pasar la puerta."
  echo "Si de verdad hace falta saltarsela, hay que decirlo en voz alta: git push --no-verify"
  exit $rc
fi
HOOK
# El bit de ejecucion NO es cosmetico: sin el, git IGNORA el enganche, avisa con
# un `hint:` que se puede silenciar con `advice.ignoredHook false`, y el push
# SALE CON RC=0. Es la variante automatica muerta en silencio.
chmod +x "$HOOKS/pre-push"
echo "Enganche instalado: $HOOKS/pre-push -> tools/verify.sh"
