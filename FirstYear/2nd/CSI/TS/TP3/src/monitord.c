#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../include/file.h"
#include <syslog.h>
#include <unistd.h>
#include <fcntl.h>

#define REGISTRY_DIR "/etc/monitord-registry.txt"
#define INIT_FILE "/etc/monitord-init.txt"
#define LOG_FILE "monitord-logs"
#define REGISTRY_ENTRY_SIZE 8192


int readln(int fd, char* buff, int tam){
	int i = 0;
	
	while(read(fd, buff+i, 1) > 0 && buff[i++] != '\n' && i < tam);

	return i;
}

// Escreve um log no ficheiro de logs
void write_to_log(char *log){
    openlog(LOG_FILE, LOG_CONS | LOG_PID | LOG_NDELAY, LOG_USER);    
    syslog(LOG_INFO, log, 1);
    closelog();
}

// Escreve um log no ficheiro de logs de acordo com a alteração feito a esse ficheiro
void make_log(char *file_path, int param){
    char log[REGISTRY_ENTRY_SIZE];
        
    switch(param) {
        case 0:
            sprintf(log, "The file %s was deleted or its name was altered.", file_path);
            break;
        case 1:
            sprintf(log, "The inode of the file %s was altered.", file_path);
            break;
        case 2:
            sprintf(log, "The type or permissions of the file %s were altered.", file_path);
            break;
        case 3:
            sprintf(log, "The size of the file %s was altered.", file_path);
            break;
        case 4:
            sprintf(log, "The number of links of the file %s were altered.", file_path);
            break;
        case 5:
            sprintf(log, "The owner of the file %s was altered.", file_path);
            break;
        case 6:
            sprintf(log, "The group of the file %s were altered.", file_path);
            break; 
        case 7:
            sprintf(log, "The hash of the file %s was altered.", file_path);
            break; 
    }

    write_to_log(log);
}

// Separa cada um dos campos da estrutura do ficheiro
char **separate(char * c,char *divider, int *size){ 
	*size = 0;
	int tam = 10;
	char **final = malloc(sizeof(char *)*tam);
	char *token;
	token = strtok(c,divider);

	while(token){
		if(*size == tam){
			tam *= 2;
			final = realloc(final, sizeof(char *)*tam);
		}	
		final[(*size)++] = token;
		token = strtok(NULL,divider);
	}
	return final;
}

// Efetua a comparação entre 2 ficheiros e efetua um log caso não sejam iguais
void compare(char *file_str, char *reg_str) {
    int s1, s2;

    char **str1 = separate(file_str, ":", &s1);
    char **str2 = separate(reg_str, ":", &s2);

    for(int i = 0; i < s1 && i < s2; i++)
        if(strcmp(str1[i], str2[i])){
            printf("%s\n%s\n", str1[i], str2[i]);
            make_log(str2[0], i);
        }
    free(str1);
    free(str2);
}

// Verifica se todos os ficheiros a ser monitorizados continuam com a sua integridade intacta
int check_integrity() {
    
    char buffer[REGISTRY_ENTRY_SIZE];
    int registry = open(REGISTRY_DIR, O_RDONLY | O_EXCL);
    int r = 0, success = 0;
    char *name, *file_as_str, *temp;
    
    if(registry != -1) {

        while((r = readln(registry, buffer, REGISTRY_ENTRY_SIZE)) > 0) {
            buffer[r-1] = '\0';

            temp = strdup(buffer);
            name = strtok(temp, ":");
            
            REG_FILE f = load_file(name);

            if(f != NULL) {

                file_as_str = to_string(f);

                file_as_str[strlen(file_as_str)-1] = '\0';
                
                compare(file_as_str, buffer);

                free(file_as_str);
                file_as_str = NULL;
                free_file(f);

            } else 
                make_log(name, 0);

            free(temp);
            temp = NULL;
        } 

        close(registry);
    } else
        success = 1;

    return success;
}

//Lista inicial de ficheiros a serem vigiados
int init_registry(){
    char buffer[REGISTRY_ENTRY_SIZE];
    int registry = open(REGISTRY_DIR, O_WRONLY | O_TRUNC | O_EXCL);
    int init = open(INIT_FILE, O_RDONLY | O_EXCL);

    int r = 0, wr, success = 0;
    char *file_as_str = NULL;

    if(registry != -1 && init != -1) {

        while((r = readln(init, buffer, REGISTRY_ENTRY_SIZE)) > 0) {

            if(buffer[r-1] == '\n')
                buffer[r-1] = '\0';

            char *path = realpath(buffer, NULL);

            if(path != NULL){
                REG_FILE f = load_file(path);

                if(f != NULL){
                    file_as_str = to_string(f);
                    wr = write(registry, file_as_str, strlen(file_as_str));
                    success = wr == -1 ? 1 : 0;
                    free_file(f);
                    free(file_as_str);
                }

                free(path);
            }
        } 

        close(init);
        close(registry);
    } else
        success = 1;

    return success;
}

int main(int argv, char **argc) {
    int success = 1;    
    if(argv == 1) 
        success = check_integrity();

    else if(argv == 2 && !strcmp(argc[1], "-i"))
        success = init_registry();

    return success;
}
