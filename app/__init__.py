import json
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

with open("config.json", encoding="utf-8") as config_json:
    config = json.load(config_json)
    db_path = config["db_path"]
