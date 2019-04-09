#!/bin/sh
printf "................... Making migrations ................... \n"
python3 manage.py makemigrations
python3 manage.py migrate
printf "................... Running tests ................... \n"
python3 manage.py test
exec "$@"