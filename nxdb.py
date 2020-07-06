import networkx as nx
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine

def db_to_nx_digraph(df: pandas.core.frame.DataFrame, source_node_col: str, target_nodes_col: str) -> networkx.classes.digraph.DiGraph:
    
    """
    Converts a dataframe with node attributes to a networkx digraph. 
    
    Params:
    
    df: A pandas dataframe with the source node, targets nodes, and any node metadata.
    source_node_col: The name of the column for the source nodes
    target_nodes_col: The name of the column with the target nodes as a "-" separated string
    
    Returns: 
    
    df_graph: A pandas dataframe with the source node, targets nodes, and any node metadata.
    """
    
    G = nx.DiGraph()
    edges_nested = []
    
    for row in df.iterrows():
        
        G.add_node(row[1][source_node_col])
        
        node_edges = [
            [row[1][source_node_col], target_node]
            for target_node in row[1][target_nodes_col].split("-") 
            if len(target_node) != 0
        ]
        
        edges_nested.append(node_edges)
    
    edges_flattened = sum(edges_nested, [])
    
    for edge in edges_flattened:
        G.add_edge(edge[0], edge[1])
        
    node_attrs = {}
    
    for record in df.to_dict(orient = "records"): 
        node_attrs.update({record[nodes_col]: {attribute: value for (attribute, value) in record.items() if attribute != nodes_col}})
        
    nx.set_node_attributes(G, node_attrs)
    
    return(G)
    
    
def nx_digraph_to_df(G: networkx.classes.digraph.DiGraph, columns_df: List[str], source_node_col: str, target_nodes_col: str) -> pandas.core.frame.DataFrame:
    
    """
    Converts a networkx digraph to a dataframe preserving node attributes. 
    
    Params:
    
    G: A networkx digraph
    columns_df: The column names absent two: the column for the source node and the one for the target nodes.
    source_node_col: The name of the column for the source nodes
    target_nodes_col: The name of the column to with the target nodes as a "-" separated string
    
    Returns: 
    
    df_graph: A pandas dataframe with the source node, targets nodes, and any node metadata.
    """
    
    nodes = list(G.nodes)
    edges = list(G.edges)

    # Building a dictionary of source nodes as keys and a list of target nodes as values before storage in the dataframe
    # The target nodes are stored in a column as "-" separated strings
    # For example if there are edges A -> B and A -> C then in A's row this is stored as "B-C"
    
    edges_dict = {x[0]: [] for x in list(G.edges)}
    
    for edge in edges:
        edges_dict[edge[0]].append(edge[1])
       
    edges_dict_formatted = {i:"-".join(j) for (i,j) in edges_dict.items()}
    
    reconstruct_df = {
        source_node_col: nodes, 
        target_nodes_col: [edges_dict_formatted.get(node, "") for node in nodes]
    }
    
    cols_from_node_metadata = [col for col in columns_df if col not in [source_node_col, target_nodes_col]]
    
    for col in cols_from_node_metadata:
        reconstruct_df.update({col: [G.nodes[node][col] for node in nodes]})
    
    df_graph = pd.DataFrame(reconstruct_df)
    
    return(df_graph)
