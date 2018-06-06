import sys
from libSpineML import smlNetwork as net
from libSpineML import smlComponent as com


"""
OverView
"""
# Create SpineMLType

## Create PopulationType

### Create NeuronType

#### @name::String	The population name
#### @url::String	URL to the neuron body component model file
#### @size::int	The population size

#### Property [0..*]	Set or zero or more Property Elements




### Create ProjectionType

#### Synapse [1..*]	Optional seed value to be used for random number generation
#### @dst_population::double	Population name of the projection synapse


"""
Reverse Building
"""

#### Create NeuronType
size = 1
name = 'LeakyIAF'
url = 'LeakyIAF.xml'

##### Create all the parameters for the neuron
propertyList = []

##### Add Resistance
propName = 'R'
abstractValue=net.FixedValueType(value = 1.0)
prop = net.PropertyType(name=propName, AbstractValue=abstractValue)
propertyList.append(prop)

##### Add Membrane Capacitance
propName = 'Cm'
abstractValue=net.UniformDistributionType(seed=1, minimum=1, maximum=10)
prop = net.PropertyType(name=propName, AbstractValue=abstractValue)
propertyList.append(prop)

## Combine to the NeuronType
NeuronType = net.NeuronType(name = name, url = url, size = size, Property=propertyList)

#### Create Projection

#Create SynapseList
## Connectivity [1]	A connectivity type
## WeightUpdate [1]	WeightUpdate model
## PostSynapse [1]	PostSynapse model




#### Create PopulationType
p = net.PopulationType(NeuronType)