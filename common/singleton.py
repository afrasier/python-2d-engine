from typing import Type


class Singleton:
    """
    Makes singleton
    """

    SINGLETON = None

    @classmethod
    def get_instance(cls, fresh: bool = False) -> __name__:
        """
        Returns a singleton of the eventmanager
        """
        if not cls.SINGLETON or fresh:
            cls.SINGLETON = cls()

        return cls.SINGLETON
