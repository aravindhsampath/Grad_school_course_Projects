#include<stdio.h>
#include<sys/time.h>
#include<sys/syscall.h>
#include<asm/unistd_64.h>
#include<errno.h>
_syscall1(int,get_stat1,void *,optimal_stat);
_syscall0(void,init_disk_stat)
struct optimal_stat_ty{
	struct timespec arrival_time;
	struct timespec start_of_service;
	struct timespec service_complete_time;
	int pid;	
}optimal_stat[25000];
unsigned long service_time[25000];
struct timespec temp;
unsigned long comp_t_ms,sos_t_ms,serv_t_ms,arr_t_ms,total_resp_time,total_serv_time;
int main(){
// System call to initialize all the counters
init_disk_stat();
sleep(460); // while disk load test is being done
printf("woke up !");
FILE *fp;
fp = fopen("stats_serv_time_optimal.csv","w");
// System call that recieves the array of structures sent by copy_to_user
int res = get_stat1(optimal_stat);
int j;
int no_of_requests = 20000;
for(j=0;j<no_of_requests;j++){
	comp_t_ms = (optimal_stat[j].service_complete_time.tv_sec*1000) + (optimal_stat[j].service_complete_time.tv_nsec/1000000);

	sos_t_ms = (optimal_stat[j].start_of_service.tv_sec*1000) + (optimal_stat[j].start_of_service.tv_nsec/1000000);
	serv_t_ms = comp_t_ms-sos_t_ms;
	arr_t_ms = (optimal_stat[j].arrival_time.tv_sec*1000) + (optimal_stat[j].arrival_time.tv_nsec/1000000);
	total_resp_time += (comp_t_ms-arr_t_ms);
	total_serv_time += serv_t_ms;
	fprintf(fp,"%lu,",serv_t_ms);
}
fprintf(fp,";; The mean response time is :  %lu  milliseconds",(total_resp_time/no_of_requests));
fprintf(fp,"The mean service time is :  %lu  milliseconds",(total_serv_time/no_of_requests));
fclose(fp);
printf("Done !");
return 0;
}
