import networkx as nx
import csv
import matplotlib.pyplot as plt
import datetime
import math

edge_list = open('anon_edge_list.csv', 'rb')
G = nx.read_edgelist(edge_list, delimiter=',', nodetype = str, create_using = nx.DiGraph())
edge_list.close()

UG = G.to_undirected()
nodes = len(UG.nodes())
edges = len(UG.edges())
exp_degree = 2*edges / float(nodes)

print "Dataset: ", nodes, edges, exp_degree
average_path_length = {}
clustering_coefficient = {}

print "Computing average_path_length"
average_path_length['Dataset'] = nx.average_shortest_path_length(UG)
clustering_coefficient['Dataset'] = nx.average_clustering(UG)
print average_path_length, clustering_coefficient

def plot_distribution(G, name):
	degree_sequence = sorted(nx.degree(G).values(), reverse = True)
	plt.loglog(degree_sequence, 'b-', marker = 'o')
	plt.savefig("DegreeDistribution_last_"+ name +".png")
	plt.show()

p_rand = float(exp_degree) / float(nodes - 1)
print "Random: ", datetime.datetime.now()
RG = nx.erdos_renyi_graph(nodes, p_rand)
print len(RG.nodes()), len(RG.edges())
print "Computing average_path_length"
average_path_length['Random_Graph'] = math.log(nodes)/float(math.log(exp_degree))
print "Computing clustering_coefficient"
clustering_coefficient['Random_Graph'] = nx.average_clustering(RG)
print average_path_length, clustering_coefficient
plot_distribution(RG, '_random')

print "Small World: ", datetime.datetime.now()
C0 = 3*(exp_degree-2)/float(4*(exp_degree-1))
Cp = clustering_coefficient['Dataset']
sw_p = 1-(Cp/C0)**(1/3.0)
print Cp, sw_p
SWG = nx.connected_watts_strogatz_graph(nodes, int(exp_degree), sw_p)
print len(SWG.nodes()), len(SWG.edges())
print "Computing average_path_length"
average_path_length['Small_World'] = nx.average_shortest_path_length(SWG)
print "Computing average_path_length"
clustering_coefficient['Small_World'] = nx.average_clustering(SWG)
print average_path_length, clustering_coefficient
plot_distribution(SWG, '_small_world')


print "Preferential Attachment: ", datetime.datetime.now()
PAG = nx.barabasi_albert_graph(nodes, int(exp_degree))
average_path_length['Preferential_Attachment'] = nx.average_shortest_path_length(PAG)
clustering_coefficient['Preferential_Attachment'] = nx.average_clustering(PAG)
print average_path_length, clustering_coefficient
plot_distribution(PAG, '_preferential_attachment')
GraphTypes = ['Dataset','Random_Graph','Small_World','Preferential_Attachment']
f = open('p4_output.txt', "a")
f.write("\nAverage Path Length: "+"\n")
for item in GraphTypes:
	f.write("\n"+item+" :\t")
	if average_path_length.has_key(item):
		f.write(str(average_path_length[item]))

f.write("\n\nClustering Coefficient: "+"\n")
for item in GraphTypes:
	f.write("\n"+item+" :\t")
	if clustering_coefficient.has_key(item):
		f.write(str(clustering_coefficient[item]))
f.close()
