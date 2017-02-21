from graph_provider import *
from estimators import NodeEstimator, EdgeEstimator, TriangleEstimator
import networkx as nx


def main():
    G = pref_attachment_graph() # / google_web_graph()
    print("Number of edges:", nx.number_of_edges(G))
    print("Number of nodes:", nx.number_of_nodes(G))
    print("Number of triangles:", sum(nx.triangles(G).values())//3)

    est = TriangleEstimator(G, num_edges=nx.number_of_edges(G))
    for size_sample in est.estimates(num_estimates=1000):
        print(size_sample)


if __name__ == "__main__":
    main()
