"""
A script to convert the drosophila connectome into SpineML 

This build upon the pure data to add in the required infered network components:

# Install libSpineML from source
# https://github.com/AdamRTomkins/libSpineML

"""
from __future__ import division

from libSpineML import smlExperiment as exp
from libSpineML import smlNetwork as net
from libSpineML import smlComponent as com
from libSpineML.smlUtils import  create_spineml_network


import csv
import sys

import cStringIO
import graphviz as gv
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

import copy

neuron_fieldnames = ['neuron_name', 'innv_neuropil', 'mem_model', 'resting_pot', 'reset_pot', 'threshold_pot', 'rfact_period', 'Cm', 'tm']

neuron_property_list = ['resting_pot', 'reset_pot', 'threshold_pot', 'rfact_period', 'Cm', 'tm']

default_neuron_models ={}

default_neuron_models['LIF'] = {'resting_pot'   :-60, 
                                'reset_pot'     :-70, 
                                'threshold_pot' :-10, 
                                'rfact_period'  :0, 
                                'Cm'            :10, 
                                'tm'            :10
                               }

synapse_fieldnames = ['pre-neuron', 'post-neuron', 'neuropil', 'weight', 'type', 'reversal_pot', 'txt', 'tst', 'pv', 'tD', 'tF', 'tLP', 'PosISI', 'NegISI']


def main(neuron_file,synapse_file):
    """ Process the parameter files and create a SpineML network """

    print "Processing Files..."
    neurons, populations, projections  = process_files(neuron_file,synapse_file)

    print "Creating SpineML representation..."
    create_spineml_network(neurons, populations,
        projections,output_filename='network.xml',project_name= 'drosophila')
  
    print "Creating Graph Visualisation..."
    create_graphviz_graph(populations,projections)

    
def process_neuroarch_files(neuron_file, info_dict, neuron_params):
    """ Convert the neuroarch files into populations, projections and neurons 
    
        neuron_file : A csv of neuron pre and post names, with the synapse count
        lpu_dict : a dictionary of neuron names : LPU
        
    """

    # Process the text files 
    neuroarch_fieldnames = ['PreSynaptic Neuron', 'PostSynaptic Neuron', 'N', 'Inferred']

    neuron_reader = csv.DictReader(open(neuron_file), fieldnames=neuroarch_fieldnames,delimiter=',')

    
    
    lpu_dict = info_dict['neurons']
    
    neurons = {}
    populations = {}
    projections = {}

    skip = True
    ns = set()
    
    for row in neuron_reader:
        if skip: 
            skip = False
            continue
            
        pre_name = row['PreSynaptic Neuron']
        post_name = row['PostSynaptic Neuron']
        
        ns.add(pre_name)
        ns.add(post_name)
        
        try:
            pre_lpu = lpu_dict[pre_name]
        except:
            pre_lpu = pre_name
        
        
        try:
            post_lpu = lpu_dict[post_name]

        except:
            post_lpu = post_name
        
        
        
        
        # NEURONS IS WRONG
        #assert False
        if pre_name not in neurons.keys():
           
            if pre_lpu not in populations: 
                populations[pre_lpu] = [pre_name]

            else:    
                populations[pre_lpu].append(pre_name)

            neurons[pre_name] = neuron_params.copy()
            neurons[pre_name]['name'] = pre_name
            neurons[pre_name]['pre'] = pre_lpu
            neurons[pre_name]['index']= len(populations[pre_lpu])-1
            
                
      
        if post_name not in neurons:
           
            if post_lpu not in populations: 
                populations[post_lpu] = [post_name]

            else:    
                populations[post_lpu].append(post_name)

            neurons[post_name] = neuron_params.copy()
            neurons[post_name]['name'] = post_name
            neurons[post_name]['index']= len(populations[post_lpu])-1
            
            print 'POST: %s <%s> %s'  %(post_name, post_lpu, neurons[post_name]['index'])
       
    print ns
    print  len(list(ns))

    neuron_reader = csv.DictReader(open(neuron_file), fieldnames=neuroarch_fieldnames,delimiter=',')        

    skip = True
    
    for row in neuron_reader:
        if skip: 
            skip = False
            continue

        pre_neuron = row['PreSynaptic Neuron']
        post_neuron = row['PostSynaptic Neuron']
        synapse_number = row['N']
        
        # get the LPU of the pre neuron
        try:
            assert 'lpus' in lpu_data
            pre_lpu = lpu_dict[pre_neuron]
        except:
            pre_lpu = pre_neuron

        
        
        # get the LPU index of the pre neuron
        pre_index = neurons[pre_neuron]['index']
        
        # get the LPU of the post neuron
        try:
            post_lpu = lpu_dict[post_neuron]
        except:
            post_lpu = post_neuron

        # get the LPU index of the post neuron
        post_index = neurons[post_neuron]['index']

        
        
        if pre_lpu not in projections: 
            projections[pre_lpu] = {}

        if post_lpu not in projections[pre_lpu]: 
            projections[pre_lpu][post_lpu] = []

        projections[pre_lpu][post_lpu].append((pre_index,post_index,int(synapse_number)))
        
    return (neurons, populations, projections)


if __name__ == "__main__":
    #main('../data/flycircuit1.2/CUNeuParsV1-2.txt','../data/flycircuit1.2/CUSynParsV1-2.txt')
    #neurons, populations, projections  = process_files('../data/flycircuit1.2/CUNeuParsV1-2.txt','../data/flycircuit1.2/CUSynParsV1-2.txt')
    
    
    import pickle
    info_dict = pickle.load(( open( "lpu_dicts.p", "rb" ) ))
    
    #neurons, populations, projections  = process_neuroarch_files('../ffbo_connectivity.csv',info_dict,{'mem_model':'LIF'})
    neurons, populations, projections  = process_neuroarch_files('vision_connectivity.csv',info_dict,{'mem_model':'LIF'})
    #neurons, populations, projections  = process_neuroarch_files('larval.csv',info_dict,{'mem_model':'LIF'})
        
    data = {"neurons": neurons,"population": populations, "projections":projections}
    pickle.dump( data, open( "tmp_data.p", "wb" ) )
    
    print "Creating SpineML representation..."
    create_spineml_network(neurons, populations,
        projections,output_filename='neuroarch_network.xml',project_name= 'neuroarch')
 
    
    #network = create_networkx_graph(populations,projections,prune=0)



