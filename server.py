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

def read_audio(WAVE_FILENAME):
	with open(WAVE_FILENAME, 'rb') as f:
		audio=f.read()
	return audio

def RecognizeSpeech(AUDIO_FILENAME):
	print AUDIO_FILENAME
	audio = read_audio(AUDIO_FILENAME)
	
	headers = {'authorization':'Bearer ' + wit_access_token,'Content-Type':'audio/mpeg'}

	resp = requests.post(API_ENDPOINT, headers = headers, data=audio)

	print resp
	data = json.loads(resp.content.decode('utf-8'))
	print (data)

	text = data['_text']
	return text

def Check(AUDIO_FILENAME):
	print("Checking")
	points = 0
	text = RecognizeSpeech(AUDIO_FILENAME)
	list_words = text.split(" ")
	for i in range(len(list_words)):
		print(list_words[i])
		if list_words[i] == "score":
			points = points + 1
	print("the total amount of points was ", points)
	print("\nYou said: {}".format(text))
	return points



@app.route("/upload", methods=['POST'])
def upload():
	print "hehe"
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
