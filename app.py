# from flask_cors import CORS
import subprocess
import json
from itertools import chain
from werkzeug.datastructures import FileStorage

from flask import Flask, render_template, request

from recyclables_classifier.recyclables_classifier import classify

app = Flask(__name__)
# CORS(app)


@app.route("/", methods=['GET'])
def main():
	"""Gets the main page"""
	return render_template('index.html') 


@app.route("/predict", methods=["POST"])
def predict():
	"""Makes prediction"""
	file_obj = request.files['file']
	file = None
	with open('images/client_image.jpeg', 'rb') as fp:
	    file = FileStorage(file_obj)
	file.save('images/client_image.jpeg')

	bash_command = "python models/tutorials/image/imagenet/classify_image.py --image_file=images/client_image.jpeg"
	result = subprocess.check_output(bash_command.split())

	# Returns best guess by tensorflow
	best_guess = []
	for i in str(result).split("("):
	    if len(i.split(")")) > 1:
	        guess = i.split(")")[1]
	    else:
	        guess = i

	    best_guess.append(guess)

	# Format best guess
	best_guess = [g.replace("b'", "") for g in best_guess]
	best_guess = [g.replace('b"', "") for g in best_guess]
	best_guess = [g.replace("\\n", "") for g in best_guess]
	best_guess = [g.replace("'", "") for g in best_guess]
	best_guess = [g.replace('"', "") for g in best_guess]
	best_guess = list(filter(None, best_guess))

	formatted_best_guess_list = []
	for guess in best_guess:
		formatted_guess = guess.strip().upper()
		formatted_best_guess_list.append(formatted_guess)
	formatted_best_guess = " or ".join(formatted_best_guess_list)

	vowels = ('a','e','i','o','u','A','E','I','O','U')
	if formatted_best_guess.startswith(vowels):
		formatted_best_guess = "an " + formatted_best_guess
	else:
		formatted_best_guess = "a " + formatted_best_guess

	results = classify(item_label=formatted_best_guess_list)
	return json.dumps({
		"output": formatted_best_guess,
		"material_type": results.get("material_type"),
		"instruction": results.get("instruction")
		})


if __name__ == "__main__":
	app.run()
