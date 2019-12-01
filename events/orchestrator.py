'''
Events Orchestrator

When using the orchestrator, use Orchestrator.get_instance() to retrieve the current
orchestrator.

Subscribe an instance to an event stream:
    orchestrator.subscribe("event_name", instance, instance.callback)
'''
import logging
from typing import Dict, Callable


class Orchestrator():
    '''
    Manages events among all modules.
    '''
    SINGLETON = None

    @staticmethod
    def get_instance(fresh: bool = False) -> 'Orchestrator':
        '''
        Returns a singleton of the eventmanager
        '''
        if not Orchestrator.SINGLETON or fresh:
            Orchestrator.SINGLETON = Orchestrator()

        return Orchestrator.SINGLETON

    def __init__(self) -> None:
        '''
        Registry should contain k/v pairs of:
            key: {
                id: callable
            }
        '''
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.registry: Dict[str, Dict[int, Callable]] = {}

    def emit(self, event: str, *args, **kwargs) -> None:
        '''
        Broadcasts an event to all subscribed instances
        '''
        self.logger.debug(f"Event emitted {event} with args {args}; kwargs {kwargs}")
        if event not in self.registry:
            self.logger.warning(f"Got event {event}, but is not in registry")
        for subscriber in self.registry.get(event, {}).values():
            subscriber(*args, **kwargs)

    def subscribe(self, event: str, instance: object, subscriber: Callable) -> None:
        '''
        Subscribe an instance's function to an event
        '''
        self.logger.debug(f"Instance: {instance} registered for event {event}")
        if event not in self.registry:
            self.registry[event] = {}

        instance_id = id(instance)
        self.registry[event][instance_id] = subscriber

    def unsubscribe(self, event: str, instance: object) -> None:
        '''
        Unsubscribe an instance's subscriber from the event
        '''
        self.logger.debug(f"Instance: {instance} unsubscribe from event {event}")
        instance_id = id(instance)
        if event in self.registry and instance_id in self.registry.get(event):
            del self.registry.get(event)[instance_id]

    def unsubscribe_all(self, instance: object) -> None:
        '''
        Unsubscribes all listeners for this instance
        '''
        self.logger.debug(f"Instance: {instance} unsubscribed from all events")
        instance_id = id(instance)
        for value in self.registry.values():
            if instance_id in value:
                del value[instance_id]
