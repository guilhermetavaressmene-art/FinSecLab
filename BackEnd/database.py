import sqlite3

import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CAMINHO_BANCO = BASE_DIR / "finseclab.db"

def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)

    conexao.execute("""
        PRAGMA foreign_keys = ON
    """)

    return conexao
    

def executar(codigo):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(codigo)

    conexao.commit()
    conexao.close()

def tabela_usuarios():
    executar("""
             CREATE TABLE IF NOT EXISTS usuarios (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT NOT NULL,
             email TEXT NOT NULL UNIQUE,
             senha TEXT NOT NULL
             )""")
    
def tabela_transacoes():
    executar("""
             CREATE TABLE IF NOT EXISTS transacoes(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             id_usuario INTEGER NOT NULL,
             valor FLOAT NOT NULL,
             tipo TEXT NOT NULL,
             descricao TEXT NOT NULL
             
             FOREIGN KEY (id_usuario)
                REFERENCES usuarios(id)
             )""")
    