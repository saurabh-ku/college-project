from flask import Flask, render_template, request
from werkzeug import secure_filename
import os

app = Flask(__name__)

ROOT_DIR = os.path.dirname(
			os.path.realpath(__file__)
			)
UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = os.path.join(
								ROOT_DIR,
								UPLOAD_FOLDER
								)

@app.route('/upload')
def upload_file():
	return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file_completed():
	if request.method == 'POST':
		f = request.files['file']
		f.save(
			os.path.join(
				app.config['UPLOAD_FOLDER'], 
				secure_filename("img.jpg")
				)
			)
		callPi()
		return 'file uploaded successfully, calling api'

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug=False)
