from cryptography.fernet import Fernet
from pymongo import MongoClient
import hashlib

client = MongoClient("mongodb+srv://root:123@cluster0.sqkox39.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['lista']
colecao = db['lista']
chave = Fernet.generate_key()
fernet = Fernet(chave)

def gerar_hash(texto):
    h = hashlib.sha256()
    h.update(texto.encode())
    return h.hexdigest()

def armazenar_documento(nome_doc, texto):
    texto_cripto = fernet.encrypt(texto.encode())
    hash_texto = gerar_hash(texto)
    colecao.insert_one({"nome_documento": nome_doc,"texto_criptografado": texto_cripto,"hash_sha256": hash_texto})
    print(f" Documento '{nome_doc}' armazenado com sucesso!")
    print(f"Hash SHA-256 registrado: {hash_texto}")

def verificar_documento(nome_doc, texto_fornecido):
    doc = colecao.find_one({"nome_documento": nome_doc})
    hash_atual = gerar_hash(texto_fornecido)
    if hash_atual == doc["hash_sha256"]:
        print(" Documento íntegro! Não houve alterações.")
    else:
        print(" Documento alterado ou diferente do original!")


while True:
        print("\n===================================")
        print("    Sistema de Documentos Cripto ")
        print("===================================")
        print("1 - Armazenar documento")
        print("2 - Verificar integridade")
        print("3 - Sair")
        print("===================================")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            nome = input("Nome do documento: ").strip()
            texto = input("Digite o texto confidencial: ").strip()
            armazenar_documento(nome, texto)
        elif opcao == "2":
            nome = input("Nome do documento a verificar: ").strip()
            texto = input("Digite o texto fornecido para verificação: ").strip()
            verificar_documento(nome, texto)
        elif opcao == "3":
            print(" Saindo do sistema de documentos...")
            break
        else:
            print(" Opção inválida! Tente novamente.")
