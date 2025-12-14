# PSI AI API - Documentação Completa

## Visão Geral

A PSI AI API é uma API REST para processamento de sessões de psicoterapia com Inteligência Artificial. A API permite:

- Upload e transcrição de áudios de sessões
- Geração automática de resumos completos e anonimizados
- Análise FAP (Functional Analytic Psychotherapy)
- Identificação de demandas do paciente
- Geração de contexto da sessão

**Base URL**: `http://localhost:8000` (desenvolvimento) ou `https://seu-dominio.com` (produção)

**Versão da API**: 1.0.0

**Formato de Dados**: JSON (exceto upload de arquivos que usa `multipart/form-data`)

---

## Autenticação

Todas as rotas (exceto `/` e `/health`) exigem autenticação via API Key.

### Método de Autenticação

Envie a API Key no header HTTP `X-API-Key` em todas as requisições autenticadas.

**Header:**
```
X-API-Key: sua-api-key-aqui
```

### Rotas Públicas (sem autenticação)

- `GET /` - Informações da API
- `GET /health` - Health check

### Rotas Protegidas (requerem autenticação)

Todas as outras rotas exigem o header `X-API-Key`.

**Códigos de Resposta de Autenticação:**
- `401 Unauthorized` - API Key não fornecida
- `403 Forbidden` - API Key inválida

---

## Modelos de Dados

### UUID
Todos os IDs são UUIDs no formato: `550e8400-e29b-41d4-a716-446655440000`

### DateTime
Datas são retornadas no formato ISO 8601: `2024-12-14T16:07:32.368883+00:00`

---

## Modelos de Entidade

### Session (Sessão)

**SessionResponse:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "psychologist_id": "550e8400-e29b-41d4-a716-446655440001",
  "patient_id": "550e8400-e29b-41d4-a716-446655440002",
  "audio_url": "https://supabase.co/storage/v1/object/public/audio-sessions/...",
  "transcription": "Transcrição completa do áudio...",
  "full_summary": "Resumo completo e detalhado da sessão...",
  "anonymous_summary": "Resumo anonimizado sem dados pessoais...",
  "patient_demand": "Demanda principal identificada...",
  "context": "Contexto da sessão incluindo situação atual...",
  "analise_da_ia": "Análise FAP completa da sessão...",
  "created_at": "2024-12-14T16:07:32.368883+00:00",
  "updated_at": "2024-12-14T16:07:32.368883+00:00"
}
```

**Campos:**
- `id` (UUID, obrigatório) - ID único da sessão
- `psychologist_id` (UUID, obrigatório) - ID do psicólogo
- `patient_id` (UUID, obrigatório) - ID do paciente
- `audio_url` (string, opcional) - URL do arquivo de áudio no Supabase Storage
- `transcription` (string, opcional) - Transcrição completa do áudio
- `full_summary` (string, opcional) - Resumo completo da sessão
- `anonymous_summary` (string, opcional) - Resumo anonimizado
- `patient_demand` (string, opcional) - Demanda principal do paciente
- `context` (string, opcional) - Contexto da sessão
- `analise_da_ia` (string, opcional) - Análise FAP completa gerada pela IA
- `created_at` (datetime, obrigatório) - Data de criação
- `updated_at` (datetime, obrigatório) - Data de última atualização

### Psychologist (Psicólogo)

**PsychologistCreate:**
```json
{
  "name": "Dr. João Silva",
  "email": "joao.silva@example.com"
}
```

**PsychologistResponse:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "name": "Dr. João Silva",
  "email": "joao.silva@example.com",
  "created_at": "2024-12-14T16:07:32.368883+00:00",
  "updated_at": "2024-12-14T16:07:32.368883+00:00"
}
```

**Campos:**
- `id` (UUID, obrigatório) - ID único do psicólogo
- `name` (string, obrigatório) - Nome do psicólogo
- `email` (string, opcional) - Email do psicólogo (formato válido)
- `created_at` (datetime, obrigatório) - Data de criação
- `updated_at` (datetime, obrigatório) - Data de última atualização

### Patient (Paciente)

**PatientCreate:**
```json
{
  "name": "Maria Santos"
}
```

**PatientResponse:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "name": "Maria Santos",
  "created_at": "2024-12-14T16:07:32.368883+00:00",
  "updated_at": "2024-12-14T16:07:32.368883+00:00"
}
```

**Campos:**
- `id` (UUID, obrigatório) - ID único do paciente
- `name` (string, obrigatório) - Nome do paciente
- `created_at` (datetime, obrigatório) - Data de criação
- `updated_at` (datetime, obrigatório) - Data de última atualização

---

## Endpoints

### Informações da API

#### GET /

Retorna informações básicas da API.

**Autenticação:** Não requerida

**Resposta 200 OK:**
```json
{
  "message": "PSI AI API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

### Health Check

#### GET /health

Verifica o status da API.

**Autenticação:** Não requerida

**Resposta 200 OK:**
```json
{
  "status": "healthy"
}
```

---

### Sessões

#### POST /sessions/

Cria uma nova sessão e processa o áudio completamente. A API retorna apenas quando todo o processamento estiver concluído (transcrição, resumos, análise FAP).

**Autenticação:** Requerida

**Content-Type:** `multipart/form-data`

**Parâmetros:**
- `psychologist_id` (UUID, obrigatório) - ID do psicólogo
- `patient_id` (UUID, obrigatório) - ID do paciente
- `audio` (File, obrigatório) - Arquivo de áudio (formatos suportados: mp3, wav, m4a, ogg)

**Exemplo de Requisição (cURL):**
```bash
curl -X POST "http://localhost:8000/sessions/" \
  -H "X-API-Key: sua-api-key-aqui" \
  -F "psychologist_id=550e8400-e29b-41d4-a716-446655440001" \
  -F "patient_id=550e8400-e29b-41d4-a716-446655440002" \
  -F "audio=@sessao.mp3"
```

**Exemplo de Requisição (JavaScript/Fetch):**
```javascript
const formData = new FormData();
formData.append('psychologist_id', '550e8400-e29b-41d4-a716-446655440001');
formData.append('patient_id', '550e8400-e29b-41d4-a716-446655440002');
formData.append('audio', audioFile); // File object

const response = await fetch('http://localhost:8000/sessions/', {
  method: 'POST',
  headers: {
    'X-API-Key': 'sua-api-key-aqui'
  },
  body: formData
});

const session = await response.json();
```

**Resposta 200 OK:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "psychologist_id": "550e8400-e29b-41d4-a716-446655440001",
  "patient_id": "550e8400-e29b-41d4-a716-446655440002",
  "audio_url": "https://supabase.co/storage/v1/object/public/audio-sessions/uuid_arquivo.mp3",
  "transcription": "Transcrição completa do áudio da sessão...",
  "full_summary": "Resumo completo e detalhado da sessão...",
  "anonymous_summary": "Resumo anonimizado sem dados pessoais...",
  "patient_demand": "Demanda principal identificada pelo paciente...",
  "context": "Contexto da sessão incluindo situação atual do paciente...",
  "analise_da_ia": "Análise FAP completa seguindo o formato do livro 'FAP Descomplicada'...",
  "created_at": "2024-12-14T16:07:32.368883+00:00",
  "updated_at": "2024-12-14T16:07:32.368883+00:00"
}
```

**Códigos de Resposta:**
- `200 OK` - Sessão criada e processada com sucesso
- `400 Bad Request` - Erro no upload do áudio (ex: bucket não encontrado)
- `401 Unauthorized` - API Key não fornecida
- `403 Forbidden` - API Key inválida
- `422 Unprocessable Entity` - Dados inválidos (ex: UUID inválido)
- `500 Internal Server Error` - Erro no processamento

**Notas Importantes:**
- ⚠️ Esta requisição pode demorar vários minutos, pois processa o áudio completamente antes de retornar
- O processamento inclui: transcrição (Whisper), geração de resumos (GPT-4) e análise FAP
- A resposta só é retornada quando todos os dados estão processados e salvos

---

#### GET /sessions/

Lista todas as sessões com filtros opcionais.

**Autenticação:** Requerida

**Query Parameters:**
- `psychologist_id` (UUID, opcional) - Filtrar por psicólogo
- `patient_id` (UUID, opcional) - Filtrar por paciente

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:8000/sessions/?psychologist_id=550e8400-e29b-41d4-a716-446655440001" \
  -H "X-API-Key: sua-api-key-aqui"
```

**Resposta 200 OK:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "psychologist_id": "550e8400-e29b-41d4-a716-446655440001",
    "patient_id": "550e8400-e29b-41d4-a716-446655440002",
    "audio_url": "https://supabase.co/storage/v1/object/public/audio-sessions/...",
    "transcription": "...",
    "full_summary": "...",
    "anonymous_summary": "...",
    "patient_demand": "...",
    "context": "...",
    "analise_da_ia": "...",
    "created_at": "2024-12-14T16:07:32.368883+00:00",
    "updated_at": "2024-12-14T16:07:32.368883+00:00"
  }
]
```

**Códigos de Resposta:**
- `200 OK` - Lista de sessões
- `401 Unauthorized` - API Key não fornecida
- `403 Forbidden` - API Key inválida

---

#### GET /sessions/{session_id}

Busca uma sessão específica por ID.

**Autenticação:** Requerida

**Path Parameters:**
- `session_id` (UUID, obrigatório) - ID da sessão

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:8000/sessions/550e8400-e29b-41d4-a716-446655440000" \
  -H "X-API-Key: sua-api-key-aqui"
```

**Resposta 200 OK:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "psychologist_id": "550e8400-e29b-41d4-a716-446655440001",
  "patient_id": "550e8400-e29b-41d4-a716-446655440002",
  "audio_url": "https://supabase.co/storage/v1/object/public/audio-sessions/...",
  "transcription": "...",
  "full_summary": "...",
  "anonymous_summary": "...",
  "patient_demand": "...",
  "context": "...",
  "analise_da_ia": "...",
  "created_at": "2024-12-14T16:07:32.368883+00:00",
  "updated_at": "2024-12-14T16:07:32.368883+00:00"
}
```

**Códigos de Resposta:**
- `200 OK` - Sessão encontrada
- `401 Unauthorized` - API Key não fornecida
- `403 Forbidden` - API Key inválida
- `404 Not Found` - Sessão não encontrada

---

### Psicólogos

#### POST /psychologists/

Cria um novo psicólogo.

**Autenticação:** Requerida

**Content-Type:** `application/json`

**Body:**
```json
{
  "name": "Dr. João Silva",
  "email": "joao.silva@example.com"
}
```

**Exemplo de Requisição:**
```bash
curl -X POST "http://localhost:8000/psychologists/" \
  -H "X-API-Key: sua-api-key-aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. João Silva",
    "email": "joao.silva@example.com"
  }'
```

**Resposta 201 Created:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "name": "Dr. João Silva",
  "email": "joao.silva@example.com",
  "created_at": "2024-12-14T16:07:32.368883+00:00",
  "updated_at": "2024-12-14T16:07:32.368883+00:00"
}
```

**Códigos de Resposta:**
- `201 Created` - Psicólogo criado com sucesso
- `400 Bad Request` - Dados inválidos
- `401 Unauthorized` - API Key não fornecida
- `403 Forbidden` - API Key inválida
- `500 Internal Server Error` - Erro ao criar psicólogo

---

#### GET /psychologists/

Lista todos os psicólogos.

**Autenticação:** Requerida

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:8000/psychologists/" \
  -H "X-API-Key: sua-api-key-aqui"
```

**Resposta 200 OK:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "name": "Dr. João Silva",
    "email": "joao.silva@example.com",
    "created_at": "2024-12-14T16:07:32.368883+00:00",
    "updated_at": "2024-12-14T16:07:32.368883+00:00"
  }
]
```

**Códigos de Resposta:**
- `200 OK` - Lista de psicólogos
- `401 Unauthorized` - API Key não fornecida
- `403 Forbidden` - API Key inválida

---

#### GET /psychologists/{psychologist_id}

Busca um psicólogo específico por ID.

**Autenticação:** Requerida

**Path Parameters:**
- `psychologist_id` (UUID, obrigatório) - ID do psicólogo

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:8000/psychologists/550e8400-e29b-41d4-a716-446655440001" \
  -H "X-API-Key: sua-api-key-aqui"
```

**Resposta 200 OK:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "name": "Dr. João Silva",
  "email": "joao.silva@example.com",
  "created_at": "2024-12-14T16:07:32.368883+00:00",
  "updated_at": "2024-12-14T16:07:32.368883+00:00"
}
```

**Códigos de Resposta:**
- `200 OK` - Psicólogo encontrado
- `401 Unauthorized` - API Key não fornecida
- `403 Forbidden` - API Key inválida
- `404 Not Found` - Psicólogo não encontrado

---

### Pacientes

#### POST /patients/

Cria um novo paciente.

**Autenticação:** Requerida

**Content-Type:** `application/json`

**Body:**
```json
{
  "name": "Maria Santos"
}
```

**Exemplo de Requisição:**
```bash
curl -X POST "http://localhost:8000/patients/" \
  -H "X-API-Key: sua-api-key-aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Maria Santos"
  }'
```

**Resposta 201 Created:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "name": "Maria Santos",
  "created_at": "2024-12-14T16:07:32.368883+00:00",
  "updated_at": "2024-12-14T16:07:32.368883+00:00"
}
```

**Códigos de Resposta:**
- `201 Created` - Paciente criado com sucesso
- `400 Bad Request` - Dados inválidos
- `401 Unauthorized` - API Key não fornecida
- `403 Forbidden` - API Key inválida
- `500 Internal Server Error` - Erro ao criar paciente

---

#### GET /patients/

Lista todos os pacientes.

**Autenticação:** Requerida

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:8000/patients/" \
  -H "X-API-Key: sua-api-key-aqui"
```

**Resposta 200 OK:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "name": "Maria Santos",
    "created_at": "2024-12-14T16:07:32.368883+00:00",
    "updated_at": "2024-12-14T16:07:32.368883+00:00"
  }
]
```

**Códigos de Resposta:**
- `200 OK` - Lista de pacientes
- `401 Unauthorized` - API Key não fornecida
- `403 Forbidden` - API Key inválida

---

#### GET /patients/{patient_id}

Busca um paciente específico por ID.

**Autenticação:** Requerida

**Path Parameters:**
- `patient_id` (UUID, obrigatório) - ID do paciente

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:8000/patients/550e8400-e29b-41d4-a716-446655440002" \
  -H "X-API-Key: sua-api-key-aqui"
```

**Resposta 200 OK:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "name": "Maria Santos",
  "created_at": "2024-12-14T16:07:32.368883+00:00",
  "updated_at": "2024-12-14T16:07:32.368883+00:00"
}
```

**Códigos de Resposta:**
- `200 OK` - Paciente encontrado
- `401 Unauthorized` - API Key não fornecida
- `403 Forbidden` - API Key inválida
- `404 Not Found` - Paciente não encontrado

---

## Códigos de Resposta HTTP

| Código | Descrição |
|--------|-----------|
| `200 OK` | Requisição bem-sucedida |
| `201 Created` | Recurso criado com sucesso |
| `400 Bad Request` | Dados inválidos na requisição |
| `401 Unauthorized` | API Key não fornecida |
| `403 Forbidden` | API Key inválida |
| `404 Not Found` | Recurso não encontrado |
| `422 Unprocessable Entity` | Dados válidos mas não processáveis (ex: UUID inválido) |
| `500 Internal Server Error` | Erro interno do servidor |

---

## Estrutura de Erros

Quando ocorre um erro, a API retorna um objeto JSON com a seguinte estrutura:

```json
{
  "detail": "Mensagem de erro descritiva"
}
```

**Exemplos de Erros:**

**401 Unauthorized:**
```json
{
  "detail": "API_KEY é obrigatória. Envie no header 'X-API-Key'"
}
```

**403 Forbidden:**
```json
{
  "detail": "API_KEY inválida"
}
```

**404 Not Found:**
```json
{
  "detail": "Sessão não encontrada"
}
```

**422 Unprocessable Entity:**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["query", "psychologist_id"],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Erro ao processar sessão: [descrição do erro]"
}
```

---

## Exemplos de Uso Completos

### Fluxo Completo: Criar Sessão

1. **Criar Psicólogo:**
```javascript
const psychologist = await fetch('http://localhost:8000/psychologists/', {
  method: 'POST',
  headers: {
    'X-API-Key': 'sua-api-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Dr. João Silva',
    email: 'joao.silva@example.com'
  })
});
const psychologistData = await psychologist.json();
```

2. **Criar Paciente:**
```javascript
const patient = await fetch('http://localhost:8000/patients/', {
  method: 'POST',
  headers: {
    'X-API-Key': 'sua-api-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Maria Santos'
  })
});
const patientData = await patient.json();
```

3. **Criar Sessão com Áudio:**
```javascript
const formData = new FormData();
formData.append('psychologist_id', psychologistData.id);
formData.append('patient_id', patientData.id);
formData.append('audio', audioFile); // File object do input

const session = await fetch('http://localhost:8000/sessions/', {
  method: 'POST',
  headers: {
    'X-API-Key': 'sua-api-key'
    // NÃO inclua Content-Type, o browser define automaticamente para FormData
  },
  body: formData
});

const sessionData = await session.json();
// sessionData contém todos os dados processados:
// - transcription
// - full_summary
// - anonymous_summary
// - patient_demand
// - context
// - analise_da_ia
```

4. **Listar Sessões do Psicólogo:**
```javascript
const sessions = await fetch(
  `http://localhost:8000/sessions/?psychologist_id=${psychologistData.id}`,
  {
    headers: {
      'X-API-Key': 'sua-api-key'
    }
  }
);
const sessionsData = await sessions.json();
```

---

## Notas Importantes para o Frontend

### 1. Upload de Áudio

- Use `FormData` para enviar arquivos
- Não defina `Content-Type` manualmente ao usar `FormData` - o browser faz isso automaticamente
- Formatos suportados: mp3, wav, m4a, ogg
- O processamento pode demorar vários minutos - considere mostrar um loading

### 2. Autenticação

- Sempre inclua o header `X-API-Key` em todas as requisições (exceto `/` e `/health`)
- Armazene a API Key de forma segura (não commite no código)
- Considere usar variáveis de ambiente no frontend

### 3. Tratamento de Erros

- Sempre verifique o status HTTP antes de processar a resposta
- Trate especialmente os códigos 401 e 403 para redirecionar para login/configuração
- Para 500, mostre mensagem amigável ao usuário

### 4. Timeout

- A rota `POST /sessions/` pode demorar muito (vários minutos)
- Configure timeout adequado (ex: 10-15 minutos)
- Considere implementar polling ou WebSocket para atualizações em tempo real (se implementado no futuro)

### 5. Formato de Datas

- Todas as datas são retornadas em ISO 8601
- Use bibliotecas como `date-fns` ou `moment.js` para formatação

### 6. UUIDs

- Todos os IDs são UUIDs
- Valide o formato antes de enviar
- Use bibliotecas como `uuid` para validação

---

## Documentação Interativa

A API também fornece documentação interativa via Swagger UI:

- **URL**: `http://localhost:8000/docs`
- Permite testar todos os endpoints diretamente no navegador
- Inclui schemas completos e exemplos

---

## Suporte

Para mais informações, consulte:
- Repositório: https://github.com/marquesedel/psiapi
- README.md no repositório

---

**Última atualização:** Dezembro 2024
**Versão da API:** 1.0.0
