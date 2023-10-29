# NRW23 Candidate Search App

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python Version](https://img.shields.io/badge/python-3.11.4-blue.svg)

## Table of Contents
- [Introduction](#introduction)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
  - [Local Deployment](#local-deployment)
  - [Online Access](#online-access)
- [Disclaimer](#disclaimer)
- [License](#license)
- [Contact](#contact)

## Introduction
This repository contains a Flask application designed for users to search for candidates who participated in the 2023 Nationalrat elections. It primarily showcases detailed information about a candidate, emphasizing the number of votes they received.

## Repository Structure
```
NRW23/
│
├── env/                       # Virtual environment directory
│
├── files/
│   └── NRW2023-kandidierende.zip  # Data containing candidate information
│
├── static/
│   └── styles.css            # CSS file for the web application styling
│
├── templates/
│   ├── index.html            # Main page template for search feature
│   └── result.html           # Results page displaying candidate details
│
├── .gitignore                # Patterns of files/directories to ignore in git
│
├── NRW23_candidate_search_app.py  # Main Flask app script
│
└── requirements.txt          # List of required Python packages for the app
```

## Getting Started

### Local Deployment

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/devobern/NRW23/tree/main]
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
   python NRW23_candidate_search_app.py
   ```

6. **Access Locally**  
   The application will be accessible at `http://127.0.0.1:5000/`.

### Online Access
Access the hosted application [here](https://devobern.pythonanywhere.com/).

## Disclaimer
This application was developed within 2 hours with assistance from OpenAI's GPT-4. Consequently, there might be occasional issues or aspects that need refinement. The primary motivation for this tool's development was the lack of a simple platform to view the votes received by individual candidates. Feedback and suggestions are always welcome.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Dataset Information

The data used in this repository is sourced from the **Bundesamt für Statistik BFS** and relates to the Nationalratswahlen 2023. 

- **Dataset Name**: NR - Kandidierende
- **Publication Date**: 8. August 2023
- **Format**: JSON
- **Access URL**: [Link to Dataset](https://ogd-stadtveinofp-app.ch/v4/ogd-sc/1-7-02-NRW2023-kandidierende.json)

### License for Dataset

The dataset is available under the "Freie Nutzung. Quellenangabe ist Pflicht" terms. Users can use this dataset for both non-commercial and commercial purposes, but proper attribution is required.

**Attribution**:  
Autor:in: Bundesamt für Statistik BFS  
Titel: NR - Kandidierende  
[Link zum Datensatz](https://opendata.swiss/de/dataset/eidg-wahlen-2023/resource/1cd03e48-bb87-4d89-825b-84ccd32a0b83)

## Contact
For inquiries or suggestions, please reach out via [email](mailto:nationalratswahlen23_app.px0na@passmail.net).