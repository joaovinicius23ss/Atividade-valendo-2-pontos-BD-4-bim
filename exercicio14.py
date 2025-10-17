from pymongo import MongoClient
import hashlib

client = MongoClient("mongodb+srv://root:123@cluster0.sqkox39.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["lista"]
colecao_usuarios = db["usuarios"]

def gerar_hash(dado):
    return hashlib.sha256(dado.encode()).hexdigest()

def registrar_usuario():
    print("\n--- Registrar Usuário ---")
    usuario = input("Nome do usuário: ").strip()
    dado_biometrico = input("Insira seu dado biométrico (simulação): ").strip()
    hash_biometrico = gerar_hash(dado_biometrico)
    colecao_usuarios.insert_one({"usuario": usuario,"hash_biometrico": hash_biometrico})
    print(f"Usuário '{usuario}' registrado com hash biométrico.")

def autenticar_usuario():
    print("\n--- Autenticação ---")
    usuario = input("Nome do usuário: ").strip()
    dado_biometrico = input("Insira seu dado biométrico (simulação): ").strip()
    hash_biometrico = gerar_hash(dado_biometrico)
    registro = colecao_usuarios.find_one({"usuario": usuario})
    if hash_biometrico == registro["hash_biometrico"]:
        print(f" Autenticação bem-sucedida para '{usuario}'.")
    else:
        print(f" Dados biométricos não correspondem. Acesso negado.")

def listar_usuarios():
    print("\n--- Usuários Registrados ---")
    usuarios = list(colecao_usuarios.find({}, {"_id": 0, "usuario": 1}))
    for u in usuarios:
        print(f"- {u['usuario']}")

while True:
        print("\n===================================")
        print("       Cofre Biométrico Simulado")
        print("===================================")
        print("1 - Registrar usuário")
        print("2 - Autenticar usuário")
        print("3 - Listar usuários")
        print("4 - Sair")
        print("===================================")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            registrar_usuario()
        elif opcao == "2":
            autenticar_usuario()
        elif opcao == "3":
            listar_usuarios()
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

