import timeit
from Crypto.Hash import SHA256

#Hash hexadecimal da password que queremos decobrir
hashPassword = "96cae35ce8a9b0244178bf28e4966c2ce1b8385723a96a6b838858cdd6ca0a1e"

#Armazena na lista top o top 200 das password mais usadas
with open("top200.txt") as file:
    top = [line.rstrip() for line in file]

#Iniciar timer para medir o tempo de descoberta da password
starttime = timeit.default_timer()

#Ciclo que percorrer o top 200 para determinar a password
for password in top:
    
    #Determina a hash hexadecimal de uma password
    h = SHA256.new()
    h.update(password.encode('utf-8'))
    hashPass = h.hexdigest()

    #Verifica se a hash calculada é igual à hash que queremos descobrir
    if hashPassword == hashPass:

        #Se for igual, então encontramos a password!
        print("PASSWORD FOUND!")
        print("Password: " + password)
        print("Time: ", timeit.default_timer() - starttime)
        break
