# Generic Test Case 


def test_bundle_creation_instantiation():
    import libSpineML
    from libSpineML import smlBundle
    c = smlBundle.Bundle()
    assert type(c) is smlBundle.Bundle

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
    c = smlBundle.Bundle()
    c.add_experiment('libSpineML/tests/test_data/experiment0.xml')
    assert type(c.experiments[0]) == smlExperiment.SpineMLType

def test_bundle_network_parsing():
    import libSpineML
    from libSpineML import smlNetwork
    from libSpineML import smlBundle
    c = smlBundle.Bundle()
    c.add_network('libSpineML/tests/test_data/model.xml')
    assert type(c.networks[0]) == smlNetwork.SpineMLType

def test_bundle_component_parsing():
    import libSpineML
    from libSpineML import smlComponent
    from libSpineML import smlBundle
    c = smlBundle.Bundle()
    c.add_component('libSpineML/tests/test_data/LeakyIAF.xml')
    assert type(c.components[0]) == smlComponent.SpineMLType



def test_bundle_smlExperiment_adding():
    import libSpineML
    from libSpineML import smlExperiment
    from libSpineML import smlBundle
    c = smlBundle.Bundle()
    s = smlExperiment.SpineMLType()
    s.add_Experiment(smlExperiment.ExperimentType())
    c.add_experiment(s)
    assert type(c.experiments[0]) == type(s)

def test_bundle_smlNetwork_adding():
    import libSpineML
    from libSpineML import smlNetwork
    from libSpineML import smlBundle
    c = smlBundle.Bundle()
    n = smlNetwork.SpineMLType()
    n.add_Population(smlNetwork.PopulationType())
    c.add_network(n)
    assert type(c.networks[0]) == type(n)


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
    c = smlBundle.Bundle()
    with pytest.raises(TypeError):
        c.add_experiment(0)

def test_bundle_network_adding_integer():
    import pytest
    import libSpineML
    from libSpineML import smlBundle
    c = smlBundle.Bundle()
    with pytest.raises(TypeError):
        c.add_network(0)

def test_bundle_component_adding_integer():
    import pytest
    import libSpineML
    from libSpineML import smlBundle
    c = smlBundle.Bundle()
    with pytest.raises(TypeError):
        c.add_component(0)



        

        
