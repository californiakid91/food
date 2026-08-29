#!/usr/bin/env bash
# Instala el enganche de git que dispara LA PUERTA antes de cada push.
# Los hooks no viajan en el repo, asi que esto se vuelve a correr en cada
# maquina. Llama al MISMO tools/verify.sh que se usa a mano: una sola lista,
# para que la variante automatica no pueda ejercer menos que la manual.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .git/hooks
cat > .git/hooks/pre-push <<'HOOK'
#!/usr/bin/env bash
# Generado por tools/install-hooks.sh — no editar a mano.
echo "pre-push: abriendo la puerta…"
"$(git rev-parse --show-toplevel)/tools/verify.sh"
rc=$?
if [ $rc -ne 0 ]; then
  echo
  echo "PUSH BLOQUEADO (rc=$rc). Nada sale a produccion sin pasar la puerta."
  echo "Si de verdad hace falta saltarsela, hay que decirlo en voz alta: git push --no-verify"
  exit $rc
fi
HOOK
chmod +x .git/hooks/pre-push
echo "Enganche instalado: .git/hooks/pre-push -> tools/verify.sh"
