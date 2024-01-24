import vosk
import pyaudio
import json
from pynput import keyboard
import pyperclip

# https://github.com/alphacep/vosk-space/blob/master/models.md
model_path = "model/vosk-model-small-ru-0.22"

model = vosk.Model(model_path)
recognizer = vosk.KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)

print("Для начала распознавания речи нажмите Alt + R")

def on_activate():
	print("work")
	# Вынужденная очистка буфера
	pyperclip.copy("")

	block = False

	def exit_func():
		global work, data, recognizer

		work = False
		pyautogui.hotkey("ctrl", "v")
		data = 0
		recognizer.Reset()
		print("exit")


	work = True
	while work:
		# Специальная конструкция для запуска функции только 1 раз
		if not block:
			block = True
			exit_key = keyboard.HotKey(keyboard.HotKey.parse('<ctrl>+v'), exit_func)
			with keyboard.Listener(
				on_press=for_canonical(exit_key.press),
				on_release=for_canonical(exit_key.release)) as e:
				e.join()

		data = stream.read(1000)
		if len(data) == 0:
			break
		
		if recognizer.AcceptWaveform(data):
			result = json.loads(recognizer.Result())
			if 'text' in result:
				textt = f"{result['text']}"
				
				if textt:
					clip = pyperclip.paste()
					new_clip = clip + textt
					pyperclip.copy(f"{new_clip} ")
				else:
					print("Empty")

	print("dont work")

def for_canonical(f):
	return lambda k: f(l.canonical(k))

hotkey = keyboard.HotKey(keyboard.HotKey.parse('<alt>+r'), on_activate)


with keyboard.Listener(
		on_press=for_canonical(hotkey.press),
		on_release=for_canonical(hotkey.release)) as l:
	l.join()

print("\nРаспознавание завершено.")

stream.stop_stream()
stream.close()
p.terminate()