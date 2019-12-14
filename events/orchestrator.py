"""
Events Orchestrator

When using the orchestrator, use Orchestrator.get_instance() to retrieve the current
orchestrator.

Subscribe an instance to an event stream:
    orchestrator.subscribe("event_name", instance, instance.callback)
"""
import logging

from common import Singleton

from typing import Dict, Callable


class Orchestrator(Singleton):
    """
    Manages events among all modules.
    """

    def __init__(self) -> None:
        """
        Registry should contain k/v pairs of:
            key: {
                event_type: {
                    instance_id: {
                        subscriber_name: callable
                    }
                }
            }
        """
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.registry: Dict[str, Dict[int, Dict[str, Callable]]] = {}

    def emit(self, event: str, *args, **kwargs) -> None:
        """
        Broadcasts an event to all subscribed instances
        """
        self.logger.debug(f"Event emitted {event} with args {args}; kwargs {kwargs}")
        if event not in self.registry:
            self.logger.debug(f"Got event {event}, but is not in registry")
            return
        for instance_subscribers in self.registry.get(event, {}).values():
            for subscriber in instance_subscribers.values():
                subscriber(*args, **kwargs)

    def subscribe(self, event: str, instance: object, subscriber: Callable) -> None:
        """
        Subscribe an instance's function to an event
        """
        self.logger.debug(f"Instance: {instance} - {subscriber} registered for event {event}")
        if event not in self.registry:
            self.registry[event] = {}

        instance_id = id(instance)
        if instance_id not in self.registry[event]:
            self.registry[event][instance_id] = {}

        subscriber_id = subscriber.__name__
        self.registry[event][instance_id][subscriber_id] = subscriber

    def unsubscribe(self, event: str, instance: object, subscriber: Callable = None) -> None:
        """
        Unsubscribe an instance's subscriber from the event
        """
        self.logger.debug(f"Instance: {instance} - {subscriber} unsubscribe from event {event}")

        instance_id = id(instance)

        # Remove the specific subscriber if specified, otherwise, remove all subscribers for that instance
        if event in self.registry and instance_id in self.registry.get(event):
            if subscriber is not None:
                subscriber_id = subscriber.__name__
                if subscriber_id not in self.registry.get(event).get(instance_id):
                    self.logger.info(
                        f"Cannot locate subscription for unsubscribe: {instance} - {subscriber_id} :: {event}"
                    )
                    return

                del self.registry.get(event)[instance_id][subscriber_id]
            else:
                del self.registry.get(event)[instance_id]

        self.cleanup_registry()

    def subscribe_all(self, instance: object) -> None:
        """
        Subscribes all listeners for an instance as defined in the class level parameter 'EVENT_HANDLERS'
        """
        instance_handlers: Dict = instance.EVENT_HANDLERS
        if instance_handlers:
            for event, handlers in instance_handlers.items():
                handler_list = handlers
                # To allow setting via either array or callable, check if it's a list
                if not isinstance(handler_list, list):
                    handler_list = [handlers]
                for handler in handler_list:
                    self.subscribe(event, instance, handler)

    def unsubscribe_all(self, instance: object) -> None:
        """
        Unsubscribes all listeners for this instance
        """
        self.logger.debug(f"Instance: {instance} unsubscribed from all events")
        instance_id = id(instance)
        for value in self.registry.values():
            if instance_id in value:
                del value[instance_id]

        self.cleanup_registry()

    def cleanup_registry(self) -> None:
        """
        Removes any empty registry keys
        """
        self.registry: Dict[str, Dict[int, Callable]] = {k: v for k, v in self.registry.items() if len(v.keys()) > 0}
