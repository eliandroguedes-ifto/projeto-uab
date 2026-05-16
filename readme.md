# Sistema de Atendimento ao Cliente

Este é um sistema web de atendimento ao cliente desenvolvido com Flask, focado em usabilidade, acessibilidade (A11y) e design responsivo.

## Características do Frontend

- **Acessibilidade**: Seguindo padrões WCAG com ARIA labels e navegação por teclado.
- **Responsividade**: Interface adaptável para Mobile, Tablet e Desktop usando Bootstrap 5.
- **UX**: Feedbacks visuais de carregamento, estados vazios e mensagens de alerta.

## Requisitos

- Python 3.11+
- Dependências listadas em `requirements.txt`

## Otimização e Performance

O sistema foi refatorado para suportar alto desempenho e escalabilidade:

- **Cache de Dados**: Estatísticas do Dashboard são mantidas em memória para reduzir carga no banco de dados.
- **Processamento Assíncrono**: Tarefas de notificação são executadas em threads de background, garantindo respostas rápidas aos usuários.
- **Arquitetura Modular**: Código organizado em serviços especializados com baixo acoplamento.
- **Segurança**: Proteção de rotas centralizada via decorators.

## Instalação

1. Crie um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure o arquivo `.env` (veja o exemplo em `spec-project.md`).

## Execução

Para rodar o sistema localmente:
```bash
python3 run.py
```

O sistema estará disponível em `http://127.0.0.1:5000`.

## Testes

Para executar os testes automatizados:
```bash
export PYTHONPATH=$PYTHONPATH:.
pytest
```

## Estrutura do Projeto

- `app/`: Código-fonte da aplicação Flask.
- `tests/`: Testes automatizados.
- `run.py`: Ponto de entrada da aplicação.
- `spec-project.md`: Especificação técnica detalhada.
- `testing.md`: Plano de testes e procedimentos.
