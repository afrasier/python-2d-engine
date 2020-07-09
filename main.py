import argparse
import sys
import logging
import logging.config

from devdemos import DEV_DEMOS
from settings import config

"""
Python 2d Engine

What started as a game has morphed into its own thing
"""

"""
The main method handles initial configurations and parses any command line arguments
"""


def main():
    # Set up our argument parser for handing command line options
    parser = argparse.ArgumentParser(description=f"{config.APP_DATA.get('name')} - v{config.APP_DATA.get('version')}")
    parser.add_argument("-ll", "--log-level", help="Set the default log level")
    parser.add_argument("-le", "--log-events", action="store_true", help="Log events")
    parser.add_argument("-dd", "--dev-demo", help="Run the specified dev demo", choices=DEV_DEMOS.keys())

    args = parser.parse_args()

    print(f"Starting {config.APP_DATA.get('name')} v{config.APP_DATA.get('version')}...")

    logging.config.dictConfig(config.LOGGING)
    logger = logging.getLogger()  # Use __name__ in subpackages

    logger.info("Configured logger")

    if args.log_level:
        logger.info(f"Overriding logger level: {args.log_level}")
        if args.log_level == "INFO":
            logger.setLevel(logging.INFO)
        if args.log_level == "DEBUG":
            logger.setLevel(logging.DEBUG)
        if args.log_level == "WARNING":
            logger.setLevel(logging.WARNING)
        if args.log_level == "ERROR":
            logger.setLevel(logging.ERROR)

    if args.log_events:
        logger.info(f"Setting log events to {args.log_events}")
        config.SETTINGS["logging"]["events"] = True

    if args.dev_demo:
        logger.info(f"Dev demo option {args.dev_demo} selected")
        demo = DEV_DEMOS.get(args.dev_demo, False)
        if demo:
            demo()
        else:
            logger.info(f"Demo requested: {args.dev_demo} but not available")
        sys.exit(0)


if __name__ == "__main__":
    main()
