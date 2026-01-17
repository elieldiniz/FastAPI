# Mini Blog API - FastAPI

Este é um projeto de backend profissional para um mini-blog, construído com FastAPI, seguindo as melhores práticas de mercado.

## 🚀 Funcionalidades

- **Autenticação**: Login via JWT (OAuth2).
- **Controle de Acesso (RBAC)**: Diferenciação entre Admin e Usuário comum.
- **Posts**: CRUD completo de posts (apenas Admins podem criar/editar/deletar).
- **Segurança**: Senhas hasheadas com bcrypt, validação de tokens JWT.
- **Documentação**: Swagger automático disponível em `/docs`.

## 🛠️ Tecnologias

- **FastAPI**: Framework web moderno e rápido.
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **Alembic**: Gerenciamento de migrações de banco de dados.
- **Pydantic**: Validação de dados e configurações.
- **PostgreSQL / SQLite**: Banco de dados.

## 🏃 Como Rodar

1.  **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Rode as migrações**:
    ```bash
    alembic upgrade head
    ```

3.  **Inicie o servidor**:
    ```bash
    uvicorn app.main:app --reload
    ```

4.  **Acesse a documentação**:
    Abra `http://127.0.0.1:8000/docs` no seu navegador.

## 📂 Estrutura do Projeto

```bash
app/
├── api/             # Rotas e dependências
├── core/            # Configurações, segurança e DB
├── models/          # Modelos SQLAlchemy (Banco de dados)
├── schemas/         # Modelos Pydantic (Validação)
├── repositories/    # Camada de acesso a dados
├── services/        # Regras de negócio
└── migrations/      # Migrações do banco de dados (Alembic)
```
