# Community detection 

## Tổng quan - Overview

Repo này thực hiện thuật toán nhận diện các cộng đồng, cụ thể trong ngữ cảnh đưa các sự kiện trên mạng xã hội
về đồ thị. Mục tiêu của bài toán này giúp bạn hiểu về thuật toán community detection và sử dụng chúng trên
các ngữ cảnh thực tế, cũng như các công cụ xử lý đồ thị (graph processing tools). 

> Friendly note: This assignment is created based on an INF553 Foundations and Applications of Data Mining course

_Từ chối trách nhiệm: Mục tiêu của repo này là giúp bạn hiểu về thuật toán community detection dựa vào kiến thức của
tác giả, đây là một phần của khoá học CSC14114 - Ứng dụng dữ liệu lớn (Big Data) - VNU-HCMUS. Nếu bạn đang học
khoá học này, bạn nên thực hiện bài tập trên lớp. Nếu bạn không phải là sinh viên khoá học này, bạn có thể tham khảo
repo này để hiểu về thuật toán community detection. Tuy nhiên, bạn không được sao chép bài tập của repo này để nộp
trên lớp._

## 1. Chuyển đổi dữ liệu - From raw data to graph

Mục tiêu cụ thể trong ngữ cảnh này là tìm các user có độ tương đồng cao với các doanh nghiệp trên tập dữ liệu 
`up_sample_data.csv` được cho.

Đầu tiên ta cần xây dựng một đồ thị từ dữ liệu được cho. Trong đó: 
- Biểu diễn bài toán dưới dạng một đồ thị vô hướng (undirected graph) 
- Mỗi node đại diện cho một user
- Mỗi cạnh nối giữa 2 node là số lần tương ứng user review cùng một doanh nghiệp. Lưu ý rằng số lần này phải 
lớn hơn một ngưỡng nhất định. Ví dụ, giả sử user1 review [business1, business2, business3] và user2 review
[business2, business3, business4, business5]. Nếu ngưỡng là 2, thì sẽ có một cạnh nối giữa user1 và user2.
Trong repo này, ta sẽ sử dụng tham số ngưỡng = 7 (`review_threshold=7`)
- Nếu một node không có cạnh nào, ta sẽ không bao gồm node đó trong đồ thị.

## 2. Các vấn đề cần giải quyết - Problem to solve

### Task 1: Cài đặt thuật toán community detection sử dụng Girvan-Newman.

Ở bài toán này, bạn cần xây dựng đồ thị dựa trên các yêu cầu ở mục 1 và sử dụng thuật toán Girvan-Newman để 
phân tách các cụm. Thuật toán Girvan-Newman phân tách cụm bằng cách loại bỏ từng cạnh có giá trị giữa các cụm
có độ đo betweenness cao nhất ra khỏi đồ thị gốc (ta sẽ giải thích giá trị betweeness ở phần sau). 
Sau đó, các thành phần liên thông của đồ thị còn lại sẽ là các cụm. 

**Để biết chi tiết thuật toán, bạn có thể tham khảo sách Mining of Massive Datasets - Chapter 10.**

You need to implement the graph construction and the Girvan-Newman algorithm by yourself.
Pandas DataFrame is possible.

#### Trọng số Betweness - Betweenness Calculation

Một số yêu cầu cần lưu ý, ta sẽ lưu trọng số của mỗi cạnh là giá trị betweenness của cạnh đó. Định dạng 
của file output sẽ là:

```text
(‘user_id1’, ‘user_id2’), betweenness value
```

Trong đó, `user_id1` và `user_id2` là 2 user_id của 2 node nối với nhau bởi cạnh đó. Lưu ý rằng user_ids 
trong mỗi tuple phải tuân theo thứ tự từ điển/lexicographical order. Cụ thể, ta cần sắp xếp giá trị betweenness theo
thứ tự giảm dần, sau đó là sắp xếp lại user_ids theo thứ tự từ điển. Kết quả của bạn không cần làm tròn.

#### Thực hiện thuật toán - Community Detection

Sau khi tính được giá trị betweenness của các cạnh, ta sẽ thực hiện thuật toán Girvan-Newman để phân tách các cụm.
Thuật toán sẽ thực hiện phân tách đồ thị ra một số cụm hợp lý, mỗi cụm này có thể coi là một cộng đồng. Ta cần tách cụm sao cho giá trị modularity của đồ thị sau khi tách cụm là lớn nhất.

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


Thuật toán Girvan-Newman yêu cầu tính toán lại giá trị betweeness sau mỗi lần xoá cạnh khỏi đồ thị. 
Trong thuật toán, giá trị `m` đại diện cho số cạnh trong đồ thị gốc, `A` là ma trận kề của đồ thị gốc.
(Hint: trong mỗi bước xoá cạnh, ta không thay đổi giá trị `m` và `A`). 
Nếu một cụm chỉ có một node, ta vẫn coi nó là một cụm hợp lệ. Ta cần lưu kết quả các cụm vào một file text; 
Mỗi dòng trong file text sẽ là một cụm, định dạng của mỗi dòng sẽ là:

```text
‘user_id1’, ‘user_id2’, ‘user_id3’, ‘user_id4’, ...
```

Giống với yêu cầu bên trên, ở bước này ta lưu ý các user_ids cũng sẽ được sắp xếp theo thứ tự từ điển. Đầu
tiên ta cần sắp xếp các cộng đồng tăng dần bởi kích thước của chúng. Và sắp xếp chúng dựa trên user_id đầu tiên 
của mỗi cộng đồng theo thứ tự từ điển. Cuối cùng, ta cần in ra giá trị modularity lớn nhất của đồ thị sau khi tách cụm.

### Task2: Cài đặt thuật toán community detection sử dụng Girvan-Newman trong NetworkX

Ở task này, ta cần thực hiện lại các yêu cầu của task 1 là detect commnunites của đồ thị được cho 
bằng thuật toán Girvan-Newman bằng cách cực đại hoá giá trị modularity. Sau đó ta sẽ so sánh kết quả của
NetworkX và phiên bản tự cài đặt ở Task1

You need to use NetworkX API to construct the graph and run the Girvan-Newman algorithm.
The following websites may help you get started with the NetworkX:
https://networkx.org/documentation/stable/index.html

## Further requirements
• This project gives you a 20% course grade.
• Anything that is not made by your own effort should be cited properly. Any plagiarism, any tricks,
or any lie will have a 0 point for the COURSE grade.
• You need to organize code files for Task 1 and Task 2 separately on Google Colab. Please guarantee
that no change is made after the deadline.
In this assignment, we use filter threshold 7.
Please use user_id directly as strings when constructing the graph, don’t hash them to integers.

## References
[1] https://web-app.usc.edu/soc/syllabus/20191/32414.pdf.