"""
ChronoOrchestrator should be used when you want to trigger events based 
"""


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

    def update(self) -> None:
        """
        Fires off chronotriggers
        """
        pass
