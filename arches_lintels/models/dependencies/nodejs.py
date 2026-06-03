import os


class NodeModel:
    def __init__(self, settings_model):
        self.settings_model = settings_model

    @property
    def get_nodejs_path(self):
        return self.settings_model.get_config_value(["dependencies","nodejs","install_directory"])

    @property
    def get_git_path(self):
        return self.settings_model.get_config_value(["dependencies","git","install_directory"])

    def _create_npm_cache(self):
        npm_cache_dir = os.path.join(self.get_nodejs_path, "npm-cache")
        if not os.path.exists(npm_cache_dir):
            os.makedirs(npm_cache_dir)
        return npm_cache_dir

    def get_node_exe_path(self):
        return os.path.join(self.get_nodejs_path, "node.exe")

    def get_git_exe_path(self):
        return os.path.join(self.get_git_path, "cmd", "git.exe")

    def build_node_environment(self, qprocessenv):
        """
        Implements Node & Git into a QProcessEnvironment.
        Returns the environment for attaching to a QProcess
        """        
        # Get the existing path and append the lintels nodejs install path to it
        path = qprocessenv.value("PATH")
        new_path = f"{self.get_nodejs_path};{path}"
        qprocessenv.insert("PATH", new_path)

        # Ensure node/npm doesn't log to or create files in AppData or user
        npm_cache_dir = self._create_npm_cache()
        qprocessenv.insert("npm_config_cache", npm_cache_dir)
        qprocessenv.insert("npm_config_prefix", self.get_nodejs_path)
        qprocessenv.insert("npm_config_globalconfig", os.path.join(self.get_nodejs_path, "npmrc"))
        qprocessenv.insert("npm_config_userconfig", os.path.join(self.get_nodejs_path, ".npmrc"))

        git_exe = self.get_git_exe_path()
        qprocessenv.insert("npm_config_git", git_exe)

        return qprocessenv