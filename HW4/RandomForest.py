import csv
import numpy as np  # http://www.numpy.org
import ast
import random


"""
Here, X is assumed to be a matrix with n rows and d columns
where n is the number of total records
and d is the number of features of each record
Also, y is assumed to be a vector of d labels
"""

class RandomForest(object):
    class __DecisionTree(object):
        def __init__(self, leaf_size = 5): 
            self.tree = {}
            self.leaf_size = leaf_size
            
        #We will try to use the entropy for making the tree. It ensures that each split we create
        #has maximum homogenity.
        
        '''    
        def entropy (data):
            #Formula for entropy is -p * log2(p) where p is the proportion of each category
            counter = {}
            #We will keep the response variable at the end
            for i in data:
                key = i[len(i) - 1]
                if key not in counter: counter[key] = 0
                counter[key] += 1
            #This counter dictionary will give us the count for each unique entry in the
            #response variable.
            #Now we need the proportion and the log.
            from math import log
            prop = [float(i)/len(data) for i in counter.values()]
            ent = [-float(i) * float(log(float(i), 2)) for i in prop]
            #We need the sum to get to the final value of the entropy
            return sum(ent)
            
        #To get the best split, however, we first need a function that
        #splits the dataset.
        
        #The data here assumes a numpy array
        def split_data(data, col, split_value):
            #define the function according to the type of data
            
            if isinstance(split_value,int) or isinstance(split_value,float):
                splt1= [i for i in data if float(i[col]) >= split_value]
                splt2= [i for i in data if float(i[col]) < split_value]
            else:
                splt1= [i for i in data if float(i[col]) == split_value]
                splt2= [i for i in data if float(i[col]) != split_value]
            
            return splt1, splt2
        '''
            
        #Using the entropy in the tree is slow and hard to implement.
        def build_tree(self,data):
            #CHecking if the tree has reached a leaf.
            #The recursive algorithm will finally always reach a leaf depending on the size. 
            if data.shape[0] <= self.leaf_size:
                #If it is a leaf, there will not be any further left and right tree.
                return np.array([-1 , np.average(data[:,-1]) , np.nan, np.nan]).reshape(1,4)
            if sum(data[:,-1] == data[0,-1]) == data.shape[0]:
                return np.array([-1 , data[0,-1] , np.nan, np.nan]).reshape(1,4)
            else:
                #This will build the tree when not reached leaf.
                #This selects a random feature at first and then selects 2 random values of
                #that feature and takes the average of that to ensure less bias.
                rand_feat = random.randint(0,data.shape[1]-2)
                             
                rand_r1 = random.randint(0,data.shape[0]-1)
                
                rand_r2 = random.randint(0,data.shape[0]-1)
                
                SplitVal = (data[rand_r1 , rand_feat] + data[rand_r2 , rand_feat])/2
                
                while_break = 0
                while (SplitVal == np.amax(data[:,rand_feat])):
                    rand_feat = random.randint(0,data.shape[1]-2)
                    SplitVal = (data[rand_r1 , rand_feat] + data[rand_r2 , rand_feat])/2
                    while_break = while_break + 1
                    
                    if while_break > (data.shape[1] * 0.5):
                        return np.array([-1 , np.average(data[:,-1]) , np.nan, np.nan]).reshape(1,4)
                
                #This is where we are doing the recursions. Calling the function within itself.
                leftree = self.build_tree(data[data[:,rand_feat]<=SplitVal])
                #For each node, building a left and right tree for it.
                righttree = self.build_tree(data[data[:,rand_feat]>SplitVal])
                root    =   np.array([rand_feat,SplitVal,1,leftree.shape[0]+1]).reshape(1,4)
               
                self.tree = np.concatenate((root,leftree,righttree) , axis = 0)
            
                return self.tree
                
#This function take the predictors and response, makes it into a dataset and predicts on it.
        def learn(self, X, y):
            # TODO: train decision tree and store it in self.tree
            data = np.zeros((X.shape[0],X.shape[1]+1))
            data[:,:-1] = X
            data[:,-1] = y
            self.tree=self.build_tree(data)
            pass
        
        #This function uses the tree we made to make predictions about the response on new rows of data.
        def classify(self, record):
            # TODO: return predicted label for a single record using self.tree
            Tree_pred =np.zeros([record.shape[0]])
            
            n_p=0
            
            while(self.tree[n_p][0]!=-1.0):
                if record[self.tree[n_p][0]]<=self.tree[n_p][1]:
                    n_p=n_p+int(self.tree[n_p][2])
                else:
                    n_p=n_p+int(self.tree[n_p][3])
            Tree_pred = self.tree[n_p][1]
            return Tree_pred


    num_trees = 0
    tree={}
    decision_trees = []
    bootstraps_datasets = [] # the bootstrapping dataset for trees
    bootstraps_labels = []   # the true class labels,corresponding to records in the bootstrapping dataset

    def __init__(self, num_trees):
        self.num_trees = num_trees
        self.decision_trees = [self.__DecisionTree() for i in range(num_trees)]

    #This will create random bootstrapped samples for each tree.
    def _bootstrapping(self, XX, n):
        # TODO: create a sample dataset with replacement of size n
        #
        # Note that you will also need to record the corresponding
        #           class labels for the sampled records for training purpose.
        #
        # Referece: https://en.wikipedia.org/wiki/Bootstrapping_(statistics)
        
        #Again, convert to numpy array
        samp_data=[]
        XX = np.array(XX)
        for i in range (n):
            samp_data.append(random.randint(0,n-1))
            
        samp_data = np.array(samp_data)
        
        predictors = XX[samp_data,0:-1]
        response = XX[samp_data,-1]
        return (predictors, response)

    #This will create random booststrapped samples with replacement to use for forest.   
    def bootstrapping(self, XX):
        # TODO: initialize the bootstrap datasets for each tree.
        for i in range(self.num_trees):
            data_sample, data_label = self._bootstrapping(XX, len(XX))
            self.bootstraps_datasets.append(data_sample)
            self.bootstraps_labels.append(data_label)

    #This will make a collection of tree which will be ou forest and which we will use for final prediction.
    def fitting(self):
        for i in range(self.num_trees):
            (self.decision_trees[i]).learn(self.bootstraps_datasets[i],self.bootstraps_labels[i])
        pass

    #This function makes the prediction using the forest.
    def voting(self, X):
        y = np.array([], dtype = int)
        for record in X:
            votes = []
            for i in range(len(self.bootstraps_datasets)):
                dataset = self.bootstraps_datasets[i]
                if list(record) not in dataset.tolist():
                    OOB_tree = self.decision_trees[i]
                    effective_vote = OOB_tree.classify(record)
                    votes.append(effective_vote)
            counts = np.bincount(votes)
            if len(counts) == 0:
                y = np.append(y,0)
            else:
                y = np.append(y, np.argmax(counts))
        return y


def main():
    X = list()
    y = list()
    XX = list() # Contains data features and data labels

    # Note: you must NOT change the general steps taken in this main() function.

    # Load data set
    with open("hw4-data.csv") as f:
        next(f, None)

        for line in csv.reader(f, delimiter = ","):
            X.append(line[:-1])
            y.append(line[-1])
            xline = [ast.literal_eval(i) for i in line]
            XX.append(xline[:])

    # Initialize according to your implementation
    forest_size = 30

    # Initialize a random forest
    randomForest = RandomForest(forest_size)

    # Create the bootstrapping datasets
    randomForest.bootstrapping(XX)

    # Build trees in the forest
    randomForest.fitting()

    # Provide an unbiased error estimation of the random forest
    # based on out-of-bag (OOB) error estimate.
    # Note that you may need to handle the special case in
    #       which every single record in X has used for training by some
    #       of the trees in the forest.
    y_truth = np.array(y, dtype = int)
    X = np.array(X, dtype = float)
    y_predicted = randomForest.voting(X)

    results = [prediction == truth for prediction, truth in zip(y_predicted, y_truth)]

    # Accuracy
    accuracy = float(results.count(True)) / float(len(results))
    print "accuracy: %.4f" % accuracy

main()
