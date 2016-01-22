import networkx as nx
import csv
import matplotlib.pyplot as plt
import datetime
import collections
import random
import snap

edge_list = open('anon_edge_list.csv', 'rb')
G = nx.read_edgelist(edge_list, delimiter=',', nodetype = str, create_using = nx.DiGraph())
edge_list.close()

print len(G.nodes())
print len(G.edges())

def plot_graph(G):
	print "Before layout: ", datetime.datetime.now()
	pos = nx.spring_layout(G)
	print "Before nx draw: ",datetime.datetime.now()
	nx.draw(G,pos,node_color='w',node_size=100)
	plt.draw()
	plt.savefig("LinkedInGraph.png")
	plt.show()

def plot_distribution(G):
	in_degree_sequence = sorted(G.in_degree().values(), reverse = True)
	plt.loglog(in_degree_sequence, 'b-', marker = 'o')
	plt.save("InDegreeDistribution.png")
	plt.show()

	out_degree_sequence = sorted(G.out_degree().values(), reverse = True)
	plt.loglog(out_degree_sequence, 'b-', marker = 'o')
	plt.save("OutDegreeDistribution.png")
	plt.show()

def plot_distribution_snap():
	SG = snap.LoadEdgeList(snap.PNGraph, "anon_edge_list_tab.txt", 0, 1)
	snap.PlotInDegDistr(SG, "InDegreeDistribution", "In-degree Distribution", 'True', 'True')
	snap.PlotOutDegDistr(SG, "OutDegreeDistribution", "Out-degree Distribution", 'True', 'True')

def convert_to_undirected(G):
	print "Converting to undirected: ", datetime.datetime.now()
	UG = G.to_undirected()
	return UG

def compute_diameter(G):
	print "Computing diameter: ", datetime.datetime.now()
	diameter = nx.diameter(G)
	print "diameter: ", diameter
	write_to_file('Diameter', diameter)

def compute_3cycles(G):
	print "Computing 3-cycles: ", datetime.datetime.now()
	triangles = nx.triangles(G)
	triangles_total = 0
	for value in triangles.values():
		triangles_total += value
	triangles_total = triangles_total / 3
	print "# of 3-cycles: ", triangles_total
	write_to_file('Number of 3-cycles', triangles_total)

def compute_bridges():
	UG = snap.LoadEdgeList(snap.PUNGraph, "anon_edge_list_tab.txt", 0, 1)
	edgeV = snap.TIntPrV()
	snap.GetEdgeBridges(UG, edgeV)
	bridges = 0
	for edge in edgeV:
		bridges += 1
	print 'Bridges: ', bridges
	write_to_file('Bridges', bridges)

def remove_edges(UG):
	SizeDict = {}
	edges = UG.edges()
	edge_count = len(UG.edges())
	for x in range(1, 101):
		edges = UG.edges()
		removable = (edge_count*x/100)
		while removable:
			index = random.randrange(len(edges))
			edges.pop(index)
			removable -= 1
		print x, len(edges)
		SampledGraph = nx.Graph()
		SampledGraph.add_nodes_from(UG)
		SampledGraph.add_edges_from(edges)
		GiantComponent = max(nx.connected_components(SampledGraph), key = len)
		SizeOfGiant = len(GiantComponent)
		SizeDict[x] = SizeOfGiant
		print x, SizeOfGiant
	print len(SizeDict)
	write_to_file('GiantComponent', SizeDict)
	return SizeDict

def sampling_plot(d):
	plt.plot(d.keys(), d.values(), "ro")
	plt.axis([0, max(d.keys()), 0, max(d.values())])
	plt.savefig('GiantComponentGraph.png')
	plt.show()

def write_to_file(measure, value):
	with open('p2_output.txt', 'a') as f:
		f.write(measure + "\t:\t" +str(value)+"\n")


UG = convert_to_undirected(G)
plot_graph(G)
#plot_distribution(G)
plot_distribution_snap()
compute_bridges()
compute_diameter(UG)
compute_3cycles(UG)
SampledPlotDict = remove_edges(UG)
print SampledPlotDict
sampling_plot(SampledPlotDict)
