import json
from Crypto.Cipher import ChaCha20
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from Crypto.Random import get_random_bytes
from pickle import dumps,loads
from base64 import b64encode,b64decode

#FUNÇÃO: Cria o ciphertext através da cifra Chacha20
def buildCiphertext(msg,key,salt):
    
    #cria o nonce de 12 bytes de forma pseudo-aletória
    nonce = get_random_bytes(12)

    #cria a cifra Chacha20 utilizando a chave e o nonce
    cipher = ChaCha20.new(key=key, nonce=nonce)
    #cifra a mensagem
    ciphertext = cipher.encrypt(dumps(msg))

    #transforma em bytes a mensagem, nonce e o salt para geração da chave
    ct = b64encode(ciphertext).decode('utf-8')
    nc = b64encode(nonce).decode('utf-8')
    st = b64encode(salt).decode('utf-8')

    #mensagem cifrada - ciphertext
    pkg = {'ciphertext' : ct, 'nonce': nc, 'salt' : st}

    return pkg

#FUNÇÃO: Cria o plaintext através da cifra ChaCha20
def buildPlaintext(msg,key):

    #retira o valor nonce da mensagem cifrada
    nonce = b64decode(msg['nonce'])
    #retira a mensagem cifrada do ciphertext
    ciphertext = b64decode(msg['ciphertext'])

    #cria a decifra Chacha20 utilizando a chave e o non
    cipher = ChaCha20.new(key=key, nonce=nonce)
    #decifra mensagem
    plaintext = cipher.decrypt(ciphertext)

    return plaintext


#FUNÇÃO: Cifra ficheiro
def encrypt():

    #ficheiro a cifrar
    doc = input('Ficheiro a cifrar:  ')
    #chave a ser utilizada na cifra
    cipherKey = input('Chave:  ').encode('utf-8')
    #nome do ficheiro cifrado
    fileName = input('Ficheiro de output:  ')

    #retira a mensagem do ficheiro a cifrar
    f = open(doc, "r")
    msg = f.read()
    f.close()

    print("MENSAGEM")
    print(msg)

    #gera o salt a ser utilizado na geração da chave de 32 bytes 
    salt = get_random_bytes(16)
    #gera chave de 32 bytes utilizando o input do utilizador
    kdf = Scrypt(
                salt=salt,
                length=32,
                n=2**14,
                r=8,
                p=1,
                )
    key = kdf.derive(cipherKey)

    #cria ficheiro cifrado
    ciphertext = buildCiphertext(msg,key,salt)

    print("CIPHERTEXT - ** Armazenado no Ficheiro " + fileName + " **")
    print(json.dumps(ciphertext))

    #escreve a mensagem cifrada em bytes no ficheiro com nome igual à variavel filename
    output = open(fileName, "w")
    output.write(json.dumps(ciphertext))
    output.close()


#Função: Decifra um ficheiro      
def decrypt():

    #ficheiro a decifrar
    doc = input('Ficheiro a decifrar:  ')
    #chave a ser utilizada na decifra
    cipherKey = input('Chave:  ').encode('utf-8')
    #nome do ficheiro com a mensagem decifrada
    fileName = input('Ficheiro de output:  ')

    #retira bytes da mensagem do ficheiro a dcifrar
    f = open(doc, "rb")
    msg = f.read()

    print("MENSAGEM")
    print(msg)

    #gera a chave de 32 bytes utilizando o input do utilizador e o salt presente na mensagem cifrada
    ciphertext = json.loads(msg)
    salt = b64decode(ciphertext['salt'])
    kdf = Scrypt(
                salt=salt,
                length=32,
                n=2**14,
                r=8,
                p=1,
                )
    key = kdf.derive(cipherKey)

    #cria a mensagem decifrada
    plaintext = buildPlaintext(ciphertext,key)

    print("PLAINTEXT - ** Armazenado no Ficheiro " + fileName + " **")
    print(loads(plaintext))

    #escreve no ficheiro a mensagem cifrada
    output = open(fileName, "w")
    output.write(loads(plaintext))


# Opções do menu do utilizador
menu = {
    0: 'SAIR',
    1: 'Cifragem',
    2: 'Decifragem',}

# Menu para determinar se o utilizador pertende 
# cifrar ou  decifrar uma mensagem
while True:
    for key in menu.keys():
        print(key, '--', menu[key] )
    option = int(input('=>  ')) 
    if option == 1:
        encrypt()
    elif option == 2:
        decrypt()
    elif option == 0:
        exit()
    else:
        print('Opção Inválida.')
