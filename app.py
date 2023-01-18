# Backend imports
from flask import Flask, render_template, request, url_for # BSD-3-Clause license, open-source: https://github.com/pallets/flask
import time # default libary

# Progress imports
from rembg import remove # MIT, open-source: https://github.com/danielgatis/rembg
from PIL import Image # Python Software Foundation License, open-source: https://github.com/python-pillow/Pillow

# Global variables
app = Flask(__name__)

# Funcntions
def removeBG(file):
    input = Image.open(file)
    output = remove(input)
    newFilename = f"static/outputs/{str(int(time.time()))}.png"
    output.save(newFilename)
    return newFilename

# def clearUpFiles(fileName):
#     return #none

# ----- Routes -----
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        
        # Allowed extenctions
        UPLOAD_FOLDER = './outputs'
        ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg']

        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        # Check if file exits
        if 'file' not in request.files:
            return render_template('Acknowledgement.html', name = 'no file')
        
        file = request.files['file']
        
        # Empty filename
        if file.filename == '':
            return render_template('Acknowledgement.html', name = 'no file name')

        # If file is secure
        # TODO Allowed file and allowed_file(file.filename)
        if file:
            filePath = removeBG(file)
            return render_template('Acknowledgement.html', name = filePath)

# END
if __name__ =="__main__":
    app.run(debug = True)

