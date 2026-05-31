import logging

logger = logging.getLogger(__name__)

def read_stderr(qprocess):
    logger.warning(
        bytes(qprocess.readAllStandardError()).decode()
    )

def read_stdout(qprocess):
    logger.debug(
        bytes(qprocess.readAllStandardOutput()).decode()
    )

def handle_process_error(error):
    logger.error(
        f"QProcess infrastructure error: {error}"
    )

def qprocess_debugging(process):
    """
    Connection for qprocesses to log
    """

    process.readyReadStandardOutput.connect(
        lambda: read_stdout(process)
    )
    process.readyReadStandardError.connect(
        lambda: read_stderr(process)
    )
    process.errorOccurred.connect(
        handle_process_error
    )

    return process