"""
ChronoOrchestrator should be used when you want to trigger events based upon time

Items are added to a registry list, in the form of
(datetime, datetime, Callable, List, Dict)
(Trigger time, Time added, Callback, Args, Kwargs)
"""
import logging

from datetime import datetime
from dateutil.relativedelta import relativedelta


from typing import List, Tuple, Callable, Dict


class ChronoOrchestrator:
    """
    As Orchestrator, but triggered based upon the progress of time
    """

    SINGLETON = None

    @staticmethod
    def get_instance(fresh: bool = False) -> "ChronoOrchestrator":
        """
        Returns a singleton of the eventmanager
        """
        if not ChronoOrchestrator.SINGLETON or fresh:
            ChronoOrchestrator.SINGLETON = ChronoOrchestrator()

        return ChronoOrchestrator.SINGLETON

    def __init__(self) -> None:
        """
        Registry contains triggers in the fashion of:
        (Trigger Time, Placement Time, Callback, kwargs)
        """
        self.logger = logging.getLogger(__name__)
        self.registry: List[Tuple[datetime, datetime, Callable, List, Dict]] = []

    def add_trigger(self, callback: Callable, cb_args: List = None, cb_kwargs: Dict = None, **kwargs) -> None:
        """
        Adds a trigger to the registry
        """
        delta = relativedelta(**kwargs)
        now = datetime.now()
        trigger_time = now + delta

        if not cb_kwargs:
            cb_kwargs = {}

        if not cb_args:
            cb_args = []

        registrant = (trigger_time, now, callback, cb_args, cb_kwargs)

        self.registry.append(registrant)
        self.registry.sort(key=lambda x: x[0])

    def update(self) -> None:
        """
        Fires off chronotriggers
        """
        now: datetime = datetime.now()

        while self.registry:
            delta = now - self.registry[0][0]
            if delta.total_seconds() >= 0:
                registrant = self.registry.pop(0)
                try:
                    registrant[2](**registrant[3], **registrant[4])
                except Exception as e:
                    self.logger.error(f"Error while executing registrant:\n\t{registrant}\n\t{e}")
            else:
                break
