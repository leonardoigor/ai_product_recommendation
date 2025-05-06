# AI Product Recommendation

Sistema completo de recomendação de produtos baseado em inteligência artificial, composto por uma API backend, um frontend interativo, um serviço de recomendação e um banco de dados.

## Índice

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Serviços](#serviços)
  - [API Backend (`api/`)](#api-backend-api)
  - [Frontend (`front/`)](#frontend-front)
  - [Serviço de Recomendação (`recommender_service_ai/`)](#serviço-de-recomendação-recommender_service_ai)
  - [Banco de Dados (`db/`)](#banco-de-dados-db)
- [Instalação](#instalação)
- [Uso](#uso)
  - [Endpoints da API](#endpoints-da-api)
  - [Atualizar Recomendações](#atualizar-recomendações)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Licença](#licença)

## Visão Geral

Este projeto tem como objetivo fornecer recomendações personalizadas de produtos para usuários, utilizando técnicas de inteligência artificial. A aplicação é composta por múltiplos serviços que trabalham em conjunto para coletar dados, processar informações e apresentar recomendações relevantes.

## Arquitetura

A arquitetura do sistema é baseada em microsserviços, com os seguintes componentes principais:

- **API Backend**: Responsável por gerenciar as requisições dos usuários e intermediar a comunicação entre o frontend e os serviços internos.
- **Frontend**: Interface gráfica que permite aos usuários interagir com o sistema e visualizar as recomendações.
- **Serviço de Recomendação**: Processa os dados dos usuários e produtos para gerar recomendações personalizadas.
- **Banco de Dados**: Armazena informações sobre usuários, produtos e interações.

A comunicação entre os serviços é facilitada pelo uso do Docker e do Docker Compose, que orquestram os containers de cada componente.

## Serviços

### API Backend (`api/`)

A API Backend é desenvolvida em [Node.js](https://nodejs.org/) e utiliza o framework [Express](https://expressjs.com/) para gerenciar as rotas e requisições HTTP. Ela serve como ponto central de comunicação entre o frontend e os demais serviços.

**Principais funcionalidades:**

- Receber requisições do frontend.
- Comunicar-se com o serviço de recomendação para obter sugestões de produtos.
- Interagir com o banco de dados para armazenar e recuperar informações.

### Endpoints da API

#### Usuários
- **GET /users**: Retorna todos os usuários.
- **POST /users**: Cria um novo usuário.

#### Itens
- **GET /items**: Retorna todos os itens (produtos).
- **POST /items**: Cria um novo item.
- **GET /items/generate**: Gera 1.000 itens aleatórios para testes.

#### Interações
- **GET /interactions**: Retorna todas as interações de usuários com produtos.
- **POST /interactions**: Cria uma nova interação de usuário com produto.

#### Scores (Pontuações de Relevância)
- **GET /scores**: Retorna todos os scores de relevância entre usuários e itens.
- **POST /scores**: Cria um novo score de relevância.
- **DELETE /scores/:score_id**: Deleta um score de relevância pelo `score_id`.

#### Recomendação de Produtos
- **GET /recommendations/:user_id**: Retorna uma lista de recomendações personalizadas para o usuário, ordenadas por relevância. Suporta paginação com parâmetros `page` e `limit`.

## Instalação

Para executar o projeto localmente, siga os passos abaixo:

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/leonardoigor/ai_product_recommendation.git
   cd ai_product_recommendation

## Uso
Executando:
```bash
docker-compose up -d --build
```
Com a aplicação em execução, você pode:

- **Visualizar produtos**: Navegue através do catálogo de produtos disponíveis.
- **Interagir com os produtos**: Os usuários podem visualizar, curtir, adicionar ao carrinho, etc.
- **Receber recomendações personalizadas**: Com base em suas interações, o sistema fornecerá sugestões de produtos.

### Atualizar Recomendações

Toda vez que você quiser atualizar as recomendações de produtos para um usuário, será necessário **disparar o serviço de recomendação** (`recommender_service_ai`) em Python para recalcular as pontuações de relevância e fornecer novas recomendações.

Para atualizar as recomendações, execute o serviço de recomendação manualmente ou configure uma rotina que o dispare automaticamente, como por exemplo:

```bash
# Exemplo de execução do serviço de recomendação
python recommender_service_ai/recommender.py
```
ou rode o container `recommender_service_ai` novamente


## Tecnologias Utilizadas

- **Frontend:**
  - [React](https://reactjs.org/): Biblioteca JavaScript para construir interfaces de usuário dinâmicas e responsivas.
  - [JavaScript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript): Linguagem de programação usada para construir a lógica de interação do frontend.
  - [CSS](https://developer.mozilla.org/pt-BR/docs/Web/CSS): Linguagem usada para estilizar a interface do usuário.

- **Backend:**
  - [Node.js](https://nodejs.org/): Ambiente de execução JavaScript no servidor, usado para construir a API backend.
  - [Express](https://expressjs.com/): Framework web para Node.js que facilita o gerenciamento de rotas e requisições HTTP.

- **Serviço de Recomendação:**
  - [Python](https://www.python.org/): Linguagem de programação usada para implementar o serviço de recomendação baseado em inteligência artificial.
  - [PyTorch](https://pytorch.org/get-started/locally/): Biblioteca de aprendizado de máquina usada para criar e treinar os modelos de recomendação.

- **Banco de Dados:**
  - [MongoDB](https://www.mongodb.com/): Banco de dados NoSQL utilizado para armazenar os dados de usuários, produtos e interações.
  - [PostgreSQL](https://www.postgresql.org/): Banco de dados relacional que pode ser utilizado em vez do MongoDB, dependendo das necessidades.

- **Infraestrutura:**
  - [Docker](https://www.docker.com/): Plataforma para containerização de aplicações, usada para garantir que todos os componentes funcionem da mesma forma em qualquer ambiente.
  - [Docker Compose](https://docs.docker.com/compose/): Ferramenta que permite definir e executar aplicações Docker multi-containers, usada para orquestrar os serviços no projeto.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE). 