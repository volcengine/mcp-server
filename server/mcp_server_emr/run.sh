set -ex

# Auto-activate local venv if present (for local dev)
if [ -d ".venv" ]; then
  . .venv/bin/activate || true
fi

python main.py
