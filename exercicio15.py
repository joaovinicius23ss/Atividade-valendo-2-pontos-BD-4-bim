from cryptography.fernet import Fernet
from pymongo import MongoClient
import hashlib

client = MongoClient("mongodb+srv://root:123@cluster0.sqkox39.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["lista"]
mensagens = db["mensagens"]

chave = Fernet.generate_key()
fernet = Fernet(chave)

def gerar_hash(msg):
    return hashlib.sha256(msg).hexdigest().encode()

def cliente_envia(msg):
    hash_msg = gerar_hash(msg)
    pacote = fernet.encrypt(msg + b'||' + hash_msg)
    mensagens.insert_one({"origem": "cliente","mensagem": msg.decode(),"hash": hash_msg.decode(),"criptografado": pacote.decode('latin1')})
    print("[CLIENTE] Mensagem criptografada e enviada ao servidor.")
    return pacote

def servidor_recebe(pacote):
    dados = fernet.decrypt(pacote)
    msg, hash_recebido = dados.split(b'||')

    if gerar_hash(msg) == hash_recebido:
        print(f"[SERVIDOR] Mensagem recebida: {msg.decode()}")
        mensagens.insert_one({"origem": "servidor","mensagem": msg.decode(),"hash": hash_recebido.decode(),"status": "íntegra"})
        resposta = input("[SERVIDOR] Digite a resposta: ").encode()
        hash_resposta = gerar_hash(resposta)
        pacote_resposta = fernet.encrypt(resposta + b'||' + hash_resposta)
        mensagens.insert_one({"origem": "servidor","mensagem": resposta.decode(),"hash": hash_resposta.decode(),"criptografado": pacote_resposta.decode('latin1')})
        return pacote_resposta
    else:
        print("[SERVIDOR] Integridade comprometida!")
        mensagens.insert_one({"origem": "servidor","mensagem": "<falha>","hash": "<corrompido>","status": "violado"})
        return None

def cliente_recebe(pacote):
    dados = fernet.decrypt(pacote)
    msg, hash_recebido = dados.split(b'||')
    if gerar_hash(msg) == hash_recebido:
        print(f"[CLIENTE] Resposta recebida: {msg.decode()}")
        mensagens.insert_one({"origem": "cliente", "mensagem": msg.decode(),"hash": hash_recebido.decode(),"status": "íntegra"})
    else:
        print("[CLIENTE] Integridade comprometida!")
        mensagens.insert_one({"origem": "cliente","mensagem": "<falha>","hash": "<corrompido>","status": "violado"})

print("Comunicação Cliente-Servidor Criptografada")
print("-" * 70)

while True:
    texto = input("[CLIENTE] Digite a mensagem (ou 'sair' para encerrar): ")
    if texto.lower() == "sair":
        break
    pacote = cliente_envia(texto.encode())
    resposta = servidor_recebe(pacote)
    if resposta:
        cliente_recebe(resposta)
    print("-" * 70)

print("Comunicação encerrada. Verifique o banco de dados 'lista.mensagens'.")

