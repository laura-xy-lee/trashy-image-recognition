import json
from itertools import chain
import os
from werkzeug.datastructures import FileStorage

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin

from models.tutorials.image.imagenet.custom_classify_image import custom_classify_image
from classify_trash.classify_recyclable_trash import classify_recyclable_trash

app = Flask(__name__)

# app.config['CORS_HEADERS'] = ['Content-Type', 'Access-Control-Allow-Origin']
# cors = CORS(app, resources={r"/predict": {"origins": "https://trashy-recyclingmap.surge.sh/"}})


@app.route("/", methods=['GET'])
def main():
    """Gets the main page"""
    return render_template('index.html')


@app.route("/predict", methods=["POST"])
@cross_origin(origin=os.environ['CORS_URL'], headers=['Content-Type','Access-Control-Allow-Origin'])
def predict():
    """Makes prediction"""
    # Save client uploaded image to path
    file_obj = request.files['file']
    with open('images/client_image.jpeg', 'rb'):
        file = FileStorage(file_obj)
    file.save('images/client_image.jpeg')

    # Get Tensorflow inception-v3's top 5 prediction
    image_predictions = custom_classify_image(image_path='images/client_image.jpeg')

    # Classify if recyclable or not
    image_labels = [i[1] for i in image_predictions]
    image_labels_hack = image_labels[0]

    image_labels_melt = [i.split(',') for i in image_labels]
    image_labels_melt = list(chain.from_iterable(image_labels_melt))

    recyclable_classification = classify_recyclable_trash(image_labels_melt)

    return jsonify({
	# json.dumps({
        # "prediction": image_labels,
        "prediction": image_labels_hack,
        "material": recyclable_classification.get("material"),
        "waste_action": recyclable_classification.get("action"),
        "instruction": recyclable_classification.get("special_instructions")
    })


if __name__ == "__main__":
    app.run()
