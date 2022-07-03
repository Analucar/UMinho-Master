#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/syscall.h>
#include "../include/file.h"

#define REGISTRY_DIR "/etc/monitord-registry.txt"
#define REGISTRY_ENTRY_SIZE 8192


// Lê uma linha do ficheiro
int readln(int fd, char* buff, int tam){
	int i = 0;
	
	while(read(fd, buff+i, 1) > 0 && buff[i] != '\n' && i < tam)
        i++;

	return i;
}

// Remove um ficheiro dos ficheiros que estão a ser monitorizados
int remove_file(FILE *temp, int reg, char *file_name){
    int success = 1, r = 0;
    char buffer[REGISTRY_ENTRY_SIZE], *copy, *token;

    while((r = readln(reg, buffer, REGISTRY_ENTRY_SIZE)) > 0) {

        buffer[r-1] = '\0';

        copy = strdup(buffer);
        token = strtok(buffer, ":");
                
        if (strcmp(token, file_name) != 0) {
            copy[r-1] = '\n';
            fwrite(copy, 1, strlen(copy), temp);
    
        } else 
            success = 0; 
        
    } 

    return success;
}

/* Coloca o conteúdo de um ficheiro temporário de registos de monitorização
no ficheiro que regista quais ficheiros estão sob monitorização */
int copy_temp_registry(FILE *tmp, int reg){
    int r = 0, wr, success = 0;
    char buffer[REGISTRY_ENTRY_SIZE];
        
    while((r = fread(buffer, sizeof(char), REGISTRY_ENTRY_SIZE, tmp)) > 0) {
        wr = write(reg, buffer, r);
        success = wr == -1 ? 1 : 0;

    }
        
    return success;
}

// Verifica se um ficheiro está a ser monitorizado
int contains(char *file_name) {
    int reg = open(REGISTRY_DIR, O_RDONLY | O_EXCL);
    char buffer[REGISTRY_ENTRY_SIZE], *token;
    int r = 0, success = 0;
    
    if(reg == -1)
        return -1;

    while((r = readln(reg, buffer, REGISTRY_ENTRY_SIZE)) > 0 && !success) {
        if(buffer[r-1] == '\n')
            buffer[r-1] = '\0';

        token = strtok(buffer, ":");
                
        if (strcmp(token, file_name) == 0) 
            success = 1;
    }

    close(reg);
    return success;
}

// Remove um ficheiro da lista de ficheiros a vigiar
// Devolve 0 se correr bem e 1 se nao removeu o ficheiro
int remove_file_handler(char *file_name) {
    int success = 1;

    char *path = realpath(file_name, NULL);

    if (path == NULL){
        printf("Invalid path.\n");
        return 1;
    }

    if(!contains(path)) {
        printf("File is not being monitored.\n");
        free(path);
        return 1;
    }

    int reg = open(REGISTRY_DIR, O_RDONLY | O_EXCL);
    FILE *temp = tmpfile();

    if(temp != NULL && reg != -1) {    

        REG_FILE f = load_file(path);

        if(f != NULL && (get_uid(f) == getuid() || getuid() == 0)) {
            success = remove_file(temp, reg, path);           

            close(reg);
            reg = open(REGISTRY_DIR, O_WRONLY | O_TRUNC | O_EXCL);
            if(reg == -1)
                success = 1;

            else{
                fseek(temp, 0, SEEK_SET);     
                success = copy_temp_registry(temp, reg);
                close(reg);
            }

            fclose(temp);
        } else 
            printf("You must be either root or the owner of the file in order to stop monitoring this file.\n");
        
    } else 
        printf("No read/write permissions over the registry file.\n");

    free(path);
    return success;
}

// Adiciona um ficheiro à lista de ficheiros a vigiar
int add_file_handler(char *file_name) {
    int success = 0, wr;
    char *path = realpath(file_name, NULL);

    if(path == NULL){
        printf("Invalid path.\n");
        return 1;
    }

    success = contains(path); 

    if(success == -1){
        printf("No read permissions over the registry file.\n");
        free(path);
        return 1;

    } else if (success == 1) {
        printf("File is already being monitored.\n");
        free(path);
        return 1;
    }
    
    int reg = open(REGISTRY_DIR, O_WRONLY | O_APPEND | O_EXCL);
    if(reg != -1) {

        REG_FILE f = load_file(path);

        if(f != NULL && (getuid() == 0 || get_uid(f) == getuid())) {
            char *f_as_str = to_string(f);

            wr = write(reg, f_as_str, strlen(f_as_str));

            success = wr == -1 ? 1 : 0;

            free_file(f);
            free(f_as_str);

        } else if (f == NULL){
            printf("Can't open the file that is going to be monitored.\n");
            success = 1;
        }
        else {
            printf("You must be either root or the owner of the file in order to monitor this file.\n");
            success = 1;
        }
        
        close(reg);

    } else
        success = 1;
     
    free(path);
    return success;
}

/* Utilizar "etc/mon -a <file_path>" para adicionar um ficheiro à monitorizaçáo
e utilizar "etc/mon -d <file_path>" para remover um ficheiro da monitorização */
int main(int argv, char **argc){
    int res;
    if(argv == 3){
        if(!strcmp(argc[1], "-a")){
            res = add_file_handler(argc[2]);
            if(!res)
                printf("Done!\n");

        }else if (!strcmp(argc[1], "-d")){
            res = remove_file_handler(argc[2]);
            if(!res)
                printf("Done!\n");

        } else 
            printf("Invalid command!\n");
        
                
    } else {
        printf("Invalid command!\n");
        printf("Start the monitorization of a file: 'etc/mon -a <file>'\n");
        printf("Cancel the monitorization of a file: 'etc/mon -d <file>'\n");
    }

    return 0;
}
