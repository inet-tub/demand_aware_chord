#!/bin/env python

import gurobi as gb
from gurobipy import GRB

import networkx as nx
import numpy as np
import math


from functions_library import *

opt_mod = gb.Model(name="linear programm")


def gurobi_optimal(G,D):
	n = len(G.nodes)
	e = opt_mod.addMVar((len(G.nodes), len(G.nodes)), name="e", vtype="B")
	dist = opt_mod.addMVar((len(G.nodes), len(G.nodes)), name="dist", vtype="I", lb=0, ub=GRB.INFINITY)
	x = opt_mod.addMVar((len(G.nodes), len(G.nodes),len(G.nodes), len(G.nodes)), name="x", vtype="B")
	opt_mod.update()
	# Adjacency Matrix (e) Constraints
	opt_mod.addConstrs((e[i,(i+1) % len(G.nodes)] == 1 for i in G.nodes), name="c-ring")
	opt_mod.addConstrs((e[i,i] == 0 for i in G.nodes), name="c-noSelfEdge")
	opt_mod.addConstrs((e[i,j] == e[j,i] for i in G.nodes for j in G.nodes), name="c-undirected")

	maxNumberE =  k+1 #math.log(n,2)-1 + 2
	opt_mod.addConstrs((e[i,:].sum() <= maxNumberE for i in G.nodes), name="c-logE")


	    
	# Distance Matrix (dist) Constraints. dist[i][j]:= SP-length between i and j
	opt_mod.addConstrs((x[i,j,:,:].sum()/2==dist[i,j] for i in G.nodes for j in G.nodes), name="c-subpath0")
	opt_mod.addConstrs((dist[i,j] <= dist[i,u] + dist[u,j] for i in G.nodes for j in G.nodes for u in G.nodes),
	                  name="c-dist2")




	# Ensuring that x shows a correct path
	opt_mod.addConstrs((x[i,j,u,v] <= e[u,v] for i in G.nodes for j in G.nodes for u in G.nodes for v in G.nodes),
	                  name="flow0")
	for i in G.nodes:
	    for j in G.nodes:
	        if i != j:
	            opt_mod.addConstr(x[i,j,i,:].sum() == 1, name="c-flowStart")
	            opt_mod.addConstr(x[i,j,:,j].sum() == 1, name="c-flowEnd")
	            for v in G.nodes:
	                if v not in [i,j]:
	                    opt_mod.addConstr((x[i,j,:,v].sum() - x[i,j,v,:].sum()) == 0, name="blue0")

	#Optimization
	nodesPairListNoDuplication = complete_node_pair_list_noDuplication(G)
	opt_mod.setObjective(sum([dist[i,j]*D[i][j] for (i,j) in nodesPairListNoDuplication]), GRB.MINIMIZE)
	opt_mod.update()
	opt_mod.optimize()

	# Getting result
	G_sol = nx.Graph()
	for i in range(n): 
	    G_sol.add_node(i)

	for i in G_sol.nodes:
	    for j in range(i+1,len(G_sol.nodes)):
	        if e[i,j].X == 1.0:
	            G_sol.add_edge(i,j)
	return G_sol




for k in range(2,13):
	G = init_ring(2**k)
	D = init_uniformDemand_matrix_symmetric(G)

	G_sol = gurobi_optimal(G,D)

	solution = calc_cost(G_sol,D)

	f = open("output.txt", "a")
	f.write(str(k) + "," + str(solution)+ "\n")
	f.close()