import math
import random
import numpy as np
from typing import List
class NeuronNetwork:
    def __init__(self,num_in:int,num_out:int,hidden:List[int]=[],activation='sigmoid'):
        self.nnArchitecture = []
        self.weights = {}
        if len(hidden) == 0:
            self.nnArchitecture.append({'in_dim':num_in,'out_dim':num_out,'activation':activation})
        else:
            hidden.append(num_out)
            in_d = num_in
            out_d = hidden[0]
            for i in range(len(hidden)):
                out_d = hidden[i] 
                if i < len(hidden)-1:
                    self.nnArchitecture.append({'in_dim':in_d,'out_dim':out_d,'activation':'relu'})
                else:
                    self.nnArchitecture.append({'in_dim':in_d,'out_dim':out_d,'activation':activation})
                in_d = hidden[i]
        self.initialize_weight()
    
    def initialize_weight(self,seed=99):
        for i in range(len(self.nnArchitecture)):
            self.weights[i] = np.random.randn(self.nnArchitecture[i]['out_dim'],self.nnArchitecture[i]['in_dim']+1)

    def guess(self,input:List[int])->bool:
        input_np = np.array([input+[1]])
        result = np.transpose(input_np)
        for layer in self.weights:
            if self.nnArchitecture[layer]['activation'] == 'sigmoid':
                result = self.sigmoid(self.weights[layer].dot(result))
            elif self.nnArchitecture[layer]['activation'] == 'relu':
                result = self.relu(self.weights[layer].dot(result))
            else:
                result = self.weights[layer].dot(result)
            result = np.vstack([result,[1]])
        
        if result[0][0] < 0.5:
            return False
        else:
            return True
            
    def mutate(self,rate:float):
        for matrix in self.weights:
            for i1 in range(len(self.weights[matrix])):
                for i2 in range(len(self.weights[matrix][i1])):
                    rd_num =  random.randrange(0, 100, 1)
                    if rd_num/100 <= rate:
                        # print(self.weights[matrix][i1])
                        self.weights[matrix][i1,i2] = random.uniform(self.weights[matrix][i1,i2]*(1-rate), self.weights[matrix][i1,i2]*(1+rate))
                        # self.weights[matrix][i1,i2] = random.randrange(0, 1)
                        # print(self.weights[matrix][i1])
                    
        return

    def sigmoid(self,X):
        return 1/(1+np.exp(-X))
    
    def relu(self,X):
        return np.maximum(0,X)


    
# brain = NeuronNetwork(2,1,[3,4])
# print(brain.guess([1,2]))
                