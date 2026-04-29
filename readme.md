# Sistema de Atendimento ao Cliente

Este é um sistema web de atendimento ao cliente desenvolvido com Flask.

## Requisitos

- Python 3.11+
- Dependências listadas em `requirements.txt`

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
