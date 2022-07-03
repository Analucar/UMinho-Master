#include "../include/file.h"
#include <openssl/evp.h>

#define METADATA_LENGTH 8192

typedef struct file {
  char *name; //nome do ficheiro
  int inode;
  int perms; // premissões
  int links; //numero de links até ao ficheiro
  long size; //tamanho do ficheiro
  int  owner; //nome do dono
  int group; // nome do grupo
  char *hash; //hash do ficheiro
} File;


// Efetua o hash do conteúdo do ficheiro
char *gen_hash(FILE * f){
    unsigned char hash[SHA256_DIGEST_LENGTH];
    char *result = (char *) malloc(sizeof(char) * 2 * SHA256_DIGEST_LENGTH + 1);
    char data[1024];
    unsigned int md_len;

    EVP_MD_CTX *mdContent = EVP_MD_CTX_new();
    int bytes;

    //inicialização da função sha256
    EVP_DigestInit_ex(mdContent, EVP_sha256(), NULL);

    //atualização da hash com o conteudo do ficheiro
    while((bytes = fread(data, 1, 1024, f)) != 0)
        EVP_DigestUpdate(mdContent, data, bytes);
    
    // finalização da hash
    EVP_DigestFinal_ex(mdContent, hash, &md_len);

    //passar a hash para string
    for(int i = 0; i < md_len; i++)
        sprintf((char *)&(result[i*2]), "%02x", hash[i]);
    
    EVP_MD_CTX_free(mdContent);

    return result;
}

// Carrega o ficheiro na estrutura
REG_FILE load_file(char * file_name){
    FILE * file = fopen(file_name, "rb");
    REG_FILE f = NULL;

    if(file != NULL){
        struct stat statbuf;

        stat(file_name, &statbuf);

        f = malloc(sizeof(struct file));
    
        // Guarda o nome do ficheiro
        f->name = strdup(file_name);

        //Guarda o inode do ficheiro
        f->inode = statbuf.st_ino;

        // Guarda as premissões do ficheiro
        f->perms = statbuf.st_mode;

        f->links = statbuf.st_nlink;
        
        // Guarda o dono do ficheiro
        f->owner = statbuf.st_uid;
        
        // Guarda o grupo dono do ficheiro
        f->group = statbuf.st_gid;
        
        // Guarda o tamanho do ficheiro
        f->size = (intmax_t) statbuf.st_size;

        // Guarda a hash do ficheiro
        f->hash = gen_hash(file);

        fclose(file);
    }
    
    return f;
}

// Liberta a memória alocada para o ficheiro
void free_file(REG_FILE f) {
    if(f != NULL){
        free(f->name);
        free(f->hash);
        free(f);
    }
}

// Converte a estrutura do ficheiro numa string
char *to_string(REG_FILE f) {
    char *result = NULL;
    
    if(f != NULL){
        result = malloc(sizeof(char) * METADATA_LENGTH + 1);
        sprintf(result, "%s:%d:%d:%ld:%d:%d:%d:%s\n", f->name, f->inode, f->perms, f->size, f->links, f->owner, f->group, f->hash);
    }

    return result;
}

// Devolve o nome do dono do ficheiro
int get_uid(REG_FILE f) {
    return f->owner;
}
