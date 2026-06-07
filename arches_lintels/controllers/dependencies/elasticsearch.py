import logging

from PyQt6.QtCore import QProcess, QTimer

from arches_lintels.models.dependencies.elasticsearch import ElasticsearchModel
from arches_lintels.controllers.utils.qprocess_debugging import qprocess_debugging
from arches_lintels.controllers.dependencies.dep_ui_updates import DependencyUIUpdates

logger = logging.getLogger(__name__)

class ElasticsearchController():
    """
    Controller for the elasticsearch processes.
    """

    def __init__(self, ui, settings_model):
        super().__init__()
        self.ui = ui

        self.dep_ui_updates = DependencyUIUpdates(
            install_label=self.ui.elasticInstalledLabel, 
            install_button = self.ui.elasticInstallButton, 
            start_button = self.ui.elasticStartButton, 
            stop_button = self.ui.elasticStopButton,
            running_label = self.ui.elasticRunningLabel
        )

        self.elasticsearch_model = ElasticsearchModel(settings_model)

        self.es_timer = QTimer()
        self.es_timer.timeout.connect(self.elasticsearch_health)
        self.es_timer_count = 0

        # Currently ES needs no installation, thus setting to installed by default, 
        # however this should change if we provide a custom config file for it to use
        self.dep_ui_updates.default_installed()

    def start_elasticsearch(self):
        primary_cmd, args, es_path = self.elasticsearch_model.start_elasticsearch()

        self.es_process = QProcess()
        self.es_process.setWorkingDirectory(es_path)
        self.es_process.stateChanged.connect(self.es_state_change)
        
        qprocess_debugging(self.es_process)
        self.es_process.start(primary_cmd, args)

    def stop_elasticsearch(self):
        if self.es_process:
            self.dep_ui_updates.default_stopping()
            print("STOPPING")
            pid = self.es_process.processId()
            command, args = self.elasticsearch_model.stop_elasticsearch(pid)
            self.stop_es_process = QProcess()
            qprocess_debugging(self.stop_es_process)
            self.stop_es_process.start(command, args)
            self.stop_es_process.waitForFinished(3000)
            # Now we can kill both processes
            self.stop_es_process.kill()
            self.es_process.kill()


    def es_state_change(self, new_state):
        if new_state == QProcess.ProcessState.Starting:
            print("Elasticsearch QProcess is starting")

        elif new_state == QProcess.ProcessState.Running:
            print("Elasticsearch QProcess is running")
            # Though QProcess is running, this doesn't mean ES is running
            self.dep_ui_updates.default_starting()
            # Start timer which connects to ES health check
            self.es_timer.start(5000)  # Check every 5 seconds

        elif new_state == QProcess.ProcessState.NotRunning:
            print("Elasticsearch has exited")
            self.es_timer.stop()
            self.es_timer_count = 0
            self.dep_ui_updates.default_not_running()

    def elasticsearch_health(self):
        result, self.es_timer_count = self.elasticsearch_model.elasticsearch_health(self.es_timer_count)
        if result in [False, True]:
            if result == False:
                self.stop_elasticsearch()
            if result == True:
                self.dep_ui_updates.default_running()
            self.es_timer.stop()
            self.es_timer_count = 0
