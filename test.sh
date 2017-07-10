cd $(dirname $0)
source venv/bin/activate

export PYTHONPATH=src:.
py.test tests "$@"
