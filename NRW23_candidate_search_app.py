from flask import Flask, render_template, request, jsonify, redirect, url_for
import zipfile
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_FILE_PATH = os.path.join(BASE_DIR, 'files', 'NRW2023-kandidierende.zip')
JSON_FILENAME = "NRW2023-kandidierende.json"
SEARCH_FIELDS = ['first_name', 'last_name', 'kanton', 'liste', 'wohnort']

DATA_CACHE = None

def get_data_from_zip():
    global DATA_CACHE
    if not DATA_CACHE:
        with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as z:
            with z.open(JSON_FILENAME) as f:
                DATA_CACHE = json.load(f)
    return DATA_CACHE

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_data = {field: request.form.get(field, '').lower().strip() for field in SEARCH_FIELDS}
    
    try:
        data = get_data_from_zip()
        candidates = data['level_kantone']
        
        results = [person for person in candidates if all([
            not search_data['first_name'] or person['vorname'].lower() == search_data['first_name'],
            not search_data['last_name'] or person['name'].lower() == search_data['last_name'],
            not search_data['kanton'] or person['kanton_bezeichnung'].lower().find(search_data['kanton']) != -1,
            not search_data['liste'] or person['liste_bezeichnung'].lower().find(search_data['liste']) != -1,
            not search_data['wohnort'] or (person['wohnort'] and person['wohnort'].lower() == search_data['wohnort'])
        ])]
        
        if results: 
            return render_template('results.html', results=results)
        
        return "Person nicht gefunden", 404

    except Exception as e:
        # Log the error for debugging purposes but do not expose to user
        print(e)
        return "Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.", 500
    
@app.route('/detail/<kanton_nummer>/<liste_nummer_kanton>/<kandidat_nummer>')
def detail(kanton_nummer, liste_nummer_kanton, kandidat_nummer):
    
    data = get_data_from_zip()
    candidates = data['level_kantone']

    person_detail = next((person for person in candidates if 
                      str(person['kanton_nummer']) == str(kanton_nummer) and 
                      str(person['liste_nummer_kanton']) == str(liste_nummer_kanton) and 
                      str(person['kandidat_nummer']) == str(kandidat_nummer)), None)
    
    if person_detail:
        return render_template('detail.html', person=person_detail)
    
    return "Person nicht gefunden", 404

if __name__ == '__main__':
    app.run()
