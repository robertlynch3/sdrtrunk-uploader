#!/usr/bin/env python
#
# server.py
#
#

from flask import Flask, request, Response
from requests import post
from json import load, dumps
import random
import string
from dotenv import load_dotenv
from os import remove, getenv, path, makedirs


load_dotenv() 

app = Flask(__name__)
app.secret_key=''.join(random.choices(string.ascii_lowercase, k=85))

# Determines if the directory exists or not

MIDDLEWARE_URL=getenv('MIDDLEWARE_URL', 'http://127.0.0.1')
LISTENING_PORT=getenv('LISTENING_PORT', '8080')
RDIO_SCANNER_URL=getenv('RDIO_SCANNER_URL', 'http://127.0.0.1:3000')
CAPTURE_DIR=getenv('CAPTURE_DIR','/var/tmp/')

if not path.isdir(CAPTURE_DIR):
    makedirs(CAPTURE_DIR)

@app.route('/', methods=['POST'])
def index():
    # Responds to SDRTrunk's test
    if 'test' in request.form:
        print('Test received')
        return('Ok')
    elif 'callDuration' in request.form:
        # A call is coming through
        form=request.form.to_dict()
        systemId=form['systemId']
        ts=form['ts']
        tg=form['tg']
        
        with open(f'{CAPTURE_DIR}{tg}_{ts}.json', "a") as fp:
            fp.write(dumps(form, indent = 4))
        if 'enc' in request.form and request.form['enc'] == 'mp3':
            return(f'0 {MIDDLEWARE_URL}:{LISTENING_PORT}/mp3upload/{systemId}/{tg}_{ts}')
        elif 'enc' in request.form and request.form['enc'] == 'm4a': 
            return(f'0 {MIDDLEWARE_URL}:{LISTENING_PORT}/m4aupload/{systemId}/{tg}_{ts}')
        else: 
            return('1 - ERROR UNKNOWN UPLOAD')
    else:
        return('Error'), 500

@app.route('/mp3upload/<int:systemId>/<string:filename>', methods=['PUT'])
def mp3upload(systemId, filename):
    try:
        with open(f'{CAPTURE_DIR}{filename}.json') as jf:
            data=load(jf)
    except:
        return('JSON file does not exist'),500
    
    try:
        post(f'{RDIO_SCANNER_URL}/api/call-upload', files=dict(audio=request.data, audioName=f'{filename}.mp3', dateTime=data['ts'], talkgroup=data['tg'], frequency = str(float(data['freq'])*10e5).split('.')[0], source=data['src'], system=systemId, key=data['apiKey']))
    except:
        return('Upload to Rdio-Scanner failed.'),500
    try:
        remove(f'{CAPTURE_DIR}{filename}.json') # Removes both the .json file
    except:
        return('Could not remove JSON file.'),500
    return Response('200', mimetype='audio/mpeg')


if __name__=="__main__":
    app.run(host=getenv('LISTEN_ADDRESS','0.0.0.0'), port=getenv('LISTEN_PORT','8080'))