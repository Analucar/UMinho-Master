import string
import scipy.stats as stats

#Função: determina a ordem das colunas através da chave recebida 
def orderKey(key):

    aux = []

    # Ciclo que percorre os caracteres da chave
    # e insere num array a sua posição no abcedário
    # Exemplo: E encontra-se na posição 4 
    i=0
    for char in key:
        pos = string.ascii_uppercase.index(char)
        aux.insert(i,pos)
        i = i+1

    # Devolve uma ordem apartir do valor das posições
    # de cada caracter. O menor valor fica em 1º lugar
    # o 2º menor fica em 2º e assim sucessivamente
    value = stats.rankdata(aux, method='ordinal')

    return value

# Função: realiza uma permutação para cifrar mensagens
# A função recebe o comprimento da chave e da mensagem,
# a ordem das colunas (passo 1) e a mensagem a cifrar
def buildCiphertext(lenKey, lenMsg, value, msg):

    finalStr = ""
    column = []
    matrix = []

    # PASSO a:
    # Ciclo que vai escrever pelas linhas da matriz
    # a mensagem a ser cifrada
    for i in range(lenMsg):
        if i%lenKey == 0:
            # substring que será escrita em cada linha
            sub = msg[i:i+lenKey]
            lst = []
            for j in sub:
                lst.append(j)
            # insere linha com a mensagem na matriz
            matrix.append(lst)
    
    # PASSO b:
    # Ciclo que guarda num array a mensagem pela ordem 
    # das colunas (passo 1). A coluna com numero 1 conterá
    # a primeira porção da mensagem e assim sucessivamente
    for n in range(1,lenKey+1):
        index = 0
        for x in value:
            # Condição que determina a ordem pela qual 
            # guardamos a mensagem
            if x==n:
                ind = 0
                for row in matrix:
                    # Condição que determina se a célula da matriz 
                    # a ser lida contém caracteres da mensagem
                    if ind*lenKey+index+1<=lenMsg:
                        # Guarada a mensagem num array designado column
                        column.append(row[index])
                    ind = ind+1
            index = index+1
    
    # Ciclo que transforma o array que contém a mensagem numa string
    for elem in column: 
        finalStr += elem
    
    return finalStr

# Função: realiza uma permutação para decifrar mensagens
# A função recebe o comprimento da chave e da mensagem,
# a ordem das colunas (passo 1) e a mensagem a decifrar
def buildPlaintext(lenKey, lenMsg, value, msg):

    finalStr = ""
    column = []
    matrix = []

    # Determina o número de linhas da matriz a criar
    rows = (lenMsg//lenKey) + 1 if lenMsg%lenKey else lenMsg//lenKey

    # Ciclo que cria uma matriz
    for i in range(0,rows):
        col = []
        for j in range(0,lenKey):
            # Bloqueia com um '*' as células que não vão conter 
            # caracteres da mensagem
            col.append('') if i*lenKey+j+1<=lenMsg else col.append('*') 
        matrix.append(col)

    # PASSO a:
    # Ciclo que escreve na matriz a mensagem segundo as 
    # colunas de forma ordenada. A 1º porção da menagem 
    # irá para a coluna com valor 1 e assim sucessivamente
    elem = 0
    for index in range(1, lenKey+1):
        col = 0
        for v in value:
            # Condição que determina a ordem pela qual 
            # escrevemos a mensagem
            if v==index:
                # Determina a porção da mensagem que irá ser alocada à coluna
                # tendo em conta as células bloqueadas com '*'
                numberElem = rows-1 if '*' in [r[col] for r in matrix] else rows
                sub = msg[elem:elem+numberElem]
                elem = elem+numberElem
                for line in range(0,rows):
                    # Escreve na matriz a substring calculada na coluna respetiva
                    if matrix[line][col] != '*':
                        matrix[line][col] = sub[line]
            col = col +1

    # PASSO b:
    # Guarda no array column a mensagem lida segundo as linhas da matriz
    for i in range(0,rows):
        for j in range(0,lenKey):
            # Condição que ignora as células que estejam bloqueadas
            if matrix[i][j] != '*':
                column.insert(i*lenKey+j,matrix[i][j])

    # Transforma o array column numa string  
    for char in column: 
        finalStr += char
    
    return finalStr

# Função: cifra mensagem
def encrypt():

    msg = input('Mensagem a cifrar:  ').upper()
    keyOne = input('Permutação 1:  ').upper() 
    keySec = input('Permutação 2:  ').upper()

    lenMsg = len(msg)
    lenOne = len(keyOne)
    lenSec = len(keySec)

    # PASSO 1:
    # Numerar cada caracter das chaves 
    # de acordo com a sua posição no abecedário
    valueOne = orderKey(keyOne)
    valueSec = orderKey(keySec)

    # PASSO 2: 
    # Fazer a primeira permutação
    # utilizando a primeira chave e a mensagem a cifrar
    cipherOne = buildCiphertext(lenOne, lenMsg, valueOne, msg)
    # PASSO 3: 
    # Fazer a segunda permutação 
    # utilizando a segunda chave e a mensagem da 1º permutação
    cipherSec = buildCiphertext(lenSec, lenMsg, valueSec, cipherOne)

    # Mensagem cifrada final
    print()
    print('====> ', cipherSec, ' <====')
    print()

#Função: decifra uma mensagem      
def decrypt():

    msg = input('Mensagem a decifrar:  ').upper()
    keyOne = input('Permutação 1:  ').upper()
    keySec = input('Permutação 2:  ').upper()

    lenMsg = len(msg)
    lenOne = len(keyOne)
    lenSec = len(keySec)

    # PASSO 1:
    # Numerar cada caracter das chaves 
    # de acordo com a sua posição no abecedário
    valueOne = orderKey(keyOne)
    valueSec = orderKey(keySec)

    # PASSO 2: 
    # Fazer a primeira permutação 
    # utilizando a segunda chave e a mensagem a decifrar
    decipherOne = buildPlaintext(lenSec, lenMsg, valueSec, msg)
    # PASSO 3: 
    # Fazer a primeira permutação 
    # utilizando a primeira chave e a mensagem da 1º permutação
    decipherSec = buildPlaintext(lenOne, lenMsg, valueOne, decipherOne)

    print()
    print('====> ', decipherSec, ' <====')
    print()
    
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