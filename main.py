import argparse
import logging
import logging.config
from settings import config

from events import Orchestrator, Event

'''
VENGEANCE PACT 

A Darkest Dungeon-like game inspired by the Stormlight Archive by Brandon Sanders
'''

'''
The main method handles initial configurations and parses any command line arguments
'''
class Test():
    def print_it(self, x):
        print(f"{x}, for sure!")

def main():
    # Set up our argument parser for handing command line options
    parser = argparse.ArgumentParser(description=f"{config.APP_DATA.get('name')} - v{config.APP_DATA.get('version')}")
    parser.add_argument('-ll', '--log-level', help="Set the default log level")

    args = parser.parse_args()

    print(args)

    print(f"Starting {config.APP_DATA.get('name')} v{config.APP_DATA.get('version')}...")

    logging.config.dictConfig(config.LOGGING)
    logger = logging.getLogger() # Use __name__ in subpackages

    logger.info("Configured logger")

    orchestrator = Orchestrator.get_instance()
    test = Test()
    orchestrator.subscribe(Event.TEST_MESSAGE, test, test.print_it)
    orchestrator.emit(Event.TEST_MESSAGE, "hellothere!")



if __name__ == "__main__":
    main()
