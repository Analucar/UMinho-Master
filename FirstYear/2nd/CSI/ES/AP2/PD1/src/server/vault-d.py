import threading, socket, os
from vaultSystem import VaultSystem
from pickle import dumps, loads
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Protocol.SecretSharing import Shamir
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives.asymmetric.x448 import X448PrivateKey
from cryptography.hazmat.primitives.asymmetric.ed448 import Ed448PrivateKey
from cryptography.hazmat.primitives.serialization import *

class ClientWorker:
    DH_KEY_SIZE = 2048
    GENERATOR = 2

    def __init__(self, connection, sys, x448Priv, x448Pub, ed448Priv, ed448Pub):
        self.connection = connection
        self.system = sys
        self.x448PrivateKey = x448Priv
        self.x448PublicKey = x448Pub
        self.Ed448PrivateKey = ed448Priv
        self.Ed448PublicKey = ed448Pub
        self.content = b""

    #Gera um chave para cifrar o ficheiro
    def keygen(self):

        key = os.urandom(16)
        return key
    
    #Gera um hash sobre o ficheiro
    def genHash(self, encryptedFile):

        h = SHA256.new()
        h.update(encryptedFile)
        return h.hexdigest()

    def shareSecret(self, n, m, encryptKey):
        
        secretKeys = Shamir.split(int(n), int(m), encryptKey)
        
        return secretKeys

    def encryptFile(self, plaintextFile, encryptKey):

        cipher = AES.new(encryptKey, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(plaintextFile)

        return ciphertext, cipher.nonce, tag

    def decryptFile(self, encryptedFile, decryptKey, nounce, tag):

        cipher = AES.new(decryptKey, AES.MODE_EAX, nonce=nounce)
        return cipher.decrypt(encryptedFile)

    def encryptSecretKeys(self, secretKeys, publicKeys):
        encryptKeys = []
        c = 0
        for key, publicKey in zip(secretKeys, publicKeys):
            pubKey = RSA.import_key(publicKey)
            cipherRsa = PKCS1_OAEP.new(pubKey)

            encryptKey = cipherRsa.encrypt(key[1])
            encryptKeys.append((key[0], encryptKey))
            c = c + 1
        
        return encryptKeys

    #Cifra a chave que foi usada para cifrar o ficheiro com a chave pública 
    def encryptKey(self, key, publicKey):
        pubKey = RSA.import_key(publicKey)
        cipherRsa = PKCS1_OAEP.new(pubKey)
        encryptKey = cipherRsa.encrypt(key)

        return encryptKey
    
    #Handler para o deposito de um ficheiro
    def depositHandler(self, plaintextFile, publicKey):
        
        encryptKey = self.keygen()

        encryptedFile, nounce, tag = self.encryptFile(plaintextFile, encryptKey)

        fileHash = self.genHash(encryptedFile)

        self.system.saveFile(fileHash, encryptedFile, nounce, tag)

        encryptedKey = self.encryptKey(encryptKey, publicKey)

        return fileHash, encryptedKey    
    
    #Handler para o deposito de um ficheiro 
    #Mas com a opcao de ser necessario varias pessoas para decifrar
    def depositMultipleHandler(self, plaintextFile, publicKeys, n, m):

        encryptKey = self.keygen()
        
        encryptedFile, nounce, tag = self.encryptFile(plaintextFile, encryptKey)

        fileHash = self.genHash(encryptedFile)
        self.system.saveFileMultiple(fileHash, encryptedFile, n, m, nounce, tag)
        
        secretKeys = self.shareSecret(n, m, encryptKey)
        encryptedKeys = self.encryptSecretKeys(secretKeys, publicKeys)

        return fileHash, encryptedKeys
    
    #Handler para obter um ficheiro
    def withdrawHandler(self, fileHash, decryptKey):
        errorMessage = ""
        decryptedFile = b''

        if not self.system.exists(fileHash):
            errorMessage = "FILE NOT FOUND"
        else:
            encryptedFile = self.system.fetchFile(fileHash)
            params = self.system.getParams(fileHash)

            if params[0][1] == 'NULL':
                decryptedFile = self.decryptFile(encryptedFile, decryptKey, params[0][3], params[0][4])
        
            else:
                errorMessage = "NO INDEX PROVIDED"

        return decryptedFile, errorMessage
 
    def withdrawMultipleHandler(self, fileHash, decryptKey, index):
        errorMessage = ""
        decryptedFile = b''

        if not self.system.exists(fileHash):
            errorMessage = "FILE NOT FOUND"

        else:

            params = self.system.getParams(fileHash)

            if params[0][1] != 'NULL':

                if index <= params[0][2]:
                    encryptedFile, keys, res, exists = self.system.fetchFileWithMultiple(fileHash, decryptKey, index)

                    if res and not exists:
                        decryptKey = Shamir.combine(keys)
                        decryptedFile = self.decryptFile(encryptedFile, decryptKey, params[0][3], params[0][4])

                    elif exists:
                        errorMessage = "INDEX ALREADY EXISTS"

                    elif res:
                        errorMessage = "TIME OUT"

                else:
                    errorMessage = "INDEX OUT OF BOUNDS"

            else:
                encryptedFile = self.system.fetchFile(fileHash)
                decryptedFile = self.decryptFile(encryptedFile, decryptKey, params[0][3], params[0][4])

        return decryptedFile, errorMessage

    def serialize_key(self, key):
        return key.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo)

    def deserialize_key(self, key_bytes):
        return load_pem_public_key(key_bytes)

    def ed448KeyExchange(self):
        print("\n------- Started Ed448KeyExchange -------")
        print("[SERVER] Received Ed448Key from CLIENT")
        
        #Recebe a public key
        self.clientEd448PubKey = self.deserialize_key(self.connection.recv(4096))
        
        #Envia a sua public key
        self.connection.send(self.serialize_key(self.Ed448PublicKey))
        
        print("[SERVER] Sent Ed448Key to the CLIENT")
        print("------- Finished Ed448KeyExchange -------\n")
 
    def x448KeyExchange(self):
        print("\n------- Started x448KeyExchange -------")
        print("[SERVER] Received x448Key from CLIENT")
        
        #Recebe a chave
        valid, peerPublicKey = self.receiveWithEd448Verification()
        peerPublicKey = self.deserialize_key(peerPublicKey)
        print("[SERVER] Sent x448Key to the CLIENT")
        
        #Envia a chave
        self.sendWithEd448Signing(self.serialize_key(self.x448PublicKey))
        sharedSecret = self.x448PrivateKey.exchange(peerPublicKey)
        self.sharedKey = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=None).derive(sharedSecret)
        
        print("[SERVER] Generated the shared key")
        print("------- Finished x448KeyExchange -------\n")
        return valid
       
    def verifyKey(self):
        print("\n------- Started KeyVerification -------")
        #Recebe a chave
        valid, peerSharedKey = self.receiveWithEd448Verification()
        print("[SERVER] Sent shared key to the CLIENT")
        #Envia a chave
        
        digest = hashes.Hash(hashes.SHA256())
        digest.update(self.sharedKey)
        hashedKey = digest.finalize()
        
        self.sendWithEd448Signing(hashedKey)
        print("[SERVER] received shared key from the CLIENT")
        print("------- Finished KeyVerification -------\n")
        
        return valid, peerSharedKey == hashedKey

    def send(self, plaintext):

        nounce = os.urandom(12)

        encryptor = Cipher(algorithms.AES(self.sharedKey), modes.GCM(nounce)).encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        
        pkg = {"ciphertext": ciphertext, "nounce": nounce, "tag": encryptor.tag}
        self.connection.send(dumps(pkg))
        
    def receive(self):

        pkg = self.connection.recv(4096)

        if not pkg:
            return False, None
        pkg = loads(pkg)
        valid = True

        decryptor = Cipher(algorithms.AES(self.sharedKey), modes.GCM(pkg['nounce'], pkg['tag'])).decryptor()
        try:
            plaintext = decryptor.update(pkg['ciphertext']) + decryptor.finalize() 

        except InvalidTag:
            valid = False
            plaintext = None

        return valid, plaintext
    
    def sendWithEd448Signing(self,  data):
        signature = self.Ed448PrivateKey.sign(data)
    
        pkg = {"signature": signature, "data": data}
    
        self.connection.send(dumps(pkg))
        
    def receiveWithEd448Verification(self):
        valid = True
    
        pkg = self.connection.recv(4096)
        pkg = loads(pkg)

        try:
            self.clientEd448PubKey.verify(pkg["signature"], pkg["data"])
            
        except InvalidSignature:
            valid = False

        return valid, pkg["data"]
    
    def processMessage(self, message):
        msg = loads(message)

        # Retirar o tipo da mensagem
        # dependendo do tipo passa para o handler correto
        if msg['requestType'] == 'DEPOSIT':

            if msg['tag'] == 1:
                print('[SERVER] Received deposit request')
                self.content = self.content + msg['fileBytes']
            else:
                print('[SERVER] Received deposit request')
                self.content = self.content + msg['fileBytes']
                fileHash, encryptedKey = self.depositHandler(self.content, msg['pubKey'])

                pkg = {'fileHash': fileHash, 'key': encryptedKey}
                pkgDumps = dumps(pkg)

                self.send(pkgDumps)

        elif msg['requestType'] == 'DEPOSIT_MULTIPLE':
            if msg['tag'] == 1:
                print('[SERVER] Received deposit request')
                self.content = self.content + msg['fileBytes']
            else:
                print('[SERVER] Received deposit request')
                self.content = self.content + msg['fileBytes']

                receivedKeysC = 0
                pubKeys = []
                while receivedKeysC != int(msg['m']):
                    
                    valid, newMsg = self.receive()
                    newMesg = loads(newMsg)
                    if valid:
                        receivedKeysC = receivedKeysC + 1
                        pubKeys.append(newMesg['pubKey'])

                fileHash, encryptedKeys = self.depositMultipleHandler(self.content, pubKeys, msg['n'],msg['m'])
                
                pkg = {'fileHash': fileHash}
                for key in encryptedKeys:
                    pkg[key[0]] = key[1]
                
                pkgDumps = dumps(pkg)
                
                self.send(pkgDumps)


        elif msg['requestType'] == 'WITHDRAW':
            print('[SERVER] Received withdraw request for file: ' + str(msg['fileHash']))
            decryptedFile, errorMessage = self.withdrawHandler(msg['fileHash'], msg['decryptKey'])


            if len(decryptedFile) > 3000:
                self.sendFile(decryptedFile)

            else:
                pkg = {'tag': 0, 'decryptedFile': decryptedFile, 'errorMessage': errorMessage}
                pkgDump = dumps(pkg)
                self.send(pkgDump)
        
        elif msg['requestType'] == 'WITHDRAW_MULTIPLE':
            print('[SERVER] Received withdraw request for file: ' + str(msg['fileHash']))
            decryptedFile, errorMessage = self.withdrawMultipleHandler(msg['fileHash'], msg['decryptKey'], msg['index'])

            if len(decryptedFile) > 3000:
                self.sendFile(decryptedFile)

            else:
                pkg = {'tag': 0, 'decryptedFile': decryptedFile, 'errorMessage' : errorMessage}
                pkgDump = dumps(pkg)
                self.send(pkgDump)

    def sendFile(self, content):

        chunks, chunk_size = len(content), 2000

        cnts = [content[i:i + chunk_size] for i in range(0, chunks, chunk_size)]
        size = len(cnts)

        for j in range(0, size):

            if j != size - 1:
                pkg = {'tag': 1, 'decryptedFile': cnts[j]}
            else:
                pkg = {'tag': 0, 'decryptedFile': cnts[j]}

            pkgDump = dumps(pkg)

            self.send(pkgDump)


    def run(self):
        
        self.ed448KeyExchange()
        valid = self.x448KeyExchange()

        if valid:   
            valid, sameKey = self.verifyKey()

            if valid and sameKey:
                while self.connection:
                    valid, message = self.receive()

                    if not message:
                        break

                    if valid:
                        self.processMessage(message)    

                    else:
                        print("[SERVER] Message authentication failed")

            else:
                print("[SERVER] Key verification failed")
        else:
            print("[SERVER] Invalid key exchange")
        
class ClientListener:

    def __init__(self, sys):
        self.port = 8080
        self.host = "localhost"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.system = sys
        self.x448PrivateKey = X448PrivateKey.generate()
        self.x448PublicKey = self.x448PrivateKey.public_key()
        self.Ed448PrivateKey = Ed448PrivateKey.generate()
        self.Ed448PublicKey = self.Ed448PrivateKey.public_key()

    def run(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)

        while True:
            connection, address = self.socket.accept()
            worker = ClientWorker(connection, self.system, self.x448PrivateKey, self.x448PublicKey, self.Ed448PrivateKey, self.Ed448PublicKey)
            threading.Thread(target=worker.run).start()

if __name__ == "__main__":
    sys = VaultSystem()
    cl = ClientListener(sys)
    cl.run()
