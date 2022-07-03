
import sys, socket, os
import cryptography
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.x448 import X448PrivateKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from pickle import dumps, loads
from cryptography.hazmat.primitives.asymmetric.ed448 import Ed448PrivateKey
from cryptography.hazmat.primitives.serialization import *
from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class Client:

    def __init__(self):
        self.clientSocket = socket.socket()
        self.host = 'localhost'
        self.port = 8080
        self.x448PrivateKey = X448PrivateKey.generate()
        self.x448PublicKey = self.x448PrivateKey.public_key()
        self.Ed448PrivateKey = Ed448PrivateKey.generate()
        self.Ed448PublicKey = self.Ed448PrivateKey.public_key()
        

    def run(self):
        self.parseArgs()
       
    def connect(self):
        try:
            self.clientSocket.connect((self.host, self.port))

        except socket.error as e:
            print(str(e))

        self.Ed448KeyExchange()
        
        valid = self.x448KeyExchange()
        verified = False

        if valid:
            valid, verified = self.verifyKey()

        else:
            print("[CLIENT] Key exchange failed")

        return valid, verified

    def printUsage(self):
        print("Insert document to digital vault - Shared Secret: python3 vault-c.py -f filePath -s n m -d publicKey1 publicKey2 ...")
        print("                                 - One User     : python3 vault-c.py -d publicKey -f filePath")
        print("Withdraw document from digital vault - Shared Secret : python3 vault-c.py -w decryptKey -i index -h fileHash -f filePath")
        print("                                     - One User      : python3 vault-c.py -w decryptKey -h fileHash -f filePath")

    def parseArgs(self):
        if len(sys.argv) == 5 and sys.argv[1] == "-d" and sys.argv[3] == "-f":
            valid, verified = self.connect()
            if valid and verified:
                self.depositHandler(sys.argv[2], sys.argv[4])

        elif len(sys.argv) == 9 and sys.argv[1] == "-w" and sys.argv[3] == '-i' and sys.argv[5] == "-h" and sys.argv[7] == "-f":
            valid, verified = self.connect()
            if valid and verified:
                self.withdrawMultipleHandler(sys.argv[2], sys.argv[6], sys.argv[8], int(sys.argv[4]))

        elif len(sys.argv) == 7 and sys.argv[1] == "-w" and sys.argv[3] == "-h" and sys.argv[5] == "-f":
            valid, verified = self.connect()
            if valid and verified:
                self.withdrawHandler(sys.argv[2], sys.argv[4], sys.argv[6])

        elif len(sys.argv) >= 8 and sys.argv[6] == "-d" and sys.argv[1] == "-f" and sys.argv[3] == "-s":
            publicKeys = sys.argv[7:]

            if (len(publicKeys) != int(sys.argv[5])):
                print("Invalid number of public keys")
                sys.exit()
            valid, verified = self.connect()
            if valid and verified:
                self.depositMultipleHandler(publicKeys, sys.argv[2], sys.argv[4], sys.argv[5])
    
        else:
            self.printUsage()

    def sendFile(self, request, content, pubKey, n=None, m=None):

        chunks, chunk_size = len(content), 2000

        cnts = [content[i:i + chunk_size] for i in range(0, chunks, chunk_size)]
        size = len(cnts)

        for j in range(0, size):

            if request == 'DEPOSIT':

                if j != size - 1:
                    pkg = {'tag': 1, 'requestType': request, 'fileBytes': cnts[j], 'pubKey': pubKey}
                else:
                    pkg = {'tag': 0, 'requestType': request, 'fileBytes': cnts[j], 'pubKey': pubKey}
            else:
                if j != size - 1:
                    pkg = {'tag': 1, 'requestType': request, 'fileBytes': cnts[j], 'n': n, 'm': m}
                else:
                    pkg = {'tag': 0, 'requestType': request, 'fileBytes': cnts[j], 'n': n, 'm': m}

            pkgDump = dumps(pkg)

            self.send(pkgDump)


    def depositHandler(self, publicKeyPath, doc):

        print("**** Deposit Handler ****")
        
        if not os.path.isfile(publicKeyPath):
            print("[CLIENT] Key path " + str(publicKeyPath) + " does not exist.")

        else:
            f = open(doc, "r")
            content = f.read()

            publicKey = open(publicKeyPath,'rb').read()
            cnt = str.encode(content)

            if len(cnt) > 3000:
                self.sendFile("DEPOSIT", cnt, publicKey)
            else:
                pkg = {'tag': 0, 'requestType': "DEPOSIT", 'fileBytes': cnt, 'pubKey': publicKey}
                pkgDump = dumps(pkg)

                self.send(pkgDump)

            valid, resp = self.receive()

            if valid:

                print(" =» Hash File: ")
                print(resp['fileHash'])

                document = "encryptedKey.key"

                file_out = open(document, "wb")
                file_out.write(resp['key'])
                file_out.close()

                print(" =» Document's Key in file: ")
                print(document)
            else:
                print("[CLIENT] Message authentication failed")

        self.clientSocket.close()

    def depositMultipleHandler(self,publicKeysPaths,doc,n,m):

        print("**** Deposit Multiple Handler ****")
        exists = True

        for key in publicKeysPaths:
            if not os.path.isfile(key):
                print("[CLIENT] Key path "  + str(key) + " does not exist")
                exists = False

        if exists:
            f = open(doc, "r")
            content = f.read()
            cnt = str.encode(content)

            if len(cnt) > 3000:
                self.sendFile("DEPOSIT_MULTIPLE", cnt,None,n,m)
            else:
                info = {'tag': 0, 'requestType': "DEPOSIT_MULTIPLE", 'fileBytes': cnt, 'n': n, 'm': m}
                infoDump = dumps(info)
                self.send(infoDump)


            for publicKeyPath in publicKeysPaths:
                publicKey = open(publicKeyPath,'rb').read()

                pkg = {'pubKey': publicKey}
                pkgDump = dumps(pkg)
                self.send(pkgDump)

            valid, resp = self.receive()
            
            if valid:

                print(" =» Hash File: ")
                print(resp['fileHash'])
                print("\n")
                lst = list(resp.keys())
                lst.remove('fileHash')
                for key, pk in zip(lst, publicKeysPaths):
                    
                    docKey = pk.split(".pem")

                    document = "encryptedKey-"  + str(key) + ".key"

                    file_out = open(document, "wb")
                    file_out.write(resp[key])
                    file_out.close()
                    print(" =» Document's Key " + str(key) +  " in file: ")
                    print(document)
                    print("\n")
                
            else:
                print("[CLIENT] Message authentication failed")

        self.clientSocket.close()

    def receiveFile(self, path):
        cnt = b""

        while True:
            valid, resp = self.receive()

            if valid:

                if resp['tag'] == 1:
                    print(resp['decryptedFile'])
                    cnt = cnt + resp['decryptedFile']
                elif resp['tag'] == 0 and ('errorMessage' not in resp or resp['errorMessage'] == ""):

                    print(resp['decryptedFile'])
                    cnt = cnt + resp['decryptedFile']

                    f = open(path, 'wb')
                    f.write(cnt)
                    f.flush()
                    f.close()
                    break
                else:
                    print('*** Error ***')
                    print(resp['errorMessage'])
                    break
            else:
                print("[CLIENT] Message authentication failed")
                break

    def withdrawHandler(self, decryptKeyPath, fileHash, path):

        print("**** Withdraw Handler ****")
        if os.path.isfile(decryptKeyPath):

            decryptKey = open(decryptKeyPath,'rb').read()
            pkg = {'requestType': "WITHDRAW", 'fileHash': fileHash, 'decryptKey': decryptKey}

            self.send(dumps(pkg))
            self.receiveFile(path)
        
        else:
            print("[CLIENT] Decrypt key file does not exists")

        self.clientSocket.shutdown(socket.SHUT_RDWR)
        self.clientSocket.close()

    def withdrawMultipleHandler(self, decryptKeyPath, fileHash, path, idx):

        print("**** Withdraw Handler ****")

        if os.path.isfile(decryptKeyPath):
            decryptKey = open(decryptKeyPath,'rb').read()
            pkg = {'requestType': "WITHDRAW_MULTIPLE", 'fileHash': fileHash, 'decryptKey': decryptKey, 'index': idx}

            self.send(dumps(pkg))
            self.receiveFile(path)

        else:
            print("[CLIENT] Decrypt key file does not exists")

        self.clientSocket.shutdown(socket.SHUT_RDWR)
        self.clientSocket.close()

                                                                       
    def Ed448KeyExchange(self):
        
        print("\n------- Started Ed448KeyExchange -------")
        #Envia a sua public key
        self.clientSocket.send(self.serialize_key(self.Ed448PublicKey))
        print("[CLIENT] Sent my public key to Server")
        
        #Recebe a public key
        self.serverEd448PubKey = self.deserialize_key(self.clientSocket.recv(4096))
        print("[CLIENT] Received public key from Server")
        print("\n------- Finished Ed448KeyExchange -------")
 
    def x448KeyExchange(self):
        print("\n------- Started x448KeyExchange -------")
        #Envia a chave
        self.sendWithEd448Signing(self.serialize_key(self.x448PublicKey))
        #Recebe a chave
        print("[CLIENT] Sent the public key")
        valid, peerPublicKey = self.receiveWithEd448Verification()
        peerPublicKey = self.deserialize_key(peerPublicKey)
        print("[CLIENT] Received the public key")
        sharedSecret = self.x448PrivateKey.exchange(peerPublicKey)
        self.sharedKey = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=None).derive(sharedSecret)
        print("[CLIENT] Generated the shared key")
        
        print("\n------- Finished x448KeyExchange -------")
        return valid
        
    def verifyKey(self):
        print("\n------- Started Key verification -------")
        digest = hashes.Hash(hashes.SHA256())
        digest.update(self.sharedKey)
        hashedKey = digest.finalize()
        
        #Envia a chave
        self.sendWithEd448Signing(hashedKey)
        
        print("\n[CLIENT] Sent hashed shared Key")
        #Recebe a chave
        valid, peerSharedKey = self.receiveWithEd448Verification()
        
        print("\n[CLIENT] Received Server hashed Key")
        print("\n------- Finished Key verification -------")
        return valid, peerSharedKey == hashedKey

    def send(self, plaintext):
        nounce = os.urandom(12)

        encryptor = Cipher(algorithms.AES(self.sharedKey), modes.GCM(nounce)).encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        
        pkg = {"ciphertext": ciphertext, "nounce": nounce, "tag": encryptor.tag}

        self.clientSocket.send(dumps(pkg))

    def receive(self):
        pkg = self.clientSocket.recv(4096)
        pkg = loads(pkg)
        valid = True

        decryptor = Cipher(algorithms.AES(self.sharedKey), modes.GCM(pkg['nounce'], pkg['tag'])).decryptor()
        try:
            plaintext = decryptor.update(pkg['ciphertext']) + decryptor.finalize()
            response = loads(plaintext)

        except InvalidTag:
            valid = False
            response = None

        return valid, response
    
    def sendWithEd448Signing(self,  data):
        signature = self.Ed448PrivateKey.sign(data)
    
        pkg = {"signature": signature, "data": data}
    
        self.clientSocket.send(dumps(pkg))
        
    def receiveWithEd448Verification(self):
        valid = True
    
        pkg = self.clientSocket.recv(4096)
        pkg = loads(pkg)

        try:
            self.serverEd448PubKey.verify(pkg["signature"], pkg["data"])
            
        except InvalidSignature:
            valid = False

        return valid, pkg["data"]

    def serialize_key(self, key):
        return key.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo)

    def deserialize_key(self, key_bytes):
        return load_pem_public_key(key_bytes)


if __name__ == "__main__":
    c = Client()
    c.run()
