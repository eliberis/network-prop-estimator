from graph_provider import *
from estimators import *
from run_plotter import produce_plot
import networkx as nx


def main():
    G = pref_attachment_graph() # / google_web_graph()
    print("Number of edges:", nx.number_of_edges(G))
    print("Number of nodes:", nx.number_of_nodes(G))
    # print("Number of triangles:", sum(nx.triangles(G).values())//3)

    # produce_plot(G, WeightedEdgeEstimator,
    #              true_val=nx.number_of_edges(G),
    #              est_quant_name='m = Number of edges')

    # produce_plot(G, WeightedNodeEstimator,
    #              true_val=nx.number_of_nodes(G),
    #              est_quant_name='n = Number of nodes')

    # produce_plot(G, WeightedTriangleEstimator,
    #              true_val=sum(nx.triangles(G).values())//3,
    #              est_quant_name='t = Number of triangles',
    #              num_edges=nx.number_of_edges(G))

    produce_plot(G, FormulaTriangleEstimator,
                 true_val=sum(nx.triangles(G).values())//3,
                 est_quant_name='t = Number of triangles')

if __name__ == "__main__":
    main()
