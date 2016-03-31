# Generic Test Cases 


def test_bundle_creation_instantiation():
    import libSpineML
    from libSpineML import spineml
    c = spineml.Bundle()
    assert type(c) is spineml.Bundle

def test_bundle_component_parsing():
    import libSpineML
    from libSpineML import experiment
    from libSpineML import spineml
    c = spineml.Bundle()
    e = experiment.ExperimentType()
    c.add_experiment('tests/test_data/experiment0.xml')
    assert type(c.experiments[0]) == experiment.SpineMLType


def test_bundle_experiment_adding():
    import libSpineML
    from libSpineML import experiment
    from libSpineML import spineml
    c = spineml.Bundle()
    s = experiment.SpineMLType()
    s.add_Experiment(experiment.ExperimentType())
    c.add_experiment(s)
    assert type(c.experiments[0]) == type(s)




def test_bundle_experiment_adding_fail():
    import pytest
    import libSpineML
    from libSpineML import spineml
    c = spineml.Bundle()
    with pytest.raises(TypeError):
        c.add_experiment(0)
        
