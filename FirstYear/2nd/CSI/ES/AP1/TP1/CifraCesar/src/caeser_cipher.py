from pycipher import Caesar
from os.path import exists
import re
from ngram_score import ngram_score
import time

#Funcao que processo a segunda opcao do programa.
#Recebe as chaves das cifras que o utilizador pretende aplicar de forma sequencial
#Ate que o utilizador introduza o valor -1 sendo o resultado final (ciphertext) apresentado ao utilizador.
def processCipher():
    key = ""
    text = input ('Text: ')

    while(key != '-1'):
        print('\nIndique a chave da próxima cifra de césar a ser aplicada.')
        print('Escreva -1 para acabar e obter o resultado da cifra')

        key = input('\nChave: ')

        if int(key) >= 0:
            text = Caesar(key = int(key)).encipher(text)

        elif key != '-1':
            print('Chave inválida')

    print('Ciphertext: ' + text + '\n')
    return text

def processDecipher():

    #Input do ciphertext que se pretente decifrar.
    ciphertext = input ('Ciphertext: ')
    key = ""

    #Para terminar o processo de decifragem a chave que se deve introduzir é -1.
    while(key != '-1'):
        print('\nIndique a chave da próxima cifra de césar a ser aplicada: ')
        print('Escreva -1 para acabar e obter o resultado da cifra.')

        key = input('\nChave: ')
        
        #Verifica se a chave é positiva e aplica a funcao de decipher da cifra de cesar com a chave.
        #Guarda o ciphertext resultante.
        if int(key) >= 0:
            ciphertext = Caesar(key = int(key)).decipher(ciphertext)

        elif key != '-1':
            print('Chave inválida')
    
    #Imprime no ecra o texto original resultante de aplicar a funcao de decifra com varias chaves.
    print('Original text: ' + ciphertext + '\n')
    
    return ciphertext

def break_caesar():
    
    stats_file = input('Statistic file: ')
    ctext = input('Ciphertext: ')
    if exists(stats_file):

        start_time = time.time()
        #Utiliza o modulo ngram_score
        fitness = ngram_score(stats_file) 

        # Remove os espaços e coloca o ciphertext em uppercase
        ctext = re.sub('[^A-Z]','',ctext.upper())

        #Testa todas as chaves e guarda os resultados do fitness score de cada uma delas
        scores = []
        for i in range(26):
            scores.append((fitness.score(Caesar(i).decipher(ctext)),i))
        
        #Obtem a chave com maior fitness score
        max_key = max(scores)
        
        #Imprime no ecrã a chave que obteve melhor resultado e o resultado da decifragem.
        print('Chave com melhor resultado = ' + str(max_key[1]) + ':')
        print(Caesar(max_key[1]).decipher(ctext))

        end_time = time.time()
        
        print('Tempo decorrido: ' + str(end_time - start_time))

    else:
        print('Path inválido.')

opt = ""

while opt != "0":
    print('\n0 - exit')
    print('1 - Cipher')
    print('2 - Decipher')
    print('3 - Break cipher')
    
    opt = input('\n>')

    if opt == '1':
        processCipher()

    elif opt == '2':
        processDecipher()

    elif opt == '3':
        break_caesar()

    elif opt != '0':
        print('Invalid option')
    
