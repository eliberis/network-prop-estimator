from graph_provider import *
import networkx as nx

def main():
    G = google_web_graph() # / pref_attachment_graph()
    print("Number of edges:", nx.number_of_edges(G))
    print("Number of nodes:", nx.number_of_nodes(G))

if __name__ == "__main__":
    main()
