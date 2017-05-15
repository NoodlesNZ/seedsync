# Copyright 2017, Inderpreet Singh, All rights reserved.

import signal
import time
import logging
import sys
import argparse


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


class Pylftpd:
    """
    Implements the service for pylftp
    It is run in the main thread (no daemonization)
    """
    _SERVICE_NAME = 'pylftp'
    _MAIN_THREAD_SLEEP_INTERVAL_IN_SECS = 0.5

    def __init__(self):
        # Parse arguments
        parser = argparse.ArgumentParser(description="PyLFTP daemon")
        parser.add_argument("--logdir", help="Directory for log files")
        parser.add_argument("--debug", action="store_true", help="Enable debug logs")
        args = parser.parse_args()

        # Logger setup
        self.logger = logging.getLogger(Pylftpd._SERVICE_NAME)
        if args.debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        if args.logdir:
            # Output logs to a file in the given directory
            handler = logging.FileHandler("{}/{}.log".format(args.logdir, Pylftpd._SERVICE_NAME))
        else:
            handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # Register the signal handlers
        signal.signal(signal.SIGTERM, self.signal)
        signal.signal(signal.SIGINT, self.signal)

    def run(self):
        self.logger.info("Starting pylftpd")

        try:
            # Start child threads here
            while True:
                time.sleep(Pylftpd._MAIN_THREAD_SLEEP_INTERVAL_IN_SECS)
        except ServiceExit:
            # Join all the threads here
            pass
        self.logger.info("Finished pylftpd")

    def signal(self, signum: int, _):
        self.logger.info("Caught signal {}".format(signal.Signals(signum).name))
        raise ServiceExit()


if __name__ == "__main__":
    if sys.hexversion < 0x03050000:
        sys.exit("Python 3.5 or newer is required to run this program.")

    pylftpd = Pylftpd()
    pylftpd.run()
