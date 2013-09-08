#include<asm/unistd.h>
#include<stdio.h>
#include<sys/errno.h>
_syscall2(int,smunch,int,pid,unsigned long,bitpattern);
int main(int argc,char** argv)
{
	unsigned long bitpattern = 0;
	int result;
	int pid;
	bitpattern |= 256;
	printf("About to make smunch call");
	pid = atoi(argv[1]);
	result = smunch(pid,bitpattern);
	printf("The result is %d",result); 
	return 0;
}
