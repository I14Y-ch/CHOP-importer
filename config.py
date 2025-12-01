import os

TEMPLATES_DIR = "templates"  # folder containing de.md, en.md, fr.md, it.md
CHOP_API_BASE_URL = "https://mct-be-bfs-itplatformnet-p.apps.p-szb-ros-shrd-prd-01.cloud.admin.ch/api/Iop"

I14Y_API_BASE_URL = os.environ["I14Y_API_BASE_URL"]

GET_TOKEN_URL = os.environ["GET_TOKEN_URL"]
CLIENT_KEY = os.environ["CLIENT_KEY"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

CHOP_YEAR = os.environ["CHOP_YEAR"]
CHOP_REVISION = os.environ["CHOP_REVISION"]

RESPONSIBLE_DEPUTY_JSON = os.environ.get("RESPONSIBLE_DEPUTY_JSON")
RESPONSIBLE_PERSON_JSON = os.environ.get("RESPONSIBLE_PERSON_JSON")