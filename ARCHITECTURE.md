# 🏗️ Boas Práticas de Arquitetura – Backend (FastAPI)

Este documento descreve a organização técnica do Mini Blog API.

## 1. Visão Geral da Arquitetura

Seguimos uma arquitetura em camadas (Layered Architecture) que separa preocupações e facilita a testabilidade.

```
Client (Frontend/API Client)
       ↓
API Routes (app/api & app/web)
       ↓
Services (app/services)
       ↓
Repositories (app/repositories)
       ↓
Database (SQLAlchemy Models)
```

## 2. Responsabilidade das Camadas

### 📌 Routes (API/Web)
- Recebem requisições HTTP.
- Validam dados básicos via Pydantic Schemas.
- Chamam os **Services** apropriados.
- **NÃO** acessam o banco de dados diretamente.

### 📌 Services (Regras de Negócio)
- Contêm toda a lógica de domínio.
- Orquestram operações entre múltiplos repositórios se necessário.
- Independentes de protocolos de transporte (HTTP/gRPC).

### 📌 Repositories (Persistência)
- Encapsulam o acesso ao banco de dados usando SQLAlchemy.
- Realizam operações CRUD.
- Mantêm o código SQL/ORM isolado.

### 📌 Models & Schemas
- **Models**: Representam as entidades no banco de dados.
- **Schemas**: Definem a estrutura de dados para entrada e saída da API (DTOs).

## 3. Injeção de Dependências

Utilizamos o sistema de `Depends` do FastAPI para:
- Gerenciar sessões de banco de dados.
- Autenticação e extração do usuário atual.
- Verificação de papéis (Admin/User).

## 4. Estilo Visual (Retro Modern)

O frontend integrado utiliza um design system "Retro Modern":
- **Cores**: Off-white (`#F5F1EA`), Verde Musgo (`#4A5D4E`), Azul Petróleo (`#2F4F4F`).
- **Tipografia**: Serifada para leitura (`Merriweather`) e Sans-serif para UI (`Inter`).
- **Filosofia**: Foco em conteúdo técnico e acadêmico, inspirado em arquivos e estudos de caso.
