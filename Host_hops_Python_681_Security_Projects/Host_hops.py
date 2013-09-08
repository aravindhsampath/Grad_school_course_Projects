import networkx as nx
from scapy.all import *
import matplotlib.pyplot as plt

g=nx.Graph()
host=['clemson.edu','fas.clemson.edu','career.clemson.edu','odce.clemson.edu','odce.clemson.edu','features.clemson.edu','mycle.clemson.edu','mycle.clemson.edu','xmail.clemson.edu','bb.clemson.edu','cs.clemson.edu','business.clemson.edu','soc.clemson.edu','ccit.clemson.edu','majorevents.clemson.edu','fas.clemson.edu']
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
	finish_graph()	

def route(h=host):
	b=trcroute(h)

def draw_edge(src,dst):
	g.add_edge(src,dst)

def finish_graph():
	nx.draw(g)
	file_name='host_hops1.png'
	file_nameg='host_hops1.graphml'
	plt.savefig(file_name)
	nx.write_graphml(g, file_nameg)
	print ("Graph Drawn")

def main():
	route()


if __name__=="__main__":
    main()
