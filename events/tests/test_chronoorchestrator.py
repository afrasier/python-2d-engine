import pytest
import logging

from _pytest.logging import LogCaptureFixture
from events import ChronoOrchestrator


class ChronoTester:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count = self.count + 1

    def alter(self, amount):
        self.count = self.count + amount


@pytest.fixture
def fresh_orchestrator() -> ChronoOrchestrator:
    return ChronoOrchestrator.get_instance(fresh=True)


def test_chronoorchestrator_singleton():
    """
    Orchestrator get instance should return the same object, unless fresh is supplied
    """
    orchestrator = ChronoOrchestrator.get_instance()
    new_orchestrator = ChronoOrchestrator.get_instance()

    assert id(orchestrator) == id(new_orchestrator)

    new_orchestrator = ChronoOrchestrator.get_instance(fresh=True)

    assert id(orchestrator) != id(new_orchestrator)


@pytest.mark.freeze_time
def test_chronoorchestrator_updates(fresh_orchestrator, freezer):
    ctester = ChronoTester()

    freezer.move_to("2019-01-01 12:00:00")
    fresh_orchestrator.add_trigger(ctester.increment, seconds=1)
    fresh_orchestrator.update()

    assert ctester.count == 0

    freezer.move_to("2019-01-01 12:00:01")
    fresh_orchestrator.update()

    assert ctester.count == 1

    freezer.move_to("2019-01-01 12:00:02")
    fresh_orchestrator.update()

    assert ctester.count == 1

    fresh_orchestrator.add_trigger(ctester.alter, cb_args=(-2,), minutes=1)

    freezer.move_to("2019-01-01 12:01:02")
    fresh_orchestrator.update()

    assert ctester.count == -1

    fresh_orchestrator.add_trigger(ctester.alter, cb_kwargs={"amount": -20}, hours=1)

    freezer.move_to("2019-01-01 13:01:02")
    fresh_orchestrator.update()

    assert ctester.count == -21
