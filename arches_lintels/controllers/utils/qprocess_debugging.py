import logging
import re

logger = logging.getLogger(__name__)


def _formatting(message):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')
    message = ansi_escape.sub('', message)
    message = message.rstrip("\r\n")
    print(message)
    return message

def read_stderr(qprocess):
    logger.warning(_formatting(bytes(qprocess.readAllStandardError()).decode("utf-8")))


def read_stdout(qprocess):
    logger.debug(_formatting(bytes(qprocess.readAllStandardOutput()).decode("utf-8")))


def handle_process_error(error):
    logger.error(f"QProcess infrastructure error: {error}")


def qprocess_debugging(process):
    """
    Connection for qprocesses to log
    """

    process.readyReadStandardOutput.connect(lambda: read_stdout(process))
    process.readyReadStandardError.connect(lambda: read_stderr(process))
    process.errorOccurred.connect(handle_process_error)

    return process
