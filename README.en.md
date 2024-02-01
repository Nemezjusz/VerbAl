# VerbAl

The main goal of the project was to create an application using available AI tools. The application automatically transcribes user-provided audio using speech-to-text technology. In the next stage, the text is analyzed and improved using, for example, ChatGPT to improve grammar and overall syntax. Finally, the application presents the results by comparing the original text with the corrected one and offers suggestions regarding grammar.

## Functionality
The application offers the possibility to analyze the sound input provided by one of the following options:
- Microphone
- Audio file

![Screenshot 2024-01-30 111825](https://github.com/Nemezjusz/VerbAl/assets/50834734/b0eae5bc-7662-4a8d-ad14-2968030ca9c9)

After the user input is entered, the sound is analyzed and processed locally using the Whisper model created by OpenAI. After processing the sound into text, the next step is its grammatical analysis. We obtain it in one of two ways:
- External analysis obtained by using the OpenAI API. The text is sent to the chosen version of ChatGPT, it is processed and corrected by it. Finally, we receive the corrected version.
- Local analysis obtained thanks to a locally hosted LLM like Llama or Mistral. The analysis and correction process is similar to the previous variant.

The final stage of the application's work is comparing both texts and highlighting the differences. The final effect can be seen below.

![Screenshot 2024-01-30 112124](https://github.com/Nemezjusz/VerbAl/assets/50834734/dff53050-5b4f-41f6-8768-d42f498bf644)

## Installation
In order to make the application work independently, it needs additional library installations. There is also an option to rely solely on the OpenAI API, but we prefer independence from big corporations.

### Python Libraries

To install the necessary libraries, you only need to run the install_libs.py file. You can do this using the following command:
```
python3 install_libs.py
```

### Whisper

We will need an additional library for sound processing ffmpeg
```
# Linux
sudo apt update && sudo apt install ffmpeg

# MacOS
brew install ffmpeg

# Windows
chco install ffmpeg
```

### Ollama

For full independence, we also need Ollama and the LLM downloaded using it.
```
# Linux
curl https://ollama.ai/install.sh | sh

# MacOS
Download link: https://ollama.ai/download/mac
```