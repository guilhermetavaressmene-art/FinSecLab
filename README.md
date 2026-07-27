# 🛡️ FinSecLab

**FinSecLab** é uma aplicação web financeira projetada com foco absoluto em **Arquitetura de Software** e **Segurança da Informação (AppSec)**. 

O projeto adota uma arquitetura desacoplada (API RESTful + Single Page Application) e implementa defesas rigorosas contra vulnerabilidades clássicas mapeadas pela OWASP, servindo como um laboratório prático de desenvolvimento seguro.

---

## 🏗️ Arquitetura do Projeto

O sistema é dividido em duas grandes peças que se comunicam via JSON (CORS habilitado):

1. **Front-End (SPA):** Construído com Vanilla JavaScript, HTML5 e Tailwind CSS. Gerencia o estado da aplicação, roteamento visual e armazenamento seguro do Token JWT no lado do cliente.
2. **Back-End (API):** Construído em Python com Flask. Estruturado no padrão de camadas (Responsabilidade Única) para facilitar testes, manutenção e auditorias:
   - **Rotas (`app.py`):** Controlers que recebem a requisição, validam o Token e devolvem JSON.
   - **Services (`services_*.py`):** Camada de regras de negócio, sanitização e validação de dados.
   - **Repositórios (`repositorio_*.py`):** Camada de abstração de persistência (Data Access Object).
   - **Database (`database.py`):** Configuração e integridade referencial do banco.

---

## 🔒 Destaques de AppSec (Security by Design)

Este projeto foi construído assumindo que o ambiente externo é hostil. As seguintes defesas foram implementadas:

* **Mitigação de IDOR (Insecure Direct Object Reference):** A API adota *Zero Trust* em relação aos payloads do Front-End. O `id_usuario` para transações e extratos é extraído criptograficamente do payload do **Token JWT**, impedindo que um usuário forje ações em nome de terceiros.
* **Autenticação Stateless (JWT):** Geração e validação de Tokens JWT assinados com chave simétrica (`HS256`) isolada em variáveis de ambiente (`.env`).
* **Proteção contra User Enumeration:** Respostas padronizadas no fluxo de autenticação ("Email ou Senha Incorretos") para mitigar ataques de força bruta focados em descoberta de contas.
* **Blindagem contra SQL Injection:** Uso estrito de *Parameterized Queries* (`?`) no SQLite3.
* **Otimização de Banco de Dados (Defesa contra DoS):** Implementação de consultas relacionais complexas (`INNER JOIN`) para eliminar o problema de *N+1 Queries*, reduzindo a carga no servidor durante requisições de extrato.
* **Armazenamento Seguro de Credenciais:** Senhas são submetidas a *salt* e *hash* usando a biblioteca `werkzeug.security` (PBKDF2) antes da persistência.

---

## 🚀 Tecnologias Utilizadas

**Back-End:**
* Python 3
* Flask & Flask-CORS
* PyJWT (JSON Web Tokens)
* Werkzeug (Security)
* SQLite3 (com `PRAGMA foreign_keys = ON`)

**Front-End:**
* HTML5 / CSS3
* Vanilla JavaScript (Fetch API, DOM Manipulation)
* Tailwind CSS (via CDN)

---

## ⚙️ Como Executar Localmente

### 1. Configurando o Back-End
Abra o terminal na raiz do projeto e crie o ambiente virtual:

```bash
# Crie e ative o ambiente virtual
python -m venv venv
source venv/Scripts/activate  # No Windows

# Instale as dependências (certifique-se de ter gerado o requirements.txt)
pip install Flask python-dotenv PyJWT Werkzeug flask-cors

# Configure as variáveis de ambiente
# Crie um arquivo .env na raiz e adicione:
# SECRET_KEY=sua_chave_secreta_super_segura_aqui

# Inicie a API
python BackEnd/app.py