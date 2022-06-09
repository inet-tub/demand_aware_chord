# Demand Aware networks

Args:  
* G (networkx Graph): Graph with 2^k nodes, with k \in \mathbb{N}. Ring structure 
* D (np.ndarray): Demand matrix for every node pair in G. Demand given in % of total traffix

## Gurobi Optimization
Using the Gurobi optimizer, I want to construct an LP that constructs the optimal network graph from a Demand matrix
