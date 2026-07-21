import repositorio

def validar_valor(valor):
    try:
        valor_convertido = float(valor)
    except ValueError:
        raise ValueError("O valor deve ser um número válido.")
    
    if valor_convertido <= 0:
        raise ValueError("O número deve ser positivo.")

    return valor_convertido

def validar_tipo(tipo):
    tipo_normalizado = tipo.strip().upper()

    if tipo_normalizado not in ['GANHO', 'GASTO']:
        raise ValueError("Tipo inválido.")
    
    return tipo_normalizado

def verificar_usuario(id_usuario):
    if repositorio.buscar_por_id(id_usuario) is None:
        raise ValueError("ID Usuário inválido.")
    
    return

def validar_descricao(descricao):
    descricao_normalizada = descricao.strip()

    desc_caracteres = len(descricao_normalizada)

    if desc_caracteres > 50 or desc_caracteres < 6:
        raise ValueError("Mín. de 6 caracteres ou Máx. de 50 caracteres.")
    
    return descricao_normalizada

def cadastro_transacoes(id_usuario, valor, tipo, descricao):
    valor_valido = validar_valor(valor)

    tipo_valido = validar_tipo(tipo)

    verificar_usuario(id_usuario)

    descricao_valida = validar_descricao(descricao)

    repositorio.cadastrar_transacao(id_usuario, valor_valido, tipo_valido, descricao_valida)

def consultar_saldo(id_usuario):
    verificar_usuario(id_usuario)

    saldo = repositorio.buscar_saldo(id_usuario)

    if saldo is None:
        return 0.0
    
    return saldo