from itertools import combinations
from networkx import DiGraph,is_isomorphic

################################################
# Exercise 1 part 1, find all motifs of size=n #
################################################

# change the number in size.txt
f = open("size.txt", "r")
tmp = f.readline()
size = tmp.split('=')

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
    # is num==1 there is only one possible subgraph
    if num==1:
        G = DiGraph()
        G.add_edge(1,1)
        arr.append(G.copy())

        return arr
    
    #base case if num > 1
    elif num==2:
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
        #recursively find all subgraphs of size num-1
        arr = sGraph(num-1, arr)
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

    #find all possible edges in graph of size = size
    for i in range(1,size):
        G.add_edge(size,i)
        G.add_edge(i,size)
    
    #find all possible combinations of edges
    for i in range(1,size*(size-1)):
        comb1.append(list(combinations(G.edges(), i)))
    
    arr_size= len(arr)
    for z in range(arr_size):
        for i in range(len(comb1)):
            for j in range(len(comb1[i])):
                # tmp is a subgraph in size = size-1
                tmp=arr[z].copy()
                #add diffrent combinations of edges with new node
                for n in range(len(comb1[i][j])):
                    tmp.add_edge(comb1[i][j][n][0],comb1[i][j][n][1])
                #add new subgraph to new list, arr1 is all possible subgraphs
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
            #if there is ismporphism remove one of the graphs, if there isn't keep looking
            if (i!=j) and (is_isomorphic(Hgraph[i], Hgraph[j]) and (Hgraph[i].size()==Hgraph[j].size())):
                Hgraph.remove(Hgraph[j])
                size = len(Hgraph)
            else:
                j=j+1
        i=i+1

    return Hgraph

#name: codeToText
#input: list of edges, size
#output: txt file and pritn the results
#explanation: gets a list of edges of all subgraphs and creates a txt file according to instruction in the exercise.
def codeToText(anwser, size):
    n=0
    str1 = ""
    flag=0
    for i in range(len(anwser)):
        #number of motif
        str1 = str1 + "#" +str(n+1) + "\n"
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
    
    #number of total motifs
    str_done = ""
    str_done = "n = " + str(size)
    str_done = str_done + "\n"
    str_done = str_done + "count = "+ str(n)
    str_done = str_done + "\n"
    str_done = str_done +str1

    #output txt file to directory
    str_name = "results_n=" + str(size) + "_a.txt"
    with open(str_name, 'w') as fw:
        fw.write(str_done)
    print(str_done)

#name: totalGraphs
#input: size
#explanation: gets number n, with the subGraph function creates all the subgraphs of size 1 to n, saves in a list (tmp) and sends it
#             to codeToText.              
def totalGraphs(size):

    anwser = subGraph(size)
    tmp = []

    #tmp is a list with all the edges of the subgraphs
    for i in range(len(anwser)):
        tmp.append(anwser[i].edges())

    codeToText(tmp, size)


totalGraphs(int(size[1]))