from flask import Flask, render_template, request, redirect, url_for
import os
import werkzeug
import openai

app = Flask(__name__)

# Konfiguracja folderu do przesyłania i dozwolonych rozszerzeń
app.config['UPLOAD_FOLDER'] = 'uploads/'  # upewnij się, że ten folder istnieje
app.config['ALLOWED_EXTENSIONS'] = {'wav', 'mp3', 'aac', 'ogg', 'm4a'}

# Ustaw klucz API OpenAI
API_KEY = open("OPENAI_API_KEY", "r").read()
openai.api_key = API_KEY

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template("main.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audiofile' not in request.files:
        return redirect(request.url)

    file = request.files['audiofile']
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = werkzeug.utils.secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Przetwarzanie pliku, jeśli jest to potrzebne
        with open(filepath, "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        # Zamiana wyniku transkrypcji na tekst
        transcription_text = str(transcript)

        # Przekazanie wyniku transkrypcji do szablonu HTML
        return render_template("result.html", transcription=transcription_text)

    return redirect(request.url)

if __name__ == '__main__':
    app.run()
