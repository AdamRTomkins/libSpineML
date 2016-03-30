# libSpineML

## Synopsis

This project provides python bindings for the SpineML schema, which can be found [here](http://bimpa.group.shef.ac.uk/SpineML/index.php)

## Code Example

### SpineML Parsing


Parsing an existing SpineML specification is easy to accumplish, by providing the path to the schema-specific XML file.

<code>
import experiment as exp
import network as net
import component as com

c = com.parse('Examples/LeakyIAF.xml')
n = net.parse('Examples/model.xml')
e = exp.parse('Examples/experiment0.xml')
</code>

This will populate the variables with the relavant objects. 

### Create a Specification

First, to create a component:

<code>
# Create a new neuron body
c = com.ComponentClassType('ComName','neuronbody')
# Add neuron parameters
c.add_Parameter(com.ParameterType('C','nS'))
c.add_Parameter(com.ParameterType('C','nS'))
c.add_Parameter(com.ParameterType('Vt','mV'))
c.add_Parameter(com.ParameterType('Er','mV'))
c.add_Parameter(com.ParameterType('Vr','mV'))
c.add_Parameter(com.ParameterType('R','MOhm'))
</code>

The majority of a component is defined within a dynamics tag, so first we will build up a dynamic object and assign it to our object using c.set_Dynamics()

A dynamics regime takes:
    initial regime
    regime
    StateVariables
    Alias?

Primerily we will set up a new regime using
<code>reg = com.RegimeType(name='integrating',...</code>

Which will require a new Time Derivitive
<code>
td = com.TimeDerivativeType('V', '((I_Syn) / C) + (Vr - V) / (R*C)')
</code>

And an On Condition:
    which in turn requires
        State Assignments
        Triggers
        Events

<code>
sa = com.StateAssignmentType('V','Vr')
tr = com.TriggerType('V > Vt')
eo = com.EventOutType('spike')
# Create the On Condition
con = com.OnConditionType('integrating',sa,eo,None,tr)
</code>

With these we can create a regime:

<code>reg = com.RegimeType('integrating',td,con)</code>

and feed this into the dynamics:
<code>dyn = com.DynamicsType('integrating',reg)</code>

Here we have to specify the 
    state variables
<code>
dyn.add_StateVariable(com.StateVariableType('V','mV'))
</code>

and finally we can set these dynamics to the component
<code>c.set_Dynamics(dyn)</code>

and finally add any ports:
<code>
c.add_Port(com.EventSendPortType('spike'))
c.add_Port(com.AnalogReducePortType('I_syn','+','mA'))
</code>


## Motivation

libSpineML will create a programatic way to build up declaritive SpineML models, with the aim of enabling easy model sharing across the computational neuroscience spectrum. This project will be closely integrated with the SpineML and SpineCreator projects to enable easy model translation from high level graphical tools such as SpineCreator, into python-based simulators such as Neurokernel.

## Installation

In Progress

## API Reference

Depending on the size of the project, if it is small and simple enough the reference docs can be added to the README. For medium size to larger projects it is important to at least provide a link to where the API reference docs live.

## Tests

In Progress

## Contributors

Adam Tomkins

## License

GNU General Public License 

## Code Generation

generate base files from generateDS:

python generateDS.py -o ../../Work/libSpineML/experiment.py  ../SpineML/Schema/SpineMLExperimentLayer.xsd 
python generateDS.py -o ../../Work/libSpineML/network.py  ../SpineML/Schema/SpineMLNetworkLayer.xsd 
python generateDS.py -o ../../Work/libSpineML/component.py  ../SpineML/Schema/SpineMLComponentLayer.xsd

