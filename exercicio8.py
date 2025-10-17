from cryptography.fernet import Fernet
from pymongo import MongoClient
import hashlib
import base64

client = MongoClient("mongodb+srv://root:123@cluster0.sqkox39.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["lista"]
colecao_chaves = db["chaves"]
colecao_mensagens = db["mensagens"]

def criar_emissor(username):
    key = Fernet.generate_key()
    colecao_chaves.insert_one({"username": username, "key": key})
    print(f"Emissor '{username}' criado. Chave simétrica registrada.")

def obter_chave(username):
    doc = colecao_chaves.find_one({"username": username})
    return doc["key"]

def assinar_mensagem(emissor, mensagem):
    key = obter_chave(emissor)
    hash_bytes = hashlib.sha256(mensagem.encode()).digest()
    f = Fernet(key)
    assinatura = f.encrypt(hash_bytes)
    colecao_mensagens.insert_one({"emissor": emissor,"mensagem": mensagem,"assinatura": assinatura})
    assinatura_b64 = base64.b64encode(assinatura).decode()
    print("Mensagem assinada e armazenada.")
    print(f"Assinatura (base64): {assinatura_b64}")

def listar_mensagens():
    msgs = list(colecao_mensagens.find())
    if not msgs:
        print("Nenhuma mensagem assinada encontrada.")
        return
    for idx, m in enumerate(msgs, start=1):
        print(f"{idx} | Emissor: {m['emissor']} | Mensagem: {m['mensagem']}")

def verificar_assinatura(idx):
    msgs = list(colecao_mensagens.find())
    if idx < 1 or idx > len(msgs):
        print("Índice inválido.")
        return
    doc = msgs[idx - 1]
    emissor = doc["emissor"]
    key = obter_chave(emissor)
    assinatura = doc["assinatura"]
    mensagem = doc["mensagem"]
    f = Fernet(key)
    hash_decrypt = f.decrypt(assinatura)
    hash_atual = hashlib.sha256(mensagem.encode()).digest()
    if hash_decrypt == hash_atual:
        print(" Assinatura válida. Mensagem autêntica e íntegra.")
    else:
        print(" Assinatura inválida. Mensagem foi alterada ou não foi assinada por esse emissor.")

def verificar_assinatura_manual(emissor, mensagem, assinatura_b64):
    key = obter_chave(emissor)
    assinatura = base64.b64decode(assinatura_b64)
    f = Fernet(key)
    hash_decrypt = f.decrypt(assinatura)
    hash_atual = hashlib.sha256(mensagem.encode()).digest()
    if hash_decrypt == hash_atual:
        print(" Assinatura válida.")
    else:
        print(" Assinatura inválida.")

while True:
        print("\n========================================")
        print("      Sistema de Assinatura Simulada  ")
        print("========================================")
        print("1 - Criar emissor (gerar chave)")
        print("2 - Assinar mensagem e armazenar")
        print("3 - Listar mensagens assinadas")
        print("4 - Verificar assinatura por índice")
        print("5 - Verificar assinatura manual")
        print("6 - Sair")
        print("========================================")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            u = input("Nome do emissor: ").strip()
            criar_emissor(u)
        elif opcao == "2":
            e = input("Emissor: ").strip()
            m = input("Mensagem a assinar: ").strip()
            assinar_mensagem(e, m)
        elif opcao == "3":
            listar_mensagens()
        elif opcao == "4":
            listar_mensagens()
            try:
                idx = int(input("Digite o índice da mensagem para verificar: ").strip())
            except ValueError:
                print("Índice inválido.")
                continue
            verificar_assinatura(idx)
        elif opcao == "5":
            e = input("Emissor: ").strip()
            m = input("Mensagem: ").strip()
            s = input("Assinatura (base64): ").strip()
            verificar_assinatura_manual(e, m, s)
        elif opcao == "6":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")
