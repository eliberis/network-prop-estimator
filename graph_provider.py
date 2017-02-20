import networkx as nx
import random
import os.path

PREF_ATTACHMENT_GRAPH_FILE = "pref_attachment.p"
GOOGLE_GRAPH_FILE = "web-Google.txt"
GOOGLE_GRAPH_POSTPROCESSED_FILE = "web_google_maxwcc.p"


def generate_pref_attachment_graph(n, r, p, seed=None):
    if seed is not None:
        random.seed(seed)

    G = nx.complete_graph(r)

    # Array of node labels repeated according to their degree in the graph.
    # The array is maintained manually for speed. Preferential sampling is
    # therefore just a regular `choice` from this array.
    repeated_nodes = [i for i in range(r) for d in range(G.degree(i))]

    for v in range(r, n):
        if v % 1000 == 0:
            print("Adding node {0} out of {1}".format(v, n))

        x = random.choice(repeated_nodes)  # Choose x preferentially

        targets = [x]  # There will be an edge from u to every node in targets

        for j in range(r-1):  # Add remaining r - 1 edges
            # Pref attachment vs random neighbour of x
            choice_list = \
                repeated_nodes if random.random() < p else G.neighbors(x)
            u = random.choice(choice_list)
            while u in targets:
                u = random.choice(choice_list)
            targets.append(u)

        G.add_edges_from(zip([v] * r, targets))  # Creates v as a node as well

        repeated_nodes.extend(targets) # Update node-degree list
        repeated_nodes.extend([v] * r)

    return G


def pref_attachment_graph():
    if os.path.isfile(PREF_ATTACHMENT_GRAPH_FILE):
        return nx.read_gpickle(PREF_ATTACHMENT_GRAPH_FILE)
    else:
        G = generate_pref_attachment_graph(600000, 3, 0.6)
        nx.write_gpickle(G, PREF_ATTACHMENT_GRAPH_FILE)
        return G


def google_web_graph():
    if os.path.isfile(GOOGLE_GRAPH_POSTPROCESSED_FILE):
        return nx.read_gpickle(GOOGLE_GRAPH_POSTPROCESSED_FILE)
    else:
        G = nx.read_edgelist(GOOGLE_GRAPH_FILE, delimiter="\t")
        Gc = max(nx.connected_component_subgraphs(G), key=len)
        nx.write_gpickle(Gc, GOOGLE_GRAPH_POSTPROCESSED_FILE)
        return Gc
