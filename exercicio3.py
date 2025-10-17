from pymongo import MongoClient
import hashlib
from cryptography.fernet import Fernet
import secrets

client = MongoClient("mongodb+srv://root:123@cluster0.sqkox39.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['lista']
colecao = db['lsita']

def gerar_salt():
    return secrets.token_hex(16)

def gerar_hash(senha, salt):
    h = hashlib.sha512()
    h.update((salt + senha).encode())
    return h.hexdigest()

def criar_usuario(username, senha):
    salt = gerar_salt()
    hash_senha = gerar_hash(senha, salt)
    colecao.insert_one({"username": username, "salt": salt,"hash_senha": hash_senha})
    print(f"Usuário '{username}' criado com sucesso!")

def autenticar_usuario(username, senha):
    doc = colecao.find_one({"username": username})
    hash_tentativa = gerar_hash(senha, doc['salt'])
    if hash_tentativa == doc['hash_senha']:
        print("Autenticação bem-sucedida!")
        return True
    else:
        print("Senha incorreta!")
        return False

def trocar_senha(username, senha_antiga, senha_nova):
    salt = gerar_salt()
    hash_senha = gerar_hash(senha_nova, salt)
    colecao.update_one({"username": username},{"$set": {"salt": salt, "hash_senha": hash_senha}})
    print("Senha alterada com sucesso!")


if __name__ == "__main__":
    while True:
        print("\n===============================")
        print("       Sistema de Login ")
        print("===============================")
        print("1 - Criar usuário")
        print("2 - Autenticar usuário")
        print("3 - Trocar senha")
        print("4 - Sair")
        print("===============================")

        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            u = input("Usuário: ").strip()
            s = input("Senha: ").strip()
            criar_usuario(u, s)
        elif opcao == "2":
            u = input("Usuário: ").strip()
            s = input("Senha: ").strip()
            autenticar_usuario(u, s)
        elif opcao == "3":
            u = input("Usuário: ").strip()
            old = input("Senha antiga: ").strip()
            new = input("Nova senha: ").strip()
            trocar_senha(u, old, new)
        elif opcao == "4":
            print(" Saindo do sistema de login...")
            break
        else:
            print(" Opção inválida!")

