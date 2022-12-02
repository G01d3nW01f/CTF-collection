/* gcc -m32 -static execve.c */

#include <stdlib.h>

int main(){
	
	char *argv[] = {"/bin/sh", NULL};
	execve(argv[0], argv, NULL);
}
