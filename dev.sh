#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

WITH_UI="${1:-}"

cleanup() {
  [[ -n "${UVICORN_PID:-}"   ]] && kill "$UVICORN_PID"   >/dev/null 2>&1 || true
  [[ -n "${STREAMLIT_PID:-}" ]] && kill "$STREAMLIT_PID" >/dev/null 2>&1 || true
  [[ -n "${VITE_PID:-}"      ]] && kill "$VITE_PID"      >/dev/null 2>&1 || true
}
trap cleanup INT TERM EXIT

if [[ ! -d .venv ]]; then python -m venv .venv; fi
source .venv/bin/activate

pip install -q -r backend/requirements.txt
if [[ "$WITH_UI" == "--ui" ]]; then
  pip install -q -r apps/ui/requirements.txt
fi

docker compose -f infra/docker-compose.yml up -d postgres

export DATABASE_URL="${DATABASE_URL:-postgresql://guardpilot:guardpilot@localhost:5432/guardpilot}"
export LOGS_DIR="${LOGS_DIR:-$PROJECT_ROOT/data}"
mkdir -p "$LOGS_DIR"

export PYTHONPATH="$PROJECT_ROOT:${PYTHONPATH:-}"

uvicorn backend.app.main:app --reload --port 8000 &
UVICORN_PID=$!
echo "⏳ Uvicorn PID=$UVICORN_PID → http://127.0.0.1:8000"

if [[ "$WITH_UI" == "--ui" ]]; then
  export GP_API_BASE="${GP_API_BASE:-http://127.0.0.1:8000}"
  streamlit run apps/ui/app.py --server.port 8501 --server.headless true &
  STREAMLIT_PID=$!
  echo "🖥️  Streamlit PID=$STREAMLIT_PID → http://127.0.0.1:8501"

elif [[ "$WITH_UI" == "--ui-react" ]]; then
  if ! command -v npm >/dev/null 2>&1; then
    echo "❌ npm not found. Please install Node.js (>=18)." >&2
    exit 1
  fi
  if [[ ! -d frontend ]]; then
    echo "❌ frontend/ not found." >&2
    exit 1
  fi
  pushd frontend >/dev/null
  if [[ ! -d node_modules ]]; then
    echo "📦 Installing frontend dependencies…"
    if [[ -f package-lock.json ]]; then
      npm ci
    else
      npm install
    fi
  fi
  echo "🧪 Starting Vite dev server…"
  npm run dev -- --strictPort &
  VITE_PID=$!
  popd >/dev/null
  echo "🖥️  React UI (Vite) PID=$VITE_PID → http://127.0.0.1:5173"
fi

wait
