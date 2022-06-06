from itertools import combinations
from networkx import DiGraph,is_isomorphic, is_connected

######################################################################
# Exercise 1 part 2, find all appearances of motifs in a given graph #
######################################################################

#enter graph through txt file
graph = DiGraph()
f = open("graph.txt", "r")
tmp = f.readline()
size = tmp.split('=')
#read the graph from txt file and create the graph
for i in f.readlines():
    str_tmp = i.split(',')
    graph.add_edge(int(str_tmp[0]),int(str_tmp[1]))


#name: subGraph
#input: size
#output: list of subgraphs
#explanation: creates a list and using function sGraph finds all subgraphs, using function removeIso removes all isomorphism.
def subGraph(num):
    Hgraph=[]
    
    Hgraph = sGraph(num, Hgraph)
    Hgraph = removeIso(Hgraph)

    return Hgraph

#name: sGraph
#input: num=size, empty list
#output: list of subgraphs
#explanation: recursively finds all subgraphs. Goes to base case size=2 and finds all subgraphs, later on uses combi to find
#             all subgraphs with a new node, sends it with a list of all subgraphs of previous size and number of nodes.
def sGraph(num, arr):
    if num==1:
        G = DiGraph()
        G.add_edge(1,1)
        arr.append(G.copy())

        return arr
    if num==2:
        G = DiGraph()
        G.add_edge(1,2)
        arr.append(G.copy())
        G.add_edge(2,1)
        arr.append(G.copy())
        G.clear()
        G.add_edge(2,1)
        arr.append(G.copy())

        return arr
    else:
        arr = sGraph(num-1, arr)
        comb = []
        for i in range(1,len(arr[0].nodes())+1):
            comb.append(list(combinations(arr[0].nodes(), i)))
        arr_size= len(arr)
        return combi(arr,num)

#name:  combi
#input: list of nodes and size
#output: list of subgraphs
#explanation: creates a directed graph with all possibled edges between size and list of nodes
#             then finds all possible combination of edges possible in a graph with number of
#             size nodes. After that creates all subgraphs with those edges and adds them to arr1.
def combi(arr, size):
    arr1 = []
    comb1 = []
    G = DiGraph()
    for i in range(1,size):
        G.add_edge(size,i)
        G.add_edge(i,size)
    for i in range(1,size*(size-1)):
        comb1.append(list(combinations(G.edges(), i)))
    arr_size= len(arr)
    for z in range(arr_size):
        for i in range(len(comb1)):
            for j in range(len(comb1[i])):
                tmp=arr[z].copy()
                for n in range(len(comb1[i][j])):
                    tmp.add_edge(comb1[i][j][n][0],comb1[i][j][n][1])
                arr1.append(tmp)
    return arr1


#name: removeIso
#input: list of subgraphs
#output: list of subgraphs
#explanation: goes over all the subgraphs which are the same size and checks if they are isomorphics, and if they are removes one of them
def removeIso(Hgraph):
    size = len(Hgraph)
    i=0
    while i<size:
        j=0
        while j<size:
            if (i!=j) and (is_isomorphic(Hgraph[i], Hgraph[j])):
                Hgraph.remove(Hgraph[j])
                size = len(Hgraph)
            else:
                j=j+1
        i=i+1

    return Hgraph

#name: codeToText
#input: list of edges, size, list of appearance of each motif
#output: txt file and pritn the results
#explanation: gets a list of edges of all subgraphs (those are the motifs) and creates a txt file according to 
#             instruction in the exercise.
def codeToText(anwser, size, counts):
    n=0
    str1 = ""
    flag=0
    for i in range(len(anwser)):
        str1 = str1 + "#" +str(n+1) + "\ncount = " + str(counts[n]) + "\n"
        str2 = ""
        for char in str(anwser[i]):
            if not (char=='(' or char==')' or char=='[' or char==']' or char==' ' or (char==',' and flag%2==0)):
                if char==',':
                    str2 = str2 + ' '
                else:
                    str2 = str2 + char
                    flag=flag+1
                if flag%2==0:
                    str2 = str2 + '\n'
        str1 = str1 + str2
        n=n+1
    
    str_done = ""
    str_done = "n = " + str(size)
    str_done = str_done + "\n"
    str_done = str_done + "count = "+ str(n)
    str_done = str_done + "\n"
    str_done = str_done +str1

    str_name = "results_n=" + str(size) + "_b.txt"
    with open(str_name, 'w') as fw:
        fw.write(str_done)
    print(str_done)


#name: countMotif
#input: list of motifs, list of subgraphs
#output: number of apperances of each motif
#explanation: goes over the motifs and check how many times they appear in subgraphs of the given graph
def countMotif(motifs, sGraphs):
    counts = []
    for i in range(len(motifs)):
        counts.append(0)
        for sg in sGraphs:
            if is_isomorphic(motifs[i],sg):
                counts[i]=counts[i]+1
    return counts
        
#name: sGraph2
#input: graph, size
#output: list of all subgraphs of size==n
#explanation: goes over the graph and find all edges, find all combinations of the edges, number of edges are according to size.
#             create subgraphs of the combinations, find if all edges are connected and if they are add the subgraph to a list.
def sGraph2(G, n):
    arr = []
    for i in G.edges():
        arr.append(i)
    comb = []
    for i in range(1, n+1):
        comb = comb + (list(combinations(arr, i)))
    tmp = []
    for i in range(len(comb)):
        graph = DiGraph()
        for j in range(len(comb[i])):
            graph.add_edge(comb[i][j][0],comb[i][j][1])
        if is_connected(graph.to_undirected()):
            tmp.append(graph)

    return tmp
    
#name: totalGraphs
#input: graph and size
#explanation: find all motifs with function subGraph, and using sGraph2 find all subgraphs of given graph G, using the function
#             countMotif find the number of times each motif is in the subgraphs. Send the results to codeTotext to create a
#             text file of the results.
def totalGraphs(G, size):

    anwser = subGraph(size)

    counts = countMotif(anwser,sGraph2(G,size))

    tmp = []
    for i in range(len(anwser)):
        tmp.append(anwser[i].edges())

    codeToText(tmp, size, counts)


totalGraphs(graph, int(size[1]))