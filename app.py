
from io import BytesIO
from PIL import Image, ImageOps
import base64
import urllib

import numpy as np
# import scipy.misc
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import tensorflow as tf
#from skimage import io
from tensorflow.keras.preprocessing import image
import webbrowser

# Flask utils
from flask import Flask, request, jsonify, send_file, render_template, redirect, url_for


app = Flask(__name__)

@app.route("/")
@app.route("/first")
def first():
    return render_template('first.html')
    
@app.route("/login")
def login():
    return render_template('login.html')    
@app.route("/chart")
def chart():
    return render_template('chart.html')

@app.route("/performance")
def performance():
    return render_template('performance.html')


@app.route("/index",methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/upload", methods=['POST'])
def upload_file():
    print("Hello")
    try:
        img = Image.open(BytesIO(request.files['imagefile'].read())).convert('RGB')
        img = ImageOps.fit(img, (224, 224), Image.ANTIALIAS)
    except:
        error_msg = "Please choose an image file!"
        return render_template('index.html', **locals())
    print("Hello2")
    # Call Function to predict
    args = {'input' : img}
    out_pred, out_prob = predict(args)
    out_prob = out_prob * 100

    print(out_pred, out_prob)

    img_io = BytesIO()
    img.save(img_io, 'PNG')

    png_output = base64.b64encode(img_io.getvalue())
    processed_file = urllib.parse.quote(png_output)

    return render_template('result.html',**locals())
def predict(args):
    img = np.array(args['input']) / 255.0
    img = np.expand_dims(img, axis = 0)
    
    # Load your trained model
    model = 'CnnWasDetModel.h5'  # CnnWasDetModel2.h5 use this model also
    # Load model from tensorflow
    model = load_model(model)

    pred = model.predict(img)
    print("pred:", pred)

    if np.argmax(pred, axis=1)[0] == 0:
        out_pred = "Empty"
    elif np.argmax(pred, axis=1)[0] == 1:
        out_pred = "Full"
    else:
        out_pred = "Normal"
    return out_pred, float(np.max(pred))

webbrowser.open('http://127.0.0.1:5000/', new=1)

if __name__ == '__main__':
    app.run()

