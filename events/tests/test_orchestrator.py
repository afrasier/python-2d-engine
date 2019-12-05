import pytest
import logging

from _pytest.logging import LogCaptureFixture
from events import Orchestrator


class UtilTestLogger:
    def __init__(self, logger):
        self.logger = logging.getLogger()

        self.EVENT_HANDLERS = {
            "noop": self.log_it,
            "noop2": [self.log_with_x, self.log_with_y],
        }

    def log_it(self, x):
        self.logger.info(x)

    def log_with_x(self, x):
        self.logger.info(f"{x}x")

    def log_with_y(self, x):
        self.logger.info(f"{x}y")


@pytest.fixture
def fresh_orchestrator() -> Orchestrator:
    return Orchestrator.get_instance(fresh=True)


def test_orchestrator_singleton():
    """
    Orchestrator get instance should return the same object, unless fresh is supplied
    """
    orchestrator = Orchestrator.get_instance()
    new_orchestrator = Orchestrator.get_instance()

    assert id(orchestrator) == id(new_orchestrator)

    new_orchestrator = Orchestrator.get_instance(fresh=True)

    assert id(orchestrator) != id(new_orchestrator)


def test_emit_no_event(caplog: LogCaptureFixture, fresh_orchestrator: Orchestrator):
    """
    Test emitting an event with no subscribers
    """
    fresh_orchestrator.emit("noop", "message")
    assert "Got event noop, but is not in registry" in caplog.text


def test_subscribe_emit_unsubscribe(
    caplog: LogCaptureFixture, fresh_orchestrator: Orchestrator
):
    """
    Test subscribing, emitting, and unsubscribing flow
    """
    with caplog.at_level(logging.INFO):
        testlogger: UtilTestLogger = UtilTestLogger(caplog)
        msg: str = "test message"

        fresh_orchestrator.subscribe("tlog", testlogger, testlogger.log_it)
        fresh_orchestrator.emit("tlog", msg)
        print(caplog.text)
        assert msg in caplog.text
        caplog.clear()

        fresh_orchestrator.subscribe("tlog2", testlogger, testlogger.log_it)

        fresh_orchestrator.unsubscribe("tlog", testlogger)
        fresh_orchestrator.emit("tlog", msg)

        assert msg not in caplog.text
        assert "Got event tlog, but is not in registry" in caplog.text
        caplog.clear()

        fresh_orchestrator.emit("tlog2", msg)
        assert msg in caplog.text
        caplog.clear()

        fresh_orchestrator.unsubscribe_all(testlogger)

        fresh_orchestrator.emit("tlog2", msg)

        assert msg not in caplog.text
        assert "Got event tlog2, but is not in registry" in caplog.text
        caplog.clear()


def test_subscribe_all(caplog: LogCaptureFixture, fresh_orchestrator: Orchestrator):
    """
    Test subscribing, emitting, and unsubscribing flow
    """
    with caplog.at_level(logging.INFO):
        testlogger: UtilTestLogger = UtilTestLogger(caplog)
        fresh_orchestrator.subscribe_all(testlogger)

        caplog.clear()

        fresh_orchestrator.emit("noop", "test")

        assert "test" in caplog.text
        assert "textx" not in caplog.text
        assert "testy" not in caplog.text

        fresh_orchestrator.unsubscribe("noop", testlogger)
        caplog.clear()

        fresh_orchestrator.emit("noop2", "test")

        assert "test" not in caplog.text
        assert "textx" in caplog.text
        assert "testy" in caplog.text

        caplog.clear()
