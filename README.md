# El Royale API

API RESTFul de gerenciamento de cadastro de hotéis, desenvolvida para o desafio da Stopover.

O nome El Royale é inspirado no filme: Maus Momentos no Hotel Royale de 2018.

## Descrição

As instruções a seguir apresentam como rodar o projeto em sua máquina.

### Pré-requisitos

É preciso ter o Docker e o Docker Compose instalados.

Por exemplo, no Arch Linux:

```sh
sudo pacman -S docker docker-compose
```

### Inicialização

Clone o repositório:

```sh
git clone https://github.com/robsonsilv4/el-royale.git && cd el-royale
```

Configure as variáveis de ambiente copiando o exemplo e gerando uma chave secreta real:

```sh
cp .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Cole o valor gerado como `DJANGO_SECRET_KEY` no arquivo `.env`.

Após, execute as migrations e inicie o container:

```sh
docker-compose run web python /code/manage.py migrate --noinput

docker-compose up -d --build
```

Caso queira criar um usuário administrador, execute:

```sh
docker-compose run web python /code/manage.py createsuperuser
```

Para carregar os dados iniciais do banco, execute:

```
docker-compose run web python /code/manage.py loaddata fixtures.json
```

### Documentação e testes

A documentação está disponível em [api/v1/docs/](http://127.0.0.1:8000/api/v1/docs/).

Se deseja acessar os recursos utilizando o browser (navegador), há uma interface web disponível.

Para executar a suíte de testes automatizados:

```sh
docker-compose run web python /code/manage.py test
```

Os testes também podem ser realizados com o Postman, utilizando a [collection de exemplo](collection).

### Estilo de código

O projeto utiliza o guia de estilos do [PEP8](https://peps.python.org/pep-0008/).

## Stack

- [Django 5.2](https://www.djangoproject.com/) (Python 3.14)
- [Django REST Framework 3.18](https://www.django-rest-framework.org/)
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [django-filter](https://django-filter.readthedocs.io/)
- [django-cors-headers](https://github.com/adamchainz/django-cors-headers)
- [drf-nested-routers](https://github.com/alanjds/drf-nested-routers)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/) (Swagger em `/api/v1/docs/` e schema em `/api/v1/schema/`)
- [PostgreSQL](https://www.postgresql.org/) / [SQLite](https://www.sqlite.org/)
- [Docker](https://www.docker.com/) / [Docker Compose](https://docs.docker.com/compose/)
- [Pipenv](https://pipenv.pypa.io/)

## Autor

- **Robson Silva** - [robsonsilv4](https://github.com/robsonsilv4)

## Licença

Esse projeto está licenciado sob os termos da licença do MIT - veja o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.
