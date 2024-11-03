

import random
import argparse
import codecs
import os
import numpy

# Sequence - represents a sequence of hidden states and corresponding
# output variables.

class Sequence:
    def __init__(self, stateseq, outputseq):
        self.stateseq  = stateseq   # sequence of states
        self.outputseq = outputseq  # sequence of outputs
    def __str__(self):
        return ' '.join(self.stateseq)+'\n'+' '.join(self.outputseq)+'\n'
    def __repr__(self):
        return self.__str__()
    def __len__(self):
        return len(self.outputseq)

# HMM model
class HMM:
    def __init__(self, transitions={}, emissions={}):
        """creates a model from transition and emission probabilities
        e.g. {'happy': {'silent': '0.2', 'meow': '0.3', 'purr': '0.5'},
              'grumpy': {'silent': '0.5', 'meow': '0.4', 'purr': '0.1'},
              'hungry': {'silent': '0.2', 'meow': '0.6', 'purr': '0.2'}}"""



        self.transitions = transitions
        self.emissions = emissions

    ## part 1 - you do this.
    def load(self, basename):
        """reads HMM structure from transition (basename.trans),
        and emission (basename.emit) files,
        as well as the probabilities."""
        print(basename)
        with open(str(basename) + ".emit") as f:
            for lines in f : 
                words = lines.rstrip('\n').split(" ")
                                #start of edge
                key = words[0]
                #end of edge
                edge = words[1]
                #value of the edge
                value = words[2]

                #https://www.geeksforgeeks.org/python-check-given-key-already-exists-in-a-dictionary/ referenced this 
                #check if key exists
                if key not in self.emissions :
                    self.emissions[key] = {} 
                    self.emissions[key][edge] = value
                else :
                    self.emissions[key][edge] = value

                print(len(self.emissions[words[0]]))

        with open(str(basename) + ".trans") as f:
            for lines in f : 
                words = lines.rstrip('\n').split(" ")
                                #start of edge
                key = words[0]
                #end of edge
                edge = words[1]
                #value of the edge
                value = words[2]

                #https://www.geeksforgeeks.org/python-check-given-key-already-exists-in-a-dictionary/ referenced this 
                #check if key exists
                if key not in self.transitions :
                    self.transitions[key] = {} 
                    self.transitions[key][edge] = value
                else :
                    self.transitions[key][edge] = value

        return 


   ## you do this.
    def generate(self, n):

        """return an n-length Sequence by randomly sampling from this HMM."""
        print(list(self.transitions['#']))
        print(list(self.transitions['#'].values()))
        states = []
        emissions = []
        #gets the starting state with probabilities by turning key value pairs into lists
        initial_state = numpy.random.choice(list(self.transitions['#']), p=list(self.transitions['#'].values()))
        initial_emission = numpy.random.choice(list(self.emissions[initial_state]), p=list(self.emissions[initial_state].values()))
        
        states.append(initial_state)
        emissions.append(initial_emission)
        
       # print("initial state: " + initial_state)
       # print("inital emission: " + initial_emission)
        next_state = "" 
        #->send in happy
        for i in range(n-1) :
            ## if next state is not empty
            if next_state == "":
                #get value for the inital state
                next_state =  numpy.random.choice(list(self.transitions[initial_state]), p=list(self.transitions[initial_state].values()))
            else:
                next_state = numpy.random.choice(list(self.transitions[next_state]), p=list(self.transitions[next_state].values()))
            emission = numpy.random.choice(list(self.emissions[next_state]), p=list(self.emissions[next_state].values()))
            
            states.append(next_state)
            emissions.append(emission)
           
        
        state_list = ""
        for s in states:
            state_list = state_list + s + " "
        print(state_list)

        emission_list = ""
        for e in emissions: 
            emission_list = emission_list + e + " "
        print(emission_list)
       
        #goal 
        return Sequence(states,emissions)
    
    '''
    set up inital matrix with P=1.0 for the # state
    for each state on day 1: P(state | eo) = d(eo | sat)

    for i = 2 to n :
        for each state s:
        sum = 0
        for s2 in states :
            sum += M[s2, i-1] * T[s2,s] * E[O[i],s]
            

            M[s2,i] = sum
    '''

    

    def forward(self, sequence):
        matrix = []
        keys = list(self.transitions.keys()) 
        print(keys)
        emissions = self.emissions
        transitions = self.transitions

        #outputs = sequence.outputseq
        #sequence_length = len(sequence) + 1

        outputs = ['purr','silent','silent','meow','meow']
        sequence_length = len(outputs) + 1
        

        for s in keys:
            states = []
            if s == "#" :
                for i in range(sequence_length) :
                    states.append(1.0) 
            else :
                for i in range(sequence_length) :
                    states.append(0.0)
            matrix.append(states)
        
        state_values = self.transitions.keys()
        print(state_values)
        #lets say the first value is purr
        starting_state = 0
        i = 0
        for s in state_values:
            if s == '#' :
                starting_state = i
                matrix[i][1] = 0
            else :
                print(outputs[0]) 
                if outputs[0] not in emissions[s] :
                    matrix[i][1] = 0
                else :
                    matrix[i][1] = float(emissions[s][outputs[0]]) * float(transitions['#'][s]) * matrix[starting_state][0]
            i = i + 1


        for i in range(2,len(outputs) + 1) :
            for s in keys:

                # set # to 0 and skip #
                if s == '#' :
                    print(starting_state)
                    print(i)
                    matrix[starting_state][i] = 0
                    continue

                sum = 0
                #happy
                for s2 in keys :
                    if s2 == '#':
                        continue
                    #print(s2)
                   # print("PREVIOUS VALUE: " + str(matrix[keys.index(s2)][i-1]))
                    #print(outputs[i-1])
                    # something like [happy's][silents]
                    #print("EMISSION: " + str(emissions[s][outputs[i-1]]))
                    #print("TRANSITION: " + transitions[s2][s])

                    if outputs[i-1] not in emissions[s] :
                        sum = sum + 0
                    else :
                        print("Current State: " +str(s))
                        print(s2)
                        print("PREVIOUS VALUE: " + str(matrix[keys.index(s2)][i-1]))   
                        print("EMISSION: " + str(emissions[s][outputs[i-1]]))
                        print("TRANSITION: " + transitions[s2][s])
                        
                        sum = sum + float(matrix[keys.index(s2)][i-1]) * float(emissions[s][outputs[i-1]])  * float(transitions[s2][s]) 
                        print("SUM " + str(sum))
                    #print("SUM: " + str(sum))
                
                print("--------")
                print("TOTAL SUM: " + str(sum))
                print("--------")
                matrix[keys.index(s)][i] = sum
            #print(i)
       
        debug_matrix = numpy.array(matrix)

   
    
        print(debug_matrix)
        print(matrix)
        print(outputs)
        print(sequence)
        print(keys)

        print(len(matrix))
        max = -1
        max_state = ""
        values = 0
        print(keys)
        for i in range(len(matrix)):
            if matrix[i][len(outputs)] > max :
                max = matrix[i][len(outputs)]
                max_state = keys[i]
            values = values + matrix[i][len(outputs)]
 
            print(matrix[i][len(outputs)])   
        print("FORWARD RESULT: " + max_state)
        print("Probability: " + str(max / values))
        return max_state
        #matrix is now a list of lists 
        
    ## you do this: Implement the Viterbi algorithm. Given a Sequence with a list of emissions,
    ## determine the most likely sequence of states.






    def viterbi(self, sequence):
        pass
    ## You do this. Given a sequence with a list of emissions, fill in the most likely
    ## hidden states using the Viterbi algorithm.

if __name__ == "__main__":
    #print(car_infer.query(variables=["Moves"],evidence={"Radio":"turns on", "Starts":"yes"}))
    h = HMM()
    h.load('cat')
    print(h.transitions)
    print("------------------------")
    print(h.emissions)
    seq = h.generate(5)
    print(seq)
    h.forward(seq)
    


