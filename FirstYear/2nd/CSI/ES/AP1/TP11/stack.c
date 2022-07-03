/* stack.c */
/* This program has a buffer overflow vulnerability. */
/* Our task is to exploit this vulnerability */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
int bof(char *str)
{
	char buffer[24];
	/* The following statement has a buffer overflow problem */

	/* tamanho do array: utilizar "strlen" para verificar
	se a string que vai ser copiada cabe no array destino */
	if (strlen(str) < strlen(buffer)) {
		/* evitar funções de risco: é melhor usar "strncpy" 
    	para controlar o tamanho a copiar de strings*/
		/* tamanho do array: utilizar "strlen" que devolve o 
    	tamanho do array que será copiado */
		strncpy(buffer, str, strlen(str));
	}

	return 1;
}

int main(int argc, char **argv)
{
	// validar índices: input do utilizador deve respeitar limites do array de argumentos 
    if (argc != 1) {
        printf("Número inválido de argumentos\n");
        return 0;
    }

	char str[517];
	FILE *badfile;
	/* verificar se o ficheiro existe antes de fazer operações baseadas no mesmo */
	if((badfile = fopen("badfile", "r")) != NULL){
		fread(str, sizeof(char), 517, badfile);
	}

	bof(str);
	printf("Returned Properly\n");
	return 1;
}
