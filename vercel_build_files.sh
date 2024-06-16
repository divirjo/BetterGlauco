

# Build the project
echo "### Instalar dependências ###"
python3.9 -m pip install --upgrade pip
python3.9 -m pip install -r requirements.txt
python -V
python3.12 -V

echo "### Executando as migrações ###"
python3.12 manage.py makemigrations 
python3.12 manage.py migrate 

echo "### Obter arquivos estáticos ###"
python3.12 manage.py collectstatic 
