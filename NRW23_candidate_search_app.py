from flask import Flask, render_template, request, jsonify, redirect, url_for
import zipfile
import json
import traceback
import os

app = Flask(__name__)

# Adjusted path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_FILE_PATH = os.path.join(BASE_DIR, 'files', 'NRW2023-kandidierende.zip')

JSON_FILENAME = "NRW2023-kandidierende.json"

def get_data_from_zip():
    with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as z:
        with z.open(JSON_FILENAME) as f:
            return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    first_name = request.form.get('first_name').lower()
    last_name = request.form.get('last_name').lower()

    try:
        data = get_data_from_zip()
        candidates = data['level_kantone']

        for person in candidates:
            if person['vorname'].lower() == first_name and person['name'].lower() == last_name:
                return render_template('result.html', person=person)

        return "Person nicht gefunden", 404

    except Exception as e:
        tb = traceback.format_exc()
        return f"Fehler: {e}\n\nTraceback:\n{tb}", 500

if __name__ == '__main__':
    app.run(debug=True)
