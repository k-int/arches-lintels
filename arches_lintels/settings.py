import os

APP_NAME = "arches_lintels"
VERSION = "1.0.0.a0"

ROOT_DIR = os.getcwd()
APP_ROOT = os.path.join(ROOT_DIR, APP_NAME)

SYS_SETTINGS_PATH = os.path.join(ROOT_DIR, "settings.json")    

# Postgresql settings
PG_USER = "postgres"
PG_ENCODING = "UTF8"
PG_PORT = "45432"

# Elasticsearch settings
ES_PORT = "49200"