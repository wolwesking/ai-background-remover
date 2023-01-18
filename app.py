from flask import Flask, render_template, request
from fileinput import filename
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

#Funcntions

# Routes
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        
        # Allowed extenctions
        UPLOAD_FOLDER = './uploads'
        ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

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
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('Acknowledgement.html', name = filename)

# END
if __name__ =="__main__":
    app.run(debug = True)

