# El Royale API

API RESTFul de gerenciamento de cadastro de hotéis, desenvolvida para o desáfio da Stopover.

O nome El Royale é inspirado no filme: Maus Momentos no Hotel Royale de 2018.

## Descrição

As instruções a seguir, irão mostrar como rodar o projeto em sua máquina.

### Pré-requisitos

É preciso ter o Docker e o Docker Compose instalados.

Por exemplo, no Arch Linux:

```sh
sudo pacman -S docker docker-compose
```

### Inicializando

Clone o repositório:

```sh
git clone https://github.com/robsonsilv4/ElRoyale.git && cd ElRoyale
```

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

A documentação está dispovível em [api/v1/docs/](http://127.0.0.1:8000/api/v1/docs/).

Também há uma interface web, caso os recursos sejam acessados utilizando o browser.

Os testes podem ser realizados com o Postman, utilizando a [collection de exemplo](collection).

### Estilo de código

O projeto utiliza o guia de estilos do [PEP8](https://www.python.org/dev/peps/pep-0008/).

## Feito utilizando

- Docker
- Docker Compose
- Python
- Pipenv
- Django
- Usuário Customizado
- Django REST Framework
- CORS
- JWT
- Filtros
- PostgreSQL
- SQLite3
- Postman
- Arch Linux
- Visual Studio Code

## Autor

- **Robson Silva** - [robsonsilv4](https://github.com/robsonsilv4)

## Licença

Esse projeto está licensiado sob os termos da licença do MIT - veja o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.
