# SpeechRecognizer

A simple utility for speech recognition.

**❗❗❗ The project uses Python version 3.11.6**

#### Download
```sh
# CodeBerg
git clone https://codeberg.org/femto/SpeechRecognizer.git
# or GitHub
git clone https://github.com/AnDsergey13/SpeechRecognizer.git
```

#### Open the folder with the project
```sh
cd SpeechRecognizer
```

#### Creating a virtual environment (Linux)
```sh
python -m venv .venv
```

#### Activating the virtual environment (Linux)
```sh
# bash
source .venv/bin/activate
# or fish
source .venv/bin/activate.fish
```

#### Installing the necessary dependencies
```sh
pip install -r requirements.txt 
```
❗ You may need to install additional packages to work with the clipboard

#### Launching the utility
```sh
python main.py
```

#### Working with the utility
1. Closing the utility. 
1.1 `Ctrl + C` - when launched in terminal
1.2 Or manually kill the process in the task manager. Because it runs in an endless loop
2. Starting Voice Recognition `Alt + R` (sound plays when starting)
3. Stop voice recognition `Ctrl + V` (sound plays when stopped)

- If you do not speak for a long time, a reminder sound will be played that the utility is working in voice recognition mode.
- To restart voice recognition, you need to press `Alt + R`
