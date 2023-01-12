# Community detection 

## Problem overview

In this problem, you will work on Girvan-Newman algorithm for detecting communities in social
networks. This problem aims to help you understand the community detection problem and how to
handle it with widely available graph processing tools.
This problem is created based on an INF553 Foundations and Applications of Data Mining course
problem, whose link is in the References section. The following paragraphs are from the webpage with
some modifications.

> Friendly note: This assignment is created based on an INF553 Foundations and Applications of Data Mining course

_Disclaimer: The purpose of this repository is to help you understand the community detection algorithm based on the author's knowledge, 
this is a part of the CSC14114 - Big Data Application course - VNU-HCMUS. If you are taking this course, you should do the assignment in class. 
If you are not a student of this course, you can refer to this repository to understand the community detection algorithm.
However, you are not allowed to copy the assignment of this repository to submit in this class._

## From raw data to graph
You aim to find users with similar business tastes from the dataset given in the CSV file,
ub_sample_data.csv.
You need to construct the social network from the given data. Each node represents a user, and there
will be an undirected edge between two nodes if the number of times that two corresponding users
review the same business is greater than or equivalent to some predefined filter threshold. For example,
suppose user1 reviewed [business1, business2, business3] and user2 reviewed [business2, business3,
business4, business5]. Then, if the threshold is 2, there will be an edge between user1 and user2.
If the user node has no edge, we will not include that node in the graph.
In this problem, we use filter threshold 7.
Please use user_id directly as strings when constructing the graph, don’t hash them to integers.

## Problem requirement

### Task 1: Community Detection using Girvan-Newman algorithm (GM) from scratch

In this task, you first construct the graph following the specification given in Section 1 and detect the
communities in the constructed graph by using Girvan-Newman algorithm. GM1 detects communities
by progressively removing edges with high betweenness scores from the original network; the
connected components of the remaining network are the communities. For the algorithm details, you
may also refer to the Mining of Massive Datasets book – Chapter 10.
You need to implement the graph construction and the Girvan-Newman algorithm by yourself.
Pandas DataFrame is possible.

#### Betweenness Calculation

You calculate the betweenness score for every edge in the constructed graph and then save the result
in a text file whose format is as follows.

(‘user_id1’, ‘user_id2’), betweenness value

The two user_ids in each tuple must be in lexicographical order. You first sort the betweenness values
in descending order. Then, you sort the first user_ids (of string type) in all the tuples in lexicographical
order. You do not need to round your result.

#### Community Detection
You divide the graph into an appropriate number of communities to reach the global highest modularity.
The formula of modularity is shown below.
**Modularity of partitioning S of graph G**

<!-- equation Q = sum(s in S)[ (edges within group s) - (expected edge within group s)] -->

![equation](https://latex.codecogs.com/gif.latex?Q%20%3D%20%5Csum_%7Bs%20%5Cin%20S%7D%5B%20%28edges%20within%20group%20s%29%20-%20%28expected%20edge%20within%20group%20s%29%5D)

<!-- equation expected edge within group s = (number of edges in group s) / (total number of edges) * (total number of edges in graph G) -->

<!-- ![equation](https://latex.codecogs.com/gif.latex?expected%20edge%20within%20group%20s%20%3D%20%28number%20of%20edges%20in%20group%20s%29%20%2F%20%28total%20number%20of%20edges%29%20*%20%28total%20number%20of%20edges%20in%20graph%20G%29) -->


<!-- equation Q(G,S) = frac(1,2m) sum(s in S)sum(i in s)sum(j in s)[A_ij - frac(k_i k_j, 2m)] -->

![equation](https://latex.codecogs.com/gif.latex?Q%28G%2CS%29%20%3D%20%5Cfrac%7B1%7D%7B2m%7D%20%5Csum_%7Bs%20%5Cin%20S%7D%5Csum_%7Bi%20%5Cin%20s%7D%5Csum_%7Bj%20%5Cin%20s%7D%5BA_%7Bij%7D%20-%20%5Cfrac%7Bk_%7Bi%7D%20k_%7Bj%7D%7D%7B2m%7D%5D)


<!-- equation normalizing cost: -1 < Q < 1 -->

![equation](https://latex.codecogs.com/gif.latex?normalizing%20cost%3A%20-1%20%3C%20Q%20%3C%201)

<!-- equation A_ij = 1 if i connects j else 0 -->

![equation](https://latex.codecogs.com/gif.latex?A_%7Bij%7D%20%3D%201%20if%20i%20connects%20j%20else%200)




The GM algorithm requires recomputing the betweenness scores after removing one edge. In the formula, “m” stands for the number of edges in the original graph, and “A” represents the adjacent matrix of the original graph. (Hint: in each removal step, we do not alter “m” and “A”).
If the community only has one user node, we still regard it as a valid community.
You need to save the resulting communities in a text file. Each line represents one community in the
following format.
```text
‘user_id1’, ‘user_id2’, ‘user_id3’, ‘user_id4’, ...
```
The user_ids in each community must be in lexicographical order. Your first sort the communities
ascendingly by their sizes. Then, you sort all the first user_ids (of string type) in the communities in
lexicographical order. The last line shows the global highest modularity.

### Task 2: Community Detection using Girvan-Newman algorithm in NetworkX

In this task, you repeat what required in Task 1, i.e., to detect the communities in the given graph by GM
algorithm such that a maximum modularity is obtained. Then, you compare the results provided by
NetworkX GM and your GM implementation.

You need to use NetworkX API to construct the graph and run the Girvan-Newman algorithm.
The following websites may help you get started with the NetworkX:
https://networkx.org/documentation/stable/index.html

## Further requirements
• This project gives you a 20% course grade.
• Anything that is not made by your own effort should be cited properly. Any plagiarism, any tricks,
or any lie will have a 0 point for the COURSE grade.
• You need to organize code files for Task 1 and Task 2 separately on Google Colab. Please guarantee
that no change is made after the deadline.

## References
[1] https://web-app.usc.edu/soc/syllabus/20191/32414.pdf.