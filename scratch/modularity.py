
def modularity(G, communities):
    if not isinstance(communities, list):
        communities = list(communities)

    out_degree = in_degree = dict(G.degree())
    deg_sum = sum(out_degree.values())
    m = deg_sum / 2
    norm = 1 / deg_sum**2

    def community_contribution(community):
        comm = set(community)
        L_c = G.len_edges(comm)

        out_degree_sum = sum(out_degree[u] for u in comm)
        in_degree_sum = out_degree_sum

        return L_c / m - out_degree_sum * in_degree_sum * norm

    return sum(map(community_contribution, communities))

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
    from girvan_newman import connected_components 
    x = [c for c in connected_components(G)]
    print(len(x))
    print(modularity(G, x))