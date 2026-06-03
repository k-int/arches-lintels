from PyQt6.QtCore import QProcessEnvironment



def node_environment(node_model):
    """
    This function calls the Node Model and inserts the Lintels node
    installation into PATH.
    """

    qprocessenv = QProcessEnvironment.systemEnvironment()
    qprocessenv = node_model.build_node_environment(qprocessenv)

    return qprocessenv
