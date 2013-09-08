import matplotlib.pyplot as plt

# Read the stats as string from all three input files
f = open("stats_serv_time_optimal.csv","r")      # optimal scheduler
f1 = open("stats2.csv","r")              # deadline scheduler
f2 = open("stats_serv_time_cfq.csv","r") #CFQ scheduler
s = f.read()
s1 = f1.read()
s2 = f2.read()

# list of individual service times
# optimal
l = []
t = s.split(";;")        # to chuck off the averages
l = t[0][0:-1].split(",")
# for deadline
l1 = []
l1 = s1[0:-1].split(",")
# for cfq
l2 = []
t2 = s2.split(";;")
l2 = t2[0][0:-1].split(",")
l = l[500:]     # ignore the first 500 requests
l1 = l1[500:]   # ignore the first 500 requests
l2 = l2[500:]   # ignore the first 500 requests

print "total records from optimal is "+str(len(l))
print str(t[1])
print "total records from deadline is "+str(len(l1))
print "total records from cfq is "+str(len(l2))
print str(t2[1])

no_of_reqs = len(l)
# plot the results for Optimal Scheduler
intlist = []
sortlist = []
for item in l:
	intlist.append(int(item))
	sortlist.append(int(item))
sortlist.sort()
max = max(sortlist)
result = [0]*max
for timeres in intlist:
	for i in range(timeres,max):
 		result[i] += 1
x = []
for num in range(len(result)):
	x.append(num)
test = []
for r in result:
	test.append(r-300)
plt.plot(x,result,'r',label = 'Optimal scheduler')

# plot the results for the deadline scheduler
intlist1 = []
for item in l1:
	intlist1.append(int(item))
result1 = [0]*max
for timeres in intlist1:
	for i in range(timeres,max):
 		result1[i] += 1
plt.plot(x,result1,'g',label = 'deadline scheduler')


# plot the results for the cfq scheduler
intlist2 = []
for item in l2:
	intlist2.append(int(item))
result2 = [0]*max
for timeres in intlist2:
	for i in range(timeres,max):
 		result2[i] += 1
plt.plot(x,result2,'b',label = 'CFQ scheduler')


plt.axis([0,max,0,no_of_reqs+500])
plt.title("Service Distribution of Disk scheduling alorithms")
plt.xlabel("Service time(t) in milliseconds")
plt.ylabel("no.of requests served under time (t)")
plt.legend(loc='lower right')
plt.savefig("diskschedplot.png",bbox_inches=0)
plt.show()

