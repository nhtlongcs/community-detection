import tabulate
from collections import OrderedDict
from copy import deepcopy

class UndirectedGraph:
    def __init__(self):
        # self.adj = {}
        self.nodes = {} # ordered set of nodes
        self.name2idx = OrderedDict()
        self.edges = set()

    def __add_node(self, u):
        if u not in self.name2idx:
            self.name2idx[u] = len(self.name2idx)
            self.nodes[u] = {}
    def len_edges(self, communities):
        if not isinstance(communities, list):
            communities = list(communities)

        L_c = 0
        for u, v in self.edges:
            for com in communities:
                if v in com:
                    L_c += 1
        return L_c
    def copy(self):
        return deepcopy(self)

    def number_of_edges(self):
        return len(self.edges)

    def add_edge(self, u, v):
        self.__add_node(u)
        self.__add_node(v)

        if v not in self.nodes[u]:
            self.nodes[u][v] = 0
        if u not in self.nodes[v]:
            self.nodes[v][u] = 0
        
        self.nodes[u][v] = 1
        self.nodes[v][u] = 1
        self.edges.add(UndirectedGraph._hash_edge(u, v))   
    
    def remove_edge(self, u, v):
        try:
            del self.nodes[u][v]
            if u != v:  # self-loop needs only one entry removed
                del self.nodes[v][u]
            self.edges.remove(UndirectedGraph._hash_edge(u, v))
        except KeyError as err:
            pass 

    def degree(self):
        degree = {}
        for i in self.nodes:
            degree[i] = len(self.nodes[i])
        return degree

    def __iter__(self):
        return iter(self.nodes)

    def __getitem__(self, n):
        return self.nodes[n]

    @staticmethod
    def _hash_edge(u, v):
        return tuple(sorted([u, v]))

    def display(self):
        display_mat = [[0 for i in range(len(self.nodes))] for j in range(len(self.nodes))]
        for i in self.nodes:
            for j in self.nodes:
                if j in self.nodes[i]:
                    display_mat[self.name2idx[i]][self.name2idx[j]] = self.nodes[i][j]
        print(tabulate.tabulate(display_mat, tablefmt="grid", headers=list(self.name2idx.keys()), showindex=list(self.name2idx.keys())))
    def __len__(self):
        return len(self.nodes)

    def get_communities(self):
        communities = []
        visited = set()
        for u in self.nodes:
            if u not in visited:
                visited.add(u)
                community = [u]
                for v in self.nodes[u]:
                    if v not in visited:
                        community.append(v)
                        visited.add(v)
                communities.append(community)
        return communities

if __name__ == "__main__":
    G = UndirectedGraph()
    G.add_edge('abc', 'd')
    G.add_edge('e', 'f')
    G.add_edge('f', 'g')
    G.display()
    print(len(G.nodes), len(G.edges))