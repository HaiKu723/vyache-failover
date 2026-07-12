"""
Vyache Failover
Health checker

Author: HaiKu
Version: 1.0.0
"""

from __future__ import annotations

from config import Config
from logger import Logger
from ssh_checker import SSHChecker
from regru import RegRu


class HealthChecker:

    def __init__(self):

        self.cfg = Config()

        self.log = Logger(
            self.cfg.log_file
        )

        self.ssh = SSHChecker(
            self.cfg.primary_ip
        )

        self.api = RegRu()

        self.fail_counter = 0
        self.recover_counter = 0

    def check(self):

        healthy = self.ssh.is_healthy()

        if healthy:

            self._healthy()

        else:

            self._failed()

    # ------------------------------

    def _healthy(self):

        self.fail_counter = 0

        self.recover_counter += 1

        self.log.info(
            f"RU1 OK ({self.recover_counter}/{self.cfg.recover_count})"
        )

        if self.recover_counter < self.cfg.recover_count:
            return

        current = self.api.get_current_ip()

        if current != self.cfg.primary_ip:

            self.log.warning(
                "Switching DNS -> PRIMARY"
            )

            if self.api.switch_to_primary():

                self.log.info(
                    "DNS switched to PRIMARY"
                )

        self.recover_counter = self.cfg.recover_count

    # ------------------------------

    def _failed(self):

        self.recover_counter = 0

        self.fail_counter += 1

        self.log.warning(
            f"RU1 FAILED ({self.fail_counter}/{self.cfg.fail_count})"
        )

        if self.fail_counter < self.cfg.fail_count:
            return

        current = self.api.get_current_ip()

        if current != self.cfg.backup_ip:

            self.log.warning(
                "Switching DNS -> BACKUP"
            )

            if self.api.switch_to_backup():

                self.log.info(
                    "DNS switched to BACKUP"
                )

        self.fail_counter = self.cfg.fail_count
