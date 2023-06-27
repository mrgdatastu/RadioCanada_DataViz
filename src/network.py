import pandas as pd
import networkx as nx
from pyvis.network import Network
import webbrowser

def create_network_graph(data):

    # Replace NaN values with "Unknown"
    data = data.fillna("Home")

    # Extract information about visited pages
    visited_pages = data[['simulated_detailed_event', 'simulated_subject']].drop_duplicates()

    # Extract visits that led to account creation
    account_creation_visits = data[data['Account_Created_journey'] == 1]

    # Create a network graph
    G = nx.DiGraph()

    # Add nodes for visited pages
    for _, row in visited_pages.iterrows():
        G.add_node(row['simulated_detailed_event'], node_type='page')
        G.add_node(row['simulated_subject'], node_type='subject')
        G.add_edge(row['simulated_subject'], row['simulated_detailed_event'], edge_type='visit')

    # Add the "Account Creation" node and connect all links leading to it
    G.add_node('Account Creation', node_type='account_creation')
    for _, row in account_creation_visits.iterrows():
        G.add_edge(row['simulated_detailed_event'], 'Account Creation', edge_type='account_creation')

    # Create PyVis network
    nt = Network(height='800px', width='100%', notebook=True)

    # Add nodes with their attributes
    for node, node_type in G.nodes(data='node_type'):
        color = 'green' if node_type == 'account_creation' else 'lightblue'
        nt.add_node(node, label=node, color=color)

    # Add edges with their attributes
    for u, v, edge_type in G.edges(data='edge_type'):
        color = 'green' if edge_type == 'account_creation' else 'gray'
        nt.add_edge(u, v, color=color)

    # Set options for the network visualization
    nt.set_options("""
    var options = {
    "nodes": {
        "shape": "dot",
        "size": 20,
        "font": {
        "size": 12,
        "color": "black"
        },
        "borderWidth": 2
    },
    "edges": {
        "width": 1,
        "font": {
        "size": 10,
        "color": "gray"
        }
    },
    "physics": {
        "stabilization": true,
        "forceAtlas2Based": {
        "gravitationalConstant": -50,
        "centralGravity": 0.01,
        "springLength": 200,
        "springConstant": 0.08
        },
        "minVelocity": 0.75
    }
    }
    """)

    # # Show the network visualization
    #nt.show('network.html')
    return ('network.html')

def open_html_file(file_path):
    webbrowser.open(file_path)

html_file_path = 'network'
open_html_file(html_file_path)