# -BetterGlauco

## Documentação

* [Documentação](/docs/Inicio.md)

## Instalação

### Variáveis de ambiente
É necessário configurar um arquivo (.env) com as variáveis de ambiente com as seguintes constantes:

HOST_TESTES="127.0.0.1"
ATIVAR_DEBUG="True"
SECRET_KEY_DJANGO=""
DB_NAME=""
DB_USER=""
DB_PASSWORD=""
DB_HOST=""
DB_PORT=""


O Banco de dados foi configurado para o Postgree SQL na [Supabase](https://supabase.com/)



### Deploy na Vercel
Para a configuração do Django na Vercel, foram muito úteis as seguintes fontes:
* [DjangoVercel](https://github.com/maesterzak/DjangoVercel/blob/main/vercel.json)
* [How to Deploy a Django App with Postgres on Vercel](https://www.youtube.com/watch?v=Ri-pFKtMX48&t=1159s), incluindo o repositório aqui no [GitHub](https://github.com/codingforinnovations/Django-on-Vercel/blob/main/build.sh)
* Conexão do Banco de Dados na Railway: [How to Start Django Project with a Database(PostgreSQL)](https://stackpython.medium.com/how-to-start-django-project-with-a-database-postgresql-aaa1d74659d8)

