import networkx as nx
from scapy.all import *

g=nx.Graph()
host=['clemson.edu','cs.clemson.edu']
hops=[]
global b

def trcroute(urls):
	for url in urls:
		try:	
			print ("Tracing :"+url)
			a,u=traceroute([url])
			for i in range(len(a)):	
				hops.append(a[i][1].src)
				g.add_node(a[i][1].src)
				print (a[i][1].src)
				j=i-1
				if (j>=0):
					draw_edge(hops[i],hops[j])
					if (hops[j]==hops[i]):
						print ("hop detected :"+hops[j])
						del(hops[j])					
						break
			print hops
			for i in range(len(hops)):
				print ("Node removed :"+hops.pop())
			a.clear()
		except:
			pass

def route(h=host):
	b=trcroute(h)

def draw_edge(src,dst):
	g.add_edge(src,dst)

def main():
	route()


if __name__=="__main__":
    main()
