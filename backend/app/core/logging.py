import logging
import sys

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
LOG_NAMESPACES = ("crawler", "ai_agent", "api")


def setup_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )

    for namespace in LOG_NAMESPACES:
        logging.getLogger(namespace).setLevel(level)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
