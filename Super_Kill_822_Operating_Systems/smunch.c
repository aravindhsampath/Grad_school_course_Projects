#include <linux/linkage.h>
#include <linux/kernel.h>
#include <linux/sched.h>
#include <linux/pid.h>
#include <linux/types.h>
#include <linux/wait.h>

int smunch(int pid, unsigned long bit_pattern) {
	struct task_struct *target;
	unsigned long flags;
	
	rcu_read_lock();
	target=find_task_by_vpid(pid);  // get the process table entry
	rcu_read_unlock();
	printk(KERN_ALERT "Found the process table entry \n");

	if(!target || (!lock_task_sighand(target,&flags))) return -1;  // if process not found or could not acquire the lock on the sig handler of the target process
	
	if(!thread_group_empty(target)) {   // if not single threaded
		printk(KERN_ALERT "process is multithreaded ! \n");
		unlock_task_sighand(target,&flags);
		return -1;
	}

	if((target->exit_state & (EXIT_ZOMBIE | EXIT_DEAD)) && (bit_pattern & (1 << (SIGKILL-1)))) {
		printk(KERN_ALERT "process is   z or dead and kill bit is set! \n");
		unlock_task_sighand(target, &flags);
		release_task(target);
	}
	else {
		if(bit_pattern & (1 << (SIGKILL-1))) {
			printk(KERN_ALERT "kill bit is set! and not a zombie \n");
			sigaddset(&target->signal->shared_pending.signal, SIGKILL);
			wake_up_process(target);
		}
		else if(!(target->exit_state & (EXIT_ZOMBIE | EXIT_DEAD))){
			printk(KERN_ALERT "not a zombie and not kill bit \n");
			target->signal->shared_pending.signal.sig[0] = bit_pattern;
			set_tsk_thread_flag(target,TIF_SIGPENDING);
			wake_up_process(target);
		}
		else{			
			printk(KERN_ALERT "zombie but not kill bit \n");
		}
		unlock_task_sighand(target, &flags);
	}
	return 0;
}
