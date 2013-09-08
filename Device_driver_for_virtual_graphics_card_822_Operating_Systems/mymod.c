#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/kernel_stat.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/pci.h>
#include <linux/delay.h>
#include <linux/ioctl.h>
#include "cj1_regs.h"
#include <linux/interrupt.h>
#include <linux/sched.h>
#include <linux/wait.h>
#include <linux/types.h>
#include <linux/irqflags.h>
#include <linux/spinlock.h>
#include <linux/mm.h>
#include <linux/mman.h>
#define NUMBUFFERS 8
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Team 08/09 --> HIRANMAYI PAI | ARAVINDH SATHISH");
DECLARE_WAIT_QUEUE_HEAD (dma_snooze);
int current_fsuid;
int cond = 0;
int i;
unsigned int buffers_map_count;
unsigned int fill = 0;
unsigned int drain = 0;
unsigned long flags;
bool flag = false; // used to indicate the fill status of the buffer
spinlock_t lock;
unsigned int buffers_allocated = 0;  // count of the number of buffers allocated
struct cdev whatever; 
struct pci_dev *kyouku_dev;
struct pci_device_id kyouku_dev_ids[]={
{PCI_DEVICE(0x1234,0x1111)},
{0}
};
struct kyouku_device{
	unsigned int *k_control_base;
	unsigned long p_control_base;
	unsigned long p_frame_buffer_base;
	unsigned int *k_frame_buffer_base;
	unsigned int *k_dma_base;
	dma_addr_t dma_buf;
}kyouku1;
struct kyouku_buffer{
	unsigned int *dma_base_address;
	unsigned long u_base_address;
	dma_addr_t dma_buf;
	unsigned int count;
}buffers[NUMBUFFERS];
void delay(void){
	udelay(1);
}

unsigned int K_READ_REG(unsigned int reg){
	unsigned int value;
	delay();
	rmb();
	value=*(kyouku1.k_control_base+(reg>>2));
	return(value);
}
void K_WRITE_REG(unsigned int reg, unsigned int value){

	delay();
	*(kyouku1.k_control_base+(reg>>2))=value;

}
irqreturn_t interrupt_handler(int irq, void* dev_id, struct pt_regs *regs) {
  unsigned int iflags;
  printk(KERN_ALERT " Kyouku_Driver : Handling an Interrupt \n");
  iflags=K_READ_REG(CfgFlags);
  K_WRITE_REG(CfgFlags,0x0);  //resetting the CfgFlags
  if((iflags & 0x01) ==0)
		return(IRQ_NONE);
  // Acquire the lock before processing
  spin_lock_irqsave(&lock,flags);
  //if (fill != drain){        // There is something in the buffer to process..
  if (buffers_allocated != 0){        // There is something in the buffer to process..
  		K_WRITE_REG(CmdDMABuffer,(unsigned int)buffers[drain].dma_buf);
  		K_WRITE_REG(CmdDMACount,(buffers[drain].count*4-1)<<1);
  		drain = (drain+1)%NUMBUFFERS;     // increment the ptr as we have freed up a buffer
  		buffers_allocated--;       // decrement the count of allocated buffers
  }
  if (flag == true){         // Circular buffer is full and we set the flag to make a wake up call
  		flag = false;
		wake_up_interruptible(&dma_snooze);
  }
  spin_unlock_irqrestore(&lock,flags);     // release the lock
  return IRQ_HANDLED;
}

int kyouku_probe(struct pci_dev *pci_dev,const struct pci_device_id *pci_id){
	
	kyouku_dev=pci_dev;
	kyouku1.p_frame_buffer_base=pci_resource_start(pci_dev,0);
	kyouku1.p_control_base=pci_resource_start(pci_dev,1);
	if(pci_enable_device(pci_dev));
	pci_set_master(pci_dev);
	return 0;
}
void kyouku_remove(struct pci_dev * pci_dev){ }

struct pci_driver kyouku_pci_drv = {
	.name ="whatever",
	.id_table=kyouku_dev_ids,
	.probe=kyouku_probe,
	.remove=kyouku_remove
};
int kyouku_open(struct inode *inode, struct file *fp) {
	printk(KERN_ALERT "Kyouku_Driver : Module Opened ! \n");
	kyouku1.k_control_base=ioremap(kyouku1.p_control_base,4096);
	kyouku1.k_frame_buffer_base=ioremap(kyouku1.p_frame_buffer_base,4096);
	return 0;
}
int kyouku_release(struct inode *inode, struct file *fp) {
	printk(KERN_ALERT "Kyouku_Driver : Module Released !  \n");
	for(i=0;i<NUMBUFFERS;i++)
		pci_free_consistent(kyouku_dev,0x10000,kyouku1.k_dma_base,kyouku1.dma_buf);
	free_irq(kyouku_dev->irq, &kyouku1);
	pci_disable_msi(kyouku_dev);
	iounmap(kyouku1.k_control_base);
	iounmap(kyouku1.k_frame_buffer_base);
	return 0;
}
int kyouku_mmap(struct file *fp,struct vm_area_struct *vma){  // Memory map for using the command registers
	if((current_fsuid)==-1){
		current_fsuid=current_fsuid();
	}
	if(current_fsuid!=0) {
	printk(KERN_ALERT "FIFO is only restricted to root users\n");
	return -1;
	}	

	io_remap_pfn_range(vma,vma->vm_start,(kyouku1.p_control_base)>>PAGE_SHIFT,4096,vma->vm_page_prot);
	return 0;
}
int buf_mmap(struct file *fp,struct vm_area_struct *vma){     // Memory map for the kernel buffers
	io_remap_pfn_range(vma,vma->vm_start,buffers[buffers_map_count].dma_buf>>PAGE_SHIFT,4096,vma->vm_page_prot);
return 0;
}
long kyouku_ioctl(struct file *fp,unsigned int cmd,unsigned long arg);
struct file_operations kyouku_fops = {
	.open= kyouku_open,
	.release=kyouku_release,
	.mmap=kyouku_mmap,
	.unlocked_ioctl=kyouku_ioctl,
	.owner=THIS_MODULE
};

long kyouku_ioctl(struct file *fp,unsigned int cmd,unsigned long arg){
	printk(KERN_ALERT "Kyouku_Driver : Executing ioctl \n");
	switch(cmd) {
		case(VMODE) :
			if(arg == GRAPHICS_ON){
				printk(KERN_ALERT "Kyouku_Driver : setting GRAPHICS_ON \n");
				K_WRITE_REG(CfgFlags, 0);
  				K_WRITE_REG(CfgMode,0x03);
  				K_WRITE_REG(CfgFrame,0x1008888);
  				K_WRITE_REG(CfgAccel,2);
				K_WRITE_REG(CfgWidth, 800);
				K_WRITE_REG(CfgHeight, 600);
  				for(i = 0;i<16;i++) K_WRITE_REG(VtxTransform+4*i,0);
 			 	K_WRITE_REG(VtxTransform+4*0,0x3f800000);
				K_WRITE_REG(VtxTransform+4*5,0x3f800000);
				K_WRITE_REG(VtxTransform+4*10,0xbf800000);
				K_WRITE_REG(VtxTransform+4*15,0x3f800000);
				K_WRITE_REG(CmdReboot,1);
				K_WRITE_REG(CmdSync,1);
			}
			else {
				printk(KERN_ALERT "Kyouku_Driver : setting GRAPHICS_OFF \n");
				K_WRITE_REG(CfgMode,0x0);
  				K_WRITE_REG(CfgFrame,0x0);
  				K_WRITE_REG(CfgAccel,0);
  				K_WRITE_REG(CfgWidth,0);
  				K_WRITE_REG(CfgHeight,0);
				K_WRITE_REG(CmdReboot,1);
  				K_WRITE_REG(CmdSync,1);
			}
			break;
		case(BIND_DMA) :
			fill=drain=0;   // Initialize buffer status pointers
			for(i =0;i < NUMBUFFERS; i++) {   // Allocate the buffers
				buffers[i].dma_base_address = pci_alloc_consistent(kyouku_dev,0x10000,&(buffers[i].dma_buf));
			}
			kyouku_fops.mmap=buf_mmap; // switch the mmap to the buffers
			for(i=0;i<NUMBUFFERS;i++){
				buffers_map_count=i;
				buffers[i].u_base_address=do_mmap(fp,0,0x10000,PROT_READ|PROT_WRITE,MAP_SHARED,0);
			}
			// return the base address to the user for writing
			if(copy_to_user((unsigned long *)arg,&(buffers[0].u_base_address),sizeof(unsigned long))!=0){
				printk(KERN_ALERT "Kyouku_Driver : Failed to copy to user \n");
			}
			kyouku_fops.mmap=kyouku_mmap;     // switch the mmap to command registers
			pci_enable_msi(kyouku_dev);
			if(request_irq(kyouku_dev->irq, 
				(irq_handler_t)interrupt_handler, 
				IRQF_DISABLED | IRQF_SHARED, 
				"interrupt_handler", 
				&kyouku1))
				printk(KERN_ALERT "Kyouku_Driver : Failed to register interrupt \n");
				
			break;
		case(START_DMA) :
			// The data is written to the kernel buffers directly by the user
			// Copy the count of commands from the user via the argument of the method
			if(copy_from_user(&(buffers[fill].count),(unsigned long*)arg,sizeof(unsigned long)));
			// Return the address of the next buffer location to the user		
			if(copy_to_user((unsigned long *)arg,&(buffers[(fill+1)%NUMBUFFERS].u_base_address),sizeof(unsigned long))!=0){
				printk(KERN_ALERT "Kyouku_Driver : Failed to copy to user \n");
			}		
			// Acquire the lock before processing
			spin_lock_irqsave(&lock,flags);
			if (fill == drain){
				// The buffer was definitely empty at this stage
				spin_unlock_irqrestore(&lock,flags);       // release the lock 
				fill = (fill+1)%NUMBUFFERS;     // Increment the fill pointer
				K_WRITE_REG(CmdDMABuffer,(unsigned int)buffers[drain].dma_buf);
				K_WRITE_REG(CmdDMACount,(buffers[drain].count*4-1)<<1);
				buffers_allocated++;	
				return 0;
			}
			// The system is busy and we have to queue any request
			fill = (fill+1)%NUMBUFFERS;
			buffers_allocated++;
			if(buffers_allocated == 8) flag=true;   // enable the flag for a specific condition to be disabled by the interrupt handler
			spin_unlock_irqrestore(&lock,flags);    // Release the lock		
			if(buffers_allocated >= 7){
				// The Queue is full ! suspend the CPU process
				wait_event_interruptible(dma_snooze, flag==false);
				return 0;
			}	
			break;
		default :
			printk(KERN_ALERT "Kyouku_Driver : Invalid IOCTL call! \n");
			break;
	}
	return 0;
}

int my_init_function(void){
	cdev_init(&whatever,&kyouku_fops);
	cdev_add(&whatever,MKDEV(127,500),1);
	if(pci_register_driver(&kyouku_pci_drv));
	current_fsuid= -1;
	//printk(KERN_ALERT "HI *R \n");
	return 0;
}
void my_exit_function(void)
{
	printk(KERN_ALERT "END OF MODULE MY MOD *R \n");
	pci_clear_master(kyouku_dev);
	pci_disable_device(kyouku_dev);
	pci_unregister_driver(&kyouku_pci_drv);
	cdev_del(&whatever);
}
module_init(my_init_function);
module_exit(my_exit_function);


