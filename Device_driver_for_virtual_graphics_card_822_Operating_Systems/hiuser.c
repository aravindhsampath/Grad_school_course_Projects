#include <stdio.h>
#include<stdlib.h>
#include<fcntl.h>
#include<errno.h>
#include<math.h>
#include<sys/mman.h>
#include<linux/ioctl.h>
#include"cj1_regs.h"

unsigned int *u_control_base;
unsigned int buffer[0x10000];
unsigned int * cb;
unsigned long temp_address;
int flag=1;
int k = 0;
int t_count;
float adj=0.1;
int clearflag=0;
int pass=0;

unsigned int U_READ_REG(unsigned int reg)
{
  unsigned int value;
  value = *(u_control_base+(reg>>2));
  return(value);
}
DMA_Cmd dma_cmd;
void U_WRITE_REG(unsigned int reg,unsigned int value)
{
  *(u_control_base+(reg>>2)) = value;
}

void start_graphics()
{
  int i;
  float one = 1.0;
  float mone = -1.0;
  U_WRITE_REG(CfgFlags, 0);
  U_WRITE_REG(CfgMode,0x03);
  U_WRITE_REG(CfgFrame,0x1008888);
  U_WRITE_REG(CfgAccel,2);
  U_WRITE_REG(CfgWidth, 800);
  U_WRITE_REG(CfgHeight, 600);
  for(i = 0;i<16;i++) U_WRITE_REG(VtxTransform+4*i,0);
  U_WRITE_REG(VtxTransform+4*0,*(unsigned int *)&one);
  U_WRITE_REG(VtxTransform+4*5,*(unsigned int *)&one);
  U_WRITE_REG(VtxTransform+4*10,*(unsigned int *)&mone);
  U_WRITE_REG(VtxTransform+4*15,*(unsigned int *)&one);
  U_WRITE_REG(CmdReboot,1);
  U_WRITE_REG(CmdSync,1);
}
void end_graphics(){
  U_WRITE_REG(CfgMode,0x0);
  U_WRITE_REG(CfgFrame,0x0);
  U_WRITE_REG(CfgAccel,0);
  U_WRITE_REG(CfgWidth,0);
  U_WRITE_REG(CfgHeight,0);
  U_WRITE_REG(CmdReboot,1);
  U_WRITE_REG(CmdSync,1);
}

float color[3][4] = {
  1.0,0.0,0.0,1.0,
  0.0,1.0,0.0,1.0,
  0.0,0.0,1.0,1.0
};

float position[3][4] = {
  -0.5,0.75,0.0,1.0,
  0.5,0.25,0.0,1.0,
  0.2,-0.75,0.0,1.0 
  
};
 
float pos_triangle1[3][4] = {
  -1.0,-0.75,0.0,1.0,
  -0.75,-0.5,0.0,1.0,
  -1.0,-0.25,0.0,1.0 
  
};
float pos_triangle2[3][4] = {
  1.0,-0.75,0.0,1.0,
  0.75,-0.5,0.0,1.0, 
  1.0,-0.25,0.0,1.0
  
};
float pos_triangle3[3][4] = {
  1.0,0.75,0.0,1.0,
  1.0,0.25,0.0,1.0,
  0.75,0.5,0.0,1.0 
};
float pos_triangle4[3][4] = {
  -1.0,0.75,0.0,1.0,
  -1.0,0.25,0.0,1.0,
  -0.75,0.5,0.0,1.0
};
float clearcolor[4] = {
  0.20,0.15,0.15,1.0
};


void change_coord()
{
int i;
for(i=0;i<3;i++)
{
	pos_triangle1[i][0]=pos_triangle1[i][0]+0.005;
	pos_triangle2[i][0]=pos_triangle2[i][0]-0.005;
	pos_triangle3[i][0]=pos_triangle3[i][0]-0.005;
	pos_triangle4[i][0]=pos_triangle4[i][0]+0.005;
}
}

void start_graphics_dma() {
	k=0;
	int i,j;
	cb[k] = CmdActiveBuffer;
	cb[++k] = 2;
	i = 0;
		cb[++k] = VtxColor;
		for (i = 0; i < 4; i++) {
			cb[++k] = *(unsigned int *) &clearcolor[i];
		}
		cb[++k] = CmdClear;
		cb[++k] = 1;
	cb[++k] = CmdPrimitive;
	cb[++k] = 4;
	i = 0;
	j = 0;
	
		
	for (i = 0; i < 3; i++) {
		cb[++k] = VtxColor;
		for (j = 0; j < 4; j++)
			cb[++k] = *(unsigned int *) &color[i][j];
		cb[++k] = VtxPosition;
		for (j = 0; j < 4; j++) {  	
		cb[++k] = *(unsigned int *) &pos_triangle1[i][j];
				}		
		cb[++k] = CmdVertex;
	}
	for (i = 0; i < 3; i++) {
		cb[++k] = VtxColor;
		for (j = 0; j < 4; j++)
			cb[++k] = *(unsigned int *) &color[i][j];
		cb[++k] = VtxPosition;
		for (j = 0; j < 4; j++) {
			cb[++k] = *(unsigned int *) &pos_triangle2[i][j];
		}
		cb[++k] = CmdVertex;
	}
	for (i = 0; i < 3; i++) {
		cb[++k] = VtxColor;
		for (j = 0; j < 4; j++)
			cb[++k] = *(unsigned int *) &color[i][j];
		cb[++k] = VtxPosition;
		for (j = 0; j < 4; j++) {
			cb[++k] = *(unsigned int *) &pos_triangle3[i][j];
		}
		cb[++k] = CmdVertex;
	}
	for (i = 0; i < 3; i++) {
		cb[++k] = VtxColor;
		for (j = 0; j < 4; j++)
			cb[++k] = *(unsigned int *) &color[i][j];
		cb[++k] = VtxPosition;
		for (j = 0; j < 4; j++) {
			cb[++k] = *(unsigned int *) &pos_triangle4[i][j];
		}
		cb[++k] = CmdVertex;
	}

	cb[++k] = CmdPrimitive;
	cb[++k] = 0;
	cb[++k] = CmdActiveBuffer;
	cb[++k] = 1;
	k++; 
}
void draw()
{
  int i,j;
  U_WRITE_REG(CmdActiveBuffer, 2);
  for(i=0;i<4;i++)
    U_WRITE_REG(VtxColor+4*i, *(unsigned int *)&clearcolor[i]);
  while(U_READ_REG(InFIFO)>0);
  U_WRITE_REG(CmdClear,1);
  U_WRITE_REG(CmdPrimitive,4);
  for(i=0;i<3;i++) {
    for(j=0;j<4;j++)
      U_WRITE_REG(VtxColor+4*j,*(unsigned int *)&color[i][j]);
    for(j=0;j<4;j++)
      U_WRITE_REG(VtxPosition+4*j,*(unsigned int *)&position[i][j]);
    U_WRITE_REG(CmdVertex,1);
  }
  U_WRITE_REG(CmdPrimitive,0);
  U_WRITE_REG(CmdActiveBuffer,1);
}

int main(void)
{
  int fd,result,i, choice;
  long res;
  printf("MENU \n 1.FIFO \n 2.DMA\n");
  printf("Enter your choice \n");
  scanf("%d",&choice);
  if(choice!=1 & choice!=2){
	printf("Invalid choice. Program terminating\n");
	return -1;
	}
  fd=open("/dev/kyouku",O_RDWR);
  u_control_base=mmap(0,4096,PROT_READ|PROT_WRITE,MAP_SHARED,fd,0);
  result=U_READ_REG(CfgFeatures);
  printf("read FIFO gives %x\n",result);
  res = ioctl(fd, VMODE, GRAPHICS_ON);
  if(choice==1){
	draw();
	sleep(2);
	}	
  else if(choice==2) {
  	res = ioctl(fd, BIND_DMA, &temp_address);
  	printf("bind dma is succcessful %lu",temp_address);
 	cb = (unsigned int *)temp_address;
 	for(i=0;i<300;i++){
	  start_graphics_dma();
	  temp_address = k;
	  res = ioctl(fd, START_DMA,&temp_address);
	  cb=(unsigned int*)temp_address;
	  change_coord();
 	 }
   	sleep(5);}

  res = ioctl(fd, VMODE, GRAPHICS_OFF);
  close(fd);
  return 0;
  
}
