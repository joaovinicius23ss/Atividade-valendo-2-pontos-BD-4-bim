from cryptography.fernet import Fernet
from pymongo import MongoClient

key = Fernet.generate_key()
fernet = Fernet(key)

nome = input("Digite o nome qaue deseja criptografar e enviar para o banco: ")
senha = input("Digite a senha que deseja criptografar e enviar para o banco: ")


senha_criptografada = fernet.encrypt(senha.encode())
nome_criptografado = fernet.encrypt(nome.encode())

print(f"Senha criptografada: {senha_criptografada}")
print(f"Nome criptografado: {nome_criptografado}")

# Conexão com o MongoDB
client = MongoClient("mongodb+srv://root:123@cluster0.sqkox39.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["test"]
collection = db["Alunos"]

documento = {
    "nome_criptografado": nome_criptografado, "senha_criptografada": senha_criptografada }
collection.insert_one(documento)
print("Nome e senha criptografados inseridos no banco de dados.")


resultado = collection.find_one({"nome_criptografado": nome_criptografado})


nome_recuperado_criptografado = resultado["nome_criptografado"]
senha_recuperada_criptografada = resultado["senha_criptografada"]

nome_descriptografado = fernet.decrypt(nome_recuperado_criptografado).decode()
senha_descriptografada = fernet.decrypt(senha_recuperada_criptografada).decode()

print(f"Nome descriptografado: {nome_descriptografado}")
print(f"Senha descriptografada: {senha_descriptografada}")


client.close()
