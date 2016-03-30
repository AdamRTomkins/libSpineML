# Generic Test Cases 

def test_component_basic_instantiation():
    from libSpineML import component as com
    c = com.ComponentClassType('ComName','neuronbody')
    assert type(c) is com.ComponentClassType




