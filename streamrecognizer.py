from cv2 import cv2
from threading import Thread
import time
import numpy as np
import pickle
import imutils
import face_recognition
from faces import Faces as faces

data = pickle.loads(
    open("ml/encoder", "rb").read())
faceClass = cv2.CascadeClassifier(
    'ml/haarcascade_frontalface_default.xml')


class StreamRecognizer:

    def __init__(self):
        print("init")
        self.video = cv2.VideoCapture(0)
        time.sleep(2.0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        # lê e converte o frame de BGR para RGB e redimensiona o width para 500px (acelera o processamento)
        ret, frame = self.video.read()
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # executa a detecção de faces
        rects = faceClass.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # ajusta as medidas do rosto para TOP,RIGHT,BOTTOM,LEFT
        rostos = [(y, x+w, y+h, x) for (x, y, w, h) in rects]

        # classifica
        encodings = face_recognition.face_encodings(rgb, rostos)
        names = []

        for encoding in encodings:
            # faz a tentativa de match entre o input e os encodings existentes
            matches = face_recognition.compare_faces(
                data["encodings"], encoding)
            name = "Unknown"

            if True in matches:
                # cria um dicionário com os pontos que combinaram na comparação
                matchedIds = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                # loop over the matched indexes and maintain a count for
                # each recognized face face
                print('[INFO] matches in frame:' + str(len(matchedIds)))
                if(len(matchedIds) > 50):
                    for i in matchedIds:
                        name = data["nomes"][i]
                        counts[name] = counts.get(name, 0) + 1
                        # determine the recognized face with the largest number
                        # of votes (note: in the event of an unlikely tie Python
                        # will select first entry in the dictionary)
                        name = max(counts, key=counts.get)

                        # atualiza lista de nomes
                        names.append(name)
                        # exibe a caixa com nome reconhecido em volta do rosto
                    faces.showFaces(frame, rostos, name, names)
                else:
                    # exibe a caixa com nome UNKNOWN em volta do rosto
                    print('[INFO] matches in frame:' + str(len(matchedIds)))
                    faces.showFaces(frame, rostos, name, None)
            else:
                # exibe a caixa com nome UNKNOWN em volta do rosto
                print('[INFO] no matches found')
                faces.showFaces(frame, rostos, name, None)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
