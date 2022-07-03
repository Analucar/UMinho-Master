#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <string.h>
#include <pwd.h>
#include <grp.h>
#include <stdint.h>
#include <openssl/sha.h>

typedef struct file * REG_FILE;

REG_FILE load_file(char *);
char *to_string(REG_FILE);
int get_uid(REG_FILE);
void free_file(REG_FILE);
