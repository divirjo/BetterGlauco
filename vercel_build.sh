#!/bin/bash

# Build the project
echo "### Instalar dependências ###"
python3.9 -m pip install --upgrade pip
python3.9 -m pip install -r requirements.txt
python -V
python3.9 -V

echo "### Executando as migrações ###"
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

echo "### Obter estatísticas...###"
python3.9 manage.py collectstatic --noinput --clear
