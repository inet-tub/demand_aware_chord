import networkx as nx
import numpy as np
import math

def init_ring(n):
    """Initializes a graph in ring structure with n nodes
    
    Args: 
        n (int): number of nodes
    
    Returns:
        G (networkx.classes.graph.Graph): Graph in ring structure
    """
    G = nx.Graph()
    for i in range(n): G.add_node(i)
    for i in range(n-1): G.add_edge(i,i+1)
    G.add_edge(0,n-1)
    #pos = nx.circular_layout(G)
    #nx.draw_networkx(G,pos=pos,with_labels=True)
    return(G)
# Demand Matrices:
def init_uniformDemand_matrix(G):
    """Returns a demand matrix, where each peer pair has the same demand in %
    
    Args:
        G (networkx.classes.graph.Graph): 
        
    Returns:
        D (numpy.ndarray): matrix with unformly distributed demands for all node pairs
    
    """
    nodesList = G.nodes
    uniformTraffic = round(1/(len(nodesList)-1),8)
    D = np.full((len(nodesList),len(nodesList)),uniformTraffic)
    for i in range(len(nodesList)):
        for j in range(len(nodesList)):
            if i >= j:
                D[i][j] = 0
    return D

def init_uniformDemand_matrix_symmetric(G):
    """Returns a demand matrix, where each peer pair has the same demand in %
    
    Args:
        G (networkx.classes.graph.Graph): 
        
    Returns:
        D (numpy.ndarray): matrix with unformly distributed demands for all node pairs
    
    """
    nodesList = G.nodes
    uniformTraffic = round(1/(len(nodesList)-1),8)
    D = np.full((len(nodesList),len(nodesList)),uniformTraffic)
    for i in range(len(nodesList)):
        D[i][i] = 0
    return D
## Zipf

def init_zipfDemandM(G):
    """Returns a demand matrix, where each peer pair has the same demand in %
    
    Args:
        G (networkx.classes.graph.Graph): 
        
    Returns:
        D (numpy.ndarray): matrix with zipfian distributed demands for all node pairs
    
    """
    nodesList = G.nodes
    D = np.full((len(nodesList),len(nodesList)),0.0)
    for i in range(len(nodesList)):
        zipfTraffic = np.random.zipf(2,len(nodesList)-1)
        sumZipf = sum(zipfTraffic)
        for j in range(i+1,len(nodesList)):
            D[i][j] = zipfTraffic[j-1]/sumZipf
            D[j][i] = zipfTraffic[j-1]/sumZipf
    return D



def complete_node_pair_list(G):
    """
    Returns: list of all possible outgoin node pairings. One row per node at row index
    """
    nodePairList =[]
    nodes = G.nodes
    for i in G.nodes:
        for j in G.nodes:
            nodePairList.append((i,j))
    return nodePairList

def complete_node_pair_list_noDuplication(G):
    """
    Returns: list of all possible node pairings without duplication
    """
    nodePairList =[]
    nodes = G.nodes
    for i in G.nodes:
        for j in range(i+1,len(G.nodes)):
            nodePairList.append((i,j))
    return nodePairList

def calc_cost(G,D):
    """Returns the cost of traffic on a graph
    
    Args:
        G (networkx.classes.graph.Graph): network graph
        D (numpy.ndarray): Demand Graph
    Returns:
        cost (numpy.ndarray): cost of total traffic between nodes of G (i.e. the number of nodes in the path minus 1)
    """
    nodesList = complete_node_pair_list(G)
    allShortestPath = nx.shortest_path(G)
    allShortestPathCost = [(len(allShortestPath[i][j])-1)*D[i][j] for (i,j) in nodesList]
    return sum(allShortestPathCost)

def calc_totalTrafficCost_single_node(node,destination,demandMatrix,G):

    shortestDistanceHopLength = [nx.shortest_path_length(G, node, i) for i in list(G.nodes)]
    costMatrix = [shortestDistanceHopLength[i]*demandMatrix[node][i] for i in destination]
    
    return sum(costMatrix)

def SP_edgeList(G,s,t):
    """
    Returns: Shortest Path as list of edge pairs
    """
    allShortestPath = nx.shortest_path(G)
    pathEdgeList = []
    for i in range(len(allShortestPath[s][t])-1):
        pathEdgeList.append((i,allShortestPath[s][t][i+1]))
    return pathEdgeList

# Helper functions
# Binary Tranformations and Operations
def intToBin(x,graphSize):
    """Transforms a nodes integer representation to str(binary) representation

    Args:
        x: integer, x <= graphSize
        graphSize: int, size of network graph

    Returns:
        str binary: binary representation of x

    """
    decimalSize = math.ceil(math.log(graphSize,2))
    temp = bin(x)
    binary = "0"*(decimalSize-len(temp)+2) +temp[2::]
    return binary

def binToInt(x,graphSize):
    """Transforms a nodes str(binary) representation to integer representation"""
    decimalSize = math.ceil(math.log(graphSize,2))
    integer = 0
    for i in range(decimalSize):
        integer += int(x[i]) * 2**(decimalSize-i-1)
    return integer
