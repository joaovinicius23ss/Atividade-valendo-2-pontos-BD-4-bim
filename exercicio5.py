import hashlib
from pymongo import MongoClient
from datetime import datetime


client = MongoClient("mongodb+srv://root:123@cluster0.sqkox39.mongodb.net/""?retryWrites=true&w=majority&appName=Cluster0")
db = client['usuarios_db']
colecao = db['usuarios']

def gerar_hash(senha: str) -> str:
    hash_obj = hashlib.sha256(senha.encode())
    return hash_obj.hexdigest()

def cadastrar_usuario(username: str, senha: str):
    hash_senha = gerar_hash(senha)
    colecao.insert_one({"username": username,"hash_senha": hash_senha,"data_criacao": datetime.now()})
    print(f" Usuário '{username}' cadastrado com sucesso!\n")


def verificar_senha(username: str, senha: str) -> bool:
    user = colecao.find_one({"username": username})
    hash_inserida = gerar_hash(senha)
    if hash_inserida == user["hash_senha"]:
        print(" Acesso permitido!\n")
        return True
    else:
        print(" Acesso negado! Senha incorreta.\n")
        return False


while True:
        print("=====================================")
        print("        Sistema de Usuários        ")
        print("=====================================")
        print("1 - Cadastrar usuário")
        print("2 - Login")
        print("3 - Sair")
        print("=====================================")
        
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            u = input("Digite o nome do usuário: ").strip()
            s = input("Digite a senha: ").strip()
            cadastrar_usuario(u, s)

        elif opcao == "2":
            u = input("Digite o nome do usuário: ").strip()
            s = input("Digite a senha: ").strip()
            verificar_senha(u, s)

        elif opcao == "3":
            print(" Saindo do sistema. Até logo!\n")
            break

        else:
            print(" Opção inválida! Tente novamente.\n")
