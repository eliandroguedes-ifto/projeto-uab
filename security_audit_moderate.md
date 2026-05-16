# Relatório de Inspeção de Cibersegurança - Projeto UAB

## Nível: MODERADA

### Resumo Executivo
- **Total de Achados:** 17
- **Severidade:**
  - **Crítica:** 2
  - **Alta:** 5
  - **Média:** 7
  - **Baixa:** 3

### Top 5 Ações Mais Urgentes
1. Configurar flags de segurança para cookies (`HttpOnly`, `Secure`).
2. Adicionar cabeçalhos de segurança HTTP (CSP, HSTS).
3. Desativar o modo `DEBUG` no arquivo `run.py`.
4. Remover a `SECRET_KEY` padrão.
5. Adicionar integridade de sub-recursos (SRI) para scripts externos.

---

## Detalhamento das Novas Vulnerabilidades (Nível Moderado)

### 11. Configuração Insegura de Cookies (A07:2021)
- **Localização:** `app/__init__.py`.
- **Impacto:** Sequestro de sessão.
- **Severidade:** Alta.
- **Recomendação:** `SESSION_COOKIE_HTTPONLY=True`.

### 12. Ausência de Cabeçalhos de Segurança (A02:2021)
- **Localização:** Global.
- **Impacto:** Vulnerabilidade a Clickjacking e XSS.
- **Severidade:** Alta.

### 13. Falta de Subresource Integrity (SRI) (A03:2021)
- **Localização:** `app/templates/admin/dashboard.html`.
- **Evidência:** `src="https://cdn.jsdelivr.net/npm/chart.js"` sem atributo `integrity`.
- **Severidade:** Média.

### 14. Validação de Input Insuficiente no Servidor (A05:2021)
- **Localização:** `app/services.py`.
- **Descrição:** Confiança excessiva na validação do lado do cliente (HTML).
- **Severidade:** Média.

### 15. Potencial IDOR em Atendimento (A01:2021)
- **Localização:** `app/routes.py` (`/atendente/responder/<id>`).
- **Descrição:** Qualquer atendente pode responder a qualquer ID de chamado sem verificação de escopo.
- **Severidade:** Média.

---
*(Os achados da etapa SUPERFICIAL foram mantidos e integrados ao controle de severidade)*
