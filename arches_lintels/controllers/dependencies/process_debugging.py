# Note, not currently implemented but should be logged for different logging levels
# e.g. error, debug, warning etc

def read_stderr(qprocess):
    error_message = bytes(qprocess.readAllStandardError()).decode()
    print(f"[Postgres STDERR]: {error_message}")

def read_stdout(qprocess):
    output_message = bytes(qprocess.readAllStandardOutput()).decode()
    print(f"[Postgres STDOUT]: {output_message}")

def handle_process_error(error):
    print(f"[QProcess Error Code]: {error}")        