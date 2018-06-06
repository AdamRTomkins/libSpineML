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

default_neuron_models['ESN'] = {}


def process_files(neuron_file,synapse_file):
    """ Convert the neuron and synapse files into populations, projections and neurons """

    # Process the text files 
    neuron_reader = csv.DictReader(open(neuron_file), fieldnames=neuron_fieldnames,delimiter=' ')
    synapse_reader = csv.DictReader(open(synapse_file), fieldnames=synapse_fieldnames,delimiter=' ')

    neurons = {}
    populations = {}
    projections = {}

    for row in neuron_reader:
        lpu = row['innv_neuropil']
        name = row['neuron_name']
        
        if lpu not in populations: 
            populations[lpu] = [name]

        else:    
            populations[lpu].append(name)

        neurons[name] = row
        neurons[name]['index']= len(populations[lpu])-1


    for row in synapse_reader:
        pre_neuron = row['pre-neuron']
        post_neuron = row['post-neuron']
        
        # get the LPU of the pre neuron
        pre_lpu = neurons[pre_neuron]['innv_neuropil']
        # get the LPU index of the pre neuron
        pre_index = neurons[pre_neuron]['index']
        # get the LPU of the post neuron
        post_lpu = neurons[post_neuron]['innv_neuropil']
        # get the LPU index of the post neuron
        post_index = neurons[post_neuron]['index']

        if pre_lpu not in projections: 
            projections[pre_lpu] = {}

        if post_lpu not in projections[pre_lpu]: 
            projections[pre_lpu][post_lpu] = []

        projections[pre_lpu][post_lpu].append((pre_index,post_index))
        
    return (neurons, populations, projections)



def create_spineml_network(neurons, populations,   
    projections,output=False,output_filename='model.xml',project_name= 'drosophila'):
    """ convert projections and populations into a SpineML network """

    output = {
        'network' : {
                     'name':None,
                     'xml' : None
                    },
        'components' : []
    }

    # create the network SpineML type
    network = net.SpineMLType()

    # for each population, create a Population type 
    for p in populations:
        population = net.PopulationType()

        # create a neuron type
        neuron = net.NeuronType()
        n = neurons.keys()[0] # The model neuron to use as the template

        # Build this Neuron Sets Property list
        # Currently all fixed value # TODO
        for np in default_neuron_models['LIF'].keys():
            # WIP: specify based on model 
            # Get non-default values
            
            value = net.FixedValueType(default_neuron_models[neurons[n]['mem_model']][np]) # Currently using a fixed value, should use valuelist
            
            name = np
            dimension = '?'#Todo Add dimensions to property list 
            neuron_property = net.PropertyType()
            neuron_property.set_name(name)
            neuron_property.set_dimension(dimension)
            neuron_property.set_AbstractValue(value)
            neuron.add_Property(neuron_property)
        neuron.set_name(p)       

        component_file_name = neurons[n]['mem_model']+'.xml' 
        neuron.set_url(component_file_name)

        output['components'].append(component_file_name)

        neuron.set_size(len(populations[p])) 

        # Assign to population
        population.set_Neuron(neuron)

        # create a projection        
        if p in projections:
            for cn, destination in enumerate(projections[p]):
                projection = net.ProjectionType(destination)

                # Add synapses
                #For every connection, we will create a new synapse
                for index, connection in enumerate(projections[p][destination]):
            
                    synapse_file_name = 'CurrExp.xml'
                    # Create a PostSynapse
                    postSynapse = net.PostSynapseType(
                        name='CurrExp', 
                        url = synapse_file_name,
                        Property=
                            [
                                net.PropertyType(name='tau_syn', AbstractValue=net.FixedValueType(value=10))
                            ], 
                        input_src_port=None, 
                        input_dst_port=None, 
                        output_src_port=None, 
                        output_dst_port=None
                    )
                    
                    output['components'].append(synapse_file_name)

                    ## Create Connectivity
                    connection_list = net.ConnectionListType()

                

                    connection_type = net.ConnectionType(connection[0],connection[1],0) # zero delay
                    connection_list.add_Connection(connection_type)     
                    
                    weightValue = net.ValueType(index=int(index),value=float(connection[2]))
               
                    update_file_name = 'FixedWeight.xml' 
                    # Create a PostSynapse
         
                    weightUpdate = net.WeightUpdateType(
                        name='"%s to %s Synapse %s weight_update' % (p,destination,cn),
                        url=update_file_name,
                        input_src_port="spike",
                        input_dst_port="spike",
                        feedback_src_port=None,
                        feedback_dst_port=None
                    )
        
                    output['components'].append(update_file_name)
                    
                        
                    prop = net.PropertyType(name='w',dimension="?")
                    prop.set_AbstractValue(weightValue)

                    io = cStringIO.StringIO()
                    prop.export(io,0)
                    st = io.getvalue()

                    weightUpdate.set_Property([prop])

                    io = cStringIO.StringIO()
                    weightUpdate.export(io,0)
                    st = io.getvalue()

                    # Create Synapse
                    synapse = net.SynapseType(
                        AbstractConnection=connection_list,
                        WeightUpdate=weightUpdate,
                        PostSynapse=postSynapse
                    )


                    projection.add_Synapse(synapse)


                population.add_Projection(projection)
        # add population to the network
        network.add_Population(population)      
                
    # Write out network to xml
    io = cStringIO.StringIO()
    network.export(io,0)
    network = io.getvalue()

    # Cleanup Replace Abstract objects with non_abstract
    subs = {
        "AbstractConnection":"ConnectionList",
        "AbstractValue":"FixedValue",
        "Population":"LL:Population",
        "Neuron":"LL:Neuron",
        "Projection":"LL:Projection",
        "<Synapse>":"<LL:Synapse>",             # REQURED DUE TO PostSynapse Overlap
        "</Synapse>":"</LL:Synapse>",
        "<PostSynapse":"<LL:PostSynapse",             # REQURED DUE TO PostSynapse Overlap
        "</PostSynapse>":"</LL:PostSynapse>",
    
        "ConnectionList": "LL:ConnectionList",

        "WeightUpdate":"LL:WeightUpdate",
        '<SpineMLType>':
        '<LL:SpineML xsi:schemaLocation="http://www.shef.ac.uk/SpineMLLowLevelNetworkLayer SpineMLLowLevelNetworkLayer.xsd http://www.shef.ac.uk/SpineMLNetworkLayer SpineMLNetworkLayer.xsd" name="%s">' % project_name,
        '</SpineMLType>':'</LL:SpineML>'
    }

    for k in subs:
        network = network.replace(k,subs[k])
    if output:
        with open(output_filename, 'w') as f:
            f.write(network)

    # Create Output SpineML JSON reprentation
    output['network']['name'] = 'model.xml'
    output['network']['xml'] = network

    # WIP: Add each component xml too
    components = set(output['components'])
    output['components'] = list(components)

    return output

def create_graphviz_graph(populations,projections):
    """ convert the projections matrix to a svg graph """

    g1 = gv.Digraph(format='svg')
    for lpu in populations.keys():
        if lpu.lower() == lpu:
            g1.node(lpu)

    for pre in projections.keys():
        if pre.lower() == pre:
            for post in projections[pre]:
                if post.lower() == post:
                    if len(projections[pre][post]) > 100:         
                        g1.edge(pre, post,weight = str(len(projections[pre][post])))


    filename = g1.render(filename='left_hemisphere')

def create_networkx_graph(populations,projections,prune=10):
    """ convert the projections matrix to a svg graph """

    network = nx.Graph()
    lpus = populations.keys()
    for lpu in lpus:
        network.add_node(lpu)

    for pre in projections.keys():
        for post in projections[pre]:
            if len(projections[pre][post]) > prune:         
                network.add_edge(pre, post, weight=1.0/len(projections[pre][post]))

    return network


