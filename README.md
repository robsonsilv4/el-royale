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

## Feito utilizando

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Python](https://www.python.org/)
- [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/)
- [Django](https://www.djangoproject.com/start/)
- Usuário Customizado
- [Django REST Framework](https://www.django-rest-framework.org/)
- CORS
- [JWT](https://jwt.io/)
- Filtros
- [PostgreSQL](https://www.postgresql.org/)
- [SQLite3](https://www.sqlite.org/index.html)
- [Postman](https://www.getpostman.com/)
- [Arch Linux](https://www.archlinux.org/)
- [Visual Studio Code](https://code.visualstudio.com/)

## Autor

- **Robson Silva** - [robsonsilv4](https://github.com/robsonsilv4)

## Licença

Esse projeto está licenciado sob os termos da licença do MIT - veja o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.
