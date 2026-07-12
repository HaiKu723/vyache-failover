"""
Vyache Failover
Configuration loader

Author: HaiKu
Version: 1.0.0
"""

from __future__ import annotations

import configparser
from pathlib import Path


CONFIG_FILE = "/etc/vyache-failover.conf"


class ConfigError(Exception):
    """Configuration error."""


class Config:

    def __init__(self) -> None:

        self._parser = configparser.ConfigParser()

        config = Path(CONFIG_FILE)

        if not config.exists():
            raise ConfigError(
                f"Configuration file not found: {CONFIG_FILE}"
            )

        self._parser.read(config)

        self._load()

    def _load(self) -> None:

        try:

            # ---------------- REG.RU ----------------

            self.regru_username = self._parser.get(
                "regru",
                "username"
            )

            self.regru_password = self._parser.get(
                "regru",
                "password"
            )

            # ---------------- DNS ----------------

            self.domain = self._parser.get(
                "dns",
                "domain"
            )

            self.record = self._parser.get(
                "dns",
                "record"
            )

            self.zone = self._parser.get(
                "dns",
                "zone"
            )

            # ---------------- Servers ----------------

            self.primary_ip = self._parser.get(
                "servers",
                "primary"
            )

            self.backup_ip = self._parser.get(
                "servers",
                "backup"
            )

            self.vpn_port = self._parser.getint(
                "servers",
                "port"
            )

            # ---------------- Settings ----------------

            self.interval = self._parser.getint(
                "settings",
                "interval"
            )

            self.fail_count = self._parser.getint(
                "settings",
                "fail_count"
            )

            self.recover_count = self._parser.getint(
                "settings",
                "recover_count"
            )

            self.log_file = self._parser.get(
                "settings",
                "log"
            )

            self.dry_run = self._parser.getboolean(
                "settings",
                "dry_run"
            )

        except Exception as e:
            raise ConfigError(str(e))

    def reload(self) -> None:
        """
        Reload configuration from disk.
        """

        self._parser.read(CONFIG_FILE)

        self._load()

    def as_dict(self) -> dict:

        return {
            "regru_username": self.regru_username,
            "domain": self.domain,
            "record": self.record,
            "zone": self.zone,
            "primary_ip": self.primary_ip,
            "backup_ip": self.backup_ip,
            "vpn_port": self.vpn_port,
            "interval": self.interval,
            "fail_count": self.fail_count,
            "recover_count": self.recover_count,
            "log_file": self.log_file,
            "dry_run": self.dry_run,
        }

    def __repr__(self):

        return (
            f"<Config "
            f"primary={self.primary_ip} "
            f"backup={self.backup_ip} "
            f"domain={self.domain}>"
        )
