from arches_lintels.settings import (
    PG_PORT,
    PG_USER,
    PG_PASSWORD,
    ES_PORT,
    ES_USER,
    ES_PASSWORD,
)

def settings_local_template(project_name, data):

    return f"""
try:
    from {project_name}.settings import *
except ImportError:
    pass

ELASTICSEARCH_HTTP_PORT = {ES_PORT}
ELASTICSEARCH_HOSTS = [
    {{"scheme": "http", "host": "localhost", "port": ELASTICSEARCH_HTTP_PORT}}
]
ELASTICSEARCH_CONNECTION_OPTIONS = {{"timeout": 30, "verify_certs": False, "basic_auth": ({ES_USER}, {ES_PASSWORD})}}

DATABASES = {{
    "default": {{
        "ATOMIC_REQUESTS": False,
        "AUTOCOMMIT": True,
        "CONN_MAX_AGE": 0,
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "HOST": "localhost",
        "NAME": "arches_her_v76",
        "OPTIONS": {{}},
        "PASSWORD": {PG_PASSWORD},
        "PORT": {PG_PORT},
        "POSTGIS_TEMPLATE": "template_postgis",
        "TEST": {"CHARSET": None, "COLLATION": None, "MIRROR": None, "NAME": None},
        "TIME_ZONE": None,
        "USER": {PG_USER},
    }}
}}

MAPBOX_API_KEY = {data['mapbox_api_key']}

DEBUG = {data['debug']}

ACCESSIBILITY_MODE = {data['accessibility_mode']}

"""
