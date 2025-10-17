from cryptography.fernet import Fernet
from pymongo import MongoClient
import hashlib
import time

client = MongoClient("mongodb+srv://root:123@cluster0.sqkox39.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['lista']
colecao_chaves = db['chaves'] 
colecao_mensagens = db['mensagens']

def criar_usuario(username):
    chave = Fernet.generate_key()
    colecao_chaves.insert_one({"username": username, "chave": chave})
    print(f"Usuário '{username}' criado com chave simétrica registrada.")

def enviar_mensagem(remetente, destinatario, texto):
    remetente_doc = colecao_chaves.find_one({"username": remetente})
    destinatario_doc = colecao_chaves.find_one({"username": destinatario})
    chave = destinatario_doc['chave']
    fernet = Fernet(chave)
    msg_cripto = fernet.encrypt(texto.encode())
    timestamp = str(time.time())
    colecao_mensagens.insert_one({"remetente": remetente,"destinatario": destinatario,"mensagem": msg_cripto,"timestamp": timestamp})
    print(f" Mensagem enviada para '{destinatario}'.")

def ler_mensagens(username):
    doc_usuario = colecao_chaves.find_one({"username": username})
    chave = doc_usuario['chave']
    fernet = Fernet(chave)
    mensagens = list(colecao_mensagens.find({"destinatario": username}).sort("timestamp", 1))
    print(f"\n Mensagens para {username}:")
    for msg in mensagens:
        texto = fernet.decrypt(msg['mensagem']).decode()
        print(f"De {msg['remetente']} - {time.ctime(float(msg['timestamp']))}: {texto}")


while True:
        print("\n===================================")
        print("        Mensageiro Criptografado ")
        print("===================================")
        print("1 - Criar usuário")
        print("2 - Enviar mensagem")
        print("3 - Ler mensagens")
        print("4 - Sair")
        print("===================================")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            username = input("Digite o nome do usuário: ").strip()
            criar_usuario(username)
        elif opcao == "2":
            remetente = input("Remetente: ").strip()
            destinatario = input("Destinatário: ").strip()
            texto = input("Mensagem: ").strip()
            enviar_mensagem(remetente, destinatario, texto)
        elif opcao == "3":
            username = input("Usuário para ler mensagens: ").strip()
            ler_mensagens(username)
        elif opcao == "4":
            print(" Saindo do mensageiro...")
            break
        else:
            print(" Opção inválida!")
