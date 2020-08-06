import os
import flask
from flask import session, url_for, jsonify, request, redirect, render_template
from module.Image_Prediction_GRU import model as model_gru
from module.ImageCaptioning_Full_script_old import model as model_lstm
from flask_cors import CORS


## Chang the directory name to the src directory  in UI Components
UPLOAD_DIRECTORY = "C:\\Users\\Govind\\SML\\Project\\UIComponents\\src"


app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


@app.route('/upload-image', methods=['POST'])
def upload_image():
	"""
	This function recieves post request with image file name and model name as parameters.
	The right model package is loaded and a prediction is generated on the given input image
	Sample request API : http://localhost:5000/upload_image
	"""
    if request.method == "POST":
        if request.files:
            image = request.files.get('Image')
            model_type = request.args['model']
            print(model_type)
            if model_type == 'gru':
                model = model_gru
            else:
                model = model_lstm
            image.save(os.path.join(UPLOAD_DIRECTORY, image.filename))
            predictions = model(os.path.join(UPLOAD_DIRECTORY, image.filename))
            response = jsonify({
                            'prediction' : ' '.join(predictions[:-1]),
                            'image_path' : os.path.join(UPLOAD_DIRECTORY, image.filename)
                       })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    response = jsonify(success=False)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response     


if __name__ == '__main__':
    app.run(debug=True)