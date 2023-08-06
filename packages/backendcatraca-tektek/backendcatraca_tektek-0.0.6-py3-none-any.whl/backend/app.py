import cv2
from decouple import config

from backend.classes.ws import WebServer
from backend.classes.camera import VideoCamera
from backend.classes.recognize import Recognize

class App():

    def __init__(self):
        camera = VideoCamera()
        web_server = WebServer(camera)
        recognize = Recognize(camera)

        web_server.main()
        recognize.main()


        while(True):
            pass