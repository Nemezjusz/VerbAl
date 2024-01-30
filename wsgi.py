from flask import Flask, render_template, request, redirect
import os, werkzeug, whisper, difflib
from openai import OpenAI
from constants import API_KEY

client = OpenAI(api_key=API_KEY)

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

# def correct_grammer_local(transcript):
#
#     from langchain.prompts import PromptTemplate
#     from langchain.chains import LLMChain
#     from langchain_community.llms import Ollama
#
#     llm = Ollama(model="llama2", temperature=0.9, )
#
#     prompt = PromptTemplate(
#         input_variables=["transcript"],
#         template="Correct grammer in following text, return only corrected text: {transcript}", )
#
#     chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
#
#     # Run the chain only specifying the input variable.
#     return chain.invoke(transcript)["text"]


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
            corrected_text[i] = f"<b style='color:green;'>{corrected_text[i]}</b>"
            if c != len(changed_words)-1:
                c+=1

    result_text = ' '.join(corrected_text)
    return result_text

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    #og = "Hey, aren't we all in the same English course? Yeah, how's it going? Not bad, except I sometimes have trouble with my grammar, isn't it? I mean, sometimes I perfect, but other times I don't, won't they? See, I'm all right with my grammar. My problem is spilling. I can't spill to save my loaf. Yeah? Yeah, after a lie in a spell chalk on my computer. It's fine, you know, look it at this way. You can lead a horse to water, but you can't eat it too, you know what I'm saying? No, no, not really. I think that she sometimes has trouble mixing metaphors, aren't she? Yeah, sorry you guys, I'm always crying over spilled chickens before they're hatched. It's all right for you all, I've got a very small vocabulary. What's that like? It's all right for you all, I've got a very small vocabulary. That's okay, I have problems with my emphasis. Being your emphasis? Yes, my emphasis on different parts of the sentences. In my job, back in course, a lot of all quadrace. What do you do? I'm a speech therapist. A speech therapist, I can't spike properly. Surprise your boss hasn't sucked you. It's all right for you all, I've got a very small vocabulary. Can I make a suggestion? Why don't you purchase a dictionary? You'll save yourself a lot of emberasmut. I tell you what, why doesn't we all try studying together, isn't it? How does the next week sound, didn't we? Great idea. Fabulous. Yeah, you give them an entrance worth two in the bush. It's all right for you all, I've got a very small vocabulary."
    #cr = "Hey, aren't we all in the same English course? Yeah, how's it going? Not bad, except I sometimes have trouble with my grammar, don't I? I mean, sometimes I'm perfect, but other times I'm not, aren't I? See, I'm alright with my grammar. My problem is spelling. I can't spell to save my life. Yeah? Yeah, I accidentally spilled chalk on my computer. It's fine, you know, look at it this way. You can lead a horse to water, but you can't eat it too, you know what I'm saying? No, no, not really. I think she sometimes has trouble mixing metaphors, doesn't she? Yeah, sorry you guys, I'm always crying over spilled milk before it's hatched. It's alright for all of you, I have a very small vocabulary. What's it like? It's alright for all of you, I have a very small vocabulary. That's okay, I have problems with my emphasis. Being your emphasis? Yes, my emphasis on different parts of the sentences. In my job, back in the course, not all quadrace. What do you do? I'm a speech therapist. A speech therapist, I can't speak properly. Surprise your boss hasn't fired you. It's alright for all of you, I have a very small vocabulary. Can I make a suggestion? Why don't you purchase a dictionary? You'll save yourself a lot of embarrassment. I tell you what, why don't we all try studying together, shall we? How does next week sound, shall we? Great idea. Fabulous. Yeah, you're giving them an inch and they take a mile. It's alright for all of you, I have a very small vocabulary."
    og = "Example of you're input"
    cr = "Example of your input"
    changed_words = find_different_words(og, cr)
    corrected_and_edited_text = replace_with_bold(cr, changed_words)
    return render_template("main.html", transcript=og, corrected_transcript=corrected_and_edited_text)


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