# 🏗️ Arquitetura do Projeto

Este projeto utiliza uma arquitetura em camadas para garantir a separação de responsabilidades e facilitar a manutenção.

## Camadas

1.  **API (Routes)**: Responsável por receber as requisições HTTP, validar os dados de entrada via Schemas e chamar os Serviços correspondentes.
2.  **Services**: Contém a lógica de negócio da aplicação. Orquestra as chamadas aos Repositórios e aplica regras de validação complexas.
3.  **Repositories**: Camada de abstração para acesso ao banco de dados. Realiza operações de CRUD puras.
4.  **Models**: Definições das entidades do banco de dados usando SQLAlchemy.
5.  **Schemas**: Modelos Pydantic para validação de dados de entrada e saída (DTOs).
6.  **Core**: Configurações globais, segurança (JWT, hashing) e conexão com o banco de dados.

## Fluxo de Dados

`Cliente -> Route -> Service -> Repository -> Banco de Dados`

## Decisões Técnicas

- **FastAPI**: Escolhido pela performance e facilidade de documentação.
- **Dependency Injection**: Utilizado extensivamente para gerenciar sessões de banco de dados e autenticação.
- **RBAC (Role Based Access Control)**: Implementado para restringir operações de escrita apenas a administradores.
