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

### Frontend (`front/`)

O frontend é uma aplicação web desenvolvida com [React](https://reactjs.org/), proporcionando uma interface amigável e interativa para os usuários.

**Principais funcionalidades:**

- Permitir que os usuários visualizem produtos e recebam recomendações.
- Enviar dados de interação dos usuários para a API Backend.
- Apresentar as recomendações de forma clara e atrativa.

### Serviço de Recomendação (`recommender_service_ai/`)

Este serviço é responsável por processar os dados e gerar recomendações personalizadas utilizando técnicas de inteligência artificial. É desenvolvido em [Python](https://www.python.org/) e utilizar bibliotecas como [Pytorch](https://pytorch.org/get-started/locally/).

**Principais funcionalidades:**

- Analisar dados de usuários e produtos.
- Aplicar algoritmos de recomendação para sugerir produtos relevantes.
- Fornecer as recomendações para a API Backend mediante requisições.

### Banco de Dados (`db/`)

O banco de dados armazena informações essenciais para o funcionamento do sistema, como dados de usuários, produtos e interações. A estrutura do banco pode ser definida no arquivo `db.json` e gerenciada por um serviço de banco de dados como o [MongoDB](https://www.mongodb.com/) ou [PostgreSQL](https://www.postgresql.org/).

**Principais funcionalidades:**

- Armazenar e recuperar dados conforme as necessidades dos serviços.
- Manter a integridade e consistência das informações.

## Instalação

Para executar o projeto localmente, siga os passos abaixo:

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/leonardoigor/ai_product_recommendation.git
   cd ai_product_recommendation
   
2. **Rodar o Projeto:**
   ```bash
   docker-compose up -d --build
