import logging
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to log levels based on the class name."""

    COLORS = {
        'Translator': Fore.CYAN,
        'WebSearch': Fore.GREEN,
        'ReadingGenerator': Fore.YELLOW,
    }

    def format(self, record):
        log_fmt = f"{self.COLORS.get(record.name, Fore.WHITE)}%(levelname)s: %(message)s{Style.RESET_ALL}"
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)