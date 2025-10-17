from flask import Flask, request, jsonify
from pymongo import MongoClient
import hashlib

app = Flask(__name__)

client = MongoClient("mongodb+srv://root:123@cluster0.sqkox39.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["lista"]
colecao_transacoes = db["transacoes"]

def gerar_hash(texto):
    return hashlib.sha256(texto.encode()).hexdigest()

@app.route("/transacao", methods=["POST"])
def criar_transacao():
    dados = request.json
    remetente = dados.get("remetente")
    destinatario = dados.get("destinatario")
    valor = dados.get("valor")
    conteudo = f"{remetente}-{destinatario}-{valor}"
    hash_tx = gerar_hash(conteudo)
    tx_id = colecao_transacoes.count_documents({}) + 1
    colecao_transacoes.insert_one({"tx_id": tx_id,"remetente": remetente,"destinatario": destinatario,"valor": valor,"hash": hash_tx})
    return jsonify({"msg": "Transação registrada", "tx_id": tx_id, "hash": hash_tx})

@app.route("/transacoes", methods=["GET"])
def listar_transacoes():
    transacoes = list(colecao_transacoes.find({}, {"_id": 0}))
    return jsonify(transacoes)

@app.route("/verificar/<int:tx_id>", methods=["GET"])
def verificar_transacao(tx_id):
    tx = colecao_transacoes.find_one({"tx_id": tx_id})
    if not tx:
        return jsonify({"erro": "Transação não encontrada"}), 404
    conteudo = f"{tx['remetente']}-{tx['destinatario']}-{tx['valor']}"
    hash_atual = gerar_hash(conteudo)
    if hash_atual == tx["hash"]:
        return jsonify({"tx_id": tx_id, "status": " Integridade confirmada"})
    else:
        return jsonify({"tx_id": tx_id, "status": " Integridade violada"})


app.run(debug=True)
