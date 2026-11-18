#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source <(uv run python -c '
from dotenv import dotenv_values
import shlex
for key, value in dotenv_values(".env").items():
    if value is None:
        continue
    print(f"export {key}={shlex.quote(value)}")
')
  set +a
fi

uv run python scripts/render_secrets.py
exec uv run streamlit run app/Home.py "$@"
