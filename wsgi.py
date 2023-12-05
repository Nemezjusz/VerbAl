from flask import Flask, render_template, request, redirect, url_for
import os
import werkzeug

app = Flask(__name__)

# Configure the upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'uploads/'  # make sure this directory exists
app.config['ALLOWED_EXTENSIONS'] = {'wav', 'mp3', 'aac', 'ogg', 'm4a'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template("main.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'audiofile' not in request.files:
        return redirect(request.url)

    file = request.files['audiofile']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = werkzeug.utils.secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # Process the file if needed
        # ...

        # Redirect or render a template after saving
        return redirect(url_for('index'))

    return redirect(request.url)


if __name__ == '__main__':
    app.run()