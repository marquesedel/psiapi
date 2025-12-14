# Guia de Deploy - PSI AI API no Portainer

Este guia explica como fazer o deploy da PSI AI API usando Portainer.

## Pré-requisitos

- Portainer instalado e configurado
- Acesso ao Portainer (admin)
- Repositório Git com o código (ou arquivos prontos)

## Opção 1: Deploy via Git Repository (Recomendado)

### Passo 1: Preparar o Repositório

1. Certifique-se de que todos os arquivos estão commitados:
   - `Dockerfile`
   - `docker-compose.yml`
   - `.dockerignore`
   - `requirements.txt`
   - Código da aplicação

### Passo 2: Deploy no Portainer

1. **Acesse o Portainer**
   - Faça login no Portainer

2. **Crie um Stack**
   - Vá em **Stacks** > **Add stack**
   - Nome: `psi-ai-api`
   - Método: **Repository**

3. **Configure o Repository**
   - **Repository URL**: URL do seu repositório Git
   - **Repository Reference**: `main` ou `master` (ou a branch desejada)
   - **Compose path**: `docker-compose.yml`
   - **Auto-update**: Ative se quiser atualizações automáticas

4. **Configure as Variáveis de Ambiente**
   
   No campo **Environment variables**, adicione:
   ```env
   OPENAI_API_KEY=sua_chave_openai
   SUPABASE_URL=https://seu-projeto.supabase.co
   SUPABASE_KEY=sua_chave_supabase
   SUPABASE_STORAGE_BUCKET=audio-sessions
   API_KEY=sua_api_key_secreta
   ```

   **OU** configure via **Environment** no Portainer após criar o stack.

5. **Deploy**
   - Clique em **Deploy the stack**
   - Aguarde o build e deploy

### Passo 3: Verificar o Deploy

1. Vá em **Containers** e verifique se o container `psi-ai-api` está rodando
2. Acesse `http://seu-servidor:8000/health` para verificar
3. Acesse `http://seu-servidor:8000/docs` para a documentação

## Opção 2: Deploy via Dockerfile (Build Manual)

### Passo 1: Fazer Upload dos Arquivos

1. No Portainer, vá em **Stacks** > **Add stack**
2. Nome: `psi-ai-api`
3. Método: **Web editor**
4. Cole o conteúdo do `docker-compose.yml`

### Passo 2: Build e Deploy

1. Configure as variáveis de ambiente (mesmas da Opção 1)
2. Clique em **Deploy the stack**
3. O Portainer fará o build automaticamente

## Opção 3: Deploy via Container (Imagem Pré-construída)

Se você já tem uma imagem Docker:

1. **Build da Imagem** (localmente ou em CI/CD):
   ```bash
   docker build -t psi-ai-api:latest .
   docker tag psi-ai-api:latest seu-registry/psi-ai-api:latest
   docker push seu-registry/psi-ai-api:latest
   ```

2. **No Portainer**:
   - Vá em **Containers** > **Add container**
   - **Image**: `seu-registry/psi-ai-api:latest`
   - **Name**: `psi-ai-api`
   - **Port mapping**: `8000:8000`
   - Configure as variáveis de ambiente
   - Clique em **Deploy the container**

## Configuração de Variáveis de Ambiente

### Variáveis Obrigatórias

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `OPENAI_API_KEY` | Chave da API OpenAI | `sk-...` |
| `SUPABASE_URL` | URL do projeto Supabase | `https://xxx.supabase.co` |
| `SUPABASE_KEY` | Chave do Supabase | `eyJ...` |
| `API_KEY` | Chave de autenticação da API | `sua_chave_secreta` |

### Variáveis Opcionais

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `SUPABASE_STORAGE_BUCKET` | Nome do bucket de storage | `audio-sessions` |
| `PORT` | Porta do servidor | `8000` |

## Health Check

A API possui um endpoint de health check:
- **URL**: `http://seu-servidor:8000/health`
- **Método**: GET
- **Resposta**: `{"status": "healthy"}`

O Portainer pode usar este endpoint para monitoramento.

## Logs

Para ver os logs da aplicação:
1. Vá em **Containers**
2. Clique no container `psi-ai-api`
3. Aba **Logs**

## Atualização da Aplicação

### Via Git (Auto-update ativado)
- Faça push para o repositório
- O Portainer detectará e atualizará automaticamente

### Manual
1. Vá em **Stacks**
2. Clique em `psi-ai-api`
3. Clique em **Editor**
4. Faça as alterações necessárias
5. Clique em **Update the stack**

## Troubleshooting

### Container não inicia
- Verifique os logs: **Containers** > `psi-ai-api` > **Logs**
- Verifique se todas as variáveis de ambiente estão configuradas
- Verifique se a porta 8000 está disponível

### Erro de conexão
- Verifique se o container está rodando
- Verifique o mapeamento de portas
- Verifique o firewall

### Erro de autenticação
- Verifique se a `API_KEY` está configurada corretamente
- Verifique se o header `X-API-Key` está sendo enviado nas requisições

## Segurança

⚠️ **Importante**:
- Nunca commite o arquivo `.env` no repositório
- Use variáveis de ambiente no Portainer
- Use chaves seguras e longas para `API_KEY`
- Configure CORS adequadamente para produção
- Use HTTPS em produção (configure reverse proxy)

## Reverse Proxy (Nginx/Traefik)

Para usar com reverse proxy, configure:

```nginx
location / {
    proxy_pass http://psi-ai-api:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## Monitoramento

- Use o health check endpoint para monitoramento
- Configure alertas no Portainer
- Monitore os logs regularmente
