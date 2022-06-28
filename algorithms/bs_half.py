import networkx as nx
import math
import numpy as np


def helper(G,demandfrom_v,v,nodes_v,counter,lastAddedNode):
    """
    
    args: 
        G: nx.Graph
        demand_v: demand from vertex v
        nodes_v
        counter
        lastAddedNode: index, init 0
    
    result:
        G: nx.Graoh
    
    """
    k = math.log(len(G.nodes),2)+1
    if len(G.edges(v)) >= k:
        return G
    
    if len(demandfrom_v) == 1:
    #    G.add_edge(v,lastAddedNode)
        return(G)
    
    if counter >= math.log(len(G.nodes),2)-1:
        return G
    #temp = lastAddedNode
    temp_demand = 0
    
    for u in nodes_v:
        if temp_demand >= round(sum(demandfrom_v[lastAddedNode:])/2,2):
            if len(G.edges(u)) < k:
                temp = nodes_v.index(u)
                G.add_edge(v,u)
                break
        temp = nodes_v.index(u)
        temp_demand += demandfrom_v[temp]
    counter += 1
    helper(G,demandfrom_v[temp:],v,nodes_v[temp:],counter,temp)
    return G

def construct_demand_aware_binary_search(G,D):
    n = len(G.nodes)
    for v in G.nodes:
        counter = int(len(G.edges(v))-2)
        demandfrom_v = list(D[v][(v+1 % (n-1)):]) + list(D[v][:(v+1 % (n-1))])
        nodes_v = list(G.nodes)[(v+1 % (n-1)):] + list(G.nodes)[:(v+1 % (n-1))]
        helper(G,demandfrom_v,v,nodes_v,counter,0)
    return G