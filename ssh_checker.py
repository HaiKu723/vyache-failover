"""
Vyache Failover
SSH checker

Author: HaiKu
Version: 1.0.0
"""

from __future__ import annotations

import subprocess


class SSHChecker:

    def __init__(
        self,
        host: str,
        key: str = "/root/.ssh/vyache_failover",
        user: str = "root",
        timeout: int = 10
    ):

        self.host = host
        self.key = key
        self.user = user
        self.timeout = timeout

    def _run(self, command: str):

        return subprocess.run(

            [
                "ssh",
                "-i",
                self.key,
                "-o",
                "BatchMode=yes",
                "-o",
                "StrictHostKeyChecking=no",
                "-o",
                f"ConnectTimeout={self.timeout}",
                f"{self.user}@{self.host}",
                command
            ],

            capture_output=True,
            text=True

        )

    def status(self):

        cmd = (
            'printf "SSH\n"; '
            'systemctl is-active awg-quick@awg0; '
            'systemctl is-active awg-quick@awg1'
        )

        process = self._run(cmd)

        if process.returncode != 0:

            return {
                "ssh": False,
                "awg0": False,
                "awg1": False
            }

        lines = [
            line.strip()
            for line in process.stdout.splitlines()
            if line.strip()
        ]

        result = {
            "ssh": False,
            "awg0": False,
            "awg1": False
        }

        if len(lines) >= 3:

            result["ssh"] = lines[0] == "SSH"
            result["awg0"] = lines[1] == "active"
            result["awg1"] = lines[2] == "active"

        return result

    def is_healthy(self):

        s = self.status()

        return all(s.values())
