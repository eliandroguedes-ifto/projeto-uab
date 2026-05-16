# Relatório de Inspeção de Cibersegurança Final - Projeto UAB

## Nível: PROFUNDA

### Resumo Executivo
- **Total de Achados:** 21
- **Severidade:**
  - **Crítica:** 2
  - **Alta:** 7
  - **Média:** 9
  - **Baixa:** 3

### Top 5 Ações Mais Urgentes
1. **Remover Segredos Hardcoded:** Desativar `DEBUG` e corrigir `SECRET_KEY` e senhas de seed.
2. **Tratamento de Erros e Logs:** Implementar `try/except` global e logging estruturado.
3. **Segurança de Sessão:** Ativar `HttpOnly`, `Secure` e `SameSite` nos cookies.
4. **Proteção de Rede:** Adicionar cabeçalhos de segurança HTTP (HSTS, CSP, X-Frame).
5. **Correção de IDOR e CSRF:** Validar permissões de acesso e adicionar tokens CSRF.

---

## Detalhamento das Novas Vulnerabilidades (Nível Profundo)

### 16. Falha Sistêmica no Tratamento de Exceções (A10:2021)
- **Localização:** Global (`app/`).
- **Descrição:** Ausência de tratamento de erros.
- **Impacto:** DoS e vazamento de informações do sistema.
- **Severidade:** Alta.

### 17. Condição de Corrida na Inicialização do Admin (A08:2021)
- **Localização:** `app/__init__.py`.
- **Descrição:** Criação não atômica de usuário administrativo em ambiente multi-processo.
- **Severidade:** Alta.

### 18. Credenciais Hardcoded em Script de Seed (A07:2021)
- **Localização:** `seed_test_data.py`.
- **Severidade:** Média.

### 19. Falta de Logging de Segurança e Auditoria (A09:2021)
- **Localização:** `app/services.py`.
- **Descrição:** Uso de `print()` impede monitoramento eficaz.
- **Severidade:** Média.

### 20. Uso de ID Incremental para Usuários (A01:2021)
- **Localização:** `app/models.py`.
- **Descrição:** Permite enumeração de base de usuários.
- **Severidade:** Média.
- **Recomendação:** Usar UUIDs.

### 21. Configuração Estática de Bcrypt Rounds (A04:2021)
- **Localização:** `app/services.py`.
- **Descrição:** Complexidade do hash não é parametrizável por ambiente.
- **Severidade:** Baixa.

---
*(Relatório final consolidando as etapas Superficial, Moderada e Profunda)*
