from cv2 import cv2
import sys
from flask import Flask, render_template, Response, render_template, request, jsonify
from streamrecognizer import StreamRecognizer
import time
import threading
import pickle
import Database as db


app = Flask(__name__)
# app.config['BASIC_AUTH_USERNAME'] = 'pi'
# app.config['BASIC_AUTH_PASSWORD'] = 'pi'
# app.config['BASIC_AUTH_FORCE'] = True


data = pickle.loads(
    open("ml/encoder", "rb").read())
faceClass = cv2.CascadeClassifier(
    'ml/haarcascade_frontalface_default.xml')


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        # get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(StreamRecognizer()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/list', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def list():
    if request.method == 'GET':
        lista = db.list()
        array = []
        for x in lista:
            array.append({
                "id": x.id,
                "nome": x.nome,
                "data": x.data
            })
        return jsonify(array), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
