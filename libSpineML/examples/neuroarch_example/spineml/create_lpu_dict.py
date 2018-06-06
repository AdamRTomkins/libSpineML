"""
A script to extact an LPU-neuron dictionary

"""
from __future__ import division

import csv
import sys

import cStringIO
import numpy as np

import copy


def main(neuron_file):

    print "Processing Files..."
    lpu_dict = process_files(neuron_file)
    
    return lpu_dict

def process_files(neuron_file):
    """ Convert the neuron and synapse files into populations, projections and neurons """
    
    print "1"
    neuron_fieldnames = ['neuron_name', 'innv_neuropil', 'mem_model', 'resting_pot', 'reset_pot', 'threshold_pot', 'rfact_period', 'Cm', 'tm']

    print "2"
    # Process the text files 
    neuron_reader = csv.DictReader(open(neuron_file), fieldnames=neuron_fieldnames,delimiter=' ')
    
    neurons = {}
    populations = {}
    
    print "3"
    for row in neuron_reader:
        lpu = row['innv_neuropil']
        name = row['neuron_name']
        
        if lpu not in populations: 
            populations[lpu] = [name]

        else:    
            populations[lpu].append(name)

        neurons[name] = lpu

    return {"neurons": neurons,"population": populations}
        
if __name__ == "__main__":

    import pickle
    
    lpu_dict = main('../data/flycircuit1.2/CUNeuParsV1-2.txt')
    
    pickle.dump( lpu_dict, open( "lpu_dicts.p", "wb" ) )
    


