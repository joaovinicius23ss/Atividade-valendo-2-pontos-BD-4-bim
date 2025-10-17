from pymongo import MongoClient
import hashlib
from cryptography.fernet import Fernet

client = MongoClient("mongodb+srv://root:123@cluster0.sqkox39.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["lista"]
colecao = db["lista"]

def gerar_hash(texto):
    return hashlib.sha256(texto.encode()).hexdigest()

def adicionar_registro(conteudo):
    hash_registro = gerar_hash(conteudo)
    colecao.insert_one({"conteudo": conteudo,"hash": hash_registro})
    print("Registro adicionado com hash calculado.")

def listar_registros():
    registros = list(colecao.find())
    for idx, r in enumerate(registros, start=1):
        print(f"{idx} | Conteúdo: {r['conteudo']} | Hash: {r['hash']}")

def validar_integridade():
    registros = list(colecao.find())
    for idx, r in enumerate(registros, start=1):
        hash_atual = gerar_hash(r["conteudo"])
        if hash_atual == r["hash"]:
            print(f"{idx} |  Registro íntegro")
        else:
            print(f"{idx} |  Registro alterado!")

if __name__ == "__main__":
    while True:
        print("\n========================================")
        print("       Validador de Integridade DB     ")
        print("========================================")
        print("1 - Adicionar registro")
        print("2 - Listar registros")
        print("3 - Validar integridade dos registros")
        print("4 - Sair")
        print("========================================"
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            c = input("Digite o conteúdo do registro: ").strip()
            adicionar_registro(c)
        elif opcao == "2":
            listar_registros()
        elif opcao == "3":
            validar_integridade()
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")
