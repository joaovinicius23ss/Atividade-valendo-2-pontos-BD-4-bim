from cryptography.fernet import Fernet
from pymongo import MongoClient
import hashlib

key = Fernet.generate_key()
fernet = Fernet(key)

client = MongoClient("mongodb+srv://root:123@cluster0.sqkox39.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["test"]
collection = db["Alunos"]

def gerar_hash_sha256(nome_arquivo):
    h = hashlib.sha256()
    h.update(nome_arquivo.encode())
    return h.hexdigest()

def armazenar_hash(nome_arquivo):
    hash_arquivo = gerar_hash_sha256(nome_arquivo)
    hash_criptografado = fernet.encrypt(hash_arquivo.encode())
    collection.insert_one({
        "nome_arquivo": nome_arquivo, "hash_criptografado": hash_criptografado})
    print("O Hash foi gerado e salvo no banco de dados.")

def verificar_integridade(nome_arquivo):
    doc = collection.find_one({"nome_arquivo": nome_arquivo})
    hash_guardado = fernet.decrypt(doc["hash_criptografado"]).decode()
    hash_atual = gerar_hash_sha256(nome_arquivo)

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

client.close()



