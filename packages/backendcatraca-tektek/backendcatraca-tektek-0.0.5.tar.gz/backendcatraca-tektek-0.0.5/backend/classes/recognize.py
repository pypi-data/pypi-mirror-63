import time
import threading
import json
import argparse
import requests 

from imutils.video import VideoStream
import face_recognition
import imutils
import pickle
import cv2
from decouple import config

from classes.utils import Utils
from classes.personmanager import PersonManager

DETECTION_METHOD=config('DETECTION_METHOD')
API_ADDRESS = config('API_ADDRESS')

class Recognize():    
    def __init__(self, camera):
        print("[INFO] loading encodings...")
        self.data = pickle.loads(open('face_recognition/encodings.pickle', "rb").read())
        self.camera = camera
        self.start_aprovation_time = 0
        self.names = []
        self.current_name =""
        self.sent_name = ""
        self.clear_names = False
        self.person = {}
        self.too_many_faces_status = False
    def detect(self):        
        # loop over frames from the video file stream
        while True:
            if (self.camera.available and self.camera.mode == 'detect'):
                # grab the frame from the threaded video stream
                frame = self.camera.image
                
                # convert the input frame from BGR to RGB then resize it to have
                # a width of 750px (to speedup processing)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb = imutils.resize(frame, width=750)
                r = frame.shape[1] / float(rgb.shape[1])

                # detect the (x, y)-coordinates of the bounding boxes
                # corresponding to each face in the input frame, then compute
                # the facial embeddings for each face
                boxes = face_recognition.face_locations(rgb, model=DETECTION_METHOD)
                encodings = face_recognition.face_encodings(rgb, boxes)
                self.names = []

                # loop over the facial embeddings
                for encoding in encodings:
                    # attempt to match each face in the input image to our known
                    # encodings
                    matches = face_recognition.compare_faces(self.data["encodings"], encoding)
                    name = "Unknown"

                    # check to see if we have found a match
                    if True in matches:
                        # find the indexes of all matched faces then initialize a
                        # dictionary to count the total number of times each face
                        # was matched
                        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                        counts = {}

                        # loop over the matched indexes and maintain a count for
                        # each recognized face face
                        for i in matchedIdxs:
                            name = self.data["names"][i]
                            counts[name] = counts.get(name, 0) + 1

                        # determine the recognized face with the largest number
                        # of votes (note: in the event of an unlikely tie Python
                        # will select first entry in the dictionary)
                        name = max(counts, key=counts.get)
                    
                    # update the list of names
                    self.names.append(name)
                                                     
                if self.too_many_faces_status == True and len(self.names) == 1:
                    self.start_aprovation_time = time.time()
                    self.clear_detected_name()
                    self.too_many_faces_status = False

                if len(self.names) == 1 and self.names[0] != 'Unknown':    
                    self.send_detected_name()
                    self.approve_recognition()
                    
                elif len(self.names) > 1:
                    message = {
                        "action":  "too_many_faces",
                        "status":  True
                    }
                    Utils.send_message_rabbitmq('peekaboo', json.dumps(message))
                    self.too_many_faces_status = True
                    
                elif len(self.names) == 0:
                    self.start_aprovation_time = time.time()
                    self.sent_name = ""
                if len(self.names) != 0:
                    self.clear_names = False 
                elif self.clear_names == False and len(self.names) == 0:
                    self.clear_detected_name()
                

    
    def send_detected_name(self):
        if self.sent_name != self.names[0]:            

            if self.names[0] not in self.person:
                person_name = PersonManager.get_person_name(self.names[0])
                self.person[self.names[0]] = person_name            
            else:
                person_name = self.person[self.names[0]]
            message = {
            "action": "detect",
            "name": person_name,
            "cod": self.names[0]
            }
            Utils.send_message_rabbitmq('peekaboo', json.dumps(message))
            self.sent = True            
            self.sent_name = self.names[0]

    def clear_detected_name(self):        
        message = {
        "action": "clear_detected_name"            
        }
        Utils.send_message_rabbitmq('peekaboo', json.dumps(message))
        self.clear_names = True
            
    
    def approve_recognition(self):     
            if self.names[0] != self.current_name:  
                self.start_aprovation_time = time.time()
                self.current_name = self.names[0]
            else:
                delay_time = time.time() - self.start_aprovation_time
                if delay_time >= 3:

                    url = API_ADDRESS+'baterponto'

                    data = {
                        "CDFUNC": self.names[0]
                    }
                    # sending get request and saving the response as response object 
                    r = requests.post(url = url, data = data) 
                    result = r.json()

                    if result['status']:                        
                        message = {
                            "action": "approve_recognition",
                            "status": True,
                            "cod": self.names[0],
                            "idsentido": result['sentido']
                        }
                        Utils.send_message_rabbitmq('peekaboo', json.dumps(message))                        
                        time.sleep(6)
                        self.clear_detected_name()

                    else:
                        message = {
                            "action": "fail_recognition",
                            "status": True
                        }                        
                        Utils.send_message_rabbitmq('peekaboo', json.dumps(message))  
                        self.clear_detected_name()                                               
                    self.sent_name = ""
                    self.start_aprovation_time = time.time()



    def main(self):    
        t1 = threading.Thread(target=self.detect, daemon=True )
        t1.start()