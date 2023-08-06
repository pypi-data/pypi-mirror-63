#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <errno.h>
#include <string.h>

int main(int argc, char **argv)
{
	int rootUid, rootGid;
	int ret;
	/* args validation */
	if (argc < 2) {
		printf("Usage: %s <cmd> <args> ..\\n", argv[0]);
		exit(1);
	}
	/* gain root user privilege */
	rootUid = geteuid();
	rootGid = getegid();
	if (setuid(rootUid) != 0) {
		perror("setuid");
		return(1);
	}
	if (setgid(rootGid) != 0) {
		perror("setgid");
		return(1);
	}
	/* execute the command with root privilege */
	ret = execvp(argv[1], &(argv[1]));
	if (ret < 0) {
		if (errno == ENOENT) {
			fprintf(stderr, "pudo: %s: command not found\\n", argv[1]);
		} else {
			char msg[128] = {0};
			sprintf(msg, "pudo: %s", argv[1]);
			perror(msg);
		}
	}
	return(1);
}
