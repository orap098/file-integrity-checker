import hashlib
import os


hash = hashlib.sha256()
arquivo = input("Escreva o nome do arquivo: ")
#path = input("caminho: ")

with open(arquivo,  "rb") as f:
    for byte in iter(lambda: f.read(4096), b""):
        hash.update(byte)
    
print(hash.hexdigest())


