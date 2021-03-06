from graph_provider import *
from estimators import *
from run_plotter import produce_plot
import networkx as nx


def main():
    G = pref_attachment_graph()  # also try google_web_graph() or amazon_graph()
    num_nodes = nx.number_of_nodes(G)
    num_edges = nx.number_of_edges(G)
    num_triangles = sum(nx.triangles(G).values())//3

    print("Number of edges:", num_edges)
    print("Number of nodes:", num_nodes)
    print("Number of triangles:", num_triangles)

    produce_plot(G, WeightedEdgeEstimator,
                 true_val=num_edges,
                 est_quant_name='m = Number of edges')

    produce_plot(G, WeightedNodeEstimator,
                 true_val=num_nodes,
                 est_quant_name='n = Number of nodes')

    produce_plot(G, WeightedTriangleEstimator,
                 true_val=num_triangles,
                 est_quant_name='t = Number of triangles',
                 num_edges=num_edges)

    produce_plot(G, FormulaEdgeEstimator,
                 true_val=num_edges,
                 est_quant_name='m = Number of edges')

    produce_plot(G, FormulaNodeEstimator,
                 true_val=num_nodes,
                 est_quant_name='n = Number of nodes')

    produce_plot(G, FormulaTriangleEstimator,
                 true_val=num_triangles,
                 est_quant_name='t = Number of triangles')

if __name__ == "__main__":
    main()
