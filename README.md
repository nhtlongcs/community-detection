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

2.2. Community Detection
You divide the graph into an appropriate number of communities to reach the global highest modularity.
The formula of modularity is shown below.

The GM algorithm requires recomputing the betweenness scores after removing one edge. In the
formula, “m” stands for the number of edges in the original graph, and “A” represents the
adjacent matrix of the original graph. (Hint: in each removal step, we do not alter “m” and “A”).
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