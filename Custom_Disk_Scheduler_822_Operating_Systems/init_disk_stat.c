#include <linux/linkage.h>
#include <linux/kernel.h>
#include <linux/time.h>
extern struct timespec sum_services;
extern struct timespec sum_waits;
extern unsigned int no_requests;
void init_disk_stat(){

	printk(KERN_ALERT "initializing global vars \n");
	sum_services.tv_sec = 0;
	sum_services.tv_nsec = 0;
	sum_waits.tv_sec = 0;
	sum_waits.tv_nsec = 0;
	no_requests = 0;
	
}
