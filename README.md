# -BetterGlauco


## Instalação
É necessário configurar um arquivo (.env) com as variáveis de ambiente com as seguintes constantes:

HOST_TESTES="127.0.0.1"
ATIVAR_DEBUG="True"
SECRET_KEY_DJANGO=""
DATABASE_URL=""
DATABASE_NAME=""
DATABASE_USER=""
DATABASE_PASSWORD=""



### Deploy na Vercel
Para a configuração do Django na Vercel, foram muito úteis as seguintes fontes:
* [DjangoVercel](https://github.com/maesterzak/DjangoVercel/blob/main/vercel.json)
* [How to Deploy a Django App with Postgres on Vercel](https://www.youtube.com/watch?v=Ri-pFKtMX48&t=1159s), incluindo o repositório aqui no [GitHub](https://github.com/codingforinnovations/Django-on-Vercel/blob/main/build.sh)