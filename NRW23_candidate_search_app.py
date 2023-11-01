from flask import Flask, render_template, request, jsonify, redirect, url_for
import zipfile
import json
import os
from flask_talisman import Talisman

app = Flask(__name__)

# Security Headers
talisman = Talisman(app)

csp = {
    'default-src': '\'self\'',
    'script-src': '\'self\'',
    'script-src-elem': '\'self\'',
    'script-src-attr': '\'none\'',
    'style-src': '\'self\'',
    'style-src-elem': '\'self\'',
    'style-src-attr': '\'none\'',
    'img-src': [
        '\'self\'',
        'img.shields.io'
        ],
    'font-src': '\'self\'',
    'connect-src': '\'self\'',
    'media-src': '\'self\'',
    'object-src': '\'self\'',
    'prefetch-src': '\'self\'',
    'child-src': '\'self\'',
    'frame-src': '\'self\'',
    'worker-src': '\'self\'',
    'frame-ancestors': '\'self\'',
    'form-action': '\'self\''
}

# HTTP Strict Transport Security (HSTS) Header
hsts = {
    'max-age': 31536000,
    'includeSubDomains': True
}

talisman.content_security_policy = csp
talisman.strict_transport_security = hsts
talisman.referrer_policy = 'strict-origin-when-cross-origin'

talisman.feature_policy = {
    'geolocation': '\'none\'',
    'autoplay': ['\'self\''],
    'camera': '\'none\''
}

talisman.permissions_policy = {
    'geolocation': '\'none\'',
    'camera': '\'none\''
}

talisman.expect_ct = True


    # 'disown-opener' is not a standard CSP directive and isn't supported directly in Flask-Talisman, so it's omitted.
    # For 'sandbox', Flask-Talisman has a separate argument. You might handle it like this:
    # talisman = Talisman(app, content_security_policy=csp, session_cookie_secure=True, force_https_permanent=True, feature_policy="microphone 'none'; geolocation 'none';", sandbox_directives=['allow-forms', 'allow-scripts'])


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_FILE_PATH = os.path.join(BASE_DIR, 'files', 'NRW2023-kandidierende.zip')
JSON_FILENAME = "NRW2023-kandidierende.json"
SEARCH_FIELDS = ['first_name', 'last_name', 'kanton', 'liste', 'wohnort']

DATA_CACHE = None

def load_data_cache():
    global DATA_CACHE
    with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as z:
        with z.open(JSON_FILENAME) as f:
            DATA_CACHE = json.load(f)

load_data_cache()

def get_data_from_zip():
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

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')


if __name__ == '__main__':
    app.run()
