from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv
from functools import wraps
import jwt
import datetime
import services_usuario, services_transacoes, database
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

pasta_backend = os.path.dirname(os.path.abspath(__file__))
caminho_env = os.path.join(pasta_backend, '..', '.env')
load_dotenv(caminho_env)

app = Flask(__name__, static_folder='../FrontEnd/templates', static_url_path='')
CORS(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave_secreta_de_emergencia_123')


database.tabela_usuarios()
database.tabela_transacoes()

def token_obrigatorio(funcao):
    @wraps(funcao)

    def decorated(*args, **kwargs):
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']

            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

            else:
                token = auth_header

        if not token:
            return jsonify({"erro": "Token de acesso não fornecido!"}), 401

        try:
            dados = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            id_usuario_logado = dados['id_usuario']

        except jwt.ExpiredSignatureError:
            return jsonify({"erro": "Seu Token expirou. Faça login novamente!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"erro": "Token inválido ou adulterado!"}), 401

        return funcao(id_usuario_logado, *args, **kwargs)

    return decorated

@app.route('/', methods=['GET'])
def home():
    return send_from_directory('../FrontEnd/templates', 'index.html')

@app.route('/finseclab', methods=['GET'])
def inicio():
    boas_vindas = {"mensagem":"Seja Bem-Vindo ao FinSecLab."}

    return jsonify(boas_vindas), 200

#ROTAS USUARIOS

@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    try:
        #Dados Front-End
        username_email_senha = request.json
        username = username_email_senha.get('username')
        email = username_email_senha.get('email')
        senha = username_email_senha.get('senha')

        #Cadastro Banco De Dados (Com segurança)
        services_usuario.cadastrar_usuario(username, email, senha)

        #Retorno Back-End
        retorno = {
            "mensagem": "Usuário cadastrado!"
        }
        return jsonify(retorno), 201

    except ValueError as error:
        erro = {"erro": str(error)}
        return jsonify(erro), 400
    
@app.route('/login', methods=['POST'])
def login():
    try:
        #Dados Front-End
        email_e_senha = request.json
        email = email_e_senha.get('email')
        senha = email_e_senha.get('senha')

        #Dados Banco de Dados
        dados_usuario = services_usuario.login_usuario(email, senha)
        id_usuario, username = dados_usuario

        #Aplicação de Segurança
        payload = {
            "id_usuario": id_usuario,
            "exp": (datetime.datetime.utcnow() + datetime.timedelta(hours=1))
        }
        token_criptografado = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")

        # FIX: Se o PythonAnywhere gerar em Bytes, converte para String!
        if isinstance(token_criptografado, bytes):
            token_criptografado = token_criptografado.decode('utf-8')

        # Retorno do Back-End
        retorno = {
            "mensagem": "Login realizado.",
            "token": token_criptografado
        }
        return jsonify(retorno), 201

    #Tratação de Erros
    except ValueError as error:
        erro = {"erro": str(error)}
        return jsonify(erro), 400

#ROTAS TRANSAÇÕES
    
@app.route('/transacao', methods=['POST'])
@token_obrigatorio
def cadastrar_transacao(id_usuario):
    try:
        dados = request.json

        valor = dados.get('valor')
        tipo = dados.get('tipo')
        descricao = dados.get('descricao')

        services_transacoes.cadastro_transacoes(id_usuario,
                                                valor,
                                                tipo,
                                                descricao)
        
        retorno = {"mensagem":"Transação concluída com sucesso!"}

        return jsonify(retorno), 201
        
    except ValueError as error:
        erro = {"erro":str(error)}
        return jsonify(erro), 400
    
@app.route('/saldo', methods=['GET'])
@token_obrigatorio
def mostrar_saldo(id_usuario_logado):
    try:
        saldo = services_transacoes.consultar_saldo(id_usuario_logado)

        #Retorno Back-End
        retorno = {
            "id_usuario": id_usuario_logado,
            "saldo": saldo
            }
        return jsonify(retorno), 200
    
    except ValueError as error:
        return jsonify({
            "erro":str(error)
            }), 400
    
@app.route("/extrato", methods=['GET'])
@token_obrigatorio
def mostrar_extrato(id_usuario_logado):
    try:
        lista_extrato = services_transacoes.puxar_extrato(id_usuario_logado)

        #Retorno Back-End
        retorno = {
            "id_usuario": id_usuario_logado,
            "extrato": lista_extrato
            }
        return jsonify(retorno), 200
    
    except ValueError as error:
        return jsonify(str(error)), 400


if __name__ == '__main__':
    app.run(debug=True)