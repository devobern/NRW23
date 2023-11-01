from flask import Blueprint, render_template, jsonify, request
from flask import current_app

# Constants
SEARCH_FIELDS = ['first_name', 'last_name', 'kanton', 'liste', 'wohnort']

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/search', methods=['POST'])
def search():
    search_data = {field: request.form.get(field, '').lower().strip() for field in SEARCH_FIELDS}
    
    try:
        data = current_app.config.get("DATA_CACHE", {})
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
        main.logger.error("An error occurred: %s", e)
        return jsonify({"error": "Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut."}), 500
    
@main.route('/search_name', methods=['POST'])
def search_name():
    name = request.form.get('name', '').lower().strip()
    
    try:
        data = current_app.config.get("DATA_CACHE", {})
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
        main.logger.error("An error occurred: %s", e)
        return jsonify({"error": "Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut."}), 500


@main.route('/detail/<kanton_nummer>/<liste_nummer_kanton>/<kandidat_nummer>')
def detail(kanton_nummer, liste_nummer_kanton, kandidat_nummer):
    
    data = current_app.config.get("DATA_CACHE", {})
    candidates = data['level_kantone']

    person_detail = next((person for person in candidates if 
                      str(person['kanton_nummer']) == str(kanton_nummer) and 
                      str(person['liste_nummer_kanton']) == str(liste_nummer_kanton) and 
                      str(person['kandidat_nummer']) == str(kandidat_nummer)), None)
    
    if person_detail:
        return render_template('detail.html', person=person_detail)
    
    return "Person nicht gefunden", 404

@main.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')