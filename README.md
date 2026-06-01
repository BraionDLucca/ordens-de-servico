# API de Gestão de Ordens de Serviço

## Visão Geral

Este projeto consiste em uma API para gerenciamento de Ordens de Serviço, desenvolvida com foco em organização arquitetural, manutenibilidade e escalabilidade.

A aplicação permite o controle completo de clientes, produtos, peças, ordens de serviço, autenticação de usuários e geração de relatórios gerenciais.

O sistema foi estruturado utilizando arquitetura em camadas e princípios SOLID, promovendo separação de responsabilidades, reutilização de código e facilidade de manutenção.

---

# Arquitetura do Sistema

A aplicação segue uma arquitetura modular baseada em camadas, organizada para isolar regras de negócio, acesso a dados e comunicação HTTP.

Fluxo da aplicação:

```text
Router → Service → Repository → Database
```

## Camadas da Aplicação

### Routers (`/routers`)

Responsáveis pelo recebimento das requisições HTTP, definição das rotas da API e integração com a camada de serviços.

### Schemas (`/schemas`)

Camada de validação e serialização de dados utilizando DTOs (Data Transfer Objects). Garante integridade e tipagem dos dados trafegados pela API.

### Services (`/services`)

Contém toda a lógica de negócio da aplicação. Centraliza regras, validações e fluxos operacionais.

### Repositories (`/repositories`)

Responsável pelo acesso e manipulação de dados no banco de dados. Isola queries e operações de persistência.

### Models (`/models`)

Entidades ORM responsáveis pelo mapeamento das tabelas do banco de dados.

---

# Estrutura do Projeto

```text
📦 ordens-de-servico
 ┣ 📂 app
 ┃ ┗ 📜 main.py
 ┣ 📂 config
 ┃ ┗ 📜 settings.py
 ┣ 📂 core
 ┃ ┗ 📜 database.py
 ┣ 📂 models
 ┃ ┣ 📜 cliente_model.py
 ┃ ┣ 📜 historico_status_model.py
 ┃ ┣ 📜 HistoricoPeca.py
 ┃ ┣ 📜 ordem_servico_model.py
 ┃ ┣ 📜 PecaOrdemServico.py
 ┃ ┣ 📜 produto_model.py
 ┃ ┗ 📜 usuario_model.py
 ┣ 📂 repositories
 ┃ ┣ 📜 auth_repository.py
 ┃ ┣ 📜 cliente_repository.py
 ┃ ┣ 📜 ordem_servico_repository.py
 ┃ ┗ 📜 report_repository.py
 ┣ 📂 routers
 ┃ ┣ 📜 auth_router.py
 ┃ ┣ 📜 cliente_router.py
 ┃ ┣ 📜 ordem_servico_router.py
 ┃ ┣ 📜 produto_router.py
 ┃ ┗ 📜 report_router.py
 ┣ 📂 schemas
 ┃ ┣ 📜 auth_schemas.py
 ┃ ┣ 📜 cliente_schemas.py
 ┃ ┣ 📜 ordem_servico_schemas.py
 ┃ ┣ 📜 produto_schemas.py
 ┃ ┗ 📜 report_schema.py
 ┣ 📂 services
 ┃ ┣ 📜 auth_service.py
 ┃ ┣ 📜 cliente_service.py
 ┃ ┣ 📜 ordem_servico_service.py
 ┃ ┣ 📜 produto_service.py
 ┃ ┗ 📜 report_service.py
 ┣ 📜 .gitignore
 ┗ 📜 requirements.txt
```

---

# Funcionalidades Principais

## Autenticação

* Cadastro e autenticação de usuários
* Controle de acesso
* Segurança baseada em tokens

## Gestão de Clientes

* Cadastro de clientes
* Atualização de informações
* Histórico de atendimento

## Gestão de Ordens de Serviço

* Abertura de ordens de serviço
* Atualização de status
* Associação de peças e produtos
* Encerramento de ordens

## Produtos e Peças

* Controle básico de estoque
* Cadastro de produtos
* Vinculação de peças às ordens de serviço

## Relatórios

* Geração de relatórios gerenciais
* Extração de métricas operacionais
* Acompanhamento de atendimentos

---

# Tecnologias Utilizadas

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn
* Banco de Dados Relacional
* Arquitetura em Camadas
* Princípios SOLID

---

# Configuração do Ambiente

## 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/ordens-de-servico.git

cd ordens-de-servico
```

---

## 2. Criar Ambiente Virtual

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv venv

source venv/bin/activate
```

---

## 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

---

## 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto contendo as variáveis esperadas pelo arquivo:

```text
config/settings.py
```

Exemplo:

```env
DATABASE_URL=
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
```

---

# Execução da Aplicação

Inicie o servidor local utilizando:

```bash
uvicorn app.main:app --reload
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:8000
```

---

# Documentação da API

Após iniciar o servidor, a documentação interativa estará disponível em:

## Swagger UI

```text
http://127.0.0.1:8000/docs
```

## ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

# Objetivos do Projeto

* Aplicar arquitetura em camadas
* Utilizar princípios SOLID
* Promover separação de responsabilidades
* Facilitar manutenção e escalabilidade
* Simular um ambiente corporativo de desenvolvimento backend

---

# Considerações Finais

O projeto foi desenvolvido com foco em boas práticas de engenharia de software, priorizando organização estrutural, clareza de código e escalabilidade da aplicação.

A arquitetura adotada permite fácil evolução do sistema, integração com novos módulos e adaptação para diferentes cenários de negócio.
