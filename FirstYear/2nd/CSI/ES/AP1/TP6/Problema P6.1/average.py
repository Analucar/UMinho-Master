from phe import paillier
import ast

def average(tipo, filename):
    
    # abertura do ficheiro com os dados
    savefile = open(filename, "r")
    dictionary = savefile.read()

    # recuperação do dicionario
    dictionary = ast.literal_eval(dictionary)
    
    # será utilizada na reconstrução do valor
    public_key_rec = paillier.PaillierPublicKey(n=int(dictionary['public_key']['n']))

    soma = 0.0
    average = 0.0
    count = 0

    # percorre cada cliente e cada tipo e para cada elemento contido nessa
    # combinação adiciona ao acumulador soma e incrementa o contador count
    for nic in dictionary.keys():
        if tipo in dictionary[nic].keys():
            for valor in dictionary[nic][tipo]:

                # reconstrução do valor
                valor = paillier.EncryptedNumber(public_key_rec, int(valor[0]), int(valor[1]))
                soma = soma + valor
                count = count + 1
    
    average = soma / count

    return average