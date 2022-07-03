from phe import paillier
import store as storer
import average as averager


if __name__ == "__main__":

    # geração do par de chaves
    pub_key, priv_key = paillier.generate_paillier_keypair(n_length=3072)
    
    print("Nome do ficheiro com os dados a serem guardados: ", end = '')
    ficheiroTeste = input()
    print("Nome do ficheiro onde os dados serão guardados: ", end = '')
    saveFile = input()
    print("A guardar dados...")
    storer.store(pub_key, ficheiroTeste, saveFile)
    print("Dados guardados com sucesso!\n")

    print("Nome do ficheiro de análise: ", end = '')
    ficheiroAnalise = input()
    print("Tipo da análise cuja média deseja calcular: ", end = '')
    tipo = input()
    average = averager.average(tipo, ficheiroAnalise)
    print("Média: " + str(priv_key.decrypt(average)))