import csv
import math
import sys
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
data_set = []
features = ["Temperature","Humidity","Light","Co2","HumidityRatio"]
count = 0

def read_data(id):
    global data_set
    global features
    csv1 = None
    data_set = []
    if id == 0:
        with open('occupancy_A.csv') as csvfile:
            csv1 = csv.reader(csvfile,delimiter = ',')
            count = 0
            for row in csv1:
                # print(row)
                if count != 0:
                    each_row = [row[0],row[1],row[2],row[3],row[4],row[5]]
                    data_set.append(each_row)
                count+=1
    elif id == 1:
        with open('occupancy_B.csv') as csvfile:
            features = ["Temperature","Humidity","Co2","HumidityRatio"]
            csv1 = csv.reader(csvfile,delimiter = ',')
            count = 0
            for row in csv1:
                # print(row)
                if count != 0:
                    each_row = [row[0],row[1],row[2],row[3],row[4]]
                    data_set.append(each_row)
                count+=1
    # print(data_set)

def entropy(dist):
    if dist[0] == 0 or dist[0] == 1:
        return 0
    return -((dist[0] * math.log(dist[0],2)) + (dist[1] * math.log(dist[1],2)))

def information_gain(data, feature, splitpoint, entro, prev,index):
    length = len(data)
    current = [0,0,0,0]
    # print(splitpoint, index)
    if index == 0:
        # print(feature)
        for i in range(length):
            if float(data[i][feature]) < splitpoint:
                index = i
                if data[i][-1] == '1':
                    current[0]+=1
                elif data[i][-1] == '0':
                    current[1]+=1
            elif float(data[i][feature]) > splitpoint:
                if data[i][-1] == '1':
                    current[2]+=1
                elif data[i][-1] == '0':
                    current[3]+=1
        # print(data[index][feature], splitpoint, data[index+1][feature])
        # print(index)
    else:
        # print("elif")
        current = prev
        for i in range(index+1, length):
            # print(i)
            if float(data[i][feature]) < splitpoint:
                index = i
                if data[i][-1] == '1':
                    current[2]-=1
                    current[0]+=1
                elif data[i][-1] == '0':
                    current[3]-=1
                    current[1]+=1
            elif float(data[i][feature]) > splitpoint:
                break
    total1 = current[0]+current[1]
    total2 = current[2]+current[3]
    # print(length, total1, total2)
    infoGain = entro - (total1/length)*entropy([current[0]/total1,current[1]/total1]) - (total2/length)*entropy([current[2]/total2,current[3]/total2])
    # print(infoGain)
    return infoGain, current, index

def choose_feature_split(data):
    length = len(data)
    all_split = []
    length2 = len(data[0])
    for j in range(length2-1):
        data = sorted(data, key = lambda col: float(col[j]))
        # look for split point in feature1
        feature1 = []
        for i in range(1,length):
            # check if not the same
            if data[i][j] == data[i-1][j]:
                continue
            else:
                x = data[i-1][j]
                labelX = data[i-1][-1]
                y = data[i][j]
                labelY = data[i][-1]
                # check if there exist a different label
                if labelX != labelY:
                    feature1.append((float(x)+float(y))/2)
                else:
                    iter = i-2
                    found = False
                    while iter >= 0:
                        if data[iter][j] == x and data[iter][-1] != labelY:
                            feature1.append((float(x)+float(y))/2)
                            found = True
                            break
                        elif data[iter][j] != x:
                            break
                        iter-=1
                    if found:
                        continue
                    iter = i+1
                    while iter < length:
                        if data[iter][j] == y and data[iter][-1] != labelX:
                            feature1.append((float(x)+float(y))/2)
                            break
                        elif data[iter][j] != y:
                            break
                        iter+=1
        all_split.append(feature1)
    
    positive = 0
    negative = 0
    for i in range(length):
        if data[i][-1] == '1':
            positive+=1
        else:
            negative+=1
        
    entro = entropy([positive/length,negative/length])

    maxInfoGain = 0
    splitpoint = None
    # print(len(all_split))
    for i in range(length2-1):
        data = sorted(data, key = lambda col: float(col[i]))
        all_split[i].sort()
        # print(all_split)
        # print(data)
        prev = [0,0,0,0] #positive example before split, negative example before split, positive example after split, negative example after split
        index = 0
        for j in range(len(all_split[i])):
            # print(all_split[i][j])
            infoGain, prev, index = information_gain(data,i,all_split[i][j],entro,prev,index)
            if infoGain > maxInfoGain:
                maxInfoGain = infoGain
                splitpoint = [i,all_split[i][j]]
    return splitpoint
            
class MyNode:
    def __init__(self, splitpoint, feature, parent, leaf):
        self.splitpoint = splitpoint
        self.feature = feature
        self.decision = None
        self.leftChild = None
        self.rightChild = None
        self.parent = parent
        self.leaf = leaf

    def split(self,data,maxDepth):
        length = len(data)
        less = []
        more = []
        negative = 0
        positive = 0
        if self.splitpoint != None:
            for i in range(length):
                if float(data[i][self.feature]) < self.splitpoint:
                    less.append(data[i])
                else:
                    more.append(data[i])
                if data[i][-1] == '0':
                    negative+=1
                else:
                    positive+=1
        else:
            for i in range(length):
                if data[i][-1] == '0':
                    negative+=1
                else:
                    positive+=1
        # print(positive, negative)
        if maxDepth == 1:
            if positive > negative:
                self.decision = True
            else:
                self.decision = False
            self.leaf = True
        elif negative == 0 and positive != 0:
            self.decision = True
            self.leaf = True
        elif negative != 0 and positive == 0:
            self.decision = False
            self.leaf = True
        elif self.splitpoint == None:
            if positive > negative:
                # print(">")
                self.decision = True
            else:
                # print("<")
                self.decision = False
            self.leaf = True
        elif negative == 0 and positive == 0:
            self.decision = self.parent.decision
            self.leaf = True
        else:
            if positive > negative:
                # print(">")
                self.decision = True
            else:
                self.decision = False
            split1 = choose_feature_split(less)
            if split1 == None:
                self.leftChild = MyNode(None,None,self,False)
            else:
                self.leftChild = MyNode(split1[1],split1[0],self,False)
            self.leftChild.split(less,maxDepth-1)
            split2 = choose_feature_split(more)
            # print(split2)
            if split2 == None:
                self.rightChild = MyNode(None,None,self,False)
            else:
                self.rightChild = MyNode(split2[1], split2[0],self,False)
            self.rightChild.split(more, maxDepth-1)

    def get_decision(self,data_point):
        if self.leaf == True:
            return self.decision
        else:
            if float(data_point[self.feature]) < self.splitpoint:
                return self.leftChild.get_decision(data_point)
            elif float(data_point[self.feature]) > self.splitpoint:
                return self.rightChild.get_decision(data_point)


class Tree:
    def __init__(self, x):
        read_data(x)
        split = choose_feature_split(data_set)
        self.root = MyNode(split[1],split[0], None, False)

    def train_tree(self, data, maxDepth):
        self.root.split(data, maxDepth)
    
    def get_prediction_accuracy(self, data):
        length = len(data)
        correct = 0
        for i in range(length):
            if self.root.get_decision(data[i]) == int(data[i][-1]):
                correct+=1
        return correct/length

    def plot(self,path):
        root = self.plot_tree(None, self.root, "Root: ")
        DotExporter(root).to_picture(path)

    def plot_tree(self, par, node, lr):
        global count
        root = None
        if par == None:
            root = Node(lr+features[node.feature] +" "+str(node.splitpoint))
        else:
            if node.leaf:
                root = Node(lr+str(node.decision)+str(count), parent=par)
                count+=1
            else:
                root = Node(lr+features[node.feature] +" "+str(node.splitpoint), parent=par)
        if node.leftChild != None:
            self.plot_tree(root, node.leftChild, "Less: ")
        if node.rightChild != None:
            self.plot_tree(root, node.rightChild, "More: ")
        return root

def cross_validation(data, path, n, m):
    global data_set
    highest_validation = 0
    highest_depth = 0
    validations = []
    trainings = []
    depths = []
    for i in range(n,m):
        depths.append(i)
        print("Depth:"+str(i))
        training = 0
        validation = 0
        for j in range(5):
            length = len(data)
            seg = int(length/5)
            tree = Tree(int(sys.argv[1])) 
            random.shuffle(data_set)
            tree.train_tree(data_set[0:seg*4], i)
            training+=tree.get_prediction_accuracy(data_set[0:seg*4])
            validation+=tree.get_prediction_accuracy(data_set[seg*4:length])
        training/=5
        validation/=5
        print("Average Training:"+str(training))
        print("Average Validation:"+str(validation))
        validations.append(validation)
        trainings.append(training)
        if validation > highest_validation:
            highest_validation = validation
            highest_depth = i
    plt.plot(depths,trainings)
    plt.plot(depths,validations,'r')
    plt.ylabel('Average Percentage')
    plt.show()
    if int(sys.argv[1]) == 0:
        plt.savefig("percentage.png")
    elif int(sys.argv[1]) == 1:
        plt.savefig("percentage2.png")
    tree = Tree(int(sys.argv[1]))
    tree.train_tree(data_set,highest_depth)
    tree.plot(path)
    print(tree.get_prediction_accuracy(data_set))
    print(highest_depth)
    return highest_depth



if len(sys.argv) == 3:
    #first argument dataset, second argument algorithm
    if sys.argv[2] == '0':
        tree = Tree(int(sys.argv[1]))
        tree.train_tree(data_set,20)
        print(tree.get_prediction_accuracy(data_set))
        tree.plot("t1.pdf")
    if sys.argv[2] == '1':
        if sys.argv[1] == '0':
            read_data(0)
            cross_validation(data_set, "t2.pdf", 9, 16)
        elif sys.argv[1] == '1':
            read_data(1)
            cross_validation(data_set, "t3.pdf", 17, 30)
