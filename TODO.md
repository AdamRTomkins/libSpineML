# To Do File

## Spine Creator Integration

1. Create a bash script to allow spine creator to use this library

script recieves the experiment number
so should this library recusivly add the experiment, then the population file, then all component files.
or maybe the bundle should reflect a more direct experiment structure.

or the script could add everything in the directory? but only that one experiment?

translator adds things recursivly, so should libspineml

Project:
	Experiment 
		

add_project 

or, the script calls nk module with experiment name and dir
	nk script adds the experiment, network, then components into libspineml


## Neurokernel Module

Callable from the command line as:
>>> SpineML2Neurokernel experiment dir

Process
	Create a smlBundle
	Load The Experiment into the bundle
	Process the Experiment
		Add the network file
		Process the Network file
			Build the Network graph
			Add Each Component File
			Process Each Component
				Build the SpineMLComponents
	Load the Manager Class
	Run the Experiment
	Return the generated files


