import cv2
from decouple import config

from classes.ws import WebServer
from classes.camera import VideoCamera
from classes.recognize import Recognize

class App():

    def __init__(self):
        camera = VideoCamera()
        web_server = WebServer(camera)
        recognize = Recognize(camera)

        web_server.main()
        recognize.main()


        while(True):
            pass