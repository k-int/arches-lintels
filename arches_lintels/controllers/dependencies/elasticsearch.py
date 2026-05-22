from PyQt6.QtCore import QProcess, QTimer

from arches_lintels.models.dependencies.elasticsearch import ElasticsearchModel
from arches_lintels.controllers.utils.process_debugging import read_stderr, read_stdout, handle_process_error
from arches_lintels.controllers.utils.update_widget_styling import update_widget_styling


class ElasticsearchController():
    """
    Controller for the elasticsearch processes.
    """

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

        self.elasticsearch_model = ElasticsearchModel()

        self.es_timer = QTimer()
        self.es_timer.timeout.connect(self.elasticsearch_health)
        self.es_timer_count = 0

    def start_elasticsearch(self):
        primary_cmd, args, es_path = self.elasticsearch_model.start_elasticsearch()

        self.es_process = QProcess()
        self.es_process.setWorkingDirectory(es_path)
        self.es_process.stateChanged.connect(self.es_state_change)
        
        # self.es_process.readyReadStandardError.connect(lambda: read_stderr(self.es_process))
        # self.es_process.readyReadStandardOutput.connect(lambda: read_stdout(self.es_process))
        # self.es_process.errorOccurred.connect(handle_process_error)

        self.es_process.start(primary_cmd, args)

    def stop_elasticsearch(self):
        if self.es_process:
            pid = self.es_process.processId()
            command, args = self.elasticsearch_model.stop_elasticsearch(pid)
            self.stop_es_process = QProcess()
            self.stop_es_process.start(command, args)
            self.stop_es_process.waitForFinished(3000)
            # Now we can kill both processes
            self.stop_es_process.kill()
            self.es_process.kill()


    def es_state_change(self, new_state):
        if new_state == QProcess.ProcessState.Starting:
            print("Elasticsearch is waking up... (Yellow Light)")

        elif new_state == QProcess.ProcessState.Running:
            print("Elasticsearch cluster is alive! (Green Light)")
            self.es_timer.start(5000)  # Check every 5 seconds

        elif new_state == QProcess.ProcessState.NotRunning:
            print("Elasticsearch has exited. (Red Light)")
            self.es_timer.stop()

    def elasticsearch_health(self):
        result, self.es_timer_count = self.elasticsearch_model.elasticsearch_health(self.es_timer_count)
        if result in [False, True]:
            if result == False:
                self.stop_elasticsearch()
            self.es_timer.stop()
            self.es_timer_count = 0
