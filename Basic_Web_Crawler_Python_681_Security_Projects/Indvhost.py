import urllib2
from BeautifulSoup import *
import urlparse
from collections import deque
from networkx import *
import matplotlib.pyplot as plt
import networkx as nx
import socket

g=nx.Graph()
root_ip=socket.gethostbyname(urlparse.urlparse('http://clemson.edu').netloc)
g.add_node(root_ip)

done=set()
link_dic={}
link_dic['http://clemson.edu']='-1'
qu=deque()

#It ll check whether the current URL is in clemson domain

def check_url(url):
	for iter in done:
		if(iter==url):    
			return 'read'
		if(iter=='#'):
			return '#'
	result=urlparse.urlparse(url)
	if ('clemson.edu' in result.netloc) and ('pdf' not in result.path) and ('jpg' not in result.path):
		return 'true'
	else:
		return 'false'


#Crawler Function

def crawl(links='http://www.clemson.edu',depth=1):
	qu.append('http://clemson.edu')
	nol=1             #Maintains no of links fetched
	curr_depth=0         #Maintains no of depth levels
	#print ("Entering while")
	while(True):
		try:
			links=qu.popleft(); 
			link=links.replace('/www.','/')
			#print ("popped link :" +link)                
			if(int(link_dic[link])<depth):
				#print('depth check passed')
				if((int(link_dic[link]))==0):
					curr_depth=1
				"""if((int(link_dic[link]))==1):
					curr_depth=2"""
				try:
					#print('enter3')
					if(check_url(link)=='true'):				#check whether a URL is n clemson.edu domain
						try:
                            				#print ('Link verified')
							pagelink=urllib2.urlopen(link)			#opening a link
							root_link=link					#assign root link to a varaiable to plot in graph
							root_ip=socket.gethostbyname(urlparse.urlparse(link).netloc)
							done.add(link)					#add links to a set to avoid repeatation of check
							soup=BeautifulSoup(pagelink.read())
							link=soup.findAll('a')
							for lin in link:
								if('href' in dict(lin.attrs)):
									#print (lin['href'])
									if(lin['href'].find('http')!=-1):
										hre=lin['href'].replace('/www.','/')
									else:
										hre=lin['href']
									#print ('%i >> parent_link : %s >> F_link : %s >> depth : %i'%(nol,root_link, hre,curr_depth))
									present_link=hre   			        #storing a present link for further use
									try:							
										present_ip=socket.gethostbyname(urlparse.urlparse(hre).netloc)
									except:
										continue
		                    					print ('%s : %s'%(hre, present_ip))
									#check_ind_host(hre)
									find_http(hre)
									link_dic[hre]=curr_depth
									nol=nol+1
									if(present_ip != root_ip) and (present_ip !='') and (root_ip!=''):
										g.add_node(present_ip)  		# add a present checking link as node
										draw_graph(root_ip,present_ip)
						except:
							print('cannot open link :'+link)
					elif(check_url(link)=='read'):
						print('URL already used :'+link)
					elif(check_url(link)=='#'):
						print('# link')
					else:
						print('Outside link :'+link)  
				except:
					print('cannot open link(2) :'+link)
		except:
			print ("Rendering Graph")
			nx.draw_networkx(g,node_size=30,with_labels=True,node_color='red')
			file_name='Indvhost_%s%s'%(depth,'.png')
			plt.savefig(file_name)
			nx.write_graphml(g, "PhyHost.graphml")
			print ("Finished")
			break

"""check whether the link is HTTP before appending to queue"""
def find_http(hre):
	#print('appending into queue')
	if(hre.find('http://')==0):
		qu.append(hre)

"""To Draw the edges of the graph"""
def draw_graph(link1,link2):
    g.add_edge(link1,link2)   

"""TO find the individual host in the server"""
def check_ind_host(hre):
	link=hre.replace('/www.','/')
	result=urlparse.urlparse(hre)
	#print(result)
	result_host=result.scheme+'://'+result.netloc
	#print(result_host)
	if((result.path=='') or (result.path=='/')) and ('clemson.edu' in result.netloc):
		i.add_node(result_host)
		i.add_edge('http://clemson.edu',result_host)
	return

def main():
    crawl()

if __name__=="__main__":
    main()
