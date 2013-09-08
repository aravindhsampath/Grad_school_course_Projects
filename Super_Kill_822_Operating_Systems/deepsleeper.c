#include <linux/wait.h>
#include <linux/sched.h>

DECLARE_WAIT_QUEUE_HEAD(gone);

void deepsleep() {
sleep_on(&gone);
}
