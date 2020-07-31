import os
import flask
# import numpy as np
# import tensorflow as tf
# import tensorflow.keras as keras
from flask import session, url_for, jsonify, request, redirect, render_template
from module.Image_Prediction_GRU import model as model_gru
from module.ImageCaptioning_Full_script_old import model as model_lstm
from flask_cors import CORS

# UPLOAD_DIRECTORY = os.path.join(os.getcwd(), "app_uploaded_files")
UPLOAD_DIRECTORY = "C:\\Users\\Govind\\SML\\Project\\React\\ImageLabelling\\src"

# if not os.path.exists(UPLOAD_DIRECTORY):
#     os.makedirs(UPLOAD_DIRECTORY)

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


@app.route('/upload-image', methods=['POST'])
def upload_image():
    if request.method == "POST":
        # print(request.files.get('Image'))
        if request.files:
            image = request.files.get('Image')
            model_type = request.args['model']
            print(model_type)
            if model_type == 'gru':
                model = model_gru
            else:
                model = model_lstm
            image.save(os.path.join(UPLOAD_DIRECTORY, image.filename))
            predictions = model(os.path.join(UPLOAD_DIRECTORY, image.filename))#['This', 'is', 'a', 'sample', 'prediction', '<end>']                                          
            response = jsonify({
                            'prediction' : ' '.join(predictions[:-1]),
                            'image_path' : os.path.join(UPLOAD_DIRECTORY, image.filename)
                       })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    response = jsonify(success=False)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response     


@app.route('/caption', methods = ['GET'])
def generate_caption():
    image_name = request.args['name']
    image_path = os.path.join(UPLOAD_DIRECTORY, image_name)

    predictions = ['This', 'is', 'a', 'sample', 'prediction', '<end>']#model(image_path)

    return jsonify({
        'prediction' : ' '.join(predictions[:-1]),
        'image_path' : os.path.join(UPLOAD_DIRECTORY, image_name)
    })

if __name__ == '__main__':
    app.run(debug=True)