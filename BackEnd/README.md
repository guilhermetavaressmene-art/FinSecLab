# 🛡️ FinSec Lab

Bem-vindo ao **FinSec Lab**, um projeto de sistema financeiro focado na construção de um Back-End robusto usando Python.

O objetivo principal deste laboratório não é apenas fazer o código funcionar, mas sim aplicar as melhores práticas de **Engenharia de Software** e **Segurança da Informação (AppSec)** desde a primeira linha de código.

---

## 🎯 Arquitetura e Padrões

Este projeto foi desenhado utilizando os princípios de **Clean Architecture** (Arquitetura Limpa) e **Separation of Concerns** (Separação de Responsabilidades), dividindo o sistema em camadas isoladas:

* **Database:** Configuração do banco de dados e ativação de chaves estrangeiras.
* **Repositório:** Camada isolada que conversa com o banco de dados. Nenhuma outra camada conhece a linguagem SQL.
* **Services (Regras de Negócio):** O cérebro da aplicação. Higieniza dados, valida regras de negócio e aplica camadas de segurança antes de permitir qualquer persistência.

---

## 🔐 Camada de Segurança (AppSec)

Neste projeto, a segurança não é uma reflexão tardia. As seguintes proteções foram implementadas nativamente:

* **Proteção contra SQL Injection (SQLi):** Uso exclusivo de *Parameterized Queries* no SQLite. O sistema confunde dados de usuário com comandos de execução.
* **Hashing de Senhas com Salt:** As senhas não trafegam e não são salvas em texto puro. Utilização da biblioteca `werkzeug.security` (algoritmo *scrypt*) para gerar hashes irreversíveis, protegendo o banco contra vazamentos e ataques de *Rainbow Tables*.
* **Prevenção contra User Enumeration:** Padronização das respostas genéricas de erro ("E-mail ou Senha incorretos") no serviço de login, impedindo que atacantes mapeiem quais e-mails estão cadastrados na base de clientes.
* **Defesa em Profundidade (Defense in Depth):** Checagens duplas de integridade (ex: duplicidade de e-mail), feitas primeiramente nas regras de negócio (Services) e garantidas por *Constraints* (`UNIQUE`) na camada de banco de dados.

---

## 🚀 Como executar o projeto

### Pré-requisitos
* Python 3.x instalado.
* Gerenciador de pacotes `pip`.

### Instalação

1. Clone este repositório:
   ```bash
   git clone [https://github.com/SEU_USUARIO/finsec-lab.git](https://github.com/SEU_USUARIO/finsec-lab.git)