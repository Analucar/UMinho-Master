import json, getpass
from Crypto.Cipher import ChaCha20, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from pickle import dumps,loads
from base64 import b64encode,b64decode

#FUNÇÃO: Cria o ciphertext através da cifra Chacha20 e cifra a chave da sessão com o RSA
def buildCiphertext(msg,sessionKey,rsa):
    
    #cria o nonce de 12 bytes de forma pseudo-aletória
    nonce = get_random_bytes(12)

    #cria a cifra Chacha20 utilizando a chave da sessão e o nonce
    cipher = ChaCha20.new(key=sessionKey, nonce=nonce)
    #cifra a mensagem
    ciphertext = cipher.encrypt(dumps(msg))

    #transforma em bytes a mensagem, nonce e o salt para geração da chave
    ct = b64encode(ciphertext).decode('utf-8')
    nc = b64encode(nonce).decode('utf-8')

    #mensagem cifrada - ciphertext
    pkg = {'ciphertext' : ct, 'nonce': nc}

    #cifrar a chave da sessão utilizando a chave pública
    cipher_rsa = PKCS1_OAEP.new(rsa)
    k = cipher_rsa.encrypt(sessionKey)

    return pkg, k

#FUNÇÃO: Cria o plaintext através da cifra ChaCha20
def buildPlaintext(msg,msgKey,privateKey):

    #Decifra a chabe da sessão utilizando a chave privada
    cipher_rsa = PKCS1_OAEP.new(privateKey)
    sessionKey = cipher_rsa.decrypt(msgKey)

    #retira o valor nonce da mensagem cifrada
    nonce = b64decode(msg['nonce'])
    #retira a mensagem cifrada do ciphertext
    ciphertext = b64decode(msg['ciphertext'])

    #cria a decifra Chacha20 utilizando a chave K e o non
    cipher = ChaCha20.new(key=sessionKey, nonce=nonce)
    #decifra mensagem
    plaintext = cipher.decrypt(ciphertext)

    return plaintext


#FUNÇÃO: Cifra ficheiro
def encrypt():

    #ficheiro a cifrar
    doc = input('Ficheiro a cifrar:  ')
    #nome do ficheiro cifrado
    fileName = input('Ficheiro com a mensagem cifrada:  ')
    #nome do ficheiro cifrado com a chave da sessão
    fileNameKey = input('Ficheiro com a chave cifrada:  ')

    #retira a mensagem do ficheiro a cifrar
    f = open(doc, "r")
    msg = f.read()
    f.close()

    print("MENSAGEM")
    print(msg)

    #cria a chave de sessão
    K = get_random_bytes(32)

    print("Deseja gerar novas chaves? [Y/N] ")
    option = input('=>  ').upper()

    if option == 'Y':

        #gera o par de chaves utilizando RSA
        rsaKey = RSA.generate(2048)

        #obrigatoriedade de armazenar as chaves em ficheiros
        publicFile = input('Ficheiro onde armazenar ' + 
                                'a chave pública (***.pem):  ')
        privateFile = input('Ficheiro onde armazenar ' + 
                                'a chave privada (***.pem):  ')

        #Password de proteção da chave privada
        password = getpass.getpass('Password de proteção da ' +
                                     'chave privada:  ').encode('utf-8')

        #Exporta a chave pública e privada para um ficheiro
        privateKey = rsaKey.export_key(format='PEM',passphrase=password)
        publicKey = rsaKey.publickey().export_key(format='PEM')

        #Armazena a chave privada no ficheiro
        private_out = open(privateFile, "wb")
        private_out.write(privateKey)
        private_out.close()

        #Armazena a chave publica no ficheiro
        public_out = open(publicFile, "wb")
        public_out.write(publicKey)
        public_out.close()

    else:

        #Le a chave publica do ficheiro fornecido
        keyEncrypted = input('Ficheiro da chave pública:  ')
        rsaKey = RSA.import_key(open(keyEncrypted).read())

    #cria a mensagem e a chave cifrada
    ciphertext, cipherKey = buildCiphertext(msg,K,rsaKey)

    print("CIPHERTEXT - ** Armazenado no Ficheiro " + fileName + " **")
    print(json.dumps(ciphertext))

    #escreve a mensagem cifrada em bytes no ficheiro com nome igual à variavel filename
    output = open(fileName, "w")
    output.write(json.dumps(ciphertext))
    output.close()

    print("CIPHERKEY - ** Armazenado no Ficheiro " + fileNameKey + " **")
    print(cipherKey)

    #escreve a chave cifrada em bytes no ficheiro com nome igual à variavel filenameKey
    outputKey = open(fileNameKey, "wb")
    outputKey.write(cipherKey)
    outputKey.close()

#Função: Decifra um ficheiro      
def decrypt():

    #ficheiro a decifrar com a mensagem
    doc = input('Ficheiro com a mensagem a decifrar:  ')
    #ficheiro a decifrar com a chave decifrada
    docKey = input('Ficheiro com a chave a decifrar:  ')
    #nome do ficheiro com a mensagem decifrada
    fileName = input('Ficheiro de output com a mensagem cifrada:  ')

    #retira bytes da mensagem do ficheiro a decifrar
    f = open(doc, "rb")
    msg = f.read()
    ciphertext = json.loads(msg)

    print("MENSAGEM")
    print(msg)

    #retira bytes da chave da sessão a decifrar
    f = open(docKey, "rb")
    msgKey = f.read()

    #Ficheiro que contém a chave privada
    privateFile = input('Ficheiro onde ler a ' + 
                            'chave privada (***.pem):  ')
    #Password de proteção da chave privada
    password = getpass.getpass('Password de proteção da ' + 
                                'chave privada:  ').encode('utf-8')
    #importa a chave privada presente no ficheiro fornecido
    rsaKey = RSA.import_key(open(privateFile).read(), passphrase=password)

    #cria a mensagem decifrada
    plaintext = buildPlaintext(ciphertext,msgKey,rsaKey)

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