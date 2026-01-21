Boas Práticas de Arquitetura – Backend (FastAPI)

Este documento descreve a arquitetura técnica adotada no Mini Blog API, detalhando a organização do código, responsabilidades de cada camada e decisões arquiteturais que visam manutenibilidade, testabilidade, escalabilidade e clareza de domínio.

1. Visão Geral da Arquitetura

O projeto segue o padrão de Arquitetura em Camadas (Layered Architecture), amplamente utilizado em sistemas backend modernos. Esse modelo promove a separação clara de responsabilidades, reduz acoplamentos desnecessários e facilita a evolução do sistema ao longo do tempo.

A comunicação entre as camadas ocorre de forma unidirecional, evitando dependências circulares e mantendo o domínio isolado de detalhes de infraestrutura.

Client (Frontend / API Client)
↓
API Routes (app/api & app/web)
↓
Services (app/services)
↓
Repositories (app/repositories)
↓
Database (SQLAlchemy Models)

🎯 Objetivos principais da arquitetura

Facilitar testes unitários e de integração

Permitir substituição de tecnologias sem impacto no domínio

Tornar o código legível e previsível

Organizar regras de negócio de forma explícita

2. Responsabilidade das Camadas
   📌 API Routes (app/api & app/web)

As Routes representam a camada de entrada do sistema e são responsáveis exclusivamente pela interação com o protocolo HTTP.

Responsabilidades:

Receber requisições HTTP (REST ou Web).

Validar dados de entrada usando Pydantic Schemas.

Extrair contexto da requisição (usuário autenticado, parâmetros, headers).

Delegar a execução da lógica para a camada de Services.

Retornar respostas HTTP padronizadas.

Restrições importantes:

❌ Não contêm regras de negócio.

❌ Não acessam o banco de dados diretamente.

❌ Não manipulam entidades ORM.

Essa abordagem mantém as rotas finas (thin controllers) e fáceis de testar.

📌 Services (app/services)

A camada de Services concentra toda a lógica de negócio da aplicação. Ela representa o coração do sistema e define como as regras do domínio são aplicadas.

Responsabilidades:

Implementar regras de negócio e validações complexas.

Orquestrar chamadas entre múltiplos repositórios.

Garantir consistência das operações (ex: criar post, validar autor, registrar histórico).

Ser independente de frameworks web ou protocolos de transporte.

Características-chave:

Não conhecem HTTP, FastAPI ou Request/Response.

Podem ser testados isoladamente com mocks.

Facilitam reutilização da lógica em outros contextos (CLI, workers, background jobs).

Essa separação torna o código mais robusto, reutilizável e testável.

📌 Repositories (app/repositories)

Os Repositories encapsulam completamente o acesso à persistência de dados, isolando o uso do ORM e evitando que outras camadas conheçam detalhes do banco.

Responsabilidades:

Executar operações CRUD usando SQLAlchemy.

Mapear entidades do domínio para o banco de dados.

Centralizar queries e filtros específicos.

Benefícios:

Permite trocar o banco de dados ou ORM com impacto mínimo.

Facilita mocks e testes de serviços.

Evita vazamento de lógica SQL para outras camadas.

📌 Models & Schemas
🔹 Models (SQLAlchemy Models)

Representam as entidades persistidas no banco.

Definem relacionamentos, chaves e constraints.

São utilizados exclusivamente pelos Repositories.

🔹 Schemas (Pydantic)

Definem contratos de entrada e saída da API.

Atuam como DTOs (Data Transfer Objects).

Garantem validação automática e documentação clara via Swagger/ReDoc.

Essa separação evita acoplamento entre camada de persistência e contrato da API.

3. Injeção de Dependências

O projeto utiliza o sistema nativo de Dependency Injection do FastAPI (Depends) para desacoplar componentes e facilitar testes.

Usos principais:

Gerenciamento do ciclo de vida da sessão do banco de dados.

Autenticação e recuperação do usuário atual.

Controle de permissões e papéis (Admin, User).

Injeção de serviços e repositórios.

Benefícios:

Redução de acoplamento entre componentes.

Facilita substituição por mocks em testes.

Centraliza regras transversais (auth, segurança, contexto).

4. Testabilidade e Qualidade do Código

A arquitetura foi pensada para permitir:

Testes unitários focados na camada de Services.

Testes de integração isolando Repositories.

Simulação de cenários de erro sem dependência do banco real.

Evolução segura do código com menor risco de regressões.

Essa estrutura segue princípios como:

Single Responsibility Principle

Dependency Inversion Principle

Clean Architecture (em adaptação prática)

5. Estilo Visual (Retro Modern)

O frontend integrado ao backend segue um design system denominado Retro Modern, alinhado com o propósito técnico e acadêmico do projeto.

🎨 Paleta de Cores

Off-white: #F5F1EA

Verde Musgo: #4A5D4E

Azul Petróleo: #2F4F4F

🔤 Tipografia

Merriweather: leitura longa e artigos técnicos.

Inter: elementos de interface e navegação.

🧠 Filosofia Visual

Ênfase em conteúdo e legibilidade.

Estética inspirada em arquivos acadêmicos, estudos de caso e documentação técnica.

Interface limpa, sem distrações visuais desnecessárias.

6. Conclusão

A arquitetura adotada no Mini Blog API busca equilibrar simplicidade e robustez, fornecendo uma base sólida para evolução futura. A separação clara de responsabilidades, aliada ao uso correto de injeção de dependências e padrões consolidados, torna o projeto adequado tanto para ambientes de produção quanto para uso educacional e portfólio profissional.
