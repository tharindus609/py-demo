import logging

from py_logger import logger
from cmd_executor import shell_cmd_executor

logger.load_json_configs()  # Load logging configs

_log = logging.getLogger(__name__)  # any logging.getLogger() calls should come after loading the configs.
_log.info("Initial info msg")

_log_2 = logging.getLogger(__name__)
_log_2.info("info after new logger instantiated")
_log_2.debug("this is a debug msg")

print(shell_cmd_executor.execute("ls -l"))
