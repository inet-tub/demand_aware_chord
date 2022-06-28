# Demand Aware networks

Args:  
* G (networkx Graph): Graph with 2^k nodes, with k \in \mathbb{N}. Ring structure 
* D (np.ndarray): Demand matrix for every node pair in G. Demand given in % of total traffix

## Goal
Find a "good" algorithm, in terms of run-time (efficiency) and correctness (near-optimal). For the following objective:

<img src="https://latex.codecogs.com/gif.latex?\text{minimize}\ \forall i,j \in V: D_{i,j} \cdot dist_{i,j} ">

## Costraints
* Each node has at most (log_2 |V| + 1) edges.






## Gurobi Optimization
Using the Gurobi optimizer, I want to construct an LP that constructs the optimal network graph from a Demand matrix




