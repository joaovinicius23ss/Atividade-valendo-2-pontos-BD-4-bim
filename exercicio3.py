import hashlib
from pymongo import MongoClient

client = MongoClient("mongodb+srv://root:123@cluster0.sqkox39.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['lista']
colecao = db['lista']

def gerar_hash(senha: str) -> str:

    hash_obj = hashlib.sha256(senha.encode())
    return hash_obj.hexdigest()

def armazenar_usuario(usuario: str, senha: str):
    if colecao.find_one({'usuario': usuario}):
        print("Usuário já existe!")
        return
    hash_senha = gerar_hash(senha)
    colecao.insert_one({'usuario': usuario, 'hash_senha': hash_senha})
    print(f"Usuário '{usuario}' criado com sucesso!")

def verificar_senha(usuario: str, senha: str) -> bool:
    usuario_encontrado = colecao.find_one({'usuario': usuario})
    hash_fornecido = gerar_hash(senha)
    if usuario_encontrado['hash_senha'] == hash_fornecido:
        return True
    return False


while True:
    print("\n1 - Criar usuário")
    print("2 - Verificar senha")
    print("3 - Sair")
    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        u = input("Usuário: ").strip()
        s = input("Senha: ").strip()
        armazenar_usuario(u, s)
    elif opcao == "2":
        u = input("Usuário: ").strip()
        s = input("Senha: ").strip()
        if verificar_senha(u, s):
            print("Acesso permitido!")
        else:
            print("Acesso negado!")
    elif opcao == "3":
        break
    else:
        print("Opção inválida.")
