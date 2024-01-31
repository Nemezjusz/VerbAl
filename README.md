# VerbAl
Aplikacja do analizy języka mówionego i jego korekty gramatycznej stworzona przy pomocy aktualnie dostępnych modeli i narzędzi AI.

## Funkcjonalności
Aplikacja oferuje możliwość analizy dźwięku wprowadzonego za pomocą jednej z następujących możliwości:
- Mikrofonu
- Pliku audio

![Zrzut ekranu 2024-01-30 111825](https://github.com/Nemezjusz/VerbAl/assets/50834734/b0eae5bc-7662-4a8d-ad14-2968030ca9c9)

Po wprowadzeniu inputu użytkownika dźwięk jest analizowany i przetwardzany lokalnie dzięki modelowi *Whisper* stworzonego przez *OpenAI*. 
Po przetworzeniu dźwięku na tekst kolejnym etapem pracy jest jego analiza pod względem gramatycznym. Uzyskujemy ją na jeden z dwóch sposobów: 
- Analiza zewnętrzna uzyskana poprzez użycie API OpenAI. Tekst jest wysyłany do wybranej wersji ChatGPT, jest on przez niego przetwarzany i poprawiany. Finalnie otrzymujemy poprawioną wersje.
- Analiza lokalna uzyskana dzięki lokalnie postawionemu LLM takiemu jak *Llama* lub *Mistral*. Analiza i poprawa odbywa się podobnie jak w poprzdnim wariancie.

Ostatnim etapem pracy aplikacji jest porównanie obu tekstów i zaznaczenie różnic. Finalny efekt możemy zobaczyć niżej. 

![Zrzut ekranu 2024-01-30 112124](https://github.com/Nemezjusz/VerbAl/assets/50834734/dff53050-5b4f-41f6-8768-d42f498bf644)

## Instalacja 
Aplikacja aby mogła w pełni niezależnie działać potrzebuje instalacji dodakowych bibliotek. Istneje także możliwość oparcia się tylko i wyłącznie na API OpenAI, lecz preferujemy niezależność od wielkich korporacji.

### Biblioteki Python

Aby zainstallować niezbędne biblioteki należy jedynie odpalić plik install_libs.py. Możemy to zrobić za pomocą komendy:
```
python3 install_libs.py
```

### Whisper

Bedziemy potrzebować dodatkowej biblioteki do przetwarzania dźwięku ffmpeg
```
# Linux
sudo apt update && sudo apt install ffmpeg

# MacOS
brew install ffmpeg

# Windows
chco install ffmpeg
```

### Ollama

Do pełnej niezależności potrzebna nam także Ollama i pobrany za jej pomocą LLM
```
# Linux
curl https://ollama.ai/install.sh | sh

# MacOS
Download link: https://ollama.ai/download/mac
```

