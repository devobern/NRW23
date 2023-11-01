from flask import Flask, render_template, request, jsonify, redirect, url_for
import zipfile
import json
import os
from flask_talisman import Talisman
import logging
from logging.handlers import RotatingFileHandler


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

# Setup logging
log_formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
log_handler = RotatingFileHandler("application.log", maxBytes=10000000, backupCount=5)  # Log rotation
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.INFO)

app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)


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
            not search_data['first_name'] or search_data['first_name'] in person['vorname'].lower(),
            not search_data['last_name'] or search_data['last_name'] in person['name'].lower(),
            not search_data['kanton'] or person['kanton_bezeichnung'].lower().find(search_data['kanton']) != -1,
            not search_data['liste'] or person['liste_bezeichnung'].lower().find(search_data['liste']) != -1,
            not search_data['wohnort'] or (person['wohnort'] and search_data['wohnort'] in person['wohnort'].lower())
        ])]
        
        if results: 
            return render_template('results.html', results=results)
        
        return "Person nicht gefunden", 404

    except Exception as e:
        # Log the error for debugging purposes but do not expose to user
        app.logger.error("An error occurred: %s", e)
        return "Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.", 500

    
@app.route('/search_name', methods=['POST'])
def search_name():
    name = request.form.get('name', '').lower().strip()
    
    try:
        data = get_data_from_zip()
        candidates = data['level_kantone']
        
        # Split the name by spaces to separate potential first and last names
        names = name.split()
        
        if len(names) == 1:
            # If only one name is provided, search both first and last names for partial matches
            results = [person for person in candidates if name in person['vorname'].lower() or name in person['name'].lower()]
        elif len(names) == 2:
            # If two names are provided, assume the first is the firstname and the second is the lastname
            first_name, last_name = names
            results = [person for person in candidates if first_name in person['vorname'].lower() and last_name in person['name'].lower()]
        else:
            # If more than two names are provided, return an empty result set
            results = []
        
        results.sort(key=lambda x: x['name'])

        return jsonify(results)

    except Exception as e:
        # Log the error for debugging purposes but do not expose to user
        app.logger.error("An error occurred: %s", e)
        return jsonify({"error": "Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut."}), 500


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
