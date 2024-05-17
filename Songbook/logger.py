from loguru import logger as log
import sys
__all__ = ["log"]
log.remove()
log.add(sys.stderr, level="INFO")