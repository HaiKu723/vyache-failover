from ssh_checker import SSHChecker

checker = SSHChecker("158.255.3.58")

status = checker.status()

print(status)

print(checker.is_healthy())

