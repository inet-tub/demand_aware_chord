from functions_library import * 

def construct_bs_binarySwap(G):
    #not vertex transitiv
    """constructs edges to enable binary search
    
    Args: 
        G: Graph in Ring (or any structure)
        
    Returns:
        G: Graph, with edges for binary search
    """
    for i in range(len(G.nodes)):
        binaryGUID = list(intToBin(i,len(G.nodes)))
        for j in range(2,len(binaryGUID)+1):
            binaryGUID = list(intToBin(i,len(G.nodes)))
            binaryGUID[-j] = str((int(binaryGUID[-j]) + 1) % 2)
            peer = binToInt(binaryGUID,len(G.nodes))
            G.add_edge(i,peer)
    return G