# Generic Test Cases 


def test_bundle_creation_instantiation():
    import libSpineML
    from libSpineML import smlBundle
    c = smlBundle.Bundle()
    assert type(c) is smlBundle.Bundle

def test_bundle_component_parsing():
    import libSpineML
    from libSpineML import smlExperiment
    from libSpineML import smlBundle
    c = smlBundle.Bundle()
    c.add_experiment('libSpineML/tests/test_data/experiment0.xml')
    assert type(c.experiments[0]) == smlExperiment.SpineMLType


def test_bundle_smlExperiment_adding():
    import libSpineML
    from libSpineML import smlExperiment
    from libSpineML import smlBundle
    c = smlBundle.Bundle()
    s = smlExperiment.SpineMLType()
    s.add_Experiment(smlExperiment.ExperimentType())
    c.add_experiment(s)
    assert type(c.experiments[0]) == type(s)


def test_bundle_smlExperiment_adding_fail():
    import pytest
    import libSpineML
    from libSpineML import smlBundle
    c = smlBundle.Bundle()
    with pytest.raises(TypeError):
        c.add_experiment(0)

def test_bundle_component_adding_integer():
    import pytest
    import libSpineML
    from libSpineML import smlBundle
    c = smlBundle.Bundle()
    with pytest.raises(TypeError):
        c.add_component(0)

def test_bundle_smlExperiment_adding_integer():
    import pytest
    import libSpineML
    from libSpineML import smlBundle
    c = smlBundle.Bundle()
    with pytest.raises(TypeError):
        c.add_component(0)


        

        
