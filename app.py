from itertools import chain
import shutil
import uuid

from werkzeug.datastructures import FileStorage
from flask import Flask, render_template, request, jsonify

from models.imagenet.custom_classify_image import custom_classify_image
from classify_trash.classify_trash import classify

app = Flask(__name__)


@app.route("/", methods=['GET'])
def main():
    """Gets the main page"""
    return render_template('index.html')


@app.route("/predict", methods=["POST"])
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

    image_labels_melt = [i.split(',') for i in image_labels]
    image_labels_melt = list(chain.from_iterable(image_labels_melt))
    image_labels_melt = [i.strip() for i in image_labels_melt]

    classification = None
    for i in image_labels_melt:
        if not classification:
            classification = classify(trash=i)

    if classification.get("is_recyclable"):
        waste_action = "Recyclable"
    else:
        waste_action = "Not Recyclable"

    return jsonify({
        "prediction": classification.get("identified_item"),
        "material": classification.get("material"),
        "waste_action": waste_action,
        "instruction": classification.get("remarks")
    })


@app.route("/report_wrong_identification", methods=["GET"])
def report_wrong_identification():
    src_file = 'images/client_image.jpeg'
    new_file_name = "images/ident_" + str(uuid.uuid4()) + ".jpeg"
    shutil.copy(src_file, new_file_name)

    return "Thank you for your feedback"


@app.route("/report_wrong_classification", methods=["GET"])
def report_wrong_classification():
    src_file = 'images/client_image.jpeg'
    new_file_name = "images/class_" + str(uuid.uuid4()) + ".jpeg"
    shutil.copy(src_file, new_file_name)

    return "Thank you for your feedback"


if __name__ == "__main__":
    app.run()
