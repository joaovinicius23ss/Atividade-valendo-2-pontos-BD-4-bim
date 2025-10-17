from cryptography.fernet import Fernet
from pymongo import MongoClient
import hashlib
import time

client = MongoClient("mongodb+srv://root:123@cluster0.sqkox39.mongodb.net/""?retryWrites=true&w=majority&appName=Cluster0")
db = client['lista']
colecao = db['lista']

chave = Fernet.generate_key()
fernet = Fernet(chave)

def gerar_hash(caminho_arquivo):
    h = hashlib.sha256()
    return h.hexdigest()

def criar_backup(caminho_arquivo):
    
    with open(caminho_arquivo, "rb") as f:
        conteudo = f.read()
    conteudo_cripto = fernet.encrypt(conteudo)

    nome_backup = f"backup_{os.path.basename(caminho_arquivo)}"
    with open(nome_backup, "wb") as f:
        f.write(conteudo_cripto)

    hash_arquivo = gerar_hash(caminho_arquivo)
    timestamp = str(time.time())

    colecao.insert_one({"arquivo_original": caminho_arquivo,"backup": nome_backup,"hash_sha256": hash_arquivo,"timestamp": timestamp})

    print(f" Backup criado: {nome_backup}")
    print(f"Hash SHA-256 armazenado: {hash_arquivo}")

def verificar_backup(caminho_arquivo):
    doc = colecao.find_one({"arquivo_original": caminho_arquivo})
    hash_atual = gerar_hash(caminho_arquivo)
    if hash_atual == doc['hash_sha256']:
        print(" Arquivo íntegro! Hashs conferem.")
    else:
        print(" Arquivo alterado! Hashs não conferem.")

while True:
        print("\n===================================")
        print("        Backup Criptografado     ")
        print("===================================")
        print("1 - Criar backup")
        print("2 - Verificar integridade do arquivo")
        print("3 - Sair")
        print("===================================")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            arquivo = input("Digite o caminho do arquivo a ser salvo em backup: ").strip()
            criar_backup(arquivo)

        elif opcao == "2":
            arquivo = input("Digite o caminho do arquivo original para verificação: ").strip()
            verificar_backup(arquivo)

        elif opcao == "3":
            print(" Saindo do sistema de backup...")
            break

        else:
            print(" Opção inválida! Tente novamente.")
