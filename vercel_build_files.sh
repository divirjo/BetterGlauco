

# Build the project
echo "____________________________________________________________________"
echo "                 Instalar dependências"
echo "____________________________________________________________________"
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
#python -V
python3 -V
export PYTHONPATH="${PYTHONPATH}://python312/bin"

echo "____________________________________________________________________"
echo "                 Executando as migrações"
echo "____________________________________________________________________"
python3 manage.py makemigrations 
python3 manage.py migrate 

echo "____________________________________________________________________"
echo "                 Carregando arquivos estaticos"
echo "____________________________________________________________________"
python3 manage.py collectstatic 
