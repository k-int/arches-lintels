from arches_lintels.controllers.dependencies.postgres import PostgresController


class ControlCentreController():
    """
    Controller for the stackedwidget control centre page.
    Rather than this class acting as the source of truth for all dependencies, it hands off
    to each of the dependency controllers to handle and spin up processes.
    """

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

        # dependencies
        self.postgres_controller = PostgresController(ui)

        self.ui.postgresInstallButton.clicked.connect(self.postgres_controller.initialise_postgres)
        self.ui.postgresRunButton.clicked.connect(self.postgres_controller.start_postgres)
        self.ui.postgresStopButton.clicked.connect(self.postgres_controller.stop_postgres)

