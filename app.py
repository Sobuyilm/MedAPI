from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import requests
pytesseract.pytesseract.tesseract_cmd = './.apt/usr/bin/tesseract'

app = Flask(__name__)
text = "b"
@app.route("/imgt", methods=["POST", "GET"])
def process_image():
    global text
    if request.method == 'POST':
        file = request.files['image']
        img = Image.open(file.stream)
        text = pytesseract.image_to_string(img, lang='eng')

        for i in text.split():
            midresponse = requests.get("https://www.drugs.com/" + i)
            if midresponse.ok:
                Medizin = str(i)
                response = requests.get("https://api.fda.gov/drug/label.json?search=dosage_and_administration:" + Medizin)

        for data in (response.json()["results"]):
            DosageAndAdministration = data["dosage_and_administration"]
            return jsonify(DosageAndAdministration)

        

@app.route('/')
def index():
    global text
    return text
    
    
    


if __name__ == "__main__":
    app.run(debug=True)
