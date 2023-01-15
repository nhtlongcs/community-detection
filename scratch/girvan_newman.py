from measure import edge_betweenness_centrality
from graph import UndirectedGraph
def _plain_bfs(G, src):
    """A fast BFS node generator"""
    G_adj = G.nodes
    seen = set()
    nextlevel = {src}
    while nextlevel:
        thislevel = nextlevel
        nextlevel = set()
        for v in thislevel:
            if v not in seen:
                seen.add(v)
                nextlevel.update(G_adj[v])
    return seen


def connected_components(G):
    seen = set()
    for v in G:
        if v not in seen:
            c = _plain_bfs(G, v)
            seen.update(c)
            yield c


def number_connected_components(G):
    return sum(1 for cc in connected_components(G))


def girvan_newman(G):
    # If the graph is already empty, simply return its connected
    # components.
    if G.number_of_edges() == 0:
        yield tuple(connected_components(G))
        return

    def most_valuable_edge(G, return_value=False):
        """Returns the edge with the highest betweenness centrality
        in the graph `G`.

        """
        # We have guaranteed that the graph is non-empty, so this
        # dictionary will never be empty.
        betweenness = edge_betweenness_centrality(G)
        if return_value:
            return max(betweenness.items(), key=lambda x: x[1])
        return max(betweenness, key=betweenness.get)

    # The copy of G here must include the edge weight data.
    g = G.copy()
    # Self-loops must be removed because their removal has no effect on
    # the connected components of the graph.
    # g.remove_edges_from(nx.selfloop_edges(g))
    while g.number_of_edges() > 0:
        yield _without_most_central_edges(g, most_valuable_edge)


def _without_most_central_edges(G, most_valuable_edge):
    original_num_components = number_connected_components(G)
    num_new_components = original_num_components
    while num_new_components <= original_num_components:
        if G.number_of_edges() == 0:
            break
        edge, v = most_valuable_edge(G, return_value=True)
        G.remove_edge(*edge)
        new_components = tuple(connected_components(G))
        num_new_components = len(new_components)
    return new_components


if __name__ == "__main__":

    from tqdm import tqdm
    import networkx as nx
    import pandas as pd 
    from itertools import islice
    # Create a graph from text file 
    # user_id, user_id
    df = pd.read_csv('../data/ub_sample_data.csv')
    # random_ids = df.user_id.sample(100).unique()
    # df = df[df.user_id.isin(random_ids)]
    from graph import UndirectedGraph
    G = UndirectedGraph()
    usr_ids = df.user_id.unique()
    business_dict = {}
    for u in tqdm(usr_ids):
        business_u = set(df[df.user_id == u].business_id.unique())
        business_dict[u] = business_u

    usr_ids = df.user_id.unique()
    edge_threshold = 7
    for u in tqdm(usr_ids):
        for v in tqdm(usr_ids, leave=False):
            if u != v:
                business_u = business_dict[u]
                business_v = business_dict[v]
                if len(business_u.intersection(business_v)) >= edge_threshold:
                    G.add_edge(u, v)
            else:
                # if u == v, business cannot be reviewed by the same user
                # G.add_node(u)
                pass

    comp = girvan_newman(G)
    c = next(comp)
    from modularity import modularity
    print(modularity(G, c))