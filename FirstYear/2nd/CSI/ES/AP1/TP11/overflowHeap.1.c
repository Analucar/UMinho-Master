#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    
    // validar índices: input do utilizador deve respeitar limites do array de argumentos 
    /* verificar se o tamanho do argumento é menor ou igual a 10 de modo que
    memória alocada seja suficiente */
    if (argc != 2 || strlen(argv[1]) > 10) {
        printf("Número inválido ou tamanho inválido dos argumentos\n");
        return 0;
    }

    char *dummy = (char *) malloc (sizeof(char) * 10);
    char *readonly = (char *) malloc (sizeof(char) * 10);
    
    /* evitar funções de risco: é melhor usar "strncpy" 
    para controlar o tamanho a copiar de strings*/
    /* tamanho do array: utilizar "strlen" que devolve o 
    tamanho do array que será copiado */
    strncpy(readonly, "laranjas", strlen("laranjas"));   
    strncpy(dummy, argv[1], strlen(argv[1]));                     

    printf("%s\n", readonly);
}
