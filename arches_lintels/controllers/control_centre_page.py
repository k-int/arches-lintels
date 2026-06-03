from arches_lintels.controllers.dependencies.postgres import PostgresController
from arches_lintels.controllers.dependencies.elasticsearch import ElasticsearchController


class ControlCentreController():
    """
    Controller for the stackedwidget control centre page.
    Rather than this class acting as the source of truth for all dependencies, it hands off
    to each of the dependency controllers to handle and spin up processes.
    """

    def __init__(self, ui, settings_model):
        super().__init__()
        self.ui = ui

        # dependencies
        self.postgres_controller = PostgresController(ui, settings_model)
        self.elasticsearch_controller = ElasticsearchController(ui, settings_model)

        self.ui.postgresInstallButton.clicked.connect(self.postgres_controller.initialise_postgres)
        self.ui.postgresRunButton.clicked.connect(self.postgres_controller.start_postgres)
        self.ui.postgresStopButton.clicked.connect(self.postgres_controller.stop_postgres)

        self.ui.elasticStartButton.clicked.connect(self.elasticsearch_controller.start_elasticsearch)
        self.ui.elasticStopButton.clicked.connect(self.elasticsearch_controller.stop_elasticsearch)