# core/logging_config.py
import logging
import sys


def setup_logging(
    level: str = "INFO",
) -> None:
    """
    Global logging configuration for router, workers, services.
    Call this ONCE at application startup.
    """

    log_level = getattr(logging, level.upper(), logging.INFO)

    root = logging.getLogger()
    root.setLevel(log_level)

    # Clear existing handlers (important for reloads / Celery)
    root.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.setFormatter(formatter)

    root.addHandler(handler)

    # Reduce noise from libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("stomp").setLevel(logging.WARNING)
    logging.getLogger("celery").setLevel(logging.INFO)

    root.info("Logging initialized (level=%s)", level)
