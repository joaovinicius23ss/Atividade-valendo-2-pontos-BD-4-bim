from cryptography.fernet import Fernet
from pymongo import MongoClient
import hashlib

client = MongoClient("mongodb+srv://root:123@cluster0.sqkox39.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["lista"]
colecao_arquivos = db["arquivos"]
fernet = Fernet(Fernet.generate_key())

def gerar_hash(conteudo):
    return hashlib.sha256(conteudo.encode()).hexdigest()

def adicionar_arquivo(nome, conteudo):
    conteudo_bytes = conteudo.encode()
    assinatura = fernet.encrypt(conteudo_bytes)
    hash_arquivo = gerar_hash(conteudo)
    colecao_arquivos.insert_one({"nome": nome,"conteudo_criptografado": assinatura,"hash": hash_arquivo})
    print(f"Arquivo '{nome}' registrado com hash e assinatura.")

def listar_arquivos():
    arquivos = list(colecao_arquivos.find({}, {"_id": 0}))
    for idx, a in enumerate(arquivos, start=1):
        print(f"{idx} | Nome: {a['nome']} | Hash: {a['hash']}")

def verificar_arquivo(idx):
    arquivos = list(colecao_arquivos.find({}, {"_id": 0}))
    arquivo = arquivos[idx - 1]
    conteudo_decrypt = fernet.decrypt(arquivo["conteudo_criptografado"]).decode()
    hash_atual = gerar_hash(conteudo_decrypt)
    if hash_atual == arquivo["hash"]:
        print(f" Arquivo '{arquivo['nome']}' íntegro e autêntico.")
    else:
        print(f" Arquivo '{arquivo['nome']}' adulterado ou corrompido.")



while True:
        print("\n====================================")
        print("       Sistema de Rastreamento       ")
        print("====================================")
        print("1 - Adicionar arquivo")
        print("2 - Listar arquivos")
        print("3 - Verificar arquivo")
        print("4 - Sair")
        print("====================================")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            nome = input("Nome do arquivo: ").strip()
            conteudo = input("Conteúdo do arquivo: ").strip()
            adicionar_arquivo(nome, conteudo)
        elif opcao == "2":
            listar_arquivos()
        elif opcao == "3":
            listar_arquivos()
            try:
                idx = int(input("Digite o índice do arquivo para verificar: ").strip())
            except ValueError:
                print("Índice inválido.")
                continue
            verificar_arquivo(idx)
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")
