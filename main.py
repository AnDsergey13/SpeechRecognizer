import vosk
import pyaudio
import simpleaudio as sa
import json
from pynput import keyboard
import pyperclip
import threading

def play_audio(filename):
	"""Функция для воспроизведения звуковых сигналов"""
	# https://simpleaudio.readthedocs.io/en/latest/simpleaudio.html#examples
	wave_obj = sa.WaveObject.from_wave_file(filename)
	play_obj = wave_obj.play()
	play_obj.wait_done()

def speech_recognition():
	global work

	# Воспроизводим звук запуска прослушки голоса
	play_audio("sound/on_2.wav")
	# Очищаем буфер, чтобы надиктованный текст не смешался с данными (при первом запуске), которые были ранее в него записаны
	pyperclip.copy("")

	# При каждом нажатии клавиш Alt + R, заново запускаем цикл распознавания голоса
	work = True
	while work:
		data = stream.read(1000)
		if len(data) == 0:
			break
		
		if recognizer.AcceptWaveform(data):
			result = json.loads(recognizer.Result())
			if 'text' in result:
				# Записываем в переменную тот текст, который был надиктован
				text = f"{result['text']}"
				
				if text:
					# Извлекаем текст из буфера обмена
					clip = pyperclip.paste()
					# Складываем его с надиктованным текстом
					new_clip = f"{clip + text} "
					# И опять записываем в буфер
					pyperclip.copy(new_clip)
				else:
					# print("Empty")
					# Воспроизводим звук, если голос не был услышан (например, когда человек молчит)
					# Так же служит напоминанием, что программа работает
					play_audio("sound/on_1.wav")

def exit_func():
	global work

	# Чтобы звуки и сообщения не выводились при повторном нажатии Сtrl + V, делаем проверку отключения цикла 
	if work:
		work = False

		play_audio("sound/off.wav")
		print("Распознавание речи - завершено")
		print("Для начала распознавания речи нажмите Alt + R")

def listen_end_command():
	"""При нажатии Сtrl + V, вставляется из буфера обмена надиктованный текст, и завершается распознавание голоса """
	exit_keys = keyboard.HotKey(keyboard.HotKey.parse('<ctrl>+v'), exit_func)
	with keyboard.Listener(
		on_press=for_canonical(exit_keys.press),
		on_release=for_canonical(exit_keys.release)) as e:
		e.join()

def for_canonical(f):
	# """Неизвестная функция, которая каким-то образом обрабатывает нажатия"""
	# Нужна ли она?
	return lambda k: f(l.canonical(k))

# Переменная для работы бесконечного цикла, при распознавании голоса
work = True

# https://github.com/alphacep/vosk-space/blob/master/models.md
# Модель нужно обязательно разархивировать 
model_path = "model/vosk-model-small-ru-0.22"
model = vosk.Model(model_path)
recognizer = vosk.KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)

# Поток для прослушки ввода Ctrl + V. Необходим для завершения распознования голоса
lc_th = threading.Thread(target=listen_end_command)
# Делаем так, чтобы при завершении основного потока программы, другой поток, так же завершился
lc_th.daemon = True
lc_th.start()


start_keys = keyboard.HotKey(keyboard.HotKey.parse('<alt>+r'), speech_recognition)
print("___ Для завершения работы программы, нажмите Ctrl + C ___")
print("Для начала распознавания речи нажмите Alt + R")
try:
	with keyboard.Listener(
			on_press=for_canonical(start_keys.press),
			on_release=for_canonical(start_keys.release)) as l:
		l.join()
except KeyboardInterrupt:
	print("\nЗавершение программы")
	stream.stop_stream()
	stream.close()
	p.terminate()