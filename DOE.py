'''
This script generates a DOE table for run in avl
--------------------------
Requires pyDOE installation before run (pip install --upgrade pyDOE)

    ## Bill Quick note ##
    Not sure if it's the version I am using, but when installed pyDOE, it was giving datatype error
    Change line 78 of doe_factorial.py script that is written for pyDOE to the following:
        rng = lvl*int(range_repeat)
    #####################

DOE options in pyDOE package:
General full factorial(fullfact)
2-Level full-factorial(ff2n)
2-Level Fractional factorial(pbdesign)

Box-Behnken(bbdesign)
Central-Composite(ccdesign)

Latin-Hypercube(lhs)
-------------------------------
When adding inputs, make sure to update __init__ and populate_array
'''

from pyDOE import *
import numpy as np

class DOE:
    def __init__(self,vel,mach):
        # list inputs
        self.velocity = vel
        self.mach = mach
        # self.test = test

        self.factors = len(locals())-1

        self.vel_vector = self.inputs(vel)
        self.mach_vector = self.inputs(mach)
        # self.test_vector = self.inputs(test)

        self.array_levels = [vel[2],mach[2]]  #,test[2]]

    # This method finds the values of the inputs in the specified levels in the input
    def populate_array(self,array):
        if self.factors != array.shape[1]:
            raise ValueError('Number of columns in full factorial array does not match number of factors')

    # If adding more factors, must change this part
        vel_out = []; mach_out = [];   #test_out =[]
        for i in range(self.factors):
            for j in range(array.shape[0]):
                if i == 0:
                    vel_out.append(self.vel_vector[int(array[j,i])])
                if i == 1:
                    mach_out.append(self.mach_vector[int(array[j,i])])
                # if i == 1:
                #     test_out.append(self.test_vector[int(array[j,i])])

        return vel_out, mach_out    #, test_out

    # This method finds the full factorial array from the levels specified in each input
    def full_factorial(self):
        full_factorial_array = fullfact(self.array_levels)
        return full_factorial_array

    # This method creates a vector of inputs with defined levels
    def inputs(self,input):
        vector = np.linspace(input[0],input[1],input[2])
        return vector





if __name__ == '__main__':
    # Each input should be input = [Low, High, Level]
    vel = [5,15,2]
    mach = [0.2,0.4,2]

    # Define the class with inputs
    run_DOE = DOE(vel,mach)

    # DOE options defined here
    array = run_DOE.full_factorial()



    vel_vector, mach_vector = run_DOE.populate_array(array)
    print(vel_vector,mach_vector)



