from collections import deque
from graph import UndirectedGraph

def edge_betweenness_centrality(G, normalized=True):
    betweenness = dict.fromkeys(G, 0.0)  # b[v]=0 for v in G
    # b[e]=0 for e in G.edges()
    betweenness.update(dict.fromkeys(G.edges, 0.0))
    nodes = G
    for s in nodes:
        # single source shortest paths
        S, P, sigma, _ = _single_source_shortest_path_basic(G, s) # use BFS
        # accumulation
        betweenness = _accumulate_edges(betweenness, S, P, sigma, s)
    # rescaling
    for n in G:  # remove nodes to only return edges
        del betweenness[n]
    betweenness = _rescale_e(
        betweenness, len(G), normalized=normalized,
    )
    return betweenness

def _single_source_shortest_path_basic(G, s):
    S = []
    P = {}
    for v in G:
        P[v] = []
    sigma = dict.fromkeys(G, 0.0)  # sigma[v]=0 for v in G
    D = {}
    sigma[s] = 1.0
    D[s] = 0
    Q = deque([s])
    while Q:  # use BFS to find shortest paths
        v = Q.popleft()
        S.append(v)
        Dv = D[v]
        sigmav = sigma[v]
        for w in G[v]:
            if w not in D:
                Q.append(w)
                D[w] = Dv + 1
            if D[w] == Dv + 1:  # this is a shortest path, count paths
                sigma[w] += sigmav
                P[w].append(v)  # predecessors
    return S, P, sigma, D

def _rescale_e(betweenness, n, normalized):
    if normalized:
        if n <= 1:
            scale = None  # no normalization b=0 for all nodes
        else:
            scale = 1 / (n * (n - 1))

    if scale is not None:
        for v in betweenness:
            betweenness[v] *= scale
    return betweenness

def _accumulate_edges(betweenness, S, P, sigma, s):
    delta = dict.fromkeys(S, 0)
    while S:
        w = S.pop()
        coeff = (1 + delta[w]) / sigma[w]
        for v in P[w]:
            c = sigma[v] * coeff
            if (v, w) not in betweenness:
                betweenness[UndirectedGraph._hash_edge(w, v)] += c
            else:
                betweenness[UndirectedGraph._hash_edge(v, w)] += c
            delta[v] += c
        if w != s:
            betweenness[w] += delta[w]
    return betweenness

if __name__ == "__main__":
    from tqdm import tqdm
    import networkx as nx
    from networkx.algorithms.community.centrality import girvan_newman
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

    result = edge_betweenness_centrality(G)
    result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    def sort_by_lexicographical_order(edge):
        return tuple(sorted(edge))
    result = [(sort_by_lexicographical_order(edge[0]), edge[1]) for edge in result]
    print(result[:5])