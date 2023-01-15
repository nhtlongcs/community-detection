from tqdm import tqdm
import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman
import pandas as pd 
from itertools import islice
# Create a graph from text file 
# user_id, user_id

if __name__ == "__main__":
    df = pd.read_csv('data/ub_sample_data.csv')
    G = nx.Graph()
    usr_ids = df.user_id.unique()
    edge_threshold = 7
    for u in tqdm(usr_ids):
        u_adjs = set(df[df.user_id == u].user_id.unique())
        for v in u_adjs:
            business_u = set(df[df.user_id == u].business_id.unique())
            business_v = set(df[df.user_id == v].business_id.unique())
            if len(business_u.intersection(business_v)) >= edge_threshold:
                G.add_edge(u, v)
    comp = girvan_newman(G)
    k = 2
    for communities in islice(comp, k):
        print(tuple(sorted(c) for c in communities))