from cryptography.fernet import Fernet
from pymongo import MongoClient
import hashlib

try:
    with open("chave.key", "rb") as f:
        chave = f.read()
except FileNotFoundError:
    chave = Fernet.generate_key()
    with open("chave.key", "wb") as f:
        f.write(chave)

fernet = Fernet(chave)
client = MongoClient("mongodb+srv://root:123@cluster0.sqkox39.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["test"]
collection = db["Alunos"]

def gerar_hash_sha512(nome_arquivo):
    h = hashlib.sha512()
    with open(nome_arquivo, "rb") as arquivo:
        for parte in iter(lambda: arquivo.read(4096), b""):
            h.update(parte)
    return h.hexdigest()

def armazenar_hash(nome_arquivo):
    try:
        hash_arquivo = gerar_hash_sha512(nome_arquivo)
        hash_criptografado = fernet.encrypt(hash_arquivo.encode())
        colecao.insert_one({"nome_arquivo": nome_arquivo, "hash_criptografado": hash_criptografado})
        print("Hash SHA-512 gerado e salvo no banco de dados.")
    except FileNotFoundError:
        print("Arquivo não encontrado.")

def verificar_integridade(nome_arquivo):
    doc = colecao.find_one({"nome_arquivo": nome_arquivo})
    if not doc:
        print("Arquivo não registrado.")
        return
    hash_guardado = fernet.decrypt(doc["hash_criptografado"]).decode()
    hash_atual = gerar_hash_sha512(nome_arquivo)
    if hash_guardado == hash_atual:
        print("Arquivo íntegro.")
    else:
        print("Arquivo alterado.")

print("1 - Registrar hash de um arquivo")
print("2 - Verificar integridade de um arquivo")
opcao = input("Escolha uma opção: ")
arquivo = input("Digite o nome do arquivo: ")

if opcao == "1":
    armazenar_hash(arquivo)
elif opcao == "2":
    verificar_integridade(arquivo)
else:
    print("Opção inválida.")

