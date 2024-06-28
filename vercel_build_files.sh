

echo "____________________________________________________________________"
echo "                  PYENV"
echo "____________________________________________________________________"


echo "____________________________________________________________________"
echo "                  POETRY"
echo "____________________________________________________________________"
pip install pipx
pipx ensurepath
pipx install poetry

echo "____________________________________________________________________"
echo "                  DEPENDENCIAS PYTHON"
echo "____________________________________________________________________"
python3 -m poetry install
poetry -m env use python3.12
python3 -m poetry shell
python3 -m poetry env info

echo "____________________________________________________________________"
echo "                  DJANGO"
echo "____________________________________________________________________"

echo "### Executando as migrações ###"
python3 manage.py makemigrations 
python3 manage.py migrate 

echo "### Obter arquivos estáticos ###"
python3 manage.py collectstatic 
