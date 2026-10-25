"""
Enterprise Structured Logging System.
"""

import logging
import sys
from typing import Optional


class EnterpriseFormatter(logging.Formatter):
    """
    Color-coded, structured log formatter suitable for both
    local development readability and cloud structured parsing.
    """

    GREY = "\x1b[38;20m"
    CYAN = "\x1b[36;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

    FORMAT_BASE = (
        "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
    )

    FORMATS = {
        logging.DEBUG: CYAN + FORMAT_BASE + RESET,
        logging.INFO: GREY + FORMAT_BASE + RESET,
        logging.WARNING: YELLOW + FORMAT_BASE + RESET,
        logging.ERROR: RED + FORMAT_BASE + RESET,
        logging.CRITICAL: BOLD_RED + FORMAT_BASE + RESET,
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno, self.FORMAT_BASE)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def setup_logging(log_level: str = "INFO", debug: bool = False) -> logging.Logger:
    """
    Initialize root and enterprise application loggers.
    """
    effective_level = logging.DEBUG if debug else getattr(logging, log_level.upper(), logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(effective_level)

    # Avoid duplicate handlers on reload
    if not root_logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(effective_level)
        console_handler.setFormatter(EnterpriseFormatter())
        root_logger.addHandler(console_handler)

    logger = logging.getLogger("app")
    logger.setLevel(effective_level)
    return logger


def log_startup_banner(
    app_name: str,
    app_version: str,
    environment: str,
    env_file_path: str,
    host: str,
    port: int,
    debug: bool,
    logger: Optional[logging.Logger] = None,
) -> None:
    """Prints a clear enterprise startup banner indicating the active environment."""
    log = logger or logging.getLogger("app")
    separator = "=" * 70
    banner = f"""
{separator}
  {app_name}
  Version      : {app_version}
  Environment  : [{environment.upper()}]
  Source File  : {env_file_path}
  Listening On : http://{host}:{port}
  Debug Mode   : {debug}
{separator}
"""
    log.info(banner)
