import zipfile
import json
import os

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_FILE_PATH = os.path.join(BASE_DIR, 'files', 'NRW2023-kandidierende.zip')
JSON_FILENAME = "NRW2023-kandidierende.json"

def load_data_into_app_context(app):
    with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as z:
        with z.open(JSON_FILENAME) as f:
            data = json.load(f)
    app.config["DATA_CACHE"] = data

def get_data_from_app_context(app):
    return app.config.get("DATA_CACHE", {})
