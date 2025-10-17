import hashlib
import time
from pymongo import MongoClient

client = MongoClient("mongodb+srv://root:123@cluster0.sqkox39.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['lista']
colecao = db['lista']

def gerar_hash(bloco):
    bloco_string = f"{bloco['index']}{bloco['timestamp']}{bloco['data']}{bloco['previous_hash']}"
    hash_obj = hashlib.sha256(bloco_string.encode())
    return hash_obj.hexdigest()

def criar_bloco_genesis():

    if colecao.count_documents({}) == 0:
        bloco = {'index': 0,'timestamp': str(time.time()),'data': "Bloco Genesis", 'previous_hash': "0"}
        bloco['hash'] = gerar_hash(bloco)
        colecao.insert_one(bloco)
        print(" Bloco Genesis criado!")

def adicionar_bloco(data):
    ultimo_bloco = list(colecao.find().sort("index", -1).limit(1))[0]
    bloco = {'index': ultimo_bloco['index'] + 1,'timestamp': str(time.time()),'data': data,'previous_hash': ultimo_bloco['hash']}
    bloco['hash'] = gerar_hash(bloco)
    colecao.insert_one(bloco)
    print(f" Bloco {bloco['index']} adicionado!")

def verificar_blockchain():

    blocos = list(colecao.find().sort("index", 1))
    valido = True

    for i in range(1, len(blocos)):
        atual = blocos[i]
        anterior = blocos[i-1]

        if atual['previous_hash'] != anterior['hash']:
            print(f" Bloco {atual['index']} está corrompido!")
            valido = False
            break

        if gerar_hash(atual) != atual['hash']:
            print(f" Hash do bloco {atual['index']} não confere!")
            valido = False
            break

    if valido:
        print(" Blockchain íntegro. Todos os blocos conferem!")


while True:
        print("\n===================================")
        print("         Blockchain Simples     ")
        print("===================================")
        print("1 - Criar bloco Genesis")
        print("2 - Adicionar novo bloco")
        print("3 - Verificar integridade")
        print("4 - Mostrar blockchain")
        print("5 - Sair")
        print("===================================")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            criar_bloco_genesis()

        elif opcao == "2":
            dados = input("Digite os dados do bloco: ").strip()
            adicionar_bloco(dados)

        elif opcao == "3":
            verificar_blockchain()

        elif opcao == "4":
            blocos = colecao.find().sort("index", 1)
            print("\n Blockchain completo:")
            for bloco in blocos:
                print(f"Index: {bloco['index']}, Data: {bloco['data']}, Hash: {bloco['hash']}, Previous: {bloco['previous_hash']}")

        elif opcao == "5":
            print(" Saindo do blockchain...")
            break

        else:
            print(" Opção inválida!")
