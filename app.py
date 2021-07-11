#Import stuff
from flask import Flask
import pytesseract as tess
from PIL import Image
import requests
from flask import Flask, request, jsonify
pytesseract.pytesseract.tesseract_cmd = './.apt/usr/bin/tesseract'


app = Flask(__name__)

@app.route("/img", methods=["POST"])
def process_image():
    file = request.files['image']

    #Read the image via file.stream
    img = Image.open(file.stream)
    text = tess.image_to_string(img)

    #Break down text into array & Extract drug from array
    for i in text.split():
        midresponse = requests.get("https://www.drugs.com/" + i)
        if midresponse.ok:
            Medizin = str(i)
        #else:
         #   return jsonify({'str': "ne"})

    #Dosage&Administration
            response = requests.get("https://api.fda.gov/drug/label.json?search=dosage_and_administration:" + Medizin)

    #Only show relevant information
    for data in (response.json()["results"]):
        DosageAndAdministration = data["dosage_and_administration"]
    return jsonify({'str': DosageAndAdministration})
        #else:
          #  return jsonify({'str': "No Drug detected"})

if __name__ == "__main__":
    app.run(debug=True)
