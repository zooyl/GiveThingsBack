#!/bin/sh
printf "................... Making migrations ................... \n"
python3 manage.py makemigrations
python3 manage.py migrate
printf "................... Collecting static files ................... \n"
python3 manage.py collectstatic
printf "................... Running tests ................... \n"
python3 manage.py test
exec "$@"