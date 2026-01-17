# 🔐 Segurança

A segurança é uma prioridade neste projeto. Abaixo estão as medidas implementadas:

## 1. Gestão de Senhas
- Nunca armazenamos senhas em texto plano.
- Utilizamos o algoritmo **bcrypt** para hashing de senhas via biblioteca `passlib`.

## 2. Autenticação e Autorização
- Implementamos **JWT (JSON Web Tokens)** para autenticação persistente.
- Tokens possuem tempo de expiração curto (configurável via `.env`).
- Controle de acesso baseado em funções (RBAC) garante que apenas administradores possam realizar alterações no blog.

## 3. Proteção contra Ataques
- **SQL Injection**: Protegido nativamente pelo uso do SQLAlchemy ORM.
- **XSS**: O backend não processa nem retorna HTML diretamente, servindo apenas dados estruturados via JSON.
- **Input Validation**: Todo dado que entra na API é validado rigorosamente pelo **Pydantic**.

## 4. Configurações Seguras
- Uso de `pydantic-settings` para gerenciar segredos.
- Recomendação de uso de variáveis de ambiente para `SECRET_KEY` em produção.
