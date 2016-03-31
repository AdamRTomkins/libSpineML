#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""SpineML Bundle Module
This modual will form a convience class to bundle together related SpineML
objects into a single standard object which can be easily passed between 
programs. The bundle will be able to interact with premade spineML objects
through the other support classes, or parse directly from XML
"""
## Add each component
## export all
## export each


import network    as spineML_Network      # SpineML layers
import experiment as spineML_Experiment
import component  as spineML_Component

class Bundle(object):
    """First line of a docstring is short and next to the quotes.
    Class and exception names are CapWords.
    Closing quotes are on their own line
    """

    experiments = []
    networks    = []
    components  = []

    def __init__(self, experiments=None, networks=None, components=None):
        if type(experiments) is not type(None):
            if type(experiments) is spineML_Experiment.SpineMLType:
                self.experiments.append(experiment)
            elif type(experiments) is list:
                for e in experiments:
                    if type(e) is spineML_Experiment.SpineMLType:
                        raise TypeError('Invalid Experiment Input: %s' % str(type(e)))
                    else:
                        self.experiments.append(e)
            else:
                raise TypeError('Invalid Experiment Input: %s' % str(type(experiments)))
        

        if type(networks) is not type(None):
            if type(networks) is spineML_Network.SpineMLType:
                self.networks.append(networks)
            elif type(networks) is list:
                for n in networks:
                    if type(n) is spineML_Network.network.SpineMLType:
                        raise TypeError('Invalid Network Input: %s' % str(type(n)))
                    else:
                        self.networks.append(n)
            else:
                raise TypeError('Invalid Network Input: %s' % str(type(networks)))

        if type(components) is not type(None):
            if type(components) is spineML_Component.SpineMLType:
                self.components.append(components)
            elif type(components) is list:
                for c in components:
                    if type(c) is spineML_Component.SpineMLType:
                        raise TypeError('Invalid Component Input: %s' % str(type(c)))
                    else:
                        self.components.append(c)
            else:
                raise TypeError('Invalid Component Input: %s' % str(type(components)))


    def add_experiment(self, experiment):
        """Add a SpineML Experiment of  ExperimentType type to the bundle
        """
        if type(experiment) is spineML_Experiment.SpineMLType:
            self.experiments.append(experiment)
        elif type(experiment) is str:  
            self.experiments.append(spineML_Experiment.parse(experiment))
        else:
            raise TypeError('Invalid Experiment Input: %s' % str(type(experiment)))
    

    def add_network(self, network):
        """Add a SpineML Network of  NetworkType type to the bundle
        """
        if type(network) is spineML_Network.SpineMLType:
            self.networks.append(network)
        elif type(network) is str:  
            self.networks.append(SpineML_Network.parse(network))
        else:
            raise TypeError('Invalid Network Input %s' % str(type(network)))


    def add_component(self, component):
        """Add a SpineML Component of ComponentType type to the bundle
        """
        if type(component) is spineML_Component.SpineMLType:
            self.components.append(component)
        elif type(component) is str:
            self.components.append(SpineML_Component.parse(component)) 
        else:
            raise TypeError('Invalid Component Input %s' % str(type(component)))



