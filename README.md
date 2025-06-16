# CheckIN - API (Backend)

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=yellow) ![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue?logo=postgresql)

## 📝 Descrição

Este é o repositório do backend para o aplicativo **CheckIN**. Desenvolvido com a velocidade e a robustez do framework **FastAPI**, esta API é responsável por toda a lógica de negócio, gerenciamento de dados e autenticação para a plataforma.

Ela foi arquitetada por *Henrique Fontaine* para servir de base para a visão do projeto concebida em conjunto com *Gabriela Sotero*, fornecendo os dados e as funcionalidades que permitem a união entre a descoberta de lugares e a conexão entre pessoas.

## ✨ Principais Funcionalidades (Endpoints)

A API fornece uma interface RESTful para as seguintes funcionalidades:

* **Autenticação de Usuários:** Rotas para cadastro, login (`/token`) e gerenciamento de perfis, utilizando tokens JWT para segurança.
* **Gerenciamento de Lugares/Eventos:** Endpoints CRUD (Create, Read, Update, Delete) para locais e eventos.
* **Sistema de Check-in:** Lógica para realizar e registrar check-ins de usuários nos locais.
* **Rede Social:** Funcionalidades para gerenciar amizades e obter a localização de amigos (com consentimento).
* **Recomendações:** Lógica de negócio para sugerir lugares com base nas preferências e contexto do usuário.

## 🛠️ Stack Tecnológica

* **Framework:** [**FastAPI**](https://fastapi.tiangolo.com/)
* **Servidor ASGI:** [**Uvicorn**](https://www.uvicorn.org/)
* **Validação de Dados:** [**Pydantic**](https://docs.pydantic.dev/)
* **Banco de Dados:** [**PostgreSQL**](https://www.postgresql.org/)
* **ORM:** [**SQLAlchemy**](https://www.sqlalchemy.org/)
* **Migrações de Banco de Dados:** [**Alembic**](https://alembic.sqlalchemy.org/)
* **Autenticação:** Tokens JWT com a biblioteca `python-jose`.

## 📚 Documentação da API

Uma das grandes vantagens do FastAPI é a **documentação automática e interativa**. Após iniciar o servidor, você pode acessá-la em:

* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Nessas páginas, você pode visualizar todos os endpoints, seus parâmetros, schemas de resposta e até mesmo testá-los diretamente do seu navegador.

## ⚙️ Como Rodar o Projeto Localmente

Siga os passos abaixo para configurar e executar a API em seu ambiente de desenvolvimento.

### Pré-requisitos

* [Python](https://www.python.org/) 3.9 ou superior
* [Git](https://git-scm.com/)
* Um servidor [PostgreSQL](https://www.postgresql.org/download/) ativo
* Gerenciador de pacotes `pip` e `venv`

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    # Substitua 'SEU-USUARIO' pelo seu nome de usuário do GitHub
    git clone [https://github.com/SEU-USUARIO/CheckIN-Backend.git](https://github.com/SEU-USUARIO/CheckIN-Backend.git)
    cd CheckIN-Backend
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Criar o ambiente
    python -m venv venv

    # Ativar (Linux/macOS)
    source venv/bin/activate

    # Ativar (Windows)
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências do projeto:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    Crie um arquivo chamado `.env` na raiz do projeto, copiando o exemplo `.env.example`.
    ```bash
    cp .env.example .env
    ```
    Agora, edite o arquivo `.env` com as suas credenciais e configurações. Ele se parecerá com isto:
    ```ini
    # Configuração do Banco de Dados (Exemplo para PostgreSQL)
    DATABASE_URL="postgresql://user:password@host:port/database_name"

    # Configuração do JWT para autenticação
    SECRET_KEY="sua_chave_secreta_super_segura_aqui"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

5.  **Aplique as migrações do banco de dados:**
    (Este passo cria as tabelas no seu banco de dados com base nos modelos definidos)
    ```bash
    alembic upgrade head
    ```

6.  **Execute o servidor de desenvolvimento:**
    ```bash
    uvicorn app.main:app --reload
    ```
    * `app.main`: o arquivo `main.py` dentro da pasta `app`.
    * `app`: o objeto `FastAPI()` criado dentro do arquivo.
    * `--reload`: reinicia o servidor automaticamente a cada mudança no código.

7.  **Pronto!** A API estará rodando em `http://127.0.0.1:8000`.

## 🤝 Contribuição

Sinta-se à vontade para abrir uma *issue* para discutir mudanças ou enviar um *pull request*.

## 📄 Licença

Este projeto está sob a licença MIT.
