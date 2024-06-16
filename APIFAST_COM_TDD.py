from flask import Flask, jsonify, request
from werkzeug.exceptions import NotFound
import datetime

app = Flask(__name__)

produtos = [
    {"id": 1, "nome": "Produto A", "preco": 4500, "update_at": datetime.datetime.now()},
    # ... outros produtos
]

# Mapear uma exceção para erros de inserção
@app.errorhandler(ValueError)
def handle_value_error(e):
    return jsonify({"mensagem": "Erro ao inserir dados"}), 500

# Atualizar
@app.route('/produtos/<int:id>', methods=['PATCH'])
def atualizar_produto(id):
    produto = next((p for p in produtos if p['id'] == id), None)
    if not produto:
        raise NotFound('Produto não encontrado')
    dados = request.get_json()
    produto.update(dados)
    produto['update_at'] = datetime.datetime.now()  # Atualizar o momento do update
    return jsonify(produto)

# Filtros
@app.route('/produtos', methods=['GET'])
def filtrar_produtos():
    min_preco = request.args.get('min_preco', default=5000, type=int)
    max_preco = request.args.get('max_preco', default=8000, type=int)
    produtos_filtrados = [p for p in produtos if min_preco < p['preco'] < max_preco]
    return jsonify(produtos_filtrados)

if __name__ == '__main__':
    app.run(debug=True)