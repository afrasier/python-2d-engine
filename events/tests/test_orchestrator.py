import pytest

from events import Orchestrator

@pytest.fixture
def fresh_orchestrator():
    return Orchestrator.get_instance(fresh)


def test_orchestrator_singleton():
    '''
    Orchestrator get instance should return the same object, unless fresh is supplied
    '''
    orchestrator = Orchestrator.get_instance()
    new_orchestrator = Orchestrator.get_instance()

    assert id(orchestrator) == id(new_orchestrator)

    new_orchestrator = Orchestrator.get_instance(fresh=True)

    assert id(orchestrator) != id(new_orchestrator)

def test_emit_no_event(caplog, fresh_orchestrator):
    '''
    Test emitting an event with no subscribers
    '''
    



