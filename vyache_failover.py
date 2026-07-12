"""
Vyache Failover

Main service

Author: HaiKu
Version: 1.0.0
"""

from __future__ import annotations

import signal
import sys
import time

from config import Config
from healthcheck import HealthChecker
from logger import Logger


class VyacheFailover:

    def __init__(self):

        self.cfg = Config()

        self.log = Logger(
            self.cfg.log_file
        )

        self.health = HealthChecker()

        self.running = True

        signal.signal(
            signal.SIGINT,
            self.stop
        )

        signal.signal(
            signal.SIGTERM,
            self.stop
        )

    # -----------------------------

    def stop(self, *_):

        self.log.info(
            "Stopping service..."
        )

        self.running = False

    # -----------------------------

    def run(self):

        self.log.info(
            "======================================="
        )

        self.log.info(
            "Vyache Failover started"
        )

        self.log.info(
            f"Primary: {self.cfg.primary_ip}"
        )

        self.log.info(
            f"Backup : {self.cfg.backup_ip}"
        )

        self.log.info(
            f"Check interval: {self.cfg.interval}s"
        )

        self.log.info(
            "======================================="
        )

        while self.running:

            try:

                self.health.check()

            except Exception as e:

                self.log.exception(str(e))

            time.sleep(
                self.cfg.interval
            )

        self.log.info(
            "Service stopped."
        )


# ---------------------------------

def main():

    service = VyacheFailover()

    service.run()


if __name__ == "__main__":

    main()
