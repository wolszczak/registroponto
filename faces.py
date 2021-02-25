from cv2 import cv2
import Database as db
from datetime import datetime
import time


class Faces:
    @staticmethod
    def showFaces(frame, rostos, nome, nomes):
        if nomes is None:
            nome = "UNKNOWN"
            for (top, right, bottom, left) in rostos:
                # draw the predicted face name on the image
                cv2.rectangle(frame, (left, top),
                              (right, bottom), (0, 255, 0), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, nome, (left, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        else:
            for ((top, right, bottom, left), nome) in zip(rostos, nomes):
                # draw the predicted face name on the image
                cv2.rectangle(frame, (left, top),
                              (right, bottom), (0, 255, 0), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, nome, (left, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                db.insert(nome, datetime.now())
                # time.sleep(5)
