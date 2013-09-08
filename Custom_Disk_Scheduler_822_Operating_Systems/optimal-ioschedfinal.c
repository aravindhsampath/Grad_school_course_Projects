/*
 * elevator optimal
 */
#include <linux/blkdev.h>
#include <linux/elevator.h>
#include <linux/bio.h>
#include <linux/module.h>
#include <linux/slab.h>
#include <linux/init.h>


struct requestList{
		struct request *data;
		struct requestList *next;
};

struct pathMember{
	int cost;
	struct requestList *head; 
};

struct optimal_data {
	struct request headpos;
	int max_requests;
	struct list_head arrival_queue;
	struct request **mylist;//complete cscan list
	struct pathMember ***C;
	int shouldBuild;
	int currentNdx;
	int dispatchSize;
	struct request **dispatch_head;
};

static long distance(long x, long y){
	long result = x - y;
	if(result < 0)
		result *= -1;
	return result;
}

static void buildTable(struct request* cscan[], int size, struct pathMember ***C)
{
	int i, j, k; 
	long cost1, cost2;
	if(size < 2) return;
	for(i = 0; i < size; i++){
		C[i][i][0].cost = 0;
		C[i][i][0].head->data = cscan[i];
		C[i][i][0].head->next = NULL;
		C[i][i][1].cost = 0;
		C[i][i][1].head->data = cscan[i];
		C[i][i][1].head->next = NULL;
	}
	for(k=0; k < size - 1; k++){
		for(i=0, j=k+1; j<size; i++, j++){
			//build left
			cost1 = ((j-(i+1))+1) * 
			distance(blk_rq_pos(cscan[i]),blk_rq_pos(cscan[i+1])) +
			C[i+1][j][0].cost;

			cost2 = ((j-(i+1))+1) *
			distance(blk_rq_pos(cscan[i]),blk_rq_pos(cscan[j])) +
			C[i+1][j][1].cost;

			if(cost1 < cost2){
				C[i][j][0].cost = cost1;
				C[i][j][0].head->data = cscan[i+1];
				if(i+1 != j)
					C[i][j][0].head->next = C[i+1][j][0].head;
				else
					C[i][j][0].head->next = NULL;
			}
			else{
				C[i][j][0].cost = cost2;
				C[i][j][0].head->data = cscan[j];
				if(i+1 != j)
					C[i][j][0].head->next = C[i+1][j][1].head;
				else
					C[i][j][0].head->next = NULL;
			}
			
			//build right
			cost1 = (((j-1)-i)+1) *
			distance(blk_rq_pos(cscan[j]),blk_rq_pos(cscan[j-1])) + 
			C[i][j-1][1].cost;

			cost2 = (((j-1)-i)+1) *
			distance(blk_rq_pos(cscan[j]), blk_rq_pos(cscan[i])) +
			C[i][j-1][0].cost;

			if(cost1 < cost2){
				C[i][j][1].cost = cost1;
				C[i][j][1].head->data = cscan[j-1];
				if(i!=j-1)
					C[i][j][1].head->next = C[i][j-1][1].head;
				else
					C[i][j][1].head->next = NULL;
			}
			else{
				C[i][j][1].cost = cost2;
				C[i][j][1].head->data = cscan[i];
				if(i!=j-1)
					C[i][j][1].head->next = C[i][j-1][0].head;
				else
					C[i][j][1].head->next = NULL;
			}

		}
	}
}


static void optimal_merged_requests(struct request_queue *q, struct request *rq,
				 struct request *next)
{
	struct optimal_data *nd = q->elevator->elevator_data;
	nd->shouldBuild = 1;
	list_del_init(&next->queuelist);
	
}

//if shouldBuild dirty bit is set, combine c-scan lists into one list and buildTable
//use headposition and table build to make best path
//turn dirty shouldBuild dirty bit off
//dispatch first guy in path
//set new head position
static int optimal_dispatch(struct request_queue *q, int force)
{
	int size = 0, ndx = 1;
	long cost1, cost2;
	struct list_head *entry;
	struct requestList *scan;
	struct optimal_data *nd = q->elevator->elevator_data;
	if(nd->shouldBuild){
		//put everything in my cscan list into an array of requests
		//in cscan order
		entry = &nd->arrival_queue;
		while(((entry = entry->next)!=&nd->arrival_queue)&&size<nd->max_requests){
			nd->mylist[size] = list_entry_rq(entry);
			size++;
		}
		if(size == 0){
			nd->dispatchSize = 0;
			nd->currentNdx = 0;
			return 0;
		}
		//might be redundant
		if(size > nd->max_requests)
			size = nd->max_requests;

		buildTable(nd->mylist, size, nd->C);

		
		cost1 = ((size-1) + 1) * distance(blk_rq_pos(&nd->headpos), blk_rq_pos(nd->mylist[0])) + nd->C[0][size-1][0].cost;
		cost2 = ((size-1) + 1) * distance(blk_rq_pos(&nd->headpos), blk_rq_pos(nd->mylist[size-1])) + nd->C[0][size-1][1].cost;
		if(cost1 < cost2){
			nd->dispatch_head[0] = nd->mylist[0];
			//for each item in C[0][size-1][0]'s path, add to dispatch_head
			scan = nd->C[0][size-1][0].head;
			while(scan != NULL && scan->data != NULL){
				nd->dispatch_head[ndx] = scan->data;
				ndx++;
				scan = scan->next;
			}
		}
		else{
			nd->dispatch_head[0] = nd->mylist[size-1];
			scan = nd->C[0][size-1][1].head;
			while(scan != NULL && scan->data != NULL){
				nd->dispatch_head[ndx] = scan->data;
				ndx++;	
				scan = scan->next;
			}
		}
		nd->dispatchSize = size;
		nd->currentNdx = 0;
		nd->shouldBuild = 0;
	}

	/*
	if (!list_empty(&nd->arrival_queue)) {
		struct request *rq;
		rq = list_entry(nd->arrival_queue.next, struct request, queuelist);
		nd->headpos.__sector =rq_end_sector(rq);
		list_del_init(&rq->queuelist);
		elv_dispatch_add_tail(q, rq);
		nd->currentNdx++;
		return 1;
	}
	*/
	if(nd->currentNdx < nd->dispatchSize){
		struct request *rq;
		rq = nd->dispatch_head[nd->currentNdx];
		nd->headpos.__sector = rq_end_sector(rq);
		list_del_init(&rq->queuelist);
		elv_dispatch_add_tail(q, rq);
		nd->currentNdx++;
		return 1;
	}
	return 0;
} 

//here we c-scan sort each new request
//set buildTable dirty bit on
#define INORDER(rq1, rq2) ((blk_rq_pos(rq1) < blk_rq_pos(rq2))?1:0)

static void optimal_add_request(struct request_queue *q, struct request *rq)
{
	struct optimal_data *nd = q->elevator->elevator_data;
	
	int head_before_req, req_before_entry, entry_before_head;
	struct list_head *entry;
	nd->shouldBuild = 1;
	
	entry = &nd->arrival_queue;
	
	head_before_req = INORDER(&nd->headpos, rq);
	while((entry=entry->next) != &nd->arrival_queue){//&nd->headpos is the problem here
		req_before_entry = INORDER(rq, list_entry_rq(entry));
		entry_before_head = INORDER(list_entry_rq(entry),&nd->headpos);
		if(head_before_req && (req_before_entry || entry_before_head)) break;
		if(!head_before_req && req_before_entry && entry_before_head) break;
	}
	
	list_add_tail(&rq->queuelist, entry);
	return;

}

//is rq in my dispatch queue lists yet?
static struct request *
optimal_former_request(struct request_queue *q, struct request *rq)
{
	struct optimal_data *nd = q->elevator->elevator_data;

	if ((nd->shouldBuild != 1) || rq->queuelist.prev == &nd->arrival_queue)
		return NULL;
	return list_entry(rq->queuelist.prev, struct request, queuelist);
}


static struct request *
optimal_latter_request(struct request_queue *q, struct request *rq)
{
	struct optimal_data *nd = q->elevator->elevator_data;

	if ((nd->shouldBuild != 1) || rq->queuelist.next == &nd->arrival_queue)
		return NULL;
	return list_entry(rq->queuelist.next, struct request, queuelist);
}

//set head position to 0
//get max size of request_queue q->nr_requests
//allocate space of arrays based on max size
//set counts to 0
//allocate space for table
static void *optimal_init_queue(struct request_queue *q)
{
	struct optimal_data *nd;
	int i, j, k;

	nd = kmalloc_node(sizeof(*nd), GFP_KERNEL, q->node);
	if (!nd)
		return NULL;
	/*
	for(i=0; i<2; i++){
		nd->counts[i] = 0;
	}
	*/
	nd->headpos.__sector = 0;
	nd->max_requests = q->nr_requests;
	nd->shouldBuild = 1;
	nd->currentNdx = 0;
	nd->dispatchSize = 0;
	nd->C = kmalloc(nd->max_requests*sizeof(struct pathMember **), GFP_KERNEL);
	for(i=0; i<nd->max_requests; i++){
		nd->C[i] = kmalloc(nd->max_requests*sizeof(struct pathMember*), GFP_KERNEL);
		for(j=0; j<nd->max_requests; j++) nd->C[i][j] = kmalloc(2*sizeof(struct pathMember), GFP_KERNEL);
	}
	nd->mylist = kmalloc(nd->max_requests*sizeof(struct request*), GFP_KERNEL);
	nd->dispatch_head = kmalloc(nd->max_requests*sizeof(struct request*), GFP_KERNEL);
	for(i = 0; i < nd->max_requests; i++){
		nd->C[i][i][0].head = kmalloc(sizeof(struct requestList), GFP_KERNEL);
		nd->C[i][i][1].head = kmalloc(sizeof(struct requestList), GFP_KERNEL);
	}
	for(k=0; k<nd->max_requests-1; k++){
		for(i = 0, j = k+1; j < nd->max_requests; i++, j++){
			nd->C[i][j][0].head = kmalloc(sizeof(struct requestList), GFP_KERNEL);
			nd->C[i][j][1].head = kmalloc(sizeof(struct requestList), GFP_KERNEL);
		}
	}
	
	
	INIT_LIST_HEAD(&nd->arrival_queue);
	return nd;
}

//free all tables and allocated data
static void optimal_exit_queue(struct elevator_queue *e)
{
	int i, j, k;
	struct optimal_data *nd = e->elevator_data;
	
	for(k=0; k<nd->max_requests-1; k++){
		for(i = 0, j = k+1; j < nd->max_requests; i++, j++){
			kfree(nd->C[i][j][0].head);
			kfree(nd->C[i][j][1].head);
		}
	}
	for(i = 0; i < nd->max_requests; i++){
		kfree(nd->C[i][i][0].head);
		kfree(nd->C[i][i][1].head);
	}
	
	kfree(nd->mylist);
	kfree(nd->dispatch_head);
	for(i=0; i<nd->max_requests; i++){	
		for(j=0; j<nd->max_requests; j++) kfree(nd->C[i][j]);
	}
	for(i=0;i<nd->max_requests;i++){
		kfree(nd->C[i]);
	}
	
	kfree(nd->C);
		
	BUG_ON(!list_empty(&nd->arrival_queue));
	kfree(nd);
}

static struct elevator_type elevator_optimal = {
	.ops = {
		.elevator_merge_req_fn		= optimal_merged_requests,
		.elevator_dispatch_fn		= optimal_dispatch,
		.elevator_add_req_fn		= optimal_add_request,
		.elevator_former_req_fn		= optimal_former_request,
		.elevator_latter_req_fn		= optimal_latter_request,
		.elevator_init_fn		= optimal_init_queue,
		.elevator_exit_fn		= optimal_exit_queue,
	},
	.elevator_name = "optimal",
	.elevator_owner = THIS_MODULE,
};

static int __init optimal_init(void)
{
	elv_register(&elevator_optimal);
	return 0;
}

static void __exit optimal_exit(void)
{
	elv_unregister(&elevator_optimal);
}

module_init(optimal_init);
module_exit(optimal_exit);


MODULE_AUTHOR("OFriel, Sampath, Thomas, Pai, Lawson, Ji");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Optimal IO scheduler");
