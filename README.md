# VerbAl
Aplikacja do analizy języka mówionego i jego korekty gramatycznej stworzona przy pomocy aktualnie dostępnych modeli i narzędzi AI.

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

