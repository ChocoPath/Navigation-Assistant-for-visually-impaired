import speech_recognition as sr
import pyttsx3
import os
import time
# import the necessary packages
from imutils.video import FPS
from imutils.video import VideoStream
import numpy as np
import imutils
import dlib
import cv2
import math



def objectdetection(obj):
    # load model
	prototxt='mobilenet_ssd/MobileNetSSD_deploy.prototxt'
	model='mobilenet_ssd/MobileNetSSD_deploy.caffemodel'
	labels=obj

	#confidence level of model
	conf=0.7

	#video input either stream or video file
	video = 0
	#video= 'input/cat.mp4'



	# initialize the list of class labels MobileNet SSD was trained to
	# detect
	CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
		"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
		"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		"sofa", "train", "tvmonitor"]
 
	
	COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))


	# load model from disk
	print("[INFO] loading model...")
	net = cv2.dnn.readNetFromCaffe(prototxt, model)

	# initialize the video stream, dlib correlation tracker, output video
	# writer, and predicted class label
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	tracker = None
	writer = None
	label = ""

	# start the frames per second throughput estimator
	fps = FPS().start()

	
	frame_width = 600
	user_x = frame_width/2
	user_y = frame_width
	while True:
		# grab the next frame from the video file
		frame = vs.read()

		# resize the frame for faster processing and then convert the
		frame = imutils.resize(frame,width=frame_width)
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
			0.007843, (300, 300), 127.5)
  
		# pass the blob through the network and obtain the detections
		# and predictions
		net.setInput(blob)
		detections = net.forward()
		fl=False
		for i in np.arange(0, detections.shape[2]):
			confidence = detections[0, 0, i, 2]
			if confidence >conf:
				idx = int(detections[0, 0, i, 1])
				if obj in CLASSES[idx] :
					fl=True
					box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
					(startX, startY, endX, endY) = box.astype("int")

					label = "{}: {:.2f}%".format(CLASSES[idx],
						confidence * 100)
					cv2.rectangle(frame, (startX, startY), (endX, endY),
						COLORS[idx], 2)
					y = startY - 15 if startY - 15 > 15 else startY + 15
					cv2.putText(frame, label, (startX, y),
						cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
					centerX = (endX+startX)/2
					centerY = (endY+startY)/2
					cv2.line(frame,(int(user_x),int(user_y)),(int(centerX),int(centerY)),(255,0,0),7)
					dir =0
					if centerX > user_x :
						dir =1
					elif centerX < user_x :
						dir = -1
					deg = math.degrees(math.atan(abs(centerX-user_x)/abs(centerY-user_y)))
					
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1)  & 0xFF
		if key == ord("q"):
			break		
		fps.update()

	fps.stop()
	print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
	cv2.destroyAllWindows()
	vs.stop()
	return fl,deg,dir

duration = 0.5
freq = 440
engine = pyttsx3.init()
engine.setProperty('rate', 150)
#engine.setProperty('voice', 'english+f1')

	
# Speech to Text conversion using google API
engine.say("Welcome to the Navigation assistant. Say help me to activate")
engine.runAndWait()
r = sr.Recognizer()
with sr.Microphone() as source:
	wakeup = False
	r.adjust_for_ambient_noise(source)
	wakeString = r.listen(source)
	wakeStringFinal = ""
	try:
		wakeStringFinal = r.recognize_google(wakeString)
	except:
		wakeStringFinal= "help me"
	if wakeStringFinal == "help me" :
		count = 0
		wakeup = True
		while count<5 and wakeup == True:
			engine.say("activated")
			engine.runAndWait()
			engine.say('what do you want to find?')
			engine.runAndWait()
			audio = r.listen(source)
			try:
				query = r.recognize_google(audio)
				print(query)
				if query == "bye":
					wakeup = False
					engine.say("bye")
					engine.runAndWait()
					break
				l= query.split()
				print 
				k = l[0]
				secondArg = l[1]				
				print (k)
				print (secondArg)
				if (k=="find"):
					print("you are finding something")
					print(secondArg)
					engine.say("searching for")
					engine.runAndWait()
					engine.say(secondArg)
					engine.runAndWait()
					found = False
					found,deg,dir=objectdetection(secondArg)
					# Text to Speech conversion for output using speech
					if found== True:
						print("object found")
						direction = "ahead"
						if dir ==-1:
							direction = "left"
						elif dir ==1:
							direction = "right"
						st=str(secondArg)+" found at "+str(int(deg))+" Degree "+str(direction)
						print(st)
						engine.say(st)

						engine.runAndWait()
						wakeup = False
					else :
						print("could not find try again")
						time.sleep(1)
						engine.say("Could not find try again")
						engine.runAndWait()
						count+=1
			except:
				time.sleep(3)
				count +=1

