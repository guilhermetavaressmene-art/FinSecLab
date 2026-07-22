import database

def executar(codigo, parametros=()):
    conexao = database.conectar()
    cursor = conexao.cursor()

    cursor.execute(codigo, parametros)

    conexao.commit()
    conexao.close()

def executar_busca(codigo, parametros=()):
    conexao = database.conectar()
    cursor = conexao.cursor()

    cursor.execute(codigo, parametros)
    dados = cursor.fetchall()

    conexao.close()
    return dados if dados else None

#USUARIOS
def cadastrar_usuario(nome, email, senha):
    executar("""
             INSERT INTO usuarios
             (username, email, senha)
             VALUES (?, ?, ?)
             """,
             (nome, email, senha))
    
    
def buscar_por_email(email):
    usuario_encontrado = executar_busca("""
                   SELECT id, username, email
                   FROM usuarios
                   WHERE email = ?
                   """,
                   (email,))
    
    if usuario_encontrado:
        return usuario_encontrado[0]
    
    return None

def buscar_por_id(id_usuario):
    usuario_encontrado = executar_busca("""
                                        SELECT username, email
                                        FROM usuarios
                                        WHERE id = ?
                                        """, 
                                        (id_usuario,))
    
    if usuario_encontrado:
        return usuario_encontrado[0]
    
    return None

def buscar_usuario_login(email):
    dados = executar_busca("""
                   SELECT id, username, senha
                   FROM usuarios
                   WHERE email = ?
                   """,
                   (email,))
    
    if dados:
        return dados[0]
    
    return None

# TRANSAÇÕES
def cadastrar_transacao(id_usuario, valor, tipo, descricao):
    executar("""
             INSERT INTO transacoes
             (id_usuario, valor, tipo, descricao)
             VALUES (?, ?, ?, ?)
             """,
             (id_usuario, valor, tipo, descricao))
    
def buscar_dados_transacao(id_transacao):
    dados = executar_busca("""
                   SELECT id_usuario, valor, tipo, descricao
                   FROM transacoes
                   WHERE id = ?
                   """,
                   (id_transacao,))
    
    if dados:
        return dados[0]
    
    return None

def buscar_saldo(id_usuario):
    saldo = executar_busca("""
                   SELECT SUM(
                   CASE
                           
                        WHEN tipo = 'GANHO' THEN valor
                        WHEN tipo = 'GASTO' THEN -valor
                        ELSE 0
                           
                   END)
                   FROM transacoes
                   WHERE id_usuario = ?
                   """,
                   (id_usuario,))
    
    if saldo and saldo[0][0] is not None:
        return float(saldo[0][0])
    
    return None