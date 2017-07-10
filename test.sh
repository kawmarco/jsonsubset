
cd $(dirname $0)

export PYTHONPATH=src:.
venv/bin/python3 -m pytest tests "$@"
