# 🔧 Configuração do Backend CheckIn

## 🚨 Problema Resolvido

O erro `npm error Missing script: "start"` ocorreu porque você estava tentando usar comandos Node.js (`npm start`) em um projeto Python/FastAPI.

## ✅ Solução

### **1. Ambiente Python**
O backend CheckIn é um projeto **Python/FastAPI**, não Node.js.

### **2. Como Executar Corretamente**

#### **Opção A: Script Automático**
```bash
cd checkin-backend
chmod +x start.sh
./start.sh
```

#### **Opção B: Manual**
```bash
cd checkin-backend

# 1. Criar ambiente virtual
python3 -m venv venv

# 2. Ativar ambiente virtual
source venv/bin/activate  # Mac/Linux
# ou
venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar .env
cp env.example .env
# Editar .env com suas credenciais

# 5. Executar servidor
python run.py
```

## 🔧 Configuração do .env

O arquivo `.env` já está configurado com as credenciais do Supabase:

```env
# Configurações do Banco de Dados - Supabase
DATABASE_URL=postgresql://postgres:checkinvinicius123456@db.nwikoaogixmhiiqcdxqs.supabase.co:5432/postgres

# Configurações de Segurança
SECRET_KEY=checkin_super_secret_key_2024_very_secure_and_unique
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configurações do Servidor
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

## 🌐 Endpoints Disponíveis

### **Públicos**
- `GET /` - Página inicial
- `GET /health` - Verificação de saúde da API
- `POST /register` - Registro de usuário
- `POST /login` - Login de usuário

### **Protegidos**
- `GET /users/me` - Obter dados do usuário atual

## 📖 Documentação

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testando a API

### **1. Health Check**
```bash
curl http://localhost:8000/health
```

### **2. Registrar Usuário**
```bash
curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/json" \
     -d '{"email": "teste@example.com", "password": "123456"}'
```

### **3. Fazer Login**
```bash
curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=teste@example.com&password=123456"
```

## 🔍 Troubleshooting

### **Erro: "npm start"**
- **Causa**: Tentando usar Node.js em projeto Python
- **Solução**: Use `python run.py` ou `./start.sh`

### **Erro: "Module not found"**
- **Causa**: Dependências não instaladas
- **Solução**: `pip install -r requirements.txt`

### **Erro: "Connection refused"**
- **Causa**: Servidor não iniciado
- **Solução**: Execute `python run.py`

### **Erro: "Database connection failed"**
- **Causa**: Credenciais do Supabase incorretas
- **Solução**: Verifique o arquivo `.env`

## 📁 Estrutura do Projeto

```
checkin-backend/
├── app/
│   ├── main.py          # Aplicação FastAPI
│   ├── models.py        # Modelos SQLAlchemy
│   ├── schemas.py       # Schemas Pydantic
│   ├── crud.py          # Operações CRUD
│   ├── auth.py          # Autenticação JWT
│   ├── database.py      # Configuração do banco
│   └── config.py        # Configurações
├── requirements.txt      # Dependências Python
├── run.py              # Script de execução
├── start.sh            # Script de inicialização
├── env.example         # Exemplo de variáveis
├── .env                # Variáveis de ambiente
└── README.md           # Documentação
```

## 🎯 Próximos Passos

1. **Executar Backend**: `./start.sh`
2. **Testar API**: Acesse http://localhost:8000/docs
3. **Integrar Frontend**: Configure o frontend para usar a API
4. **Testar Funcionalidades**: Registro, login, endpoints protegidos

## 🔗 Integração com Frontend

O frontend (React) pode se comunicar com o backend (FastAPI) através dos endpoints REST. Configure as URLs da API no frontend para apontar para `http://localhost:8000`.

---

**Status**: ✅ **PROBLEMA RESOLVIDO** 