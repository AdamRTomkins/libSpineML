"""
A script to convert the drosophila connectome into SpineML 

This build upon the pure data to add in the required infered network components:
  Fixed Weight Update
  Add Synapse

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

    net_dict = {}
    
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
            net_dict[pre_name] = pre_lpu
        except:
            pre_lpu = pre_name
        
        
        try:
            post_lpu = lpu_dict[post_name]
            net_dict[post_name] = post_lpu
        except:
            post_lpu = post_name
        
        import pickle
        pickle.dump( net_dict, open( "teddy_network_dictionary.p", "wb" ) )
        
        
        
        # NEURONS IS WRONG
        #assert False
        if pre_name not in neurons.keys():
           
            if pre_lpu not in populations: 
                populations[pre_lpu] = [pre_name]

            else:    
                populations[pre_lpu].append(pre_name)

            neurons[pre_name] = neuron_params.copy()
            neurons[pre_name]['name'] = "naff_" +pre_name
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
2
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
    projections,output_filename='model.xml',project_name= 'drosophila'):
    """ convert projections and populations into a SpineML network """

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
            
            #value = net.FixedValueType(neurons[n][np]) # Currently using a fixed value, should use valuelist
            value = net.FixedValueType(default_neuron_models['LIF'][np]) # Currently using a fixed value, should use valuelist
            
            name = np
            dimension = '?'#Todo Add dimensions to property list 
            neuron_property = net.PropertyType()
            neuron_property.set_name(name)
            neuron_property.set_dimension(dimension)
            neuron_property.set_AbstractValue(value)
            neuron.add_Property(neuron_property)
        neuron.set_name(p)        
        neuron.set_url(neurons[n]['mem_model']+'.xml')
        neuron.set_size(len(populations[p])) 

        # Assign to population
        population.set_Neuron(neuron)

        # create a projection        
        if p in projections:
            for cn, destination in enumerate(projections[p]):
                projection = net.ProjectionType(destination)

                # Add synapses
                #For every connection, we will create a new synapse

                # Create a PostSynapse
                postSynapse = net.PostSynapseType(
                    name='CurrExp', 
                    url='CurrExp.xml', 
                    Property=
                        [
                            net.PropertyType(name='tau_syn', AbstractValue=net.FixedValueType(value=10))
                        ], 
                    input_src_port=None, 
                    input_dst_port=None, 
                    output_src_port=None, 
                    output_dst_port=None
                )

                ## Create Connectivity
                connection_list = net.ConnectionListType()
                weight_list = net.ValueListType()
                
                for index, connection in enumerate(projections[p][destination]):

                    connection_type = net.ConnectionType(connection[0],connection[1],0) # zero delay
                    connection_list.add_Connection(connection_type)     
                    
                    weight_list.add_Value(net.ValueType(index=int(index),value=float(connection[2])))
                    
                    io = cStringIO.StringIO()
                    weight_list.export(io,0)
                    st = io.getvalue()
                    print st

                
                # WIP: Add update value to be seet to a list based on the number of synapses
                # Create a weightUpdate 
                """
                <LL:WeightUpdate name="MED to DMP Synapse 0 weight_update" url="FixedWeight.xml" input_src_port="spike" input_dst_port="spike">
                    <Property name="w" dimension="?">
                        <ValueList>
                            <Value index="0" value="0"/>
                            <Value index="1" value="1"/>
                            <Value index="999" value="0"/>
                            <Value index="0" value="999"/>
                        </ValueList>
                    </Property>
                </LL:WeightUpdate>
                """
                weightUpdate = net.WeightUpdateType(
                    name='"%s to %s Synapse %s weight_update' % (p,destination,cn),
                    url='FixedWeight.xml', 
                    #Property=[net.PropertyType(name='w', AbstractValue=net.FixedValueType(value=1))],
                    #Property=[],
                    input_src_port="spike",
                    input_dst_port="spike",
                    feedback_src_port=None,
                    feedback_dst_port=None
                )
                                
                prop = net.PropertyType(name='w',dimension="?")
                prop.set_AbstractValue(weight_list)
                
                io = cStringIO.StringIO()
                prop.export(io,0)
                st = io.getvalue()
                print st                
                
                weightUpdate.set_Property([prop])
            
                io = cStringIO.StringIO()
                weightUpdate.export(io,0)
                st = io.getvalue()
                print st

                    
                # Create Synapse
                synapse = net.SynapseType(
                    AbstractConnection=connection_list,
                    WeightUpdate=weightUpdate,
                    PostSynapse=postSynapse
                )


                projection.add_Synapse(synapse)


                population.add_Projection(projection)

           
            #network.add_Population(population)
        else:
              print "Population %s has no projections" % p
        # add population to the network
        network.add_Population(population)      
                
    # Write out network to xml
    io = cStringIO.StringIO()
    network.export(io,0)
    io = io.getvalue()

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
        io = io.replace(k,subs[k])

    with open(output_filename, 'w') as f:
        f.write(io)

    print io
    return io

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
    print filename

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

    """
    nx.draw_circular(network)
    plt.savefig("graph.png")
    plt.show()
    """
    return network


if __name__ == "__main__":
    #main('../data/flycircuit1.2/CUNeuParsV1-2.txt','../data/flycircuit1.2/CUSynParsV1-2.txt')
    #neurons, populations, projections  = process_files('../data/flycircuit1.2/CUNeuParsV1-2.txt','../data/flycircuit1.2/CUSynParsV1-2.txt')
    
    
    import pickle
    info_dict = pickle.load(( open( "lpu_dicts.p", "rb" ) ))
    
    neurons, populations, projections  = process_neuroarch_files('../ffbo_connectivity.csv',info_dict,{'mem_model':'LIF'})
    #neurons, populations, projections  = process_neuroarch_files('larval.csv',info_dict,{'mem_model':'LIF'})
        
    data = {"neurons": neurons,"population": populations, "projections":projections}
    pickle.dump( data, open( "tmp_data.p", "wb" ) )
    
    print "Creating SpineML representation..."
    create_spineml_network(neurons, populations,
        projections,output_filename='neuroarch_network.xml',project_name= 'neuroarch')
 
    
    #network = create_networkx_graph(populations,projections,prune=0)



