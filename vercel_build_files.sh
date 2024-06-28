

echo "____________________________________________________________________"
echo "                  PYENV"
echo "____________________________________________________________________"
pyenv update
pyenv install 3.12:latest

echo "____________________________________________________________________"
echo "                  POETRY"
echo "____________________________________________________________________"
pip install pipx
pipx install poetry

echo "____________________________________________________________________"
echo "                  DEPENDENCIAS PYTHON"
echo "____________________________________________________________________"
poetry install


echo "____________________________________________________________________"
echo "                  DJANGO"
echo "____________________________________________________________________"

echo "### Executando as migrações ###"
python3 manage.py makemigrations 
python3 manage.py migrate 

echo "### Obter arquivos estáticos ###"
python3 manage.py collectstatic 
