from cryptography.fernet import Fernet
from pymongo import MongoClient

client = MongoClient("mongodb+srv://root:123@cluster0.sqkox39.mongodb.net/""?retryWrites=true&w=majority&appName=Cluster0")
db = client['lista']
colecao = db['usuarios']
colecao2 = db['mensagens']

def cadastrar_usuario(username: str):

    key = Fernet.generate_key()  # chave simétrica
    colecao.insert_one({"username": username, "key": key})
    print(f"Usuário '{username}' cadastrado com sucesso!")

def obter_chave(username: str) -> bytes:
    user = colecao.find_one({"username": username})
    return user["key"]

def enviar_mensagem(remetente: str, destinatario: str, mensagem: str):
    key = obter_chave(destinatario)
    fernet = Fernet(key)
    msg_criptografada = fernet.encrypt(mensagem.encode())
    colecao2.insert_one({ "de": remetente,"para": destinatario,"mensagem": msg_criptografada})
    print("Mensagem enviada com sucesso!")


def ler_mensagens(username: str):
    key = obter_chave(username)
    fernet = Fernet(key)
    mensagens = colecao2.find({"para": username})
    print(f"\nMensagens para {username}:")
    for msg in mensagens:
        conteudo = fernet.decrypt(msg["mensagem"]).decode()
        print(f"De {msg['de']}: {conteudo}")

while True:
        print("\n1 - Cadastrar usuário")
        print("2 - Enviar mensagem")
        print("3 - Ler mensagens")
        print("4 - Sair")
        opcao = input("> ").strip()

        if opcao == "1":
            u = input("Nome do usuário: ").strip()
            cadastrar_usuario(u)

        elif opcao == "2":
            de = input("Remetente: ").strip()
            para = input("Destinatário: ").strip()
            msg = input("Mensagem: ").strip()
            enviar_mensagem(de, para, msg)

        elif opcao == "3":
            u = input("Usuário que vai ler: ").strip()
            ler_mensagens(u)

        elif opcao == "4":
            break

        else:
            print("Opção inválida!")
