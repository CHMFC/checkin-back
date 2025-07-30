# CheckIn Backend API

API REST para sistema de CheckIn desenvolvida com FastAPI e PostgreSQL.

## 🚀 Funcionalidades

- ✅ Autenticação JWT
- ✅ Registro de usuários
- ✅ Login de usuários
- ✅ Endpoints protegidos
- ✅ Validação de dados com Pydantic
- ✅ CORS configurado
- ✅ Documentação automática (Swagger/OpenAPI)

## 📋 Pré-requisitos

- Python 3.8+
- PostgreSQL
- pip

## 🛠️ Instalação

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd checkin-back
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados**
   - Crie um banco PostgreSQL
   - Copie o arquivo `env.example` para `.env`
   - Edite o arquivo `.env` com suas configurações:

```env
DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost/seu_banco
SECRET_KEY=sua_chave_secreta_muito_segura_aqui
```

5. **Execute o servidor**
```bash
python run.py
```

## 📚 Endpoints da API

### Públicos
- `GET /` - Página inicial
- `GET /health` - Verificação de saúde da API
- `POST /register` - Registro de usuário
- `POST /login` - Login de usuário

### Protegidos (requer autenticação)
- `GET /users/me` - Obter dados do usuário atual

## 🔐 Autenticação

A API usa JWT (JSON Web Tokens) para autenticação:

1. **Registre um usuário:**
```bash
curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "senha123"}'
```

2. **Faça login:**
```bash
curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=user@example.com&password=senha123"
```

3. **Use o token em requisições protegidas:**
```bash
curl -X GET "http://localhost:8000/users/me" \
     -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 📖 Documentação

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testando a API

### Com curl:

1. **Registrar usuário:**
```bash
curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/json" \
     -d '{"email": "teste@example.com", "password": "123456"}'
```

2. **Fazer login:**
```bash
curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=teste@example.com&password=123456"
```

3. **Acessar endpoint protegido:**
```bash
curl -X GET "http://localhost:8000/users/me" \
     -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` baseado no `env.example`:

```env
# Configurações do Banco de Dados
DATABASE_URL=postgresql://usuario:senha@localhost/nome_do_banco

# Configurações de Segurança
SECRET_KEY=sua_chave_secreta_muito_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configurações do Servidor
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

## 📁 Estrutura do Projeto

```
checkin-back/
├── app/
│   ├── __init__.py
│   ├── main.py          # Aplicação FastAPI
│   ├── models.py        # Modelos SQLAlchemy
│   ├── schemas.py       # Schemas Pydantic
│   ├── crud.py          # Operações CRUD
│   ├── auth.py          # Autenticação JWT
│   ├── database.py      # Configuração do banco
│   └── config.py        # Configurações
├── requirements.txt      # Dependências
├── run.py              # Script de execução
├── env.example         # Exemplo de variáveis de ambiente
└── README.md           # Este arquivo
```

## 🚨 Segurança

- ✅ Senhas hasheadas com bcrypt
- ✅ Tokens JWT com expiração
- ✅ Validação de email
- ✅ CORS configurado
- ⚠️ **IMPORTANTE**: Em produção, sempre use uma SECRET_KEY forte e única

## 🔄 Próximos Passos

- [ ] Adicionar testes unitários
- [ ] Implementar refresh tokens
- [ ] Adicionar logs estruturados
- [ ] Implementar rate limiting
- [ ] Adicionar validação de força de senha
- [ ] Implementar recuperação de senha
- [ ] Adicionar monitoramento e métricas

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
