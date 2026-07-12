# Vyache Failover

Automatic DNS failover service with server health monitoring and DNS switching.

Автоматический сервис отказоустойчивости с мониторингом серверов и переключением DNS.

---

## Features / Возможности

- Automatic server health monitoring
- SSH-based server checks
- Automatic DNS switching via REG.RU API
- Primary / Backup server architecture
- Configurable failure and recovery thresholds
- Systemd service support
- Lightweight Python implementation

---

## How it works / Как работает

The service monitors the primary server.

Сервис проверяет основной сервер:

Primary server
158.255.1.22
|
|
Health check
|
v
DNS record
vpn.example.com
|
|
Backup server
158.255.3.44


If the primary server becomes unavailable:

Если основной сервер недоступен:

vpn.example.com

158.255.1.22
|
v

158.255.3.44


The DNS record is automatically switched to the backup server.

---

# Installation / Установка

## Requirements

- Python 3.10+
- Linux server
- SSH access to monitored servers
- DNS provider API access


## Clone repository

git clone https://github.com/HaiKu723/vyache-failover.git

cd vyache-failover

Create virtual environment
python3 -m venv /opt/vyache-env

source /opt/vyache-env/bin/activate

Install dependencies:

pip install -r requirements.txt
Configuration / Настройка

Copy example configuration:

cp vyache-failover.conf.example /etc/vyache-failover.conf

Edit:

nano /etc/vyache-failover.conf

Example:

[regru]
username=your@email.com
password=api_password

[dns]
domain=vpn.example.com
record=vpn
zone=example.com

[servers]
primary=1.2.3.4
backup=5.6.7.8
port=39743

[settings]
interval=20
fail_count=3
recover_count=15
log=/var/log/vyache-failover.log
dry_run=true
SSH setup

Generate SSH key:

ssh-keygen -t ed25519 -f ~/.ssh/vyache_failover

Copy public key to monitored servers:

ssh-copy-id -i ~/.ssh/vyache_failover.pub root@SERVER_IP

Test:

ssh -i ~/.ssh/vyache_failover root@SERVER_IP
Run manually / Запуск вручную
python3 vyache_failover.py
Systemd service

Create service:

nano /etc/systemd/system/vyache-failover.service

Example:

[Unit]
Description=Vyache Failover
After=network.target

[Service]
WorkingDirectory=/opt/vyache-failover
ExecStart=/opt/vyache-env/bin/python /opt/vyache-failover/vyache_failover.py
Restart=always

[Install]
WantedBy=multi-user.target

Enable:

systemctl daemon-reload

systemctl enable vyache-failover

systemctl start vyache-failover

Check status:

systemctl status vyache-failover

Logs:

journalctl -u vyache-failover -f
Project structure
vyache-failover/
│
├── config.py
├── logger.py
├── ssh_checker.py
├── regru.py
├── healthcheck.py
├── vyache_failover.py
├── vyache-failover.conf.example
├── requirements.txt
└── README.md
Security

Important:

Never commit /etc/vyache-failover.conf
Never publish API passwords
Use SSH keys instead of passwords
Keep .gitignore enabled
License

MIT License

Author

HaiKu723

Vyache Failover
Automatic DNS failover and health monitoring tool.


---

After That:

git add README.md

git commit -m "Add documentation"

git push
