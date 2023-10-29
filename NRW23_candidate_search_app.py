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
    first_name = request.form.get('first_name').lower() if request.form.get('first_name') else ""
    last_name = request.form.get('last_name').lower() if request.form.get('last_name') else ""
    kanton = request.form.get('kanton').lower() if request.form.get('kanton') else ""
    liste = request.form.get('liste').lower() if request.form.get('liste') else ""
    wohnort = request.form.get('wohnort').lower() if request.form.get('wohnort') else ""

    try:
        data = get_data_from_zip()
        candidates = data['level_kantone']
        
        results = []

        for person in candidates:
            if (not first_name or person['vorname'].lower() == first_name) and \
            (not last_name or person['name'].lower() == last_name) and \
            (not kanton or person['kanton_bezeichnung'].lower().find(kanton) != -1) and \
            (not liste or person['liste_bezeichnung'].lower().find(liste) != -1) and \
            (not wohnort or (person['wohnort'] and person['wohnort'].lower() == wohnort)):
                results.append(person)

        
        if results: 
            return render_template('results.html', results=results)
        
        return "Person nicht gefunden", 404

    except Exception as e:
        tb = traceback.format_exc()
        return f"Fehler: {e}\n\nTraceback:\n{tb}", 500
    
@app.route('/detail/<string:combined_id>')
def detail(combined_id):
    # Splitting the combined_id to get the individual components
    kanton_nummer, liste_nummer_kanton, kandidat_nummer = combined_id.split('_')
    
    # Convert them to appropriate data types
    kanton_nummer = int(kanton_nummer)
    liste_nummer_kanton = int(liste_nummer_kanton)
    kandidat_nummer = int(kandidat_nummer)
    
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
    app.run(debug=True)
