import json
from phe import paillier
import re

def store(pub_key, filename, saveFile):

    # abertura do ficheiro que contem os dados
    testfile = open(filename, "r")
    
    # dicionario onde serão armazenados os dados
    dictionary =  {}

    for linha in testfile:
        
        # obter o NIC de cada cliente
        nic = re.search(r'([A-Z0-9]+)', linha)
        nic = nic.group(0)

        # obter os tuplos de cada cliente
        valores = re.findall(r'([A-Z0-9]+)\,\s([0-9\,]+)', linha)

        # adição do cliente ao dicionário caso ainda não esteja
        if nic not in dictionary.keys():
            dictionary[nic] = {}

        # percorre cada tuplo
        for pair in valores:

            # tipo de analise
            tipo = pair[0]

            # valor e sua cifra
            valor = float(pair[1].replace(",","."))
            valor = pub_key.encrypt(valor)
            
            # prepara o valor para poder ser guardado no ficheiro
            valor_para_serializar = (str(valor.ciphertext()), valor.exponent)

            # se o tipo de analise ainda nao estiver no dicionario
            # adiciona-se o mesmo e o valor em questão a lista
            if tipo not in dictionary[nic].keys():
                dictionary[nic][tipo] = [valor_para_serializar]

            # se estiver apenas adiciona-se o valor ao fim da lista
            else: dictionary[nic][tipo].append(valor_para_serializar)

    testfile.close()
    
    # usado para deserialization dos valores
    dictionary['public_key'] = { 'g':pub_key.g, 'n':pub_key.n}

    # guarda-se o dicionário num ficheiro
    savefile = open(saveFile, "w")
    savefile.write(json.dumps(dictionary))
    savefile.close()