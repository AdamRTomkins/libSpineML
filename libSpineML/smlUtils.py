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
import numpy as numpy

import copy

neuron_fieldnames = ['neuron_name', 'innv_neuropil', 'mem_model', 'resting_pot', 'reset_pot', 'threshold_pot', 'rfact_period', 'Cm', 'tm']

neuron_property_list = ['resting_pot', 'reset_pot', 'threshold_pot', 'rfact_period', 'Cm', 'tm']

default_neuron_models ={}


# LIF models
default_neuron_models['LIF'] = {'resting_pot'   :-60, 
                                'reset_pot'     :-70, 
                                'threshold_pot' :-10, 
                                'rfact_period'  :0, 
                                'Cm'            :10, 
                                'tm'            :10
                               }

default_neuron_models['CurrExp'] = {'tau_syn'   :10}
default_neuron_models['FixedWeight'] = {'w'   :0.5}




# ESN Model Neurons
default_neuron_models['ESNNode'] =  {}
default_neuron_models['ESNInput'] =  {}
default_neuron_models['ESNConnection'] = {}
default_neuron_models['ESNWeight'] = {'w'   :1}

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


    def process_neuroarch_files(connections_json,lpu_dict,neuron_file,neuron_params = None):
        """ Convert the connection_json into populations, projections and neurons 

            neuron_file : A csv of neuron pre and post names, with the synapse count
            lpu_dict : a dictionary of neuron names : LPU

        """
   

        # TODO: Allow interchangavle neuron_params!
        if neuron_params != None:
            neuron_params = {'mem_model':
                                {'name':'LIF', 'filename':'LIF.xml'},
                             'weight_update' : {'name':'FixedWeight', 'filename':'FixedWeight.xml'},
                             'synapse' : {'name':'CurrExp', 'filename':'CurrExp.xml'}
                            }
        else:
            assert 'mem_model' in neuron_params
            assert 'weight_update' in neuron_params
            assert 'synapse' in neuron_params

        neurons = {}
        populations = {}
        projections = {}

        skip = True

        for row in neuron_reader:
            if skip: 
                skip = False
                continue

            pre_name = row['PreSynaptic Neuron']
            post_name = row['PostSynaptic Neuron']
            # Add feature, load neuron details from json
            # In the mean time, 


            try:
                pre_lpu = lpu_dict[pre_name]
            except:
                pre_lpu = pre_name

            try:
                post_lpu = lpu_dict[post_name]

            except:
                post_lpu = post_name

            if pre_name not in neurons.keys():

                if pre_lpu not in populations: 
                    populations[pre_lpu] =  {
                                                'neuron_schema':neuron_params['mem_model'],
                                                'neurons': [pre_name]
                                            }

                else:    
                    populations[pre_lpu]['neurons'].append(pre_name)

                neurons[pre_name] = {}
                neurons[pre_name]['name'] = pre_name
                neurons[pre_name]['pre'] = pre_lpu
                neurons[pre_name]['index']= len(populations[pre_lpu])-1

                # Note: Every neuron type in a population must be the same
                # Todo: break population down into neuron-type based sub populations if required.

            if post_name not in neurons:
                if post_lpu not in populations: 
                    populations[post_lpu] =  {
                                                'neuron_schema':neuron_params['mem_model'],
                                                'neurons': [post_name]
                                            }

                else:    
                    populations[post_lpu]['neurons'].append(post_name)

                neurons[post_name]['name'] = post_name
                neurons[post_name]['index']= len(populations[post_lpu])-1
                neurons[post_name]['data'] = neuron_params['mem_model']

        neuron_reader = csv.DictReader(open(neuron_file), fieldnames=neuroarch_fieldnames,delimiter=',')        

        skip = True

        for row in neuron_reader:
            if skip: 
                skip = False
                continue

            pre_neuron = row['PreSynaptic Neuron']
            post_neuron = row['PostSynaptic Neuron']
            
            # if there is a specific synaose number, use that, if not use the inferred connection
            if row['N'] != 'undefined':
                if row['N']>0:
                    synapse_number = row['N']
            elif row['Inferred'] >0:
                synapse_number = row['Inferred']
            else:
                print "Skipping Row %s" % row
                continue


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


            # ToDo: Add different per connection information based on JSON if it enabled
            synapse_information =  neuron_params['synapse']
            weight_update_infromation = neuron_params['weight_update']



            projections[pre_lpu][post_lpu].append((pre_index,post_index,int(synapse_number),synapse_information,weight_update_information))

    return (neurons, populations, projections)


def create_spineml_network(neurons, populations,   
    projections,output=False,output_filename='model.xml',network_name='model',project_name= 'drosophila',network_components = None):
    """ convert projections and populations into a SpineML network """


    if network_components == None:
        network_components = default_neuron_models.copy()

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

        # Note: Every neuron in a population must be the same. 

        population = net.PopulationType()

        # create a neuron type
        neuron = net.NeuronType()
        #n = neurons.keys()[0] # The model neuron to use as the template
        n = populations[p]['neuron_schema'] # The model neuron to use as the template

        # Build this Neuron Sets Property list
        
        # Currently all fixed value # TODO
        assert n['name'] in default_neuron_models.keys()

        for np in default_neuron_models[n['name']].keys():
            # WIP: specify based on model 
            # Get non-default values
            
            #value = net.FixedValueType(default_neuron_models[neurons[n]['mem_model']][np]) # Currently using a fixed value, should use valuelist
            #value = net.FixedValueType(index=0, value=default_neuron_models[n['name']][np]) # Currently using a fixed value, should use valuelist
            
            prop_list = net.ValueListType()

            # Add a value for every neuron
            for i in numpy.arange(len(populations[p]['neurons'])):
                #value = net.FixedValueType(default_neuron_models[update_name][np]) 
                value = net.ValueType(index=int(i),value=float(default_neuron_models[n['name']][np]))
                prop_list.add_Value(value)

            name = np
            dimension = '?'#Todo Add dimensions to property list 
            neuron_property = net.PropertyType()
            neuron_property.set_name(name)
            neuron_property.set_dimension(dimension)
            neuron_property.set_AbstractValue(prop_list)
            neuron.add_Property(neuron_property)

        neuron.set_name(p)       

        component_file_name = n['filename']

        neuron.set_url(component_file_name)

        output['components'].append(component_file_name)

        neuron.set_size(len(populations[p]['neurons']))


        # Assign to population
        population.set_Neuron(neuron)

        # create a projection        
        if p in projections:
            for cn, destination in enumerate(projections[p]):
                projection = net.ProjectionType(destination)

                
                # Add synapses
                #For every connection, we will create a new synapse
                for index, connection in enumerate(projections[p][destination]):
            
                

                    # read this from projections
                    synapse_details = connection[3]
                    synapse_file_name = synapse_details['filename']
                    synapse_name = synapse_details['name']
                    

                    synapse_properties = []
                    prop_list = net.ValueListType()

                    for np in default_neuron_models[synapse_name].keys():
                        prop_list = net.ValueListType()

                        # Add a value for every neuron
                        for i in numpy.arange(len(populations[p]['neurons'])):
                            #value = net.FixedValueType(default_neuron_models[update_name][np]) 
                            #value = net.ValueType(index=int(i),value=float(default_neuron_models[synapse_name][np]))
                            
                            value = net.ValueType(index=int(i),value=float(default_neuron_models[synapse_name][np]))
                            prop_list.add_Value(value)

                        dimension = '?'#Todo Add dimensions to property list 
                        synapse_property = net.PropertyType()
                        synapse_property.set_name(np)
                        synapse_property.set_dimension(dimension)
                        synapse_property.set_AbstractValue(prop_list)
                        synapse_properties.append(synapse_property)

                    # Create a PostSynapse
                    postSynapse = net.PostSynapseType(
                        name=synapse_name, 
                        url = synapse_file_name,
                        Property=synapse_properties,
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
                    
                    #weightValue = net.ValueType(index=int(index),value=float(connection[2]))
                    
                   

                    # read this from projections
                    update_details = connection[4]
                    
                    update_file_name = update_details['filename']
                    update_name = update_details['name']

                    # Create a Weight Update               
                    update_properties = []
                    for np in default_neuron_models[update_name].keys():

                        prop_list = net.ValueListType()
                        #value = net.FixedValueType(default_neuron_models[update_name][np])

                        if np in update_details['override'].keys():
                            value = net.ValueType(index=int(index),value=float(update_details['override'][np]))                                
                        else:
                            value = net.ValueType(index=int(index),value=float(default_neuron_models[update_name][np]))
                        prop_list.add_Value(value)
 
                        dimension = '?'#Todo Add dimensions to property list 
                        update_property = net.PropertyType()
                        update_property.set_name(np)
                        update_property.set_dimension(dimension)
                        #update_property.set_AbstractValue(value)
                        update_property.set_AbstractValue(prop_list)
                        update_properties.append(update_property)
    
 
                    weightUpdate = net.WeightUpdateType(
                        name='"%s_to_%s_Synapse_%s_weight_update' % (p,destination,cn),
                        url=update_file_name,
                        #Property=update_properties,
                        # WIP store somewhere!
                        input_src_port=None,
                        input_dst_port=None,
                        feedback_src_port=None,
                        feedback_dst_port=None
                    )

                   
                    
                    ##
                    weightUpdate.set_Property(update_properties)

                    output['components'].append(update_file_name)
                    
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
        network.name = network_name

    # Write out network to xml
    io = cStringIO.StringIO()
    network.export(io,0)
    network_xml = io.getvalue()

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
        network_xml = network_xml.replace(k,subs[k])
    if output:
        with open(output_filename, 'w') as f:
            f.write(network_xml)

    # Create Output SpineML JSON reprentation
    output['network']['name'] = network_name
    output['network']['filename'] = output_filename

    output['network']['xml'] = network_xml
    output['network']['component'] = network

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

# WIP: Update to process connection list
def process_connection_json(connections_json,lpu_dict,neuron_params = None):
    """ Convert the connection_json into populations, projections and neurons 
    """

    if neuron_params == None:
        neuron_params = {'mem_model':
                            {'name':'LIF', 'filename':'LIF.xml'},
                         'weight_update' :
                            {'name':'FixedWeight', 'filename':'FixedWeight.xml','override':{}},
                         'synapse' :
                            {'name':'CurrExp', 'filename':'CurrExp.xml'},
                         'input_model':
                            {'name':'ESNInput', 'filename':'ESNInput.xml'}, # Add a new neuron class for inputs populations to allow for easy ESNs
                        }
    else:
        assert 'mem_model' in neuron_params
        assert 'weight_update' in neuron_params
        assert 'synapse' in neuron_params

    neuroarch_dict = {}

    neurons = {}
    populations = {}
    projections = {}

    skip = True

    if 'success' in connections_json: connections_json = connections_json['success']
    
    for nid in connections_json['nodes'].keys():

        neuron = connections_json['nodes'][nid]

        try:
            name = neuron['uname']
        except:
            name = neuron['name']


        # Allow Input Populations 
        if connections_json['nodes'][nid]['class'] == u'Input':
            print " Adding Input Node: %s  " % name
            lpu = name
            lpu_dict[name] = lpu    
        else:
            try:
                lpu = lpu_dict[name]
            except:
                # If the neuron is not in the LPU dict,
                lpu = 'unknown-visual'
                lpu_dict[name] = lpu

        neuroarch_dict[nid] = name

        if name not in neurons.keys():

            if lpu not in populations:
                 # TODO: Automatic LPU splitting for different models

                 if not connections_json['nodes'][nid]['class'] == u'Input':
                
                    populations[lpu] =  {
                            'neuron_schema':neuron_params['mem_model'],
                            'neurons': [name]
                        }
                 else:
            
                    # ESN input population
                    populations[lpu] =  {
                            'neuron_schema':neuron_params['input_model'],
                            'neurons': [name]
                        }
                    

            else:    
                populations[lpu]['neurons'].append(name)

            neurons[name] = neuron_params.copy()
            neurons[name]['name'] = name
            neurons[name]['pre'] = lpu
            neurons[name]['index']= len(populations[lpu]['neurons'])-1

    for pre_id in connections_json['edges'].keys():

        #pre_neuron = neuroarch_dict[pre_id]
        pre_neuron = neuroarch_dict[pre_id]

        for post_id in connections_json['edges'][pre_id].keys():

            #post_neuron = neuroarch_dict[post_id]
            post_neuron = post_id

            try:
                synapse_number = connections_json['edges'][pre_id][post_id]['synapses']; # WIP extract synapses
            except:
                print "Synapse Error"
                assert False

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

    
            synapse_information = copy.deepcopy(neuron_params['synapse'])
            
            # allow the number of synapses to act as a override to weight if required.           
            weight_update_information = copy.deepcopy(neuron_params['weight_update'])
            weight_update_information['override']['w'] = synapse_number

            projections[pre_lpu][post_lpu].append((pre_index,post_index,int(synapse_number),synapse_information, weight_update_information))

            
    return (neurons, populations, projections)


def extract_adjacency_matrix(populations,projections, weight_parameter=None):
    """ given a popuation list, extract an adjacency matrix """
    
    # Calculate the size of the adjacency matrix
    N = sum([len(populations[p]['neurons']) for p in populations.keys()])
    
    index = 0
    neuron_index = {}
    for p in populations:
        for n in populations[p]['neurons']:
            neuron_index[(p,n)] = index
            index += 1
    
    adjacency_matrix = numpy.zeros((N,N)) 
    
    # populate adjacy matrix based on override value
    for pre in projections:
        for post in projections[pre]:
            for con in projections[pre][post]:
                pre_name = populations[pre]['neurons'][con[0]]
                post_name = populations[post]['neurons'][con[1]]

                pre_index = neuron_index[(pre,pre_name)] 
                post_index = neuron_index[(post,post_name)] 

                weight = 1
                if weight_parameter != None:
                    assert weight_parameter in con[4]['override']
                    weight = con[4]['override'][weight_parameter]


                adjacency_matrix[pre_index,post_index] = weight
    
    return adjacency_matrix, neuron_index

def inject_adjacency_matrix(populations,projections, adjacency_matrix, neuron_index, weight_parameter='w'):
    """given an adjacency matrix and its index, inject the weights into the projections, doesn't create or distroy connections"""
    
    # assert that all the index is in the original populations
    for (population,name) in neuron_index.keys():
        assert name in populations[population]['neurons']

    # loop through the index, extract weight and inject it into the projections
    for pre in projections:
        for post in projections[pre]:
            for con in projections[pre][post]:
                pre_name = populations[pre]['neurons'][con[0]]
                post_name = populations[post]['neurons'][con[1]]

                pre_index = neuron_index[(pre,pre_name)] 
                post_index = neuron_index[(post,post_name)] 

                weight = con[4]['override'][weight_parameter] = adjacency_matrix[pre_index,post_index]
            
            
    return populations,projections

def set_esn_weights(populations,projections, weight_parameter='w',spectral_radius=1.0):
    print "WARNING: This resets all connection weights, including input weights"

    adjacency_matrix, neuron_index = extract_adjacency_matrix(populations,projections)  
    rand_matrix = adjacency_matrix* (2*numpy.random.rand(adjacency_matrix.shape[0],adjacency_matrix.shape[1])-1)
    
    # compute the spectral radius of these weights:
    radius = numpy.max(numpy.abs(numpy.linalg.eigvals(rand_matrix)))

    # rescale them to reach the requested spectral radius:
    rand_matrix = rand_matrix * (spectral_radius / radius)

    populations_rand,projections_rand = inject_adjacency_matrix( populations,projections, rand_matrix, neuron_index, weight_parameter) 

    return populations_rand, projections_rand, rand_matrix

