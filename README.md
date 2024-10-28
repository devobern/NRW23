# NRW23 Candidate Search App
> ⚠️ **Notice:** The website previously linked here is no longer available as it is not relevant anymore. Please disregard any references to it.

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python Version](https://img.shields.io/badge/python-3.11.4-blue.svg)

## Table of Contents
- [NRW23 Candidate Search App](#nrw23-candidate-search-app)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Repository Structure](#repository-structure)
  - [Getting Started](#getting-started)
    - [Local Deployment](#local-deployment)
    - [Online Access](#online-access)
  - [Disclaimer](#disclaimer)
  - [License](#license)
  - [Dataset Information](#dataset-information)
    - [License for Dataset](#license-for-dataset)
  - [Contact](#contact)

## Introduction
This repository contains a Flask application designed for users to search for candidates who participated in the 2023 Nationalrat elections (Switzerland). It primarily showcases detailed information about a candidate, emphasizing the number of votes they received.

## Repository Structure
```
NRW23/
│
├── files/
│   └── NRW2023-kandidierende.zip  # Data containing candidate information
│
├── static/
│   ├── JS/
│   │   └── script.js             # JavaScript file for interactive features
│   │
│   └── styles.css                # CSS file for the web application styling
│
├── templates/
│   ├── detail.html               # Detail page template for a specific candidate
│   ├── index.html                # Main page template for search feature
│   ├── privacy-policy.html       # Privacy policy template
│   └── results.html              # Results page displaying candidates
│
├── .gitignore                    # Patterns of files/directories to ignore in git
│
├── app.py                        # Main Flask app script
│
├── LICENSE                       # License file
│
├── main_routes.py                # Routes for the Flask app
│
├── README.md                     # README documentation
│
├── requirements.txt              # List of required Python packages for the app
│
└── utils.py                      # Utility functions for the app
```

## Getting Started

### Local Deployment

1. **Clone the Repository**
   ```bash
   git clone https://github.com/devobern/NRW23/tree/main
   ```

2. **Navigate to Directory**
   ```bash
   cd NRW23
   ```

3. **Create & Activate Virtual Environment**  
   Ensure you have `python3` and `virtualenv` installed. 
   ```bash
   virtualenv env
   source env/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the App**
   ```bash
   python run.py
   ```

6. **Access Locally**  
   The application will be accessible at http://127.0.0.1:5000/.

   Note: Due to the Content Security Policy (CSP), the app cannot be run locally without dev certificates. To address this, you can use mkcert to generate your own certificate. For a guide on how to use mkcert, please refer to this [tutorial](https://web.dev/articles/how-to-use-local-https).

### Online Access
Access the hosted application [here](https://devobern.pythonanywhere.com/).

## Disclaimer
This application is an ongoing project and serves as a bit of a playground for me. It was developed with the primary motivation to provide a simple platform to view the votes received by individual candidates. There might be occasional issues or aspects that need refinement. Feedback and suggestions are always welcome.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Dataset Information

The data used in this repository is sourced from the **Bundesamt für Statistik BFS** and relates to the Nationalratswahlen 2023. 

- **Dataset Name**: NR - Kandidierende
- **Publication Date**: 8. August 2023
- **Format**: JSON
- **Access URL**: [Link to Dataset](https://opendata.swiss/de/dataset/eidg-wahlen-2023/resource/1cd03e48-bb87-4d89-825b-84ccd32a0b83)

### License for Dataset

The dataset is available under the "Freie Nutzung. Quellenangabe ist Pflicht" terms. Users can use this dataset for both non-commercial and commercial purposes, but proper attribution is required.

**Attribution**:  
Autor:in: Bundesamt für Statistik BFS  
Titel: NR - Kandidierende  
[Link zum Datensatz](https://opendata.swiss/de/dataset/eidg-wahlen-2023/resource/1cd03e48-bb87-4d89-825b-84ccd32a0b83)

## Contact
For inquiries or suggestions, please reach out via [email](mailto:nationalratswahlen23_app.px0na@passmail.net).