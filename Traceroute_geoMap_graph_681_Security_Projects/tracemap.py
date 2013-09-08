from scapy.all import *
import sys
import socket
import matplotlib.pyplot as plt
import networkx as nx
import simplekml
import GeoIP

targets = ['130.127.200.19', '130.127.235.65', '130.127.69.57', '130.127.8.221', '130.127.62.178', '130.127.56.8', '130.127.21.72', '130.127.235.144', '130.127.235.56', '130.127.49.41', '130.127.236.91', '130.127.69.75', '130.127.130.253', '130.127.69.73', '130.127.235.49']
kml = simplekml.Kml()

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

g.add_node("172.22.96.1")
nodes_added = ["172.22.96.1"]
node_list = set ([])
for l in target_hops:
	node_list.update(l)
gic=GeoIP.open('/home/aravindh/Downloads/GeoLiteCity.dat',GeoIP.GEOIP_STANDARD)
counter = 0
print "node list is ---> " ,node_list
for node in node_list:
	g.add_node(node)
	print "node is -->  " ,node
	try:
		longitude = gic.record_by_addr(node)['longitude']
		latitude = gic.record_by_addr(node)['latitude']
		coords = (longitude,latitude)
		print "Co ords is ----> ",coords
		kml.newpoint(name = node,coords=[coords])
		print "new point created in the map"
	except:
		pass
i = 0
color = "bgrcmyk"*10
pos=nx.random_layout(g)
nx.draw_networkx_nodes(g,pos,node_color = 'r')
nx.draw_networkx_labels(g,pos,font_size =8)
for ip in target_hops:
	c = color[i]
 
	i = i+1
	for n in range(len(ip)-1):
		g.add_edge(ip[n],ip[n+1])
		g[ip[n]][ip[n+1]]['color']= c
		nx.draw_networkx_edges(g,pos,edgelist = [(ip[n],ip[n+1])],edge_color = c)
kml.save("nodes.kml")
#nx.write_graphml(g,"traceroutewithcolormap.graphml")
#plt.savefig("/home/aravindh/traceroutewithcolormap.png")

