from cryptography.fernet import Fernet
from pymongo import MongoClient
import hashlib

client = MongoClient("mongodb+srv://root:123@cluster0.sqkox39.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["lista"]
colecao_votos = db["votos"]

fernet = Fernet(Fernet.generate_key())

def gerar_hash(texto):
    return hashlib.sha256(texto.encode()).hexdigest()

def registrar_voto(eleitor, voto):
    voto_bytes = voto.encode()
    voto_criptografado = fernet.encrypt(voto_bytes)
    hash_voto = gerar_hash(voto)
    colecao_votos.insert_one({"eleitor": eleitor,"voto_criptografado": voto_criptografado,"hash": hash_voto})
    print("Voto registrado com segurança.")

def listar_votos():
    votos = list(colecao_votos.find())
    for idx, v in enumerate(votos, start=1):
        print(f"{idx} | Eleitor: {v['eleitor']} | Hash: {v['hash']}")

def verificar_integridade(idx):
    votos = list(colecao_votos.find())
    v = votos[idx - 1]
    voto_decrypt = fernet.decrypt(v["voto_criptografado"]).decode()
    hash_atual = gerar_hash(voto_decrypt) 

if __name__ == "__main__":
    while True:
        print("\n========================================")
        print("       Sistema de Votação Segura       ")
        print("========================================")
        print("1 - Registrar voto")
        print("2 - Listar hashes de votos")
        print("3 - Verificar integridade de um voto")
        print("4 - Sair")
        print("========================================")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            eleitor = input("Nome do eleitor: ").strip()
            voto = input("Escolha do voto: ").strip()
            registrar_voto(eleitor, voto)
        elif opcao == "2":
            listar_votos()
        elif opcao == "3":
            listar_votos()
            try:
                idx = int(input("Digite o índice do voto para verificar: ").strip())
            except ValueError:
                print("Índice inválido.")
                continue
            verificar_integridade(idx)
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")
