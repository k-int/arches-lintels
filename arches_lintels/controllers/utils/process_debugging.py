# Note, not currently implemented but should be logged for different logging levels
# e.g. error, debug, warning etc

# Usage in another controller e.g.
# self.es_process.readyReadStandardError.connect(lambda: read_stderr(self.es_process))
# self.es_process.readyReadStandardOutput.connect(lambda: read_stdout(self.es_process))
# self.es_process.errorOccurred.connect(handle_process_error)


def read_stderr(qprocess):
    error_message = bytes(qprocess.readAllStandardError()).decode()
    print(f"[Postgres STDERR]: {error_message}")

def read_stdout(qprocess):
    output_message = bytes(qprocess.readAllStandardOutput()).decode()
    print(f"[Postgres STDOUT]: {output_message}")

def handle_process_error(error):
    print(f"[QProcess Error Code]: {error}")        