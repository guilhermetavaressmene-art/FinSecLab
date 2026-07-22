# 🛡️ FinSec Lab

## 📖 Sobre o Projeto
O **FinSec Lab** é uma API RESTful desenvolvida em Python, projetada com um foco rigoroso em **Application Security (AppSec)** e **Clean Architecture**. O sistema simula o núcleo financeiro (Back-End) de uma aplicação bancária, permitindo o cadastro de usuários, autenticação segura, registro de transações financeiras e consulta de saldos.

Este projeto é um laboratório prático de Engenharia de Software focado em construir um ambiente *Zero Trust* (Confiança Zero), blindado contra as principais vulnerabilidades da web (OWASP Top 10).

## 🏗️ Arquitetura (Clean Architecture)
O projeto segue o princípio de Separação de Responsabilidades (*Separation of Concerns*), dividido em camadas claras:
* **Camada de Roteamento (`app.py`):** Recebe requisições HTTP (JSON), gerencia os Status Codes e atua como a porta de entrada da API.
* **Camada de Serviço (`services_*.py`):** O "cérebro" do sistema. Contém todas as regras de negócio, sanitização de dados e validações.
* **Camada de Repositório (`repositorio_*.py`):** Abstrai e gerencia a comunicação exclusiva com o banco de dados.
* **Banco de Dados (`database.py`):** Configuração, estruturação e criação das tabelas relacionais.

---

## 🚧 Backlog do Produto (O que vamos construir)

### 🔒 Segurança e Regras de Negócio Implementadas
* **Cadastro de Usuários:** Validação estrita de formato de e-mail e limites de caracteres (*Defense in Depth*).
* **Autenticação Segura:** Proteção contra ataques de dicionário e *Rainbow Tables* utilizando Hashing com Salt (via `werkzeug.security`). Senhas nunca são salvas em texto plano.
* **Prevenção de Enumeração (User Enumeration):** O sistema não revela se um e-mail existe ou não no banco de dados durante tentativas de login falhas.
* **Defesa contra SQL Injection (SQLi):** Todas as interações com o banco de dados utilizam queries parametrizadas (*bind parameters*).
* **Processamento via SQL:** O cálculo do saldo final (Ganhos vs Gastos) é delegado ao motor nativo do banco de dados utilizando `SUM(CASE WHEN...)`.
* **Respostas Padronizadas (HTTP Status Codes):** Retornos claros (`200`, `201`, `400`), evitando vazamento de informações da infraestrutura (*Information Disclosure*).

Para que o FinSec Lab se torne uma API de nível corporativo, as próximas implementações focarão em Identidade, Auditoria e Proteção de Infraestrutura.

### 🔐 Identidade e Controle de Acesso (Zero Trust)
* [ ] **Autenticação via JWT (JSON Web Tokens):** Substituir a confiança cega no Front-End por crachás digitais criptografados (Tokens) gerados no login.
* [ ] **Middlewares de Proteção de Rota:** Decoradores customizados no Flask para bloquear rotas sensíveis caso não haja um Token válido no *Header* (`Authorization: Bearer <token>`).
* [ ] **Correção de Broken Access Control (BAC):** A API deixará de aceitar o `id_usuario` no corpo (*body*) da requisição. A identidade será extraída exclusivamente do Token validado.

### 💰 Novas Rotas Financeiras
* [ ] **Endpoint de Saldo (`GET /saldo`):** Rota protegida que retorna o saldo atual do usuário autenticado.
* [ ] **Endpoint de Extrato (`GET /extrato`):** Rota para listar o histórico de transações, implementando paginação para evitar sobrecarga no banco de dados.

### 🛡️ Defesas Avançadas (AppSec)
* [ ] **Rate Limiting:** Proteção contra ataques de Força Bruta no `/login`, limitando o número