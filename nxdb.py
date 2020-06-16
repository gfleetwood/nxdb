import networkx as nx
import pandas as pd
from datetime import datetime
import psycopg2
from sqlalchemy import create_engine

def db_to_nx_digraph(df: pandas.core.frame.DataFrame, nodes_col: str, edges_col: str) -> networkx.classes.digraph.DiGraph:
    
    G = nx.DiGraph()
    edges = []
    
    for row in df.iterrows():
        
        G.add_node(row[1][nodes_col])
        
        node_edges = [
            [row[1][nodes_col],j]
            for j in row[1][edges_col].split("-") 
            if len(j) != 0
        ]
        
        edges.append(node_edges)
    
    # List of lists to a single list
    edges_flattened = sum(edges, [])
    
    for edge in edges_flattened:
        G.add_edge(edge[0], edge[1])
        
    node_attrs = {}
    
    for record in df.to_dict(orient = "records"): 
        node_attrs.update({record[nodes_col]: {i:j for (i,j) in record.items() if i != nodes_col}})
        
    nx.set_node_attributes(G, node_attrs)
    
    return(G)
    
    
def nx_digraph_to_df(G: networkx.classes.digraph.DiGraph, columns: List[str], nodes_col: str, edges_col: str) -> pandas.core.frame.DataFrame:

    edges_dict = {x[0]: [] for x in list(G.edges)}
    
    for edge in list(G.edges):
        edges_dict[edge[0]].append(edge[1])
        
    # Edges targets are stored as "-" separated strings. For example if there are edges
    # A -> B and A -> C then in A's row this is stored as "B-C"
    edges_dict_formatted = {i:"-".join(j) for (i,j) in edges_dict.items()}
    
    nodes = list(G.nodes)
    cols = [col for col in columns if col not in [nodes_col, edges_col]]
    
    reconstruct_df = {
        nodes_col: nodes, 
        edges_col: [edges_dict_formatted.get(node, "") for node in nodes]
    }
    
    # Parsing metadata for each node
    
    for col in cols:
        reconstruct_df.update({col: [G.nodes[node][col] for node in nodes]})
    
    df_graph = pd.DataFrame(reconstruct_df)[columns]
    
    return(df_graph)
