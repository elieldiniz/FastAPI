# 🎯 Mini Blog Profissional - FastAPI

Este projeto é uma implementação de referência de um sistema de blog profissional utilizando **FastAPI**, focado em segurança, arquitetura limpa e uma experiência de leitura "Retro Modern".

## 🚀 Funcionalidades Principais

- **Sistema de Usuários**: Registro e Login com JWT.
- **RBAC (Role Based Access Control)**: Distinção entre administradores e leitores.
- **Gestão de Conteúdo**: Dashboard administrativo para CRUD de posts.
- **Frontend Integrado**: SSR (Server-Side Rendering) com Jinja2 e HTMX para interatividade sem complexidade de SPA.
- **Design Retro Modern**: Estética focada em legibilidade e estilo técnico/acadêmico.
- **API Completa**: Documentação automática via Swagger/ReDoc.

## 🛠️ Stack Tecnológica

- **API**: FastAPI
- **DB**: SQLAlchemy 2.0 + PostgreSQL/SQLite
- **Auth**: JWT + OAuth2 + Bcrypt
- **Migrations**: Alembic
- **Templates**: Jinja2 + HTMX
- **Config**: Pydantic Settings

## 📂 Estrutura do Repositório

- `app/api`: Endpoints REST tradicionais.
- `app/web`: Rotas para renderização de páginas HTML.
- `app/services`: Lógica de negócio.
- `app/repositories`: Acesso ao banco de dados.
- `app/static`: Ativos (CSS, Imagens, JS).
- `app/templates`: Páginas Jinja2.

## 🏁 Como Começar

1. **Instalação**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Banco de Dados**:
   ```bash
   alembic upgrade head
   python3 -m app.seed
   ```

3. **Criar um Usuário Admin**:
   Para criar novos administradores com segurança, utilize o utilitário CLI:
   ```bash
   python3 -m app.cli create-admin --email admin@meublog.com --password minha-senha --name "Nome do Admin"
   ```

4. **Execução**:
   ```bash
   uvicorn app.main:app --reload
   ```

Acesse em: `http://localhost:8000`

---

*Desenvolvido seguindo as melhores práticas de engenharia de software.*
