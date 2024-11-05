import sys
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
        print('CURRENT DOMAIN: ' + basename)
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
        print("Generating...")
        """return an n-length Sequence by randomly sampling from this HMM."""
        #print(list(self.transitions['#']))
        #print(list(self.transitions['#'].values()))
        
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
        #initialize the matrix
        matrix = []

        #get all the types of states
        keys = list(self.transitions.keys()) 
        print(keys)
        #define emissions and transitions
        emissions = self.emissions
        transitions = self.transitions

        #get the observations
        outputs = sequence
        sequence_length = len(sequence) + 1

        #outputs = ['purr','silent','silent','meow','meow']
        #sequence_length = len(outputs) + 1
        
        #Initalize the matrix and set # to 1 
        for s in keys:
            states = []
            if s == "#" :
                for i in range(sequence_length) :
                    states.append(1.0) 
            else :
                for i in range(sequence_length) :
                    states.append(0.0)
            matrix.append(states)
        
        
        #check where the value of starting state is
        starting_state = 0
        i = 0

        #initial the '-' column 
        for s in keys:
            #if set the starting to 0
            if s == '#' :
                starting_state = i
                matrix[i][1] = 0
            else :
                #get the starting values
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
                    print('Starting  State: '  + str(starting_state))
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

        max = -1
        max_state = ""
        values = 0
        print(keys)

        #Get the max probability and the state
        for i in range(len(matrix)):
            if matrix[i][len(outputs)] > max :
                max = matrix[i][len(outputs)]
                max_state = keys[i]
            values = values + matrix[i][len(outputs)]
 
            print(matrix[i][len(outputs)])   
            
        print(sequence)
        print("FORWARD RESULT: " + max_state)
        print("Probability: " + str(max / values))
        return max_state
        #matrix is now a list of lists 
        
    ## you do this: Implement the Viterbi algorithm. Given a Sequence with a list of emissions,
    ## determine the most likely sequence of states.






    def viterbi(self, sequence):
          #initialize the matrix
        matrix = []
        backtrack_matrix = []

        #get all the types of states
        keys = list(self.transitions.keys()) 
        print(keys)
        #define emissions and transitions
        emissions = self.emissions
        transitions = self.transitions

        #get the observations
        outputs = sequence
        sequence_length = len(sequence) + 1

        #outputs = ['purr','silent','silent','meow','meow']
        #sequence_length = len(outputs) + 1
        
        #Initalize the matrix and set # to 1 
        for s in keys:
            states = []
            backtrack = []
            if s == "#" :
                for i in range(sequence_length) :
                    states.append(1.0) 
                    backtrack.append(1.0)
            else :
                for i in range(sequence_length) :
                    states.append(0.0)
                    backtrack.append(0)

            backtrack_matrix.append(backtrack)
            matrix.append(states)
        
        
        #check where the value of starting state is
        starting_state = 0
        i = 0

        #initial the '-' column 
        for s in keys:
            #if set the starting to 0
            if s == '#' :
                starting_state = i
                matrix[i][1] = 0
            else :
                #get the starting values
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
                    print('Starting  State: '  + str(starting_state))
                    print(i)
                    matrix[starting_state][i] = 0
                    backtrack_matrix[starting_state][i] = 0
                    continue

                sum = 0
                observe_max = -1
                max_index = 0

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
                    
                        print("Current State: " + str(s))
                        print(s2)
                        print("PREVIOUS VALUE: " + str(matrix[keys.index(s2)][i-1]))   
                        print("EMISSION: " + str(emissions[s][outputs[i-1]]))
                        print("TRANSITION: " + transitions[s2][s])
                        observation_val = float(matrix[keys.index(s2)][i-1]) * float(emissions[s][outputs[i-1]])  * float(transitions[s2][s])
                        sum = sum + observation_val
                        
                        if (observation_val > observe_max) :
                            observe_max = observation_val
                            max_index = keys.index(s2) 

                        print("Observation Value: " + str(observation_val))
                        print("Observation Max: " + str(observe_max))
                        print("SUM " + str(sum))
                    #print("SUM: " + str(sum))
                
                print('MAX INDEX: ' + str(max_index))
                print("--------")
                print("OBSERVE MAX: " + str(observe_max))
                print("--------")
                matrix[keys.index(s)][i] = observe_max
                backtrack_matrix[keys.index(s)][i] = max_index

            #print(i)
       
        debug_matrix = numpy.array(matrix)

   
        print(debug_matrix)
        print(matrix)

        max = -1
        max_state = ""
        values = 0
        print(keys)
        
        max_index = 0
        #Get the max probability and the state
        for i in range(len(matrix)):
            if matrix[i][len(outputs)] > max :
                max = matrix[i][len(outputs)]
                max_state = keys[i]
                max_index = keys.index(max_state)
            values = values + matrix[i][len(outputs)]

            print(matrix[i][len(outputs)])   
            
        
        print('MAXIMUM INDEX: ' + str(max_index))
        print("Length: " + str(len(backtrack_matrix)))
        
        
        
        debug_backtrack_matrix = numpy.array(backtrack_matrix)
        print(debug_backtrack_matrix)

        viterbi_sequence = []
        #append the last state
        viterbi_sequence.append(max_state)

        print(backtrack_matrix[max_index][len(outputs)])
        ## value of index
        back_val = int(backtrack_matrix[max_index][len(outputs)])
        #append the value going back
        viterbi_sequence.append(keys[back_val])
        
        print('--------------------------------')
        for b in reversed(range(len(outputs))) :
            back_val = int(backtrack_matrix[back_val][b]) 
            viterbi_sequence.append(keys[back_val])
        #pop extra values
        viterbi_sequence.pop()
        viterbi_sequence.pop()
        viterbi_sequence.reverse()
        print('--------------------------------')
        print(backtrack_matrix[back_val][len(outputs) - 1])


        print(sequence)
        print("FORWARD RESULT: " + max_state)
        print("Probability: " + str(max / values))


        print(viterbi_sequence)
        return max_state
    ## You do this. Given a sequence with a list of emissions, fill in the most likely
    ## hidden states using the Viterbi algorithm.

if __name__ == "__main__":
    #print(car_infer.query(variables=["Moves"],evidence={"Radio":"turns on", "Starts":"yes"}))
    #if len(sys.argv) < 2:
    #    print("Usage: wordfreq {--load --forward file")
    #    sys.exit(-1)


    parser = argparse.ArgumentParser()


    #The directory that will be walked
    parser.add_argument("domain", help="help the pat")
    parser.add_argument("--forward", help="This will strip a part of the word")
    parser.add_argument("--viterbi", help="This will strip a part of the word")

    parser.add_argument("--generate", help="Number of observations you would like to generate")

    args = parser.parse_args()

    print("ARGUMENTS")
    print("------------")
    print('domain: ' + str(args.domain))
    print('generate: ' + str(args.generate))
    print('forward: ' + str(args.forward))
    print('viterbi: ' + str(args.viterbi))

    print("------------")

    domain = args.domain
    num_sequence = args.generate
    observation = args.forward
    viterbi = args.viterbi

    h = HMM()
    h.load(domain)
    if args.generate is not None:
        h.generate(int(num_sequence))

    if args.forward is not None:
        print('YAYYY')
        with open(observation) as f:
            print("HETAT")
            for lines in f : 
                print("RARSRA" + lines)
                
                words = lines.rstrip('\n').split(" ")
                h.forward(words)

    if args.viterbi is not None:
        print('YAYYY')
        with open(viterbi) as f:
            for lines in f : 
                words = lines.rstrip('\n').split(" ")
                h.viterbi(words)
''' 
    h = HMM()
    h.load('partofspeech')
    print(h.transitions)
    print("------------------------")
    print(h.emissions)
    seq = h.generate(10)
    print(seq)
    h.forward(seq)
'''    


