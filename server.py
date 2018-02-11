import requests
import json
import wave
import sys

API_ENDPOINT='https://api.wit.ai/speech'

wit_access_token = 'PGXQAYLLA7R7BAJLDBVODGN4QXSADSNN'

def read_audio(WAVE_FILENAME):
	with open(WAVE_FILENAME, 'rb') as f:
		audio=f.read()
	return audio

def RecognizeSpeech(AUDIO_FILENAME):
	audio = read_audio(AUDIO_FILENAME)
	headers = {'authorization':'Bearer ' + wit_access_token,'Content-Type':'audio/wav'}
	resp = requests.post(API_ENDPOINT, headers = headers, data=audio)
	data = json.loads(resp.content.decode('utf-8'))
	text = data['_text']
	return text

points = 0
text = RecognizeSpeech('audio.wav')
list_words = text.split(" ")

print(list_words, list_words.count("score"))
