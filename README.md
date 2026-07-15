# 🛡️ FinSec Lab

Bem-vindo ao **FinSec Lab**, um projeto de sistema financeiro focado na construção de um Back-End robusto usando Python.

O objetivo principal deste laboratório não é apenas fazer o código funcionar, mas sim aplicar as melhores práticas de **Engenharia de Software** e **Segurança da Informação (AppSec)** desde a primeira linha de código.

---

## 🎯 Arquitetura e Padrões

Este projeto foi desenhado utilizando os princípios de **Clean Architecture** (Arquitetura Limpa) e **Separation of Concerns** (Separação de Responsabilidades), dividindo o sistema em camadas isoladas:

* **Database:** Configuração da base de dados e ativação de chaves estrangeiras.
* **Repositório:** Camada isolada que comunica com a base de dados. Nenhuma outra camada conhece a linguagem SQL.
* **Services (Regras de Negócio):** O cérebro da aplicação. Higieniza dados, valida regras de negócio e aplica camadas de segurança antes de permitir qualquer persistência.

---

## 🔐 Camada de Segurança (AppSec)

Neste projeto, a segurança não é uma reflexão tardia. As seguintes proteções foram implementadas nativamente:

* **Proteção contra SQL Injection (SQLi):** Uso exclusivo de *Parameterized Queries* no SQLite. O sistema impede que dados do utilizador sejam interpretados como comandos de execução.
* **Hashing de Senhas com Salt:** As senhas não trafegam e não são guardadas em texto limpo. Utilização da biblioteca `werkzeug.security` (algoritmo *scrypt*) para gerar hashes irreversíveis, protegendo a base de dados contra fugas e ataques de *Rainbow Tables*.
* **Prevenção contra User Enumeration:** Padronização das respostas genéricas de erro ("Email ou Senha incorretos") no serviço de login, impedindo que atacantes mapeiem quais emails estão registados.
* **Defesa em Profundidade (Defense in Depth):** Verificações duplas de integridade (ex: duplicidade de email), feitas primeiramente nas regras de negócio (Services) e garantidas por *Constraints* (`UNIQUE`) na camada de base de dados.

---

## 🚀 Como executar o projeto

### Pré-requisitos
* Python 3.x instalado.
* Gestor de pacotes `pip`.

### Instalação

1. Clone este repositório:
   ```bash
   git clone [https://github.com/guilhermetavaressmene-art/FinSecLab.git](https://github.com/guilhermetavaressmene-art/FinSecLab.git)