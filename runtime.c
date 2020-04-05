#include <stdio.h>

int read_int() {
	int x = 0;
	printf("read_int\n");
	scanf("%d", &x);
	return x;
}

void print_int(int x) {
	printf("%d", x);
}