from cryptography.fernet import Fernet
from pymongo import MongoClient
import hashlib

client = MongoClient("mongodb://localhost:27017")
db = client["auth_demo"]
users = db["users"]

fernet = Fernet(Fernet.generate_key())

def _gera_salt():
    return Fernet.generate_key().decode()

def _derive(password, salt, iterations=150000):
    return hashlib.pbkdf2_hmac("sha512", password.encode(), salt.encode(), iterations)

def _comparar(a, b):
    if len(a) != len(b):
        return False
    r = 0
    for x, y in zip(a, b):
        r |= ord(x) ^ ord(y)
    return r == 0

def create_user(username, password):
    if users.find_one({"username": username}):
        print("usuário já existe")
        return
    salt = _gera_salt()
    iterations = 150000
    dk = _derive(password, salt, iterations)
    users.insert_one({
        "username": username,
        "salt": salt,
        "iterations": iterations,
        "derived_key_hex": dk.hex()
    })
    print("usuário criado")

def authenticate_user(username, password):
    doc = users.find_one({"username": username})
    if not doc:
        print("usuário não encontrado")
        return False
    salt = doc["salt"]
    iterations = int(doc["iterations"])
    stored_hex = doc["derived_key_hex"]
    dk = _derive(password, salt, iterations)
    if _comparar(dk.hex(), stored_hex):
        print("autenticação bem-sucedida")
        return True
    else:
        print("senha incorreta")
        return False

def change_password(username, old_password, new_password):
    if not authenticate_user(username, old_password):
        print("não autorizado")
        return
    salt = _gera_salt()
    iterations = 150000
    dk = _derive(new_password, salt, iterations)
    users.update_one({"username": username}, {"$set": {"salt": salt, "iterations": iterations, "derived_key_hex": dk.hex()}})
    print("senha alterada")


while True:
        print("1 criar | 2 autenticar | 3 trocar senha | 4 sair")
        op = input("> ").strip()
        if op == "1":
            u = input("usuario: ").strip()
            p = input("senha: ").strip()
            create_user(u, p)
        elif op == "2":
            u = input("usuario: ").strip()
            p = input("senha: ").strip()
            authenticate_user(u, p)
        elif op == "3":
            u = input("usuario: ").strip()
            old = input("senha atual: ").strip()
            new = input("nova senha: ").strip()
            change_password(u, old, new)
        elif op == "4":
            break
        else:
            print("opção inválida")
