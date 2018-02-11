import requests
import json
import wave
import sys
import os
from flask import Flask, request, jsonify
from werkzeug.datastructures import ImmutableMultiDict
from datetime import datetime
import audiotranscode

app = Flask(__name__)

API_ENDPOINT='https://api.wit.ai/speech'

wit_access_token = 'PGXQAYLLA7R7BAJLDBVODGN4QXSADSNN'

# Read the audio
def read_audio(WAVE_FILENAME):
	with open(WAVE_FILENAME, 'rb') as f:
		audio=f.read()
	return audio

def RecognizeSpeech(AUDIO_FILENAME):
	print AUDIO_FILENAME
	audio = read_audio(AUDIO_FILENAME)
	headers = {'authorization':'Bearer ' + wit_access_token,'Content-Type':'audio/mpeg'}
	resp = requests.post(API_ENDPOINT, headers = headers, data=audio)
	data = json.loads(resp.content.decode('utf-8'))
	text = data['_text']
	return text

def Check(AUDIO_FILENAME):
	points, passes, shots = 0, 0, 0
	text = RecognizeSpeech(AUDIO_FILENAME)
	list_words = text.split(" ")
	for i in range(len(list_words)):
		print(list_words[i])
		if (list_words[i] == "score" or list_words[i] == "scores"):
			points += 1
		elif (list_words[i] == "pass" or list_words[i] == "passed" or list_words[i] == "passes"):
			passes += 1
		elif(list_words[i] == "shot" or list_words[i] == "shoots"):
			shots += 1
	print("the total amount of points was ", points)
	print("\nYou said: {}".format(text))
	return points, passes, shots

@app.route("/upload", methods=['POST'])

# this is upload function
def upload():
	file = request.files['file']
	print file
	format = "%Y-%m-%dT%H:%M:%S"
	now = datetime.utcnow().strftime(format)
	print now
	filename = now + '_' + file.filename
	print filename
	fullpath = os.path.join('upload_folder', filename) # .m4a
	file.save(fullpath)

	at = audiotranscode.AudioTranscode()
	at.transcode(fullpath, fullpath + ".mp3") 

	file_uploaded = True
	total = Check(fullpath + ".mp3")
	
	return jsonify(
		pointA=total,
		pointB=total,
	)

app.run(host='0.0.0.0', port=8008, debug=True)
