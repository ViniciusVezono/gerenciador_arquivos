# Gerenciador de Arquivos

##  About
O **Gerenciador de Arquivos** é uma aplicação Full Stack moderna que permite o armazenamento, visualização, download e gerenciamento de imagens na nuvem (AWS S3) de forma isolada e segura. A autenticação e proteção de rotas são gerenciadas através do Clerk. O backend foi projetado utilizando os princípios da **Clean Architecture**, com separação clara de responsabilidades, injeção de dependências e cobertura de testes.

---

##  Frontend Dependencies
O frontend é construído com as melhores e mais recentes tecnologias do ecossistema React:
- **React 18** com **TypeScript**
- **Vite** - Bundler ultrarrápido
- **Tailwind CSS** - Estilização utilitária e design responsivo
- **TanStack Router** - Roteamento type-safe para React
- **TanStack Query (React Query)** - Gerenciamento de estado de servidor e data fetching
- **Clerk React** - Plataforma de autenticação

---

##  Backend Dependencies
O backend fornece uma API REST robusta, rápida e altamente escalável:
- **FastAPI** - Framework web moderno e de alta performance
- **Uvicorn** - Servidor ASGI super rápido
- **SQLAlchemy 2.0** - ORM moderno para comunicação com o banco de dados
- **PostgreSQL (`psycopg2-binary`)** - Banco de dados relacional
- **Boto3** - SDK da AWS para integração com o S3
- **PyJWT & Clerk** - Validação de tokens de autenticação via JWKS
- **Loguru** - Logging estruturado
- **Pytest** - Framework para testes unitários e de integração

---

## 🏛️ Arquitetura do Projeto

O projeto foi estruturado buscando modularidade, clareza e manutenção facilitada, adotando fortemente conceitos de **Clean Architecture** no backend e uma separação em camadas no frontend.

### 🐍 Backend (Clean Architecture)
```text
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── health.py        # Endpoint de healthcheck
│   │   │   │   └── images.py        # Endpoints de upload, listagem e exclusão
│   │   │   ├── __init__.py
│   │   │   └── router.py            # Roteador agrupando as rotas da v1
│   │   ├── deps.py                  # Funções de injeção de dependência (S3, DB, Segurança)
│   │   └── __init__.py
│   ├── core/
│   │   ├── config.py                # Configurações usando Pydantic BaseSettings (.env)
│   │   ├── exceptions.py            # Handlers globais e exceções customizadas
│   │   └── security.py              # Autenticação e validação de tokens JWT (Clerk JWKS)
│   ├── domain/
│   │   └── image/
│   │       ├── entities.py          # Entidade pura de Imagem com regras de negócio
│   │       ├── repository.py        # Interface/Protocolo de ImageRepository
│   │       └── service.py           # Regras de orquestração e casos de uso (ImageService)
│   ├── infrastructure/
│   │   ├── persistence/
│   │   │   ├── repositories/
│   │   │   │   └── image.py         # Implementação de ImageRepository usando SQLAlchemy
│   │   │   └── database.py          # Conexão com o PostgreSQL e sessão do SQLAlchemy
│   │   └── storage/
│   │       ├── base.py              # Interface/Protocolo do Cliente de Storage
│   │       └── s3.py                # Implementação do cliente S3 via Boto3
│   ├── models/
│   │   ├── __init__.py
│   │   └── image.py                 # Modelo da tabela images no banco (ORM)
│   ├── schemas/
│   │   └── image.py                 # Pydantic models para Request/Response da API
│   └── main.py                      # Arquivo principal que inicializa a aplicação FastAPI
├── alembic/                         # Configurações do Alembic (Migrations do banco)
│   └── versions/                    # Histórico de arquivos de migração gerados
├── tests/                           # Suíte de testes unitários e de integração (Pytest)
│   ├── api/
│   │   └── test_images.py           # Testes E2E dos endpoints chamando o TestClient
│   ├── domain/
│   │   └── test_image_service.py    # Testes unitários das regras de negócio puras
│   └── conftest.py                  # Fixtures do Pytest (Banco in-memory, Mocks do S3)
├── alembic.ini                      # Arquivo de configuração do Alembic
├── docker-entrypoint.sh             # Script de inicialização (aguarda o banco e roda migrations)
├── Dockerfile                       # Instruções de build da imagem Docker do backend
└── requirements.txt                 # Dependências Python do projeto
```
Essa separação minuciosa permite que a camada de domínio (`domain`) permaneça completamente agnóstica às tecnologias externas, garantindo que testes unitários rodem em milissegundos.

### ⚛️ Frontend
```text
frontend/
├── src/
│   ├── components/
│   │   ├── AuthButtons.tsx          # Botões e ações do Clerk (Login/Logout)
│   │   └── Header.tsx               # Header principal da aplicação
│   ├── routes/
│   │   ├── __root.tsx               # Rota raiz global (Layout principal e Provider do Clerk)
│   │   ├── index.tsx                # Página de Dashboard (Galeria de imagens, Upload e Download)
│   │   ├── login.tsx                # Página isolada de autenticação
│   │   └── register.tsx             # Página de cadastro
│   ├── services/
│   │   ├── image.queries.ts         # Hooks do React Query (useQuery, useMutation)
│   │   └── image.service.ts         # Camada de comunicação HTTP (Fetch isolado para a API)
│   ├── types/
│   │   └── image.types.ts           # Interfaces e tipos do TypeScript espelhando os schemas
│   ├── main.tsx                     # Ponto de entrada do React e Router
│   ├── index.css                    # Estilos globais e injeção do Tailwind
│   └── routeTree.gen.ts             # Arquivo de rotas auto-gerado pelo TanStack Router
├── public/                          # Arquivos estáticos (favicon, etc)
├── .env.local                       # Variáveis de ambiente (ex: Chave pública do Clerk)
├── index.html                       # Template HTML raiz da SPA
├── package.json                     # Dependências NPM e scripts do projeto
├── tailwind.config.js               # Configurações de tema do Tailwind CSS
└── vite.config.ts                   # Configurações de build e dev server do Vite
```

---

##  Instruções para rodar localmente

### Pré-requisitos
- Docker & Docker Compose
- Node.js (v18+) — apenas se quiser rodar o frontend fora do Docker

### Opção 1: Usando o script automatizado (Recomendado)
O projeto inclui um script que cria os `.env` a partir dos exemplos e sobe tudo automaticamente:
```bash
chmod +x run-dev.sh
./run-dev.sh
```

### Opção 2: Subindo manualmente com Docker Compose

1. Crie os arquivos de ambiente copiando os exemplos:
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
```

2. Configure as variáveis de ambiente:
   - No `backend/.env`, preencha a `CLERK_JWKS_URL` com a URL do seu JWKS do Clerk.
   - No `frontend/.env.local`, preencha a chave pública do Clerk (`VITE_CLERK_PUBLISHABLE_KEY`).

3. Suba todos os containers:
```bash
docker compose up -d --build
```

Isso irá inicializar **4 serviços** automaticamente:

| Serviço | Container | Porta | Descrição |
|---|---|---|---|
| `db` | `postgres_db` | `5432` | Banco de dados PostgreSQL |
| `ministack` | `ministack_aws` | `4566` | Simulador local do AWS S3 |
| `api` | `fastapi_backend` | `8000` | Backend FastAPI (roda migrations automaticamente ao iniciar) |
| `frontend` | `frontend_app` | `3000` | Frontend React (Vite) |

4. Acesse `http://localhost:3000` no seu navegador!

---

##  Funcionalidades Implementadas / Não Implementadas

### Funcionalidades Implementadas (Obrigatórias e Bônus)
- **Autenticação**: Cadastro e login (email e senha) gerenciados pelo Clerk. Sessão é persistente durante o uso. Ações do backend (upload, listagem, deleção) são estritamente restritas ao usuário autenticado validando o JWT (JWKS).
- **Página Principal (Meus Arquivos)**: Lista arquivos em cards com nome original, tamanho formatado e data de upload. Oferece botões dedicados de ação: Visualizar, Download e Deletar.
- **Upload de Arquivos**: Interface via formulário (Drag & Drop ou clique). Validação rigorosa de segurança limitando a 10MB e restringindo aos tipos aceitos (`.png`, `.jpg`, `.jpeg`, `.gif`, `.pdf`, `.txt`). Feedback visual de loading, sucesso e tratamento de erros.
- **Download / Visualização de Arquivos**: Geração de **Links com Expiração** (Presigned URLs via S3/LocalStack). O download é restrito apenas aos arquivos da própria conta do usuário. (Streaming no lado do LocalStack/S3).
- **Exclusão de Arquivos**: Exclusão **Física** no storage (S3) e no banco de dados para evitar lixo residual, restrita exclusivamente aos próprios arquivos.
- **Backend / API & Metadata**: APIs REST completas (`GET`, `POST`, `DELETE`). O banco de dados salva a metadata rigorosamente: id, user_id, filename (nome original), file_key (chave no s3), mime_type, tamanho e data de criação.

### Não Implementadas
- Deploy da Aplicação (App preparado via Docker, mas sem CI/CD para cloud no momento)

---

##  Decisões Técnicas Tomadas

1. **Clean Architecture no Backend**: Optei por não manter um monolito. A separação do FastAPI em `domain` (regras puras), `infrastructure` (AWS S3, banco de dados) e `api` (rotas) permitiu cobrir a lógica de negócios com testes unitários executados em milissegundos, utilizando Mocks nativos sem depender do banco ou S3.
2. **LocalStack/Ministack para S3**: Em vez de salvar arquivos localmente no disco do servidor, utilizei o Ministack para simular a API do AWS S3 via Docker. Isso torna a arquitetura Cloud-Native desde o dia 1: para ir para produção, basta trocar as credenciais e endpoint no `.env` para apontar para a AWS real, sem alterar 1 linha de código da aplicação.
3. **Autenticação Desacoplada (Clerk)**: Delegar o gerenciamento de credenciais ao Clerk eliminou os riscos de vazamento de senhas. O backend foi configurado de forma inteligente para validar a assinatura dos JWTs (`RS256`) através das chaves públicas do Clerk (JWKS), garantindo que apenas usuários donos do token acessem as rotas sem onerar o banco de dados.
4. **TanStack Ecosystem no React**: O uso conjunto de `TanStack Router` (roteamento type-safe impedindo erros de rota inexistente) e `TanStack Query` (gerenciamento de requisições, retries automáticos e loading states nativos) cortou a necessidade de bibliotecas de estado verbosas como Redux, mantendo o frontend extremamente focado em UI.

---

##  Principais desafios e a utlização da IA
Durante o desenvolvimento enfrentei grandes desafios inicialmente para configurações de ambientes de desenvolvimento e inicialização principalmente na api utilizando a FastApi. Inicialmente como forma de ao mesmo tempo entender e aprender como funciona a arquitetura da aplicação da FastApi com Python, utilizei a IDE Antigravity com o modelo Gemini para auxiliar a inicialização e também utilizando as documentações oficiais e conteudos na internet (vídeos e StackOverflow). Após a inicialização, procurei muitos documentações relacionadas á implementação do miniStack(serviço open-source simulando a AWS localmente e que utiliza as mesmas credenciais de uma instância real da AWS).

Com a infraestrutura completa e implementada, comecei inicialmente a implementação da api de forma monolito, para um melhor entendimento inicialmente do framework. Endpoints estrturados e com suas funções principais bem definidas, as autenticações mockadas para fazer todos os testes e então partir para uma arquitetura mais limpa e bem organizada, separando as responsabilidades em camadas e arquivos diferentes, facilitando a manutenção e escalabilidade do projeto.

Em relação ao frontend foi utilizado as documentações oficiais do Tanstack e a própria CLI do tanstack para inicializar o projeto e realizar as configs necessárias. Para a inicialização das configurações do Clerk, foi utilizado o próprio prompt de Agent em que está na documentação oficial.

Com as configurações e ambiente corretamentes, o projeto foi ganhando forma e separando as pastas e arquivos de acordo com cada funcionalidade, sempre seguindo as boas práticas de desenvolvimento, organização e uma arquitetura de melhor entendimento(types, routes e services). 

Além da inicialização, a IA foi utilizada para **correção de bugs e resolução de problemas** que surgiram durante o desenvolvimento. Entre os principais casos:
- **Incompatibilidade de versões entre bibliotecas**: O `httpx 0.28` quebrava o `TestClient` do FastAPI 0.109.0 — a IA identificou a incompatibilidade e sugeriu o pin `httpx<0.28`.
- **Erros de importação no Docker após refatoração**: Ao migrar de monolito para Clean Architecture, o `alembic/env.py` ainda referenciava o caminho antigo `app.db.database`. A IA rastreou o traceback e corrigiu o import para o novo caminho `app.infrastructure.persistence.database`.
- **`exec format error` no Docker**: O script `docker-entrypoint.sh` criado no Windows não tinha shebang (`#!/bin/bash`) e estava com quebras de linha CRLF incompatíveis com o Linux nos containers — a IA diagnosticou ambos os problemas e aplicou a correção.
- **Variáveis de ambiente ausentes**: O entrypoint do Docker não encontrava o host do banco (`$POSTGRES_SERVER`) porque a variável existia apenas como default no Python (Pydantic), mas não estava exportada no `.env`. A IA identificou a causa raiz e adicionou a variável.
- **Erros de compatibilidade com Python 3.14**: O SQLAlchemy 2.0.25 apresentava `AssertionError` por mudanças internas no sistema de tipos do Python 3.14. A IA sugeriu o upgrade para `SQLAlchemy>=2.0.30`.

Em todos esses cenários, a IA atuou como uma ferramenta de apoio — diagnosticando erros a partir de logs e tracebacks, sugerindo correções pontuais e explicando o motivo de cada problema para que eu pudesse aprender com cada situação.

---
##  Useful Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Clerk Authentication Docs](https://clerk.com/docs)
- [TanStack Router Docs](https://tanstack.com/router/latest)
- [TanStack Query Docs](https://tanstack.com/query/latest)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [SQLAlchemy 2.0 Docs](https://docs.sqlalchemy.org/en/20/)
