from scapy.all import *
import sys
import socket
import matplotlib.pyplot as plt
import networkx as nx

targets = ['130.127.200.19', '130.127.235.65', '130.127.69.57', '130.127.8.221', '130.127.62.178', '130.127.56.8', '130.127.21.72', '130.127.235.144', '130.127.235.56', '130.127.49.41', '130.127.236.91', '130.127.69.75', '130.127.130.253', '130.127.69.73', '130.127.235.49']


#172.22.100.75

target_hops = []
for target in targets:
	ans,unans = traceroute(target)
	hops = []
	h_key = ans.get_trace().keys()[0]
	for key in ans.get_trace()[h_key].keys():
		hops.append(ans.get_trace()[h_key][key][0])
	target_hops.append(hops)
print target_hops
g = nx.Graph()

#g.add_node("172.22.96.1")
g.add_node(socket.gethostbyname(socket.gethostname()))
#nodes_added = ["172.22.96.1"]
nodes_added = [socket.gethostbyname(socket.gethostname())]
#nx.draw_networkx_nodes(g,pos,nodelist = ["172.22.96.1"],node_color = 'r')
#node_list = list(set(target_hops))
node_list = set ([])
for l in target_hops:
	node_list.update(l)
print "The set - node_list is ",node_list

for node in node_list:
	g.add_node(node)
i = 0
color = "bgrcmyk"*10
pos=nx.random_layout(g)
nx.draw_networkx_nodes(g,pos,node_color = 'r')
nx.draw_networkx_labels(g,pos,font_size =8)
for ip in target_hops:
	c = color[i]
	print "the color for now is ---   ",c  
	i = i+1
	for n in range(len(ip)-1):
#		pos=nx.spring_layout(g)
#		if ip[n+1] not in nodes_added:
#			g.add_node(ip[n+1])
#			nodes_added.append(ip[n+1])
#			nx.draw_networkx_nodes(g,pos,nodelist = [ip[n+1]],node_color = 'r')
#			print "The nodes_added list at this point is :   " ,nodes_added	
		g.add_edge(ip[n],ip[n+1])
		g[ip[n]][ip[n+1]]['color']= c
		nx.draw_networkx_edges(g,pos,edgelist = [(ip[n],ip[n+1])],edge_color = c)
	#nx.draw_networkx_nodes(g,pos,node_color = 'r')


#nx.draw(g)
#nx.draw_networkx(g,node_color='r')
nx.write_graphml(g,"traceroutewithcolorhome.graphml")
plt.savefig("/home/aravindh/traceroutewithcolorhome.png")
