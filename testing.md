# Plano de Testes - Sistema de Atendimento

Este documento descreve a estratégia de testes para o Sistema de Atendimento, seguindo a metodologia **TDD First (Test-Driven Development)**. O objetivo é garantir a integridade das regras de negócio, a segurança dos acessos e a estabilidade do sistema frente a novas alterações.

## 1. Estratégia de Testes

### 1.1 Metodologia TDD
A implementação seguirá o ciclo **Red-Green-Refactor**:
1.  **Red**: Escrever um teste que falha para uma nova funcionalidade ou correção.
2.  **Green**: Implementar o código mínimo necessário para fazer o teste passar.
3.  **Refactor**: Melhorar o código mantendo os testes passando.

### 1.2 Níveis de Teste
*   **Testes de Unidade (Services):** Foco na lógica de negócio isolada no `app/services.py`. Uso intensivo de mocks para banco de dados quando necessário.
*   **Testes de Integração (Routes & Models):** Validação do fluxo completo entre rotas, sessões e persistência no banco de dados (usando SQLite em memória para os testes).

### 1.3 Ferramentas
*   **Framework:** `pytest`
*   **Mocks:** `pytest-mock`
*   **Cobertura:** `pytest-cov`

---

## 2. Cenários de Teste (Prioridade: Críticos)

### 2.1 Autenticação e Segurança
| Funcionalidade | Cenário | Objetivo |
| :--- | :--- | :--- |
| Login | Sucesso com credenciais válidas | Garantir que usuários autorizados acessem o sistema e iniciem sessão. |
| Login | Falha com senha incorreta | Validar que o sistema bloqueia acessos com senhas inválidas. |
| Autorização | Acesso negado a rotas restritas | Verificar se um 'CLIENTE' não consegue acessar o 'Dashboard Admin'. |

### 2.2 Cadastro de Clientes
| Funcionalidade | Cenário | Objetivo |
| :--- | :--- | :--- |
| Registro | Novo cliente com dados válidos | Validar a criação de conta e o hash de senha no banco. |
| Registro | Tentativa com email já existente | Impedir a duplicação de contas com o mesmo endereço de email. |

### 2.3 Solicitações de Atendimento
| Funcionalidade | Cenário | Objetivo |
| :--- | :--- | :--- |
| Criação | Solicitação com campos obrigatórios | Garantir que o cliente consiga abrir um chamado com assunto e descrição. |
| Resposta | Atendente respondendo chamado | Validar a alteração de status para 'EM_ANDAMENTO' ou 'RESOLVIDO' após resposta. |
| Integridade | Solicitação órfã (sem cliente) | Garantir a integridade referencial (Foreign Key) no modelo de dados. |

### 2.4 Administração
| Funcionalidade | Cenário | Objetivo |
| :--- | :--- | :--- |
| Estatísticas | Cálculo correto de totais | Validar se o dashboard soma corretamente os chamados por status ('ABERTO', etc). |

---

## 3. Implementação dos Testes (Exemplos de Referência)

Os testes devem ser criados no diretório `/tests/`. Abaixo, um exemplo de estrutura para o teste de autenticação:

```python
# tests/test_services.py
def test_autenticar_usuario_sucesso(mocker):
    # Mock do modelo Usuario
    mock_user = mocker.Mock()
    mock_user.senha_hash = "hash_valido"
    mocker.patch('app.models.Usuario.query.filter_by().first', return_value=mock_user)
    mocker.patch('app.services.bcrypt.check_password_hash', return_value=True)
    
    from app.services import autenticar_usuario
    result = autenticar_usuario("teste@email.com", "senha123")
    assert result == mock_user
```

---

## 4. Execução dos Testes

Para executar a suíte de testes automatizada, utilize os seguintes comandos no terminal:

```bash
# Executar todos os testes
pytest

# Executar testes com relatório de cobertura
pytest --cov=app tests/

# Executar testes de forma verbosa
pytest -v
```

---

## 5. Manutenção e Regressão
*   Nenhum Pull Request deve ser aceito se houver falha nos testes existentes.
*   Novas funcionalidades devem vir acompanhadas de seus respectivos testes (TDD).
*   A cobertura mínima recomendada é de **80%**.
