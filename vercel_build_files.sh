

# Build the project
echo "### Instalar dependências ###"
install python3-brlapi
python3.9 -m pip install --upgrade pip
python3.9 -m pip install -r requirements.txt
python -V
python3.9 -V

echo "### Executando as migrações ###"
python3.9 manage.py makemigrations 
python3.9 manage.py migrate 

echo "### Obter arquivos estáticos ###"
python3.9 manage.py collectstatic 
