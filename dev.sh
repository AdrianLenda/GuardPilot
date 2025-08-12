#!/usr/bin/env bash
# dev.sh — start GuardPilot (backend) + opcjonalnie UI
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

WITH_UI="${1:-}"   # użycie: ./dev.sh --ui

cleanup() {
  [[ -n "${UVICORN_PID:-}"  ]] && kill "$UVICORN_PID"  >/dev/null 2>&1 || true
  [[ -n "${STREAMLIT_PID:-}" ]] && kill "$STREAMLIT_PID" >/dev/null 2>&1 || true
}
trap cleanup INT TERM EXIT

# 1) venv
if [[ ! -d .venv ]]; then python -m venv .venv; fi
source .venv/bin/activate

# 2) deps
pip install -q -r backend/requirements.txt
# UI zależności tylko gdy prosimy o UI
if [[ "$WITH_UI" == "--ui" ]]; then
  pip install -q -r ui/requirements.txt
fi

# 3) Postgres (Codespaces / lokalnie z compose)
docker compose -f infra/docker-compose.yml up -d postgres

# 4) ENV + katalog na logi
export DATABASE_URL="${DATABASE_URL:-postgresql://guardpilot:guardpilot@localhost:5432/guardpilot}"
export LOGS_DIR="${LOGS_DIR:-$PROJECT_ROOT/data}"
mkdir -p "$LOGS_DIR"

# 5) start backend (w tle)
uvicorn backend.app.main:app --reload --port 8000 &
UVICORN_PID=$!
echo "⏳ Uvicorn PID=$UVICORN_PID → http://127.0.0.1:8000"

# 6) opcjonalnie UI
if [[ "$WITH_UI" == "--ui" ]]; then
  export GP_API_BASE="${GP_API_BASE:-http://127.0.0.1:8000}"
  (cd ui && streamlit run app.py --server.port 8501 --server.headless true) &
  STREAMLIT_PID=$!
  echo "🖥️  Streamlit PID=$STREAMLIT_PID → http://127.0.0.1:8501"
fi

# 7) czekaj na procesy (Ctrl+C zatrzyma oba)
wait
