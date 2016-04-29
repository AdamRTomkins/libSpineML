# Generic Test Case 


def test_bundle_creation_instantiation():
    import libSpineML
    from libSpineML import smlBundle
    b = smlBundle.Bundle()
    assert type(b) is smlBundle.Bundle

def test_bundle_creation_loaded_experiment_list_instantiation():
    import libSpineML
    from libSpineML import smlExperiment
    from libSpineML import smlComponent
    from libSpineML import smlNetwork
    from libSpineML import smlBundle
    
    e = smlExperiment.SpineMLType()
    e.add_Experiment(smlExperiment.ExperimentType())

    b = smlBundle.Bundle([e,e])
    assert type(b) is smlBundle.Bundle

def test_bundle_creation_loaded_network_list_instantiation():
    import libSpineML
    from libSpineML import smlExperiment
    from libSpineML import smlComponent
    from libSpineML import smlNetwork
    from libSpineML import smlBundle

    n = smlNetwork.SpineMLType()
    n.add_Population(smlNetwork.PopulationType())

    b = smlBundle.Bundle(None,[n,n])
    assert type(b) is smlBundle.Bundle


def test_bundle_creation_loaded_component_list_instantiation():
    import libSpineML
    from libSpineML import smlExperiment
    from libSpineML import smlComponent
    from libSpineML import smlNetwork
    from libSpineML import smlBundle

    c = smlComponent.SpineMLType()
    c.set_ComponentClass(smlComponent.ComponentClassType())

    b = smlBundle.Bundle(None,None,[c,c])
    assert type(b) is smlBundle.Bundle

def test_bundle_creation_loaded_experiment_list_and_integer_instantiation():
    import libSpineML
    import pytest
    from libSpineML import smlExperiment
    from libSpineML import smlComponent
    from libSpineML import smlNetwork
    from libSpineML import smlBundle

    e = smlExperiment.SpineMLType()
    e.add_Experiment(smlExperiment.ExperimentType())

    with pytest.raises(TypeError):
        b = smlBundle.Bundle([e,None])


def test_bundle_creation_loaded_network_list_and_integer_instantiation():
    import libSpineML
    import pytest
    from libSpineML import smlExperiment
    from libSpineML import smlComponent
    from libSpineML import smlNetwork
    from libSpineML import smlBundle

    n = smlNetwork.SpineMLType()
    n.add_Population(smlNetwork.PopulationType())

    with pytest.raises(TypeError):
        b = smlBundle.Bundle(None,[n,None])


def test_bundle_creation_loaded_component_list_and_integer_instantiation():
    import libSpineML
    import pytest
    from libSpineML import smlExperiment
    from libSpineML import smlComponent
    from libSpineML import smlNetwork
    from libSpineML import smlBundle

    c = smlComponent.SpineMLType()
    c.set_ComponentClass(smlComponent.ComponentClassType())

    with pytest.raises(TypeError):
        b = smlBundle.Bundle(None,None,[c,None])




def test_bundle_creation_loaded_instantiation():
    import libSpineML
    from libSpineML import smlExperiment
    from libSpineML import smlComponent
    from libSpineML import smlNetwork
    from libSpineML import smlBundle
    e = smlExperiment.SpineMLType()
    e.add_Experiment(smlExperiment.ExperimentType())

    n = smlNetwork.SpineMLType()
    n.add_Population(smlNetwork.PopulationType())

    c = smlComponent.SpineMLType()
    c.set_ComponentClass(smlComponent.ComponentClassType())

    b = smlBundle.Bundle(e,n,c)
    assert type(b) is smlBundle.Bundle

def test_bundle_experiment_parsing():
    import libSpineML
    from libSpineML import smlExperiment
    from libSpineML import smlBundle
    b = smlBundle.Bundle()
    b.add_experiment('libSpineML/tests/test_data/experiment0.xml')
    assert type(b.experiments[0]) == smlExperiment.SpineMLType

def test_bundle_network_parsing():
    import libSpineML
    from libSpineML import smlNetwork
    from libSpineML import smlBundle
    b = smlBundle.Bundle()
    b.add_network('libSpineML/tests/test_data/model.xml')
    assert type(b.networks[0]) == smlNetwork.SpineMLType

def test_bundle_component_parsing():
    import libSpineML
    from libSpineML import smlComponent
    from libSpineML import smlBundle
    b = smlBundle.Bundle()
    b.add_component('libSpineML/tests/test_data/LeakyIAF.xml')
    assert type(b.components[0]) == smlComponent.SpineMLType



def test_bundle_smlExperiment_adding():
    import libSpineML
    from libSpineML import smlExperiment
    from libSpineML import smlBundle
    b = smlBundle.Bundle()
    s = smlExperiment.SpineMLType()
    s.add_Experiment(smlExperiment.ExperimentType())
    b.add_experiment(s)
    assert type(b.experiments[0]) == type(s)

def test_bundle_smlNetwork_adding():
    import libSpineML
    from libSpineML import smlNetwork
    from libSpineML import smlBundle
    b = smlBundle.Bundle()
    n = smlNetwork.SpineMLType()
    n.add_Population(smlNetwork.PopulationType())
    b.add_network(n)
    assert type(b.networks[0]) == type(n)


def test_bundle_smlComponent_adding():
    import libSpineML
    from libSpineML import smlComponent
    from libSpineML import smlBundle
    b = smlBundle.Bundle()
    c = smlComponent.SpineMLType()
    c.set_ComponentClass(smlComponent.ComponentClassType())
    b.add_component(c)
    assert type(b.components[0]) == type(c)





# Add Integers instead of Expected types to the Bundle
def test_bundle_smlExperiment_adding_integer():
    import pytest
    import libSpineML
    from libSpineML import smlBundle
    b = smlBundle.Bundle()
    with pytest.raises(TypeError):
        b.add_experiment(0)

def test_bundle_network_adding_integer():
    import pytest
    import libSpineML
    from libSpineML import smlBundle
    b = smlBundle.Bundle()
    with pytest.raises(TypeError):
        b.add_network(0)

def test_bundle_component_adding_integer():
    import pytest
    import libSpineML
    from libSpineML import smlBundle
    b = smlBundle.Bundle()
    with pytest.raises(TypeError):
        b.add_component(0)



# Export Functions
#	Export each file in each list
#'''
#
#def test_export_single_component_function():
#    import libSpineML
#    from libSpineML import smlBundle
#    from libSpineML import smlComponent
#    b = smlBundle.Bundle()
#    b.add_component('libSpineML/tests/test_data/LeakyIAF.xml')
#    # Assuming a method export_component(path="./",index=None)
#    # Which exports the component to as export_test_component_0.xml where the number is the index
#    # Potentially this could more intelligently name the files from the hightest object
#    b.export_component('libSpineML/tests/test_data/',0)
#    b.add_component('libSpineML/tests/test_data/export_test_component_0.xml')
#    assert type(b.components[1]) == smlComponent.SpineMLType
#'''


# Test recursive Adding

# test network add component
def test_recusive_adding_for_networks():
    import libSpineML
    from libSpineML import smlBundle
    from libSpineML import smlNetwork
    b = smlBundle.Bundle()
    b.add_network('libSpineML/tests/test_data/model.xml',True)
    assert(len(b.components)==1)

def test_not_recusive_adding_for_networks():
    import libSpineML
    from libSpineML import smlBundle
    from libSpineML import smlNetwork
    import pdb
    b = smlBundle.Bundle()
    b.add_network('libSpineML/tests/test_data/model.xml',False)
    assert(len(b.components)==0)


def test_recusive_adding_for_experiments():
    import libSpineML
    from libSpineML import smlBundle
    from libSpineML import smlExperiment
    b = smlBundle.Bundle()
    b.add_experiment('libSpineML/tests/test_data/experiment0.xml',True)
    assert(len(b.networks)==1)
    assert(len(b.components)==1)












