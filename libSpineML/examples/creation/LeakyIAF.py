from libSpineML import smlExperiment as exp
from libSpineML import smlNetwork as net
from libSpineML import smlComponent as com
import sys

# Create a new neuron body
c = com.ComponentClassType('LeakyIAF','neuronbody')
# Add neuron parameters
c.add_Parameter(com.ParameterType('C','nS'))
c.add_Parameter(com.ParameterType('C','nS'))
c.add_Parameter(com.ParameterType('Vt','mV'))
c.add_Parameter(com.ParameterType('Er','mV'))
c.add_Parameter(com.ParameterType('Vr','mV'))
c.add_Parameter(com.ParameterType('R','MOhm'))

# Specify Neuron Dynamics
td = com.TimeDerivativeType('V', '((I_Syn) / C) + (Vr - V) / (R*C)')
sa = com.StateAssignmentType('V','Vr')
tr = com.TriggerType('V > Vt')
eo = com.EventOutType('spike')

# Create the On Condition
con = com.OnConditionType('integrating',[sa],[eo],None,tr)

# Create Dynamics
reg = com.RegimeType('integrating',[td],[con])

dyn = com.DynamicsType('integrating',[reg])
dyn.add_StateVariable(com.StateVariableType('V','mV'))
c.set_Dynamics(dyn) 

# Add Ports
c.add_Port(com.EventSendPortType('spike'))
c.add_Port(com.AnalogReducePortType('I_syn','+','mA'))

# Finalise and Export
LeakyIAF = com.SpineMLType(c)
LeakyIAF.export(sys.stdout,0)
