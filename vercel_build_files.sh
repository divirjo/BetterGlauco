

echo "____________________________________________________________________"
echo "                  PYENV"
echo "____________________________________________________________________"


echo "____________________________________________________________________"
echo "                  POETRY"
echo "____________________________________________________________________"
pip install pipx
pipx install poetry

echo "____________________________________________________________________"
echo "                  DEPENDENCIAS PYTHON"
echo "____________________________________________________________________"
python -m poetry install
poetry -m env use python3.12
python -m poetry shell
python -m poetry env info

echo "____________________________________________________________________"
echo "                  DJANGO"
echo "____________________________________________________________________"

echo "### Executando as migrações ###"
python manage.py makemigrations 
python manage.py migrate 

echo "### Obter arquivos estáticos ###"
python manage.py collectstatic 
