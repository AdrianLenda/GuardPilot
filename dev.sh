#!/usr/bin/env bash
# dev.sh – start GuardPilota w trybie deweloperskim
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

############################
# 1. Wirtualne środowisko  #
############################
if [[ ! -d .venv ]]; then
  python -m venv .venv
fi
source .venv/bin/activate

##################################
# 2. Zależności (instaluj raz)   #
##################################
pip install -q -r backend/requirements.txt

########################################
# 3. Postgres w kontenerze (Codespace) #
########################################
docker compose -f infra/docker-compose.yml up -d postgres

######################################
# 4. Zmienne środowiskowe i katalog  #
######################################
export DATABASE_URL="${DATABASE_URL:-postgresql://guardpilot:guardpilot@localhost:5432/guardpilot}"
export LOGS_DIR="${LOGS_DIR:-$PROJECT_ROOT/data}"
mkdir -p "$LOGS_DIR"

##################################
# 5. Start backend (Uvicorn)     #
##################################
exec uvicorn backend.app.main:app --reload --port 8000
