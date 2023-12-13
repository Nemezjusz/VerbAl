from flask import Flask, render_template, request, redirect
import os, werkzeug, whisper
from openai import OpenAI

client = OpenAI(api_key="api-key")

app = Flask(__name__)

# Configure the upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'uploads/'  # make sure this directory exists
app.config['ALLOWED_EXTENSIONS'] = {'wav', 'mp3', 'aac', 'ogg', 'm4a'}

model = whisper.load_model("base")


def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result['text']


def correct_grammer(transcript):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a grammar assistant, skilled in correcting grammar"},
            {"role": "user", "content": f"Correct grammer in following text, return only corrected text: {transcript}"}
        ]
    )
    return completion.choices[0].message.content


def find_changed_words(original_text, corrected_text):
    original_words = original_text.split()
    corrected_words = corrected_text.split()

    changed_words = [word for original, corrected in zip(original_words, corrected_words) if original != corrected]

    return changed_words


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

        text = transcribe_audio(filepath)
        corrected_text = correct_grammer(text)

        return render_template("main.html", transcript=text, corrected_transcript=corrected_text)

    return redirect(request.url)



if __name__ == '__main__':
    app.run()