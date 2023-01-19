# Backend imports
from flask import Flask, render_template, request, url_for, jsonify, make_response # BSD-3-Clause license, open-source: https://github.com/pallets/flask
import time # default libary
import atexit # default libary
import os # default libary
import functools


# Progress imports
from rembg import remove # MIT, open-source: https://github.com/danielgatis/rembg
from PIL import Image, ImageColor# Python Software Foundation License, open-source: https://github.com/python-pillow/Pillow

# Global variables
app = Flask(__name__)

# Funcntions
def clearUp(path):
    os.remove(path)
    
def changeBackground(file, type, background):
    if type == "png":
        image = Image.open(file)
        bgImage = Image.open(background)
        image = image.convert('RGBA')
        bgImage = bgImage.convert('RGBA')

        image = remove(image)
        bgImage = bgImage.resize(image.size)
        bgImage = Image.alpha_composite(bgImage, image)

        # saving the file and convert
        bg = bgImage.convert('RGBA')
        newFilename = f"static/outputs/{str(int(time.time()))}.png"
        bgImage.save(newFilename)
        return newFilename
        
    elif type == "jpeg":
        image = Image.open(file)
        bgImage = Image.open(background)
        image = image.convert('RGBA')
        bgImage = bgImage.convert('RGBA')

        image = remove(image)
        bgImage = bgImage.resize(image.size)
        bgImage = Image.alpha_composite(bgImage, image)

        # saving the file and convert
        bgImage = bgImage.convert('RGB')
        newFilename = f"static/outputs/{str(int(time.time()))}.jpeg"
        bgImage.save(newFilename)
        return newFilename

    elif type == "jpg":
        image = Image.open(file)
        bgImage = Image.open(background)
        image = image.convert('RGBA')
        bgImage = bgImage.convert('RGBA')

        image = remove(image)
        bgImage = bgImage.resize(image.size)
        bgImage = Image.alpha_composite(bgImage, image)

        # saving the file and convert
        bgImage = bgImage.convert('RGB')
        newFilename = f"static/outputs/{str(int(time.time()))}.jpg"
        bgImage.save(newFilename)
        return newFilename

def solidBackground(file, type, color):
    if type == "png":
        input = Image.open(file)
        input = remove(input)
        input = input.convert('RGBA')

        newColor = ImageColor.getcolor(color, 'RGBA')
        background = Image.new('RGBA', input.size, newColor)
        newImage = Image.alpha_composite(background, input)

        newFilename = f"static/outputs/{str(int(time.time()))}.png"
        newImage.save(newFilename)
        return newFilename
    elif type == "jpeg":
        input = Image.open(file)
        input = remove(input)
        input = input.convert('RGBA')

        newColor = ImageColor.getcolor(color, 'RGBA')
        background = Image.new('RGBA', input.size, newColor)
        newImage = Image.alpha_composite(background, input)

        newImage = newImage.convert('RGB')
        newFilename = f"static/outputs/{str(int(time.time()))}.jpeg"
        newImage.save(newFilename)
        return newFilename
    elif type == "jpg":
        input = Image.open(file)
        input = remove(input)
        input = input.convert('RGBA')

        newColor = ImageColor.getcolor(color, 'RGBA')
        background = Image.new('RGBA', input.size, newColor)
        newImage = Image.alpha_composite(background, input)

        newImage = newImage.convert('RGB')
        newFilename = f"static/outputs/{str(int(time.time()))}.jpg"
        newImage.save(newFilename)
        return newFilename

def removeBackground(file, type):
    if type == "png":
        input = Image.open(file)
        removed = remove(input)
        output = removed.convert('RGBA')
        newFilename = f"static/outputs/{str(int(time.time()))}.png"
        output.save(newFilename)
        return newFilename
    elif type == "jpeg":
        input = Image.open(file)
        removed = remove(input)
        output = removed.convert('RGB')
        newFilename = f"static/outputs/{str(int(time.time()))}.jpeg"
        output.save(newFilename)
        return newFilename
    elif type == "jpg":
        input = Image.open(file)
        removed = remove(input)
        output = removed.convert('RGB')
        newFilename = f"static/outputs/{str(int(time.time()))}.jpg"
        output.save(newFilename)
        return newFilename


# ----- Routes -----
# default page
@app.route('/', methods=['POST', 'GET'])
def index():
    # uploading
    if request.method == 'POST':
        # Allowed extenctions
        UPLOAD_FOLDER = './outputs'
        ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'JPG', 'PNG', 'JPEG']

        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        # Check if file exits
        if 'file' not in request.files:
            return render_template('index.html', error = 'no image')
        
        file = request.files['file']
        
        # Empty filename
        if file.filename == '':
            return render_template('index.html', error = 'no file imge')

        # If file is secure
        if file:
            if file.filename.split('.')[1] in ALLOWED_EXTENSIONS:
                # get file format
                file_format = request.form['fileFormat']
                selected_option = request.form['options']

                # Chechking
                if selected_option == 'change_background':
                    if 'background' not in request.files:
                        return render_template('index.html', error = 'no background')
        
                    background = request.files['background']
        
                    # Empty filename
                    if background.filename == '':
                        return render_template('index.html', error = 'no background name')

                     # Do background color
                    if background and background.filename.split('.')[1] in ALLOWED_EXTENSIONS:
                        filePath = changeBackground(file, file_format, background)
                        atexit.register(functools.partial(clearUp, filePath))
                        return render_template('index.html', src = filePath)
                        
                elif selected_option == 'solid_background':
                    selected_color = request.form['colorPicker']
                    filePath = solidBackground(file, file_format, selected_color)
                    return render_template('index.html', src = filePath)
                else:
                    # remove_bg
                    filePath = removeBackground(file, file_format)

                    #cleaning up
                    atexit.register(functools.partial(clearUp, filePath))
                    return render_template('index.html', src = filePath)
            else:
                return render_template('index.html', error = 'invalid file format')
        else:
            return render_template('index.html', error = 'file error')

    elif request.method == 'GET':
        return render_template('index.html')

    

# deleting

# ENDa
if __name__ =="__main__":
    app.run(debug = True)

