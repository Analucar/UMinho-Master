import sqlite3 as sl
import threading 
import datetime
import time

class VaultSystem:

    def __init__(self):
        self.registryFile = "vaultRegistry.db"
        self.fileFolder = "Vault" 
        self.requests = {}
        self.filesLock = threading.Lock()
        self.requestsLock = threading.Lock()
        self.requestsCondition = threading.Condition(lock = self.requestsLock)

        try:
            self.db = sl.connect(self.registryFile, check_same_thread=False)
            c = self.db.cursor()

            c.execute("CREATE TABLE IF NOT EXISTS FILES ("
                      "         HASH BLOB PRIMARY KEY NOT NULL, "
                      "         N INT, M INT, "
                      "         NOUNCE BLOB, TAG BLOB);")

        except sl.Error as e:
            print(e)

    def saveFile(self, fileHash, encryptedFile, nounce, tag):
        
        path = self.fileFolder + "/" + str(fileHash)
        with self.filesLock:
            f = open(path, 'wb')
            f.write(encryptedFile)
            f.close()
            c = self.db.cursor()
            c.execute("INSERT INTO FILES (HASH, N, M, NOUNCE, TAG) VALUES (?,?,?,?,?)",
                                        (fileHash, 'NULL', 'NULL', nounce, tag));
            self.db.commit()

    def saveFileMultiple(self, fileHash, encryptedFile, n, m, nounce, tag):
        
        path = self.fileFolder + "/" + str(fileHash)
        with self.filesLock:
            f = open(path, 'wb')
            f.write(encryptedFile)
            f.close()
            c = self.db.cursor()
            c.execute("INSERT INTO FILES (HASH, N, M, NOUNCE, TAG) VALUES (?,?,?,?,?)",
                                        (fileHash, n, m, nounce, tag));
            self.db.commit()

    def exists(self, fileHash):
        data = []

        with self.filesLock:
            c = self.db.cursor()
            c.execute(f"SELECT * FROM FILES WHERE HASH = '{fileHash}'")
            data = c.fetchall()

        return data != []

    def needsMultiple(self, fileHash):
        
        with self.filesLock:
            c = self.db.cursor()
            c.execute(f"SELECT N FROM FILES WHERE HASH = '{fileHash}'")
            data = c.fetchall()
        
        return data[0] != 'NULL'

    def getParams(self, fileHash):
        
        with self.filesLock:
            c = self.db.cursor()
            c.execute(f"SELECT * FROM FILES WHERE HASH = '{fileHash}'")
            data = c.fetchall()
        return data

    def fetchFile(self, fileHash):
        path = self.fileFolder + "/" + str(fileHash)
        
        with self.filesLock:
            with open(path, 'rb') as f:
                return f.read()

    def fetchFileWithMultiple(self, fileHash, key, index):
        keys = []
        noTimeout = True
        encryptedFile = b''
        exists = False

        with self.requestsCondition:

            if fileHash not in self.requests:
                self.requests[fileHash] = {'counter': 0, 'keys': [(index, key)]}
            
            else:
                l = list(filter(lambda x: x[0] == index, self.requests[fileHash]['keys']))
                exists = l != []

                if not exists:
                    self.requests[fileHash]['keys'].append((index, key))

            if not exists:

                data = self.getParams(fileHash)
                print(data)
            
                while len(self.requests[fileHash]['keys']) < data[0][1] and noTimeout:
                     noTimeout = self.requestsCondition.wait(60)  
                 
                if noTimeout or len(self.requests[fileHash]['keys']) >= data[0][1] :
                    
                    if self.requests[fileHash]['counter'] == 0:
                        time.sleep(10)

                    encryptedFile = self.fetchFile(fileHash)

                    keys = self.requests[fileHash]['keys']
                    self.requests[fileHash]['counter'] += 1

                    if fileHash in self.requests and self.requests[fileHash]['counter'] == len(self.requests[fileHash]['keys']):
                        self.requests.pop(fileHash)

                    else:
                        self.requestsCondition.notify_all()

                else:
                    self.requests[fileHash]['keys'].remove((index, key))

                    if self.requests[fileHash]['keys'] == []:
                        self.requests.pop(fileHash)

        return encryptedFile, keys, noTimeout, exists

