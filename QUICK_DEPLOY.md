# Deploy Rápido no Portainer

## Passo a Passo Simplificado

### 1. Prepare o Repositório
Certifique-se de que os seguintes arquivos estão no repositório:
- ✅ `Dockerfile`
- ✅ `docker-compose.yml` ou `portainer-stack.yml`
- ✅ `requirements.txt`
- ✅ Todo o código da aplicação

### 2. No Portainer

1. **Acesse Portainer** → **Stacks** → **Add stack**

2. **Configure o Stack:**
   - **Name**: `psi-ai-api`
   - **Build method**: **Repository** (recomendado) ou **Web editor**

3. **Se usar Repository:**
   - **Repository URL**: URL do seu Git
   - **Compose path**: `docker-compose.yml`
   - **Auto-update**: ✅ Ativado (opcional)

4. **Configure Environment Variables:**
   ```
   OPENAI_API_KEY=sk-...
   SUPABASE_URL=https://...
   SUPABASE_KEY=eyJ...
   SUPABASE_STORAGE_BUCKET=audio-sessions
   API_KEY=sua-chave-secreta
   ```

5. **Deploy!** → Clique em **Deploy the stack**

### 3. Verificar

- Container rodando: **Containers** → `psi-ai-api`
- Health check: `http://seu-servidor:8000/health`
- Docs: `http://seu-servidor:8000/docs`

## Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| Container não inicia | Verifique logs e variáveis de ambiente |
| Erro 401/403 | Verifique se `API_KEY` está configurada |
| Porta ocupada | Altere a porta no docker-compose.yml |

## Próximos Passos

- Configure reverse proxy (Nginx/Traefik)
- Configure HTTPS
- Configure backup do banco de dados
- Configure monitoramento
