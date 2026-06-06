import os

APP_NAME = "arches_lintels"
VERSION = "1.0.0.a0"

ROOT_DIR = os.getcwd()
APP_ROOT = os.path.join(ROOT_DIR, APP_NAME)

SYS_SETTINGS_PATH = os.path.join(ROOT_DIR, "settings.json")    

# Postgresql settings
PG_USER = "postgres"
PG_PASSWORD = "postgis"
PG_ENCODING = "UTF8"
PG_PORT = "45432"

# Elasticsearch settings
ES_USER = "elastic"
ES_PASSWORD = "Arch35L1nt3l5"
ES_PORT = 49200

ARCHES_VERSIONS = [
    "7.5",
    "7.6",
    "8.0",
    "8.1",
]

ARCHES_APPS = [
    "arches_her",
    "arches_for_science",
    "arches_controlled_lists",
    "arches_lingo",
    "arches_component_lab",
    "arches_querysets"
]

# Available ontologies to add to projects
ONTOLOGIES_PATH = os.path.join(APP_ROOT, "arches", "ontologies")

ONTOLOGIES = {
    "CIDOC CRM": os.path.join(ONTOLOGIES_PATH, "cidoc_crm"),
    "LinkedArt": os.path.join(ONTOLOGIES_PATH, "linkedart")
}