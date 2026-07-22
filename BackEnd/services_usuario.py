from werkzeug.security import generate_password_hash, check_password_hash
import repositorio_usuarios

#VERIFICAÇÕES e VALIDAÇÕES
def verificar_email(email):
    if repositorio_usuarios.buscar_por_email(email) is None:
        raise ValueError("Usuário não encontrado.")

def verificar_id(id_usuario):
    if repositorio_usuarios.buscar_por_id(id_usuario) is None:
        raise ValueError("Email ou Senha incorretos.")

    return

def validar_email(email):
    email_normalizado = email.strip()

    if '@' in email_normalizado and '.' in email_normalizado:
        return email_normalizado
    
    raise ValueError("Digite um e-mail válido")

def validar_username(username):
    username_normalizado = username.strip().upper()

    if not username_normalizado:
        raise ValueError("Caracteres inválidos")
    
    num_caracteres_username = len(username_normalizado)

    if num_caracteres_username > 20 or num_caracteres_username < 6:
        raise ValueError("Mín. 6 caracteres & Máx. 20 caracteres.")
    
    return username_normalizado

def validar_senha(senha):
    senha_normalizada = senha.strip()

    if not senha_normalizada:
        raise ValueError("Caracteres inválidos")

    num_caracteres_senha = len(senha_normalizada)

    if num_caracteres_senha < 8:
        raise ValueError("Mínimo de 8 caracteres.")
    
    if not any(caracter.isdigit() for caracter in senha_normalizada):
        raise ValueError("Ao menos 1' número.")

    return senha_normalizada


#REGRAS DE NEGÓCIO
def cadastrar_usuario(username, email, senha):
        username_normalizado = validar_username(username)
        email_normalizado = validar_email(email)
        senha_normalizada = validar_senha(senha)

        if repositorio_usuarios.buscar_por_email(email_normalizado) is not None:
            raise ValueError("Email ja cadastrado.")
        
        senha_criptografada = generate_password_hash(senha_normalizada)

        repositorio_usuarios.cadastrar_usuario(username_normalizado, email_normalizado, senha_criptografada)

def login_usuario(email, senha):
    email_digitado = validar_email(email)
    senha_normalizada = validar_senha(senha)

    dados = repositorio_usuarios.buscar_usuario_login(email_digitado)

    if dados is None:
        raise ValueError("Email ou Senha Incorretos.")

    id_user, username, hash_salvo = dados

    if check_password_hash(hash_salvo, senha_normalizada) is False:
        raise ValueError("Email ou Senha incorretos.")
    
    return (id_user, username)

def buscar_user_email(email):
    verificar_email(email)

    user_encontrado = repositorio_usuarios.buscar_por_email(email)
    return user_encontrado[0]

def buscar_user_id(id_usuario):
    verificar_id(id_usuario)

    user_encontrado = repositorio_usuarios.buscar_por_id(id_usuario)
    return user_encontrado[0]