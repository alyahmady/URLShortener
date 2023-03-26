#!/bin/bash

set -e
set -o errexit
set -o pipefail
set -o nounset

python3 manage.py collectstatic --noinput

gunicorn URLShortener.asgi:application
