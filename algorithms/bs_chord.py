from functions_library import * 

def construct_bs_chord(G):
    #vertex transitiv
    """constructs edges to enable original (CHORD-like) binary search
    
    Args: 
        G: Graph
        
    Returns:
        G: Graph
    """
    n = len(G.nodes)
    for i in range(n):
        binaryGUID = list(intToBin(i,n))
        j = 1
        while G.degree(i) < math.log(n,2)+1:
            G.add_edge(i,(i+2**j) % n)
            j+=1
    return G