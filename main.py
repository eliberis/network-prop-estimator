from graph_provider import *
from estimators import *
import networkx as nx


def main():
    G = pref_attachment_graph() # / google_web_graph()
    print("Number of edges:", nx.number_of_edges(G))
    print("Number of nodes:", nx.number_of_nodes(G))
    print("Number of triangles:", sum(nx.triangles(G).values())//3)

    est = FormulaTriangleEstimator(G)
    for size_sample in est.estimates(num_estimates=2000):
        print(size_sample)


if __name__ == "__main__":
    main()
