from cryptography.fernet import Fernet
from pymongo import MongoClient
import hashlib

client = MongoClient("mongodb+srv://root:123@cluster0.sqkox39.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["lista"]
colecao = db["certificados"]

fernet = Fernet(Fernet.generate_key())

def gerar_hash(texto):
    return hashlib.sha512(texto.encode()).hexdigest()

def adicionar_certificado(nome, conteudo):
    conteudo_bytes = conteudo.encode()
    conteudo_criptografado = fernet.encrypt(conteudo_bytes)
    hash_cert = gerar_hash(conteudo)
    colecao.insert_one({"nome": nome,"certificado_criptografado": conteudo_criptografado, "hash": hash_cert})
    print(f"Certificado de '{nome}' armazenado com segurança.")

def listar_certificados():
    certificados = list(colecao.find())
    for idx, c in enumerate(certificados, start=1):
        print(f"{idx} | Nome: {c['nome']} | Hash: {c['hash']}")

def verificar_certificado(idx):
    certificados = list(colecao.find())
    c = certificados[idx - 1]
    conteudo_decrypt = fernet.decrypt(c["certificado_criptografado"]).decode()
    hash_atual = gerar_hash(conteudo_decrypt)
    if hash_atual == c["hash"]:
        print(f" Certificado de '{c['nome']}' é autêntico e íntegro.")
    else:
        print(f" Certificado de '{c['nome']}' foi alterado ou corrompido.")


while True:
        print("\n========================================")
        print("      Repositório de Certificados       ")
        print("========================================")
        print("1 - Adicionar certificado")
        print("2 - Listar certificados")
        print("3 - Verificar certificado")
        print("4 - Sair")
        print("========================================")

        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            nome = input("Nome do certificado: ").strip()
            conteudo = input("Conteúdo do certificado: ").strip()
            adicionar_certificado(nome, conteudo)
        elif opcao == "2":
            listar_certificados()
        elif opcao == "3":
            listar_certificados()
            try:
                idx = int(input("Digite o índice do certificado para verificar: ").strip())
            except ValueError:
                print("Índice inválido.")
                continue
            verificar_certificado(idx)
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")
