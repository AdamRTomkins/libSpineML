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
from libSpineML.smlUtils import  process_connection_json


import csv
import sys

import cStringIO
import graphviz as gv
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

import copy


def main(connection_json,lpu_dict):
    """ Process the parameter files and create a SpineML network """

    neurons, populations, projections = process_connection_json(connections_json,lpu_dict,neuron_params = None) 
    print "Creating SpineML representation..."
    create_spineml_network(neurons, populations,
        projections,output_filename='network.xml',project_name= 'drosophila')
  

if __name__ == "__main__":
    
    
    import pickle
    info_dict = pickle.load(( open( "spineml/lpu_dicts.p", "rb" ) ))
    connections_json = pickle.load(( open( "spineml/example_connections_json.p", "rb" ) ))
    main(connections_json,info_dict)
    #neurons, populations, projections  = process_neuroarch_files('../ffbo_connectivity.csv',info_dict,{'mem_model':'LIF'})
    #neurons, populations, projections  = process_neuroarch_files('vision_connectivity.csv',info_dict,{'mem_model':'LIF'})
    #neurons, populations, projections  = process_neuroarch_files('larval.csv',info_dict,{'mem_model':'LIF'})
        
    #data = {"neurons": neurons,"population": populations, "projections":projections}
    #pickle.dump( data, open( "tmp_data.p", "wb" ) )
    
    #print "Creating SpineML representation..."
    #create_spineml_network(neurons, populations,
    #projections,output_filename='neuroarch_network.xml',project_name= 'neuroarch')
 
    
    #network = create_networkx_graph(populations,projections,prune=0)



