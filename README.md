# PSI AI API

API para processamento de sessões de psicoterapia com IA, utilizando OpenAI para transcrição e análise de áudios.

## Funcionalidades

- Upload e armazenamento de áudios de sessões
- Transcrição automática usando Whisper API
- Geração de resumos completos
- Geração de resumos anonimizados para compartilhamento
- Identificação de demandas do paciente
- Geração de contexto da sessão

## Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
# Crie um arquivo .env com as seguintes variáveis:
OPENAI_API_KEY=sk-your-openai-api-key-here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key-here
SUPABASE_STORAGE_BUCKET=audio-sessions
API_KEY=your-secret-api-key-here
```

**Importante**: A `API_KEY` é obrigatória para autenticação. Gere uma chave segura usando:
```bash
python3 generate_api_key.py
```

## Configuração do Supabase

As tabelas e configurações já foram criadas automaticamente via MCP.

### Estrutura do Banco

- **sessions**: Armazena todas as sessões e seus dados processados
- **Storage Bucket**: `audio-sessions` para armazenar os arquivos de áudio

## Execução

### Desenvolvimento Local

```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`

Documentação interativa: `http://localhost:8000/docs`

### Docker

```bash
# Build da imagem
docker build -t psi-ai-api .

# Executar container
docker run -p 8000:8000 --env-file .env psi-ai-api
```

### Docker Compose

```bash
docker-compose up -d
```

### Deploy no Portainer

Consulte o arquivo [DEPLOY.md](./DEPLOY.md) para instruções detalhadas de deploy no Portainer.

## Endpoints

### POST /sessions/
Cria uma nova sessão e processa o áudio.

**Parâmetros:**
- `psychologist_id`: UUID do psicólogo
- `patient_id`: UUID do paciente
- `audio`: Arquivo de áudio (multipart/form-data)

### GET /sessions/{session_id}
Busca uma sessão específica.

### GET /sessions/
Lista todas as sessões (com filtros opcionais `psychologist_id` e `patient_id`).

## Autenticação

Todas as rotas (exceto `/` e `/health`) exigem autenticação via API_KEY.

Envie a API_KEY no header `X-API-Key` em todas as requisições:

```bash
curl -X GET "http://localhost:8000/sessions/" \
  -H "X-API-Key: sua-api-key-aqui"
```

## Variáveis de Ambiente

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `OPENAI_API_KEY` | Sim | Chave da API OpenAI |
| `SUPABASE_URL` | Sim | URL do projeto Supabase |
| `SUPABASE_KEY` | Sim | Chave anon do Supabase |
| `API_KEY` | Sim | Chave de autenticação da API |
| `SUPABASE_STORAGE_BUCKET` | Não | Nome do bucket (padrão: `audio-sessions`) |
| `PORT` | Não | Porta do servidor (padrão: `8000`) |

## Tecnologias

- FastAPI
- OpenAI API (Whisper + GPT-4)
- Supabase (PostgreSQL + Storage)
- Python 3.11+
- Docker

