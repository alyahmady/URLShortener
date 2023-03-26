#!/bin/bash

set -e
set -o errexit
set -o pipefail
set -o nounset

python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
python3 manage.py initialize

gunicorn URLShortener.asgi:application
