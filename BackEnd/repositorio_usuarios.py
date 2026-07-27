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
