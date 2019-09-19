# El Royale API

API RESTFul de gerenciamento de cadastro de hotéis, desenvolvida para o desáfio da Stopover.

O nome El Royale é inspirado no filme Maus Momentos no Hotel Royale de 2018.

## Descrição

As instruções a seguir, irão mostrar como rodar o projeto em sua máquina.

### Pré-requisitos

É preciso ter o Docker e Docker Compose instalados.

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

```
docker-compose run web python /code/manage.py createsuperuser
```

Estes são os endpoints disponibilizados pela API:

| Endpoints             | Métodos | Descrição |
| --------------------- | ------- | --------- |
| api/v1/users/         | POST    |           |
| api/v1/login/         | POST    |           |
| api/v1/login/refresh/ | POST    |           |
| api/v1/hotels/        | POST    |           |
| api/v1/hotels/        | GET     |           |
| api/v1/hotels/?page   | GET     |           |
| api/v1/hotels/id/     | GET     |           |
| api/v1/hotels/id/     | PUT     |           |
| api/v1/hotels/?state  | GET     |           |
| api/v1/hotels/?city   | GET     |           |
| api/v1/rooms/         | POST    |           |
| api/v1/rooms/         | GET     |           |
| api/v1/rooms/id/      | GET     |           |
| api/v1/rooms/id/      | PUT     |           |

Também é possível consultar a [documentção](https://documenter.getpostman.com/view/3396193/SVmwvd7Y) gerada pelo Postman.

Os testes podem ser feitos utilizando a [collection de exemplo](https://www.getpostman.com/collections/f4fdd8fe943d8b24239a).

### Estilo de código

O projeto utiliza o guia de estiolos do [PEP8](https://www.python.org/dev/peps/pep-0008/).

## Feito utilizando

- Docker
- Docker Compose
- Python
- Pipenv
- Django
- Django REST Framework
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
