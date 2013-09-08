#include <stdio.h>
#include <asm/unistd.h>
#include <sys/errno.h>
_syscall0(void, deepsleep);

main() {
printf("Go to sleep\n");
deepsleep();
printf("Woke up! \n");
}

