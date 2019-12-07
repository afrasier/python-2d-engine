import pytest
import logging

from _pytest.logging import LogCaptureFixture
from events import Orchestrator


class UtilTestLogger:
    def __init__(self, logger):
        self.logger = logging.getLogger()

        self.EVENT_HANDLERS = {
            "noop": self.log_with_z,
            "noop2": [self.log_with_x, self.log_with_y],
        }

    def log_it(self, x):
        self.logger.info(x)

    def log_with_x(self, x):
        self.logger.info(f"{x}x")

    def log_with_y(self, x):
        self.logger.info(f"{x}y")

    def log_with_z(self, x):
        self.logger.info(f"{x}z")


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
    with caplog.at_level(logging.DEBUG):
        fresh_orchestrator.emit("noop", "message")
        assert "Got event noop, but is not in registry" in caplog.text


def test_unsubscribe_no_subscriber(caplog: LogCaptureFixture, fresh_orchestrator: Orchestrator):
    """
    Test unsubscribing with no subscriber
    """
    with caplog.at_level(logging.INFO):
        testlogger: UtilTestLogger = UtilTestLogger(caplog)
        fresh_orchestrator.subscribe("noop", testlogger, testlogger.log_it)

        fresh_orchestrator.unsubscribe("noop", testlogger, testlogger.log_with_x)

        assert "Cannot locate subscription for unsubscribe" in caplog.text

        caplog.clear()

        fresh_orchestrator.unsubscribe("noop", testlogger)
        fresh_orchestrator.emit("noop", "test")

        assert "test" not in caplog.text

        caplog.clear()

        fresh_orchestrator.subscribe("noop", testlogger, testlogger.log_with_z)
        fresh_orchestrator.subscribe("noop", testlogger, testlogger.log_with_x)
        fresh_orchestrator.unsubscribe("noop", testlogger, testlogger.log_with_z)
        print(fresh_orchestrator.registry)
        fresh_orchestrator.emit("noop", "test")

        assert "testz" not in caplog.text
        assert "testx" in caplog.text

        caplog.clear()


def test_subscribe_emit_unsubscribe(caplog: LogCaptureFixture, fresh_orchestrator: Orchestrator):
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
        caplog.clear()

        fresh_orchestrator.emit("tlog2", msg)
        assert msg in caplog.text
        caplog.clear()

        fresh_orchestrator.unsubscribe_all(testlogger)

        fresh_orchestrator.emit("tlog2", msg)

        assert msg not in caplog.text
        caplog.clear()


def test_subscribe_all(caplog: LogCaptureFixture, fresh_orchestrator: Orchestrator):
    """
    Test subscribing, emitting, and unsubscribing flow
    """
    with caplog.at_level(logging.INFO):
        testlogger: UtilTestLogger = UtilTestLogger(caplog)
        fresh_orchestrator.subscribe_all(testlogger)
        print(fresh_orchestrator.registry)
        caplog.clear()

        fresh_orchestrator.emit("noop", "test")

        assert "testz" in caplog.text
        assert "testx" not in caplog.text
        assert "testy" not in caplog.text

        fresh_orchestrator.unsubscribe("noop", testlogger)
        caplog.clear()

        fresh_orchestrator.emit("noop2", "test")

        assert "testz" not in caplog.text
        assert "testx" in caplog.text
        assert "testy" in caplog.text

        caplog.clear()
