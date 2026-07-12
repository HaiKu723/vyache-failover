"""
Vyache Failover
REG.RU API client

Author: HaiKu
Version: 1.0.0
"""

from __future__ import annotations

import requests

from config import Config


class RegRuError(Exception):
    pass


class RegRu:

    API_URL = "https://api.reg.ru/api/regru2"

    def __init__(self):

        self.cfg = Config()

        self.auth = {
            "username": self.cfg.regru_username,
            "password": self.cfg.regru_password,
            "output_content_type": "json",
        }


    def _request(self, method: str, data: dict):

        payload = self.auth.copy()
        payload.update(data)

        try:

            response = requests.post(
                f"{self.API_URL}/{method}",
                data=payload,
                timeout=15
            )

            response.raise_for_status()

        except Exception as e:

            raise RegRuError(
                f"REG.RU connection error: {e}"
            )


        result = response.json()


        if result.get("result") != "success":

            raise RegRuError(
                result.get(
                    "error_text",
                    "Unknown REG.RU error"
                )
            )


        return result



    # Получение записей зоны

    def get_records(self):

        return self._request(
            "zone/get_resource_records",
            {
                "domain_name": self.cfg.zone
            }
        )



    # Текущий IP vpn

    def get_vpn_ips(self):

        result = self.get_records()

        ips = []

        domains = (
            result
            .get("answer", {})
            .get("domains", [])
        )


        for domain in domains:

            for record in domain.get("rrs", []):

                if (
                    record.get("rectype") == "A"
                    and record.get("subname") == self.cfg.record
                ):

                    ips.append(
                        record.get("content")
                    )


        return ips



    def get_current_ip(self):

        ips = self.get_vpn_ips()

        if len(ips) == 1:

            return ips[0]

        return None



    # Добавление A записи

    def add_ip(self, ip: str):

        if self.cfg.dry_run:

            print(
                f"[DRY RUN] ADD {self.cfg.record} -> {ip}"
            )

            return True


        return self._request(
            "zone/add_alias",
            {
                "domain_name": self.cfg.zone,
                "subname": self.cfg.record,
                "ipaddr": ip,
            }
        )

    # Удаление A записи

    def remove_ip(self, ip: str):

        if self.cfg.dry_run:

            print(
                f"[DRY RUN] REMOVE {self.cfg.record} -> {ip}"
            )

            return True


        return self._request(
            "zone/remove_record",
            {
                "domain_name": self.cfg.zone,
                "subname": self.cfg.record,
                "record_type": "A",
                "content": ip,
            }
        )



    # Переключение

    def switch_to_primary(self):

        current = self.get_vpn_ips()


        if (
            len(current) == 1
            and current[0] == self.cfg.primary_ip
        ):

            return False


        for ip in current:

            self.remove_ip(ip)


        self.add_ip(
            self.cfg.primary_ip
        )


        return True



    def switch_to_backup(self):

        current = self.get_vpn_ips()


        if (
            len(current) == 1
            and current[0] == self.cfg.backup_ip
        ):

            return False


        for ip in current:

            self.remove_ip(ip)


        self.add_ip(
            self.cfg.backup_ip
        )


        return True
