cd $(dirname $0)
source venv/bin/activate

export PYTHONPATH=src:deps/xxhash_cython:.
py.test tests "$@"
