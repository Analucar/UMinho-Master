import sys, re, datetime

def getAmount():
    amount = input("Introduza o montante a pagar: ")
    res = re.match("[0-9]+\.[0-9]{2}", amount)
    
    if not res:
        print("Valor do montante não é válido")
        sys.exit()
    
    try:
        amount = float(amount)

    except(ValueError, TypeError):
        print("Valor do montante não é válido")
        sys.exit()

    return amount

def getBirthdate():

    birthdate = input("Introduza a data de nascimento (YYYY/MM/DD): ")
    res = re.match("[0-9]{4}\/[0-9]{2}\/[0-9]{2}", birthdate)

    if not res:
        print("Data de nascimento inválida")
        sys.exit()

    else:
        res = birthdate.split("/")
        year = int(res[0])
        month = int(res[1])
        day = int(res[2])
                
        try:
            birthdate = datetime.date(year = year, month = month, day = day)
            return birthdate

        except(ValueError, TypeError):
            print("Data de nascimento inválida!")
            sys.exit()

    return birthdate
  

def getName():
    name = input("Introduza o seu nome: ")

    res = re.match("[^a-zA-Z]", name)

    if res:
        print("Nome inválido")
        sys.exit()

    return name


def validNIF(numero):

    soma = sum([int(dig) * (9 - pos) for pos, dig in enumerate(numero)])
    resto = soma % 11
    if (numero[-1] == '0' and resto == 1):
        resto = (soma + 10) % 11

    return resto == 0

def getNIF():

    nif = input("Introduza o seu NIF: ")

    res = re.match("^[0-9]{9}$", nif).group(0)
    
    if res == None:
        print("NIF inválido")
        sys.exit()
    
    if not validNIF(res):
        print("NIF inválido")
        sys.exit()

    return nif

def getNIC():

    nic = input("Introduza o seu NIC: ")

    res = re.match("^[0-9]{8}$", nic)
    
    if res == None:
        print("NIC inválido")
        sys.exit()
    
    return nic

def getCCNum():

    ccnum = input("Introduza o seu número de cartão de crédito: ")

    res = re.match("^[0-9]{4}\s[0-9]{4}\s[0-9]{4}\s[0-9]{4}$", ccnum)
    
    if res == None:
        print("Número de cartão de crédito inválido")
        sys.exit()
    
    return ccnum

def getExpiryDate():

    expirydate = input("Introduza a data de validade (MM/YY): ")
    res = re.match("[0-9]{2}\/[0-9]{2}", expirydate)

    if res == None:
        print("Data de validade inválida")
        sys.exit()

    else:
        res = expirydate.split("/")
        month = int(res[0])

        if month >= 1 and month <= 12:
            return expirydate

        else:
            print("Data de validade inválida!")
            sys.exit()

def getCVC():

    cvc = input("Introduza o seu CVC/CVV: ")

    res = re.match("^[0-9]{3}$", cvc)
    
    if res == None:
        print("NIC inválido")
        sys.exit()
    
    return cvc
        
def getCCInfo():
    
    ccnum = getCCNum()

    expiryDate = getExpiryDate()

    cvc = getCVC()

    return ccnum, expiryDate, cvc

amount = getAmount()

birthdate = getBirthdate()

name = getName()

nif = getNIF()

nic = getNIC()

ccnum, expirationDate, cvc = getCCInfo()

print("Todos os inputs são válidos: ")
print("Valor a pagar: " + str(amount))
print("Data de nascimento: " + str(birthdate))
print("Nome: " + str(name))
print("NIF: " + str(nif))
print("NIC: " + str(nic))
print("Número de cartão de crédito: " + str(ccnum))
print("Validade: " + str(expirationDate))
print("CVC/CVV: " + str(cvc))
