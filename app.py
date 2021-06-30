#Import stuff
from flask import Flask
import pytesseract as tess
from PIL import Image
import requests
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route("/", methods=["POST"])
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
       
    #Dosage&Administration
            response = requests.get("https://api.fda.gov/drug/label.json?search=dosage_and_administration:" + Medizin)

    #Only show relevant information
    for data in (response.json()["results"]):
        DosageAndAdministration = data["dosage_and_administration"]
    return jsonify({'str': DosageAndAdministration})
        

if __name__ == "__main__":
    app.run(debug=True)
