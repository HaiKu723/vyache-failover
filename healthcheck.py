"""
Vyache Failover
Health checker

Author: HaiKu
Version: 1.0.1
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

        # текущее состояние DNS
        self.mode = "primary"


    # -----------------------------

    def check(self):

        healthy = self.ssh.is_healthy()

        if healthy:

            self._healthy()

        else:

            self._failed()


    # -----------------------------

    def _healthy(self):

        self.fail_counter = 0

        self.recover_counter += 1

        self.log.info(
            f"RU1 OK ({self.recover_counter}/{self.cfg.recover_count})"
        )


        # если уже primary - ничего не делаем

        if self.mode == "primary":
            return


        # ждём стабильное восстановление

        if self.recover_counter < self.cfg.recover_count:
            return


        self.log.warning(
            "Switching DNS -> PRIMARY"
        )


        try:

            if self.api.switch_to_primary():

                self.log.info(
                    "DNS switched to PRIMARY"
                )


            self.mode = "primary"
            self.recover_counter = 0


        except Exception as e:

            self.log.error(
                f"PRIMARY switch failed: {e}"
            )


    # -----------------------------

    def _failed(self):

        self.recover_counter = 0

        self.fail_counter += 1


        self.log.warning(
            f"RU1 FAILED ({self.fail_counter}/{self.cfg.fail_count})"
        )


        # если уже backup - не дёргаем DNS

        if self.mode == "backup":
            return


        if self.fail_counter < self.cfg.fail_count:
            return


        self.log.warning(
            "Switching DNS -> BACKUP"
        )


        try:

            if self.api.switch_to_backup():

                self.log.info(
                    "DNS switched to BACKUP"
                )


            self.mode = "backup"
            self.fail_counter = 0


        except Exception as e:

            self.log.error(
                f"BACKUP switch failed: {e}"
            )
