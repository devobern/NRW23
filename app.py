from flask import Flask, url_for
from flask_talisman import Talisman
import logging
from logging.handlers import RotatingFileHandler
from utils import load_data_into_app_context
from main_routes import main


def create_app(): 
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

    # Setup logging
    log_formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    log_handler = RotatingFileHandler("application.log", maxBytes=10000000, backupCount=5)  # Log rotation
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.INFO)

    app.logger.addHandler(log_handler)
    app.logger.setLevel(logging.INFO)

    with app.app_context():
            csp['script-src'].append(url_for('static', filename='main.js', _external=True))
            talisman.content_security_policy = csp
            load_data_into_app_context(app)

    # Register the blueprint
    app.register_blueprint(main)
            
    return app

app = create_app()