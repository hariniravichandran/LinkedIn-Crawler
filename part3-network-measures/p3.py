import networkx as nx
import csv
import matplotlib.pyplot as plt
import datetime
import collections

edge_list = open('anon_edge_list.csv', 'rb')
G = nx.read_edgelist(edge_list, delimiter=',', nodetype = str, create_using = nx.DiGraph())
edge_list.close()

print len(G.nodes())
print len(G.edges())

def compute_clustering(G):
	print "Computing average clustering coefficient: ", datetime.datetime.now()
	lc = nx.average_clustering(G)
	print lc
	write_to_file('Average local clustering coefficient', lc)
	gc = nx.transitivity(G)
	print gc
	write_to_file('Average global clustering coefficient', gc)

def compute_pagerank(G):
	print "Computing pagerank: ", datetime.datetime.now()
	pr = nx.pagerank(G)
	top_10_pr = collections.Counter(pr).most_common(10)
	print top_10_pr
	write_to_file('Top 10 nodes according to pagerank', top_10_pr)

def compute_ev_centrality(G):
	print "Computing eigenvector_centrality: ", datetime.datetime.now()
	evc = nx.eigenvector_centrality(G)
	top_10_ev = collections.Counter(evc).most_common(10)
	print top_10_ev
	write_to_file('Top 10 nodes according to eigenvector_centrality', top_10_ev)

def compute_degree_centrality(G):
	print "Computing in_degree_centrality: ", datetime.datetime.now()
	dc = nx.in_degree_centrality(G)
	top_10_dc = collections.Counter(dc).most_common(10)
	print top_10_dc
	write_to_file('Top 10 nodes according to degree centrality', top_10_dc)

def compute_jaccard_similarity(G):
	print "Computing Jaccard similarity: ", datetime.datetime.now()
	tuples = nx.jaccard_coefficient(G)
	j_dict = {}
	jaccard_dict = {}
	count = 1
	for x, y, j in tuples:
		print count
		count+=1
		j_dict[(x,y)] = j
		if j == 1:
			jaccard_dict[(x,y)] = j
			max_j = x, y, j
			break
	print "Dict written"
	max_jaccard = max_j if max_j else collections.Counter(j_dict).most_common(1)
	print max_jaccard
	write_to_file('Two most similar nodes by Jaccard', max_jaccard)

def write_to_file(measure, value):
	with open('p3_output.txt', 'a') as f:
		f.write(measure + "\t:\t" +str(value)+"\n")

UG = G.to_undirected()
compute_clustering(UG)
compute_pagerank(G)
compute_ev_centrality(G)
compute_degree_centrality(G)
compute_jaccard_similarity(UG)