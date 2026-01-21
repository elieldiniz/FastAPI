# 🔐 Documento de Segurança & Boas Práticas

**Mini Blog API – FastAPI**

Este documento detalha as práticas de segurança e padrões adotados neste projeto para garantir uma aplicação robusta e profissional.

## 1. Princípios de Segurança

Este projeto segue os princípios fundamentais:
- **Nunca confiar no cliente (frontend)**: Todas as validações ocorrem no backend.
- **Princípio do menor privilégio**: Usuários têm apenas as permissões necessárias para suas funções.
- **Separação de responsabilidades**: Camadas distintas para rotas, lógica e dados.
- **Configuração segura por padrão**.

## 2. Gerenciamento de Segredos (Secrets)

- Utilizamos `pydantic-settings` para carregar configurações de variáveis de ambiente ou arquivos `.env`.
- **Atenção**: Nunca comite o arquivo `.env` com segredos reais para o controle de versão.

## 3. Senhas & Autenticação

### Hash de Senha
- Algoritmo: **bcrypt**
- Biblioteca: `passlib`
- Regras: Nunca armazenar senhas em texto plano; comparar sempre via hash.

### JWT (JSON Web Token)
- Configuração: Tokens de acesso curtos (30 minutos por padrão).
- Armazenamento: Suporta tanto cabeçalho `Authorization: Bearer <token>` quanto Cookies HTTP-only para maior segurança em aplicações web.

## 4. Controle de Acesso (RBAC)

Implementamos dois papéis principais:
- **Admin**: Permissões totais (Criar, Editar, Excluir posts).
- **User**: Permissões de leitura e acesso ao próprio perfil.

As permissões são verificadas em **todas** as rotas protegidas no backend.

## 5. Validação de Dados (Input Validation)

- Ferramenta: **Pydantic**.
- Validamos 100% dos dados de entrada para evitar injeção e dados inconsistentes.

## 6. Prevenção contra Ataques Comuns

- **SQL Injection**: Protegido pelo uso do SQLAlchemy ORM (nunca montamos SQL manual).
- **XSS**: Backend serve apenas dados limpos; o uso de Jinja2 no frontend lida com a sanitização de saída por padrão.
- **Brute Force**: Recomendado o uso de middlewares de Rate Limiting em produção.

## 7. Banco de Dados

- Gerenciamento via **Alembic** para migrações seguras.
- Uso de índices em campos de busca frequente (`email`, `title`).
