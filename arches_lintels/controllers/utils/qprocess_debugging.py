import logging

logger = logging.getLogger(__name__)


def _formatting(message):
    return message.rstrip("\r\n")

def read_stderr(qprocess):
    logger.warning(_formatting(bytes(qprocess.readAllStandardError()).decode()))


def read_stdout(qprocess):
    logger.debug(_formatting(bytes(qprocess.readAllStandardOutput()).decode()))


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
