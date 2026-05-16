# Relatório de Inspeção de Cibersegurança - Projeto UAB

## Nível: SUPERFICIAL

### Resumo Executivo
- **Total de Achados:** 10
- **Severidade:**
  - **Crítica:** 2
  - **Alta:** 3
  - **Média:** 3
  - **Baixa:** 2

### Top 5 Ações Mais Urgentes
1. Desativar o modo `DEBUG` no arquivo `run.py`.
2. Remover a `SECRET_KEY` padrão e configurar obrigatoriedade via variável de ambiente.
3. Implementar proteção CSRF em todos os formulários.
4. Configurar o `Dockerfile` para utilizar um usuário não-root.
5. Implementar Rate Limiting na funcionalidade de login.

---

## Detalhamento das Vulnerabilidades

### 1. Modo Debug Ativado em Produção (A02:2021)
- **Localização:** `run.py`, linha 9.
- **Descrição:** O aplicativo Flask é iniciado com `debug=True`.
- **Evidência:** `app.run(host=host, port=port, debug=True)`
- **Impacto:** RCE (Remote Code Execution).
- **Severidade:** Crítica.
- **Recomendação:** `app.run(debug=False)`.

### 2. Uso de Chave Secreta Hardcoded (A02:2021)
- **Localização:** `app/__init__.py`, linha 14.
- **Descrição:** Fallback para string fixa.
- **Evidência:** `'uma-chave-secreta-padrao'`
- **Impacto:** Falsificação de cookies de sessão.
- **Severidade:** Crítica.

### 3. Ausência de Proteção CSRF (A01:2021)
- **Localização:** Global.
- **Descrição:** Falta de tokens de validação em requisições POST.
- **Impacto:** Ações não autorizadas via navegador do usuário.
- **Severidade:** Alta.

### 4. Container Docker como Root (A02:2021)
- **Localização:** `Dockerfile`.
- **Severidade:** Média.
- **Recomendação:** Adicionar `RUN useradd -m myuser && USER myuser`.

### 5. Falta de Rate Limiting (A07:2021)
- **Localização:** `app/routes.py`.
- **Severidade:** Alta.
- **Impacto:** Brute force de senhas.

### 6. Banco de Dados SQLite Exposto (A02:2021)
- **Localização:** `app/__init__.py`.
- **Descrição:** Caminho relativo para SQLite pode falhar ou expor o arquivo.
- **Severidade:** Média.

### 7. Uso de Threading sem Gestão (A06:2021)
- **Localização:** `app/services.py`.
- **Descrição:** `threading.Thread` para jobs em background sem persistência ou retry.
- **Severidade:** Média.

### 8. Exposição de Mensagens de Erro Genéricas (A07:2021)
- **Localização:** `app/routes.py`.
- **Descrição:** "Credenciais inválidas" é bom, mas o fluxo de erro pode ser melhorado para evitar enumeração de usuários.
- **Severidade:** Baixa.

### 9. Logs em STDOUT via Print (A09:2021)
- **Localização:** `app/services.py`.
- **Severidade:** Baixa.

### 10. CORS não configurado (A02:2021)
- **Localização:** `app/__init__.py`.
- **Descrição:** Política de mesma origem padrão pode ser muito restritiva ou permissiva dependendo do deploy.
- **Severidade:** Baixa.
