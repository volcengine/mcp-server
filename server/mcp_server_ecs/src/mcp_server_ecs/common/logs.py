import logging
import os
from typing import TypeVar

from concurrent_log_handler import ConcurrentRotatingFileHandler

from mcp_server_ecs.common.config import log_config

_WRITE_MODE = "a"
T = TypeVar("T")

LOG = logging.getLogger(__name__)
LOG.propagate = False

try:
    LOG.setLevel(getattr(logging, log_config["level"].upper(), logging.INFO))
    log_dir = os.path.dirname(log_config["file"])
    os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s %(filename)s line:%(lineno)d %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    rotate_handler = ConcurrentRotatingFileHandler(
        log_config["file"],
        _WRITE_MODE,
        log_config["max_size"],
        log_config["backup_count"],
    )
    rotate_handler.setLevel(logging.INFO)
    rotate_handler.setFormatter(formatter)
    LOG.addHandler(rotate_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    LOG.addHandler(console_handler)

except Exception as e:
    print(f"Log initialize failed: {str(e)}")
