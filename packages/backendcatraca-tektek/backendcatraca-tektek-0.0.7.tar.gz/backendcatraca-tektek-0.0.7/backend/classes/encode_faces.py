from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

from decouple import config

DATASET= 'face_recognition/dataset'
ENCODIGS = 'face_recognition/encodings_making.pickle'
DETECTION_METHOD='hog'

class EncodeFace():
	
	def __init__(self):
		# grab the paths to the input images in our dataset
		print("[INFO] quantifying faces...")
		self.imagePaths = list(paths.list_images(DATASET))

		# initialize the list of known encodings and known names
		self.knownEncodings = []
		self.knownNames = []

	def enconde(self):
		# loop over the image paths
		try:
			for (i, imagePath) in enumerate(self.imagePaths):
				# extract the person name from the image path
				print("[INFO] processing image {}/{}".format(i + 1,
					len(self.imagePaths)))
				name = imagePath.split(os.path.sep)[-2]
				print(imagePath)
				# load the input image and convert it from RGB (OpenCV ordering)
				# to dlib ordering (RGB)
				image = cv2.imread(imagePath)
				rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

				# detect the (x, y)-coordinates of the bounding boxes
				# corresponding to each face in the input image
				boxes = face_recognition.face_locations(rgb,model=DETECTION_METHOD)

				# compute the facial embedding for the face
				encodings = face_recognition.face_encodings(rgb, boxes)

				# loop over the encodings
				for encoding in encodings:
					# add each encoding + name to our set of known names and
					# encodings
					self.knownEncodings.append(encoding)
					self.knownNames.append(name)

			# dump the facial encodings + names to disk
			print("[INFO] serializing encodings...")
			data = {"encodings": self.knownEncodings, "names": self.knownNames}
			f = open(ENCODIGS, "wb")
			f.write(pickle.dumps(data))
			f.close()
			message = {"status": True,
						"message":"Finish"
			}

			return message
		except Exception as e:
			message = {"status": True,
						"message": str(e)
			}			
			print(str(e))
			return message