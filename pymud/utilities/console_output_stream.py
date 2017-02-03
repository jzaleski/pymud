import sys


class ConsoleOutputStream:
    def write(self, message):
        sys.stdout.write(message)
        sys.stdout.flush()
