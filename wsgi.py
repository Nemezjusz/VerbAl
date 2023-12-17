from flask import Flask, render_template, request, redirect
import os, werkzeug, whisper, difflib
from openai import OpenAI

client = OpenAI(api_key="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")

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


def find_different_words(original_text, corrected_text):
    d = difflib.Differ()
    diff = list(d.compare(corrected_text.split(), original_text.split() ))

    different_words = [word[2:] for word in diff if word.startswith('- ')]

    return different_words
def replace_with_bold(corrected_text, changed_words):
    corrected_text = corrected_text.split()
    c = 0
    for i in range(len(corrected_text)):
        if corrected_text[i] == changed_words[c]:
            corrected_text[i] = f"<b style='color:red;'>{corrected_text[i]}<b/>"
            if c != len(changed_words)-1:
                c+=1

    result_text = ' '.join(corrected_text)
    return result_text

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    text = "After loading your file using Audio File button or providing it via Microphone you will see " \
           "your transcribed text in this section"
    corrected_text = "Here you will see <b>corrected</b> text"
    return render_template("main.html", transcript=text, corrected_transcript=corrected_text)


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
        changed_words = find_different_words(text, corrected_text)
        corrected_and_edited_text = replace_with_bold(corrected_text, changed_words)

        return render_template("main.html", transcript=text, corrected_transcript=corrected_and_edited_text)

    return redirect(request.url)



if __name__ == '__main__':
    app.run()