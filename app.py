from flask import Flask, render_template, request, jsonify
import os
# import json

app = Flask(__name__)

wz08_codes = [
    {"WZ08": 2573, "Beschreibung": "Herstellung von Werkzeugen", "Abschnitt": "C"},
    {"WZ08": 25732, "Beschreibung": "Herstellung von Sägen und von Maschinenwerkzeugen für die Holzbearbeitung",
     "Abschnitt": "C"},
    {"WZ08": 261, "Beschreibung": "Herstellung von elektronischen Bauelementen und Leiterplatten", "Abschnitt": "C"},
    {"WZ08": 266,
     "Beschreibung": "Herstellung von Bestrahlungs- und Elektrotherapiegeräten und elektromedizinischen Geräten",
     "Abschnitt": "C"},
    {"WZ08": 273, "Beschreibung": "Herstellung von Kabeln und elektrischem Installationsmaterial", "Abschnitt": "C"},
    {"WZ08": 274, "Beschreibung": "Herstellung von elektrischen Lampen und Leuchten", "Abschnitt": "C"}
]

# pdf_dir = r'D:\\Anmeldungen\\Work'  # Path to directory containing PDF files


@app.route('/')
def default_dialog():
    return "Welcome to WZ08!"


@app.route('/readinessProbe')
def readiness_probe():
    if os.environ.get('READINESS') == "1":
        resp = jsonify({'message': 'Application in NOT ready.'})
        resp.status_code = 400
        return resp
    resp = jsonify({'message': 'Application is ready.'})
    resp.status_code = 200
    return resp


@app.route('/livenessProbe')
def liveness_probe():
    if os.environ.get('LIVENESS') == "1":
        resp = jsonify({'message': 'I am NOT alive!'})
        resp.status_code = 400
        return resp
    resp = jsonify({'message': 'I am alive!'})
    resp.status_code = 200
    return resp


@app.route('/startupProbe')
def startup_probe():
    if os.environ.get('STARTUP') == "1":
        resp = jsonify({'message': 'Application is NOT starting!'})
        resp.status_code = 400
        return resp
    resp = jsonify({'message': 'Application is starting'})
    resp.status_code = 200
    return resp


@app.route('/upload')
def upload_file_dialog():
    return render_template('upload.html')


@app.route('/uploadPdfFile', methods=['POST'])
def upload_pdf_file():
    if 'uploadFile' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    files = request.files.getlist('uploadFile')
    file = files[0]  # we assume only a single file
    file.save(file.filename)
    # >>> run OCR code here <<<
    resp = jsonify({'gegenstand': 'Online Marketing, IT-Unternehmensberatung, Websiteerstellung, Websiteoptimierung, Domainrecherche -verwaltung und -registrierung, Suchmaschinenoptimierung, Onpage-und Offpageoptimierung, Schwachstellen-& Rankinganalysen, Google AdwordsAnzeigenwerbung, lokales Google-Marketing (Google Places, Google Maps, Google Street view, Google Hotpot, Google Analytics), E-Mailmarketing, Contenterstellungund -optimierung, SEO Landingpageerstellungund -optimierung, Webdesign, Webhosting, Vertriebsorganisation im Online Marketing, Erstellung und Optimierung von Onlineshops, Vertrieb von Waren und Dienstleistungen aller Art über Internet auf Provisionsbasis, persönliche Betreuung und Beratung von Neu-und Bestandskunden, Vermittlung und Weiterverkauf (Reselling) von Computersoftware für o. g. Zwecke, Beratung zu Marketing in sozialen Netzwerken wie Xing, Twitter, Facebook, Google+ o. ä., Vermittlung von o. g. Dienstleistungen'})
    resp.status_code = 201
    return resp


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        return 'file uploaded successfully'


@app.route('/wz08', methods=['GET'])
def call_wz08():
    return jsonify(wz08_codes)


@app.route('/wz08/<wz_code>', methods=['GET'])
def call_zw08_by_id(wz_code=None):
    for code in wz08_codes:
        if wz_code == str(code["WZ08"]):
            # return code["Beschreibung"]
            return jsonify(code)
    return jsonify({"500": "unknown"})


@app.route('/args', methods=['GET'])
def call_args():
    args = request.args
    return args


if __name__ == '__main__':
    port = os.environ.get('FLASK_PORT') or 8080
    port = int(port)

    app.run(port=port, host='0.0.0.0')
