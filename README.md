# libSpineML

## Synopsis

This project provides python bindings for the SpineML schema, which can be found [here](http://bimpa.group.shef.ac.uk/SpineML/index.php)



## Code Example

### SpineML Parsing


Parsing an existing SpineML specification is easy to accumplish, by providing the path to the schema-specific XML file.

```
import experiment as exp
import network as net
import component as com

c = com.parse('Examples/LeakyIAF.xml')
n = net.parse('Examples/model.xml')
e = exp.parse('Examples/experiment0.xml')
```

This will populate the variables with the relavant objects. 

Importantly, parsing returns a SpineMLType, as the highest level XML tag.

### Recursive Parsing

Experiment and Network level parsing allow recursive loading of linked spineML classes, for more convientient loading.

```
e = exp.parse('examples/experiment0.xml',recursive=True)
```
This will populate the network and component layers.
### SpineML exporting

Our individual SpineML Classes can export XML generated through the programatic interface, using the <code>export()</code> function.

```
import sys
from libSpineML import experiment
x = experiment.SpineMLType()
x.add_Experiment(experiment.ExperimentType())
x.export(sys.stdout,0)
```


### Create a Specification

First, to create a component:

```
# Create a new neuron body
c = com.ComponentClassType('ComName','neuronbody')
# Add neuron parameters
c.add_Parameter(com.ParameterType('C','nS'))
c.add_Parameter(com.ParameterType('C','nS'))
c.add_Parameter(com.ParameterType('Vt','mV'))
c.add_Parameter(com.ParameterType('Er','mV'))
c.add_Parameter(com.ParameterType('Vr','mV'))
c.add_Parameter(com.ParameterType('R','MOhm'))
```

The majority of a component is defined within a dynamics tag, so first we will build up a dynamic object and assign it to our object using c.set_Dynamics()

A dynamics regime takes an initial regime, a regime object and State Variables

Primerily we will set up a new regime using
```reg = com.RegimeType(name='integrating',...```

Which will require a new Time Derivitive
```
td = com.TimeDerivativeType('V', '((I_Syn) / C) + (Vr - V) / (R*C)')
```

And an On Condition, which in turn requires State Assignments, Triggers and Events

```
sa = com.StateAssignmentType('V','Vr')
tr = com.TriggerType('V > Vt')
eo = com.EventOutType('spike')
# Create the On Condition
con = com.OnConditionType('integrating',sa,eo,None,tr)
```

With these we can create a regime:

```
reg = com.RegimeType('integrating',td,con)
```

and feed this into the dynamics:

```
dyn = com.DynamicsType('integrating',reg)
```

Here we have to specify the state variables

```
dyn.add_StateVariable(com.StateVariableType('V','mV'))
```

and finally we can set these dynamics to the component
```
c.set_Dynamics(dyn) 
```

and finally add any ports:

```
c.add_Port(com.EventSendPortType('spike'))
c.add_Port(com.AnalogReducePortType('I_syn','+','mA'))
```


## Motivation

libSpineML will create a programatic way to build up declaritive SpineML models, with the aim of enabling easy model sharing across the computational neuroscience spectrum. This project will be closely integrated with the SpineML and SpineCreator projects to enable easy model translation from high level graphical tools such as SpineCreator, into python-based simulators such as Neurokernel.

## Installation

``` python setup.py install ```

## API Reference

You can read the full documentation at [ReadTheDocs}(http://libspineml.readthedocs.org/en/latest/)

## Tests

This project uses the pytest framework, you can run tests using <code>python setup.py test</code>

Further testing is achieved using the <code> py.test </code> command. Continuous integration testing is achieved using Travis CI.

For code coverage, [pytest-cov](https://pypi.python.org/pypi/pytest-cov) is required which can be installed easily with pip using <code>pip install pytest-cov</code>. With this the code coverage can be tested using the command <code>py.test --cov=libSpineML tests/</code> 
[![Build Status](https://travis-ci.org/AdamRTomkins/libSpineML.svg?branch=master)](https://travis-ci.org/AdamRTomkins/libSpineML)

## Contributors

Adam Tomkins

## License

GNU General Public License 3.0

## Code Generation

generate base files using generateDS, in combination with the schema files you can find on the [SpineML site](http://bimpa.group.shef.ac.uk/SpineML/index.php/Documentation) 

python generateDS.py -o experiment.py  SpineMLExperimentLayer.xsd 
python generateDS.py -o network.py  SpineMLNetworkLayer.xsd 
python generateDS.py -o component.py  SpineMLComponentLayer.xsd

