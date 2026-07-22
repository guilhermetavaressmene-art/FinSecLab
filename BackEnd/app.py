from flask import Flask, jsonify, request
import database
import services_usuario, services_transacoes

app = Flask(__name__)

database.tabela_transacoes()
database.tabela_usuarios()

@app.route('/finseclab', methods=['GET'])
def inicio():
    boas_vindas = {"mensagem":"Seja Bem-Vindo ao FinSecLab."}

    return jsonify(boas_vindas), 200

#ROTAS USUARIOS

@app.route('/usuarios', methods=['POST'])
def cadastrar_usuario():
    try:
        dados = request.json

        username = dados.get('username')
        email = dados.get('email')
        senha = dados.get('senha')

        services_usuario.cadastrar_usuario(
                    username,
                    email,
                    senha
                )

        retorno = {"mensagem":"Usuário cadastrado com sucesso!"}

        return jsonify(retorno), 201

    except ValueError as erro:
        error = {"erro":str(erro)}

        return jsonify(error), 400
    
@app.route('/login', methods=['POST'])
def login():
    try:
        dados = request.json

        email = dados.get('email')
        senha = dados.get('senha')

        services_usuario.login_usuario(email, senha)

        retorno = {"mensagem":"Login realizado!"}

        return jsonify(retorno), 200
    
    except ValueError as error:
        erro = {"erro":str(error)}

        return jsonify(erro), 400

#ROTAS TRANSAÇÕES
    
@app.route('/transacao', methods=['POST'])
def cadastrar_transacao():
    try:
        dados = request.json

        id_usuario = dados.get('id_usuario')
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


if __name__ == '__main__':
    app.run(debug=True)