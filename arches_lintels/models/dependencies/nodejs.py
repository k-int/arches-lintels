import os


class NodeModel:
    def __init__(self, settings_model):
        self.settings_model = settings_model

    @property
    def get_nodejs_path(self):
        return self.settings_model.get_config_value(["dependencies","nodejs","install_directory"])

    def get_node_exe_path(self):
        """
        NodeJS doesn't have a bin/ dir unlike psql or ES, so we just return the top level containing
        npm, npx, and node.exe.
        """
        return os.path.join(self.get_nodejs_path, "node.exe")

    def build_node_environment(self, qprocessenv):
        """
        Implements Node into a QProcessEnvironment
        """        
        # Get the existing path and append the lintels nodejs install path to it
        path = qprocessenv.value("PATH")
        new_path = f"{self.get_nodejs_path};{path}"
        qprocessenv.insert("PATH", new_path)
        return qprocessenv