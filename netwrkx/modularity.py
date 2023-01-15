
# def modularity(G, communities):
#     if not isinstance(communities, list):
#         communities = list(communities)

#     out_degree = in_degree = dict(G.degree())
#     deg_sum = sum(out_degree.values())
#     m = deg_sum / 2
#     norm = 1 / deg_sum**2

#     def community_contribution(community):
#         comm = set(community)
#         # for com in communities: if edge in com: add to L_c
#         L_c = G.len_edges(comm)

#         out_degree_sum = sum(out_degree[u] for u in comm)
#         in_degree_sum = out_degree_sum

#         return L_c / m - out_degree_sum * in_degree_sum * norm

#     return sum(map(community_contribution, communities))


def modularity(G, communities):
    if not isinstance(communities, list):
        communities = list(communities)


    out_degree = in_degree = dict(G.degree(weight='weight'))
    deg_sum = sum(out_degree.values())
    m = deg_sum / 2
    norm = 1 / deg_sum**2

    def community_contribution(community):
        comm = set(community)
        L_c = 0 
        # L_c = sum(wt for u, v, wt in G.edges(comm, data='weight', default=1) if v in comm)
        for u, v, wt in G.edges(comm, data='weight', default=1):
            if v in comm:
                L_c += 1
        print(L_c)
        out_degree_sum = sum(out_degree[u] for u in comm)
        in_degree_sum = out_degree_sum

        return L_c / m - out_degree_sum * in_degree_sum * norm

    return sum(map(community_contribution, communities))

