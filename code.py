import speech_recognition as sr
import pyttsx3
import os
import time
# import the necessary packages
from imutils.video import FPS
import numpy as np
import imutils
import dlib
import cv2



def objectdetection(obj):
    # load model
	prototxt='mobilenet_ssd/MobileNetSSD_deploy.prototxt'
	model='mobilenet_ssd/MobileNetSSD_deploy.caffemodel'
	labels=obj

	#confidence level of model
	confidence=0.7

	#video input either stream or video file
	#video = 0
	video= 'input/cat.mp4'


	# initialize the list of class labels MobileNet SSD was trained to
	# detect
	CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
		"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
		"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		"sofa", "train", "tvmonitor"]

	# load model from disk
	print("[INFO] loading model...")
	net = cv2.dnn.readNetFromCaffe(prototxt, model)

	# initialize the video stream, dlib correlation tracker, output video
	# writer, and predicted class label
	print("[INFO] starting video stream...")
	vs = cv2.VideoCapture(video)
	tracker = None
	writer = None
	label = ""

	# start the frames per second throughput estimator
	fps = FPS().start()

	# loop over frames from the video file stream
	while True:
		# grab the next frame from the video file
		(grabbed, frame) = vs.read()

		# check to see if we have reached the end of the video file
		if frame is None:
			break

		# resize the frame for faster processing and then convert the
		# frame from BGR to RGB ordering (dlib needs RGB ordering)
		frame = imutils.resize(frame, width=600)
		rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


		# if our correlation object tracker is None we first need to
		# apply an object detector to seed the tracker with something
		# to actually track
		if tracker is None:
			# grab the frame dimensions and convert the frame to a blob
			(h, w) = frame.shape[:2]
			blob = cv2.dnn.blobFromImage(frame, 0.007843, (w, h), 127.5)

			# pass the blob through the network and obtain the detections
			# and predictions
			net.setInput(blob)
			detections = net.forward()

			# ensure at least one detection is made
			if len(detections) > 0:
				# find the index of the detection with the largest
				# probability -- out of convenience we are only going
				# to track the first object we find with the largest
				# probability; future examples will demonstrate how to
				# detect and extract *specific* objects
				i = np.argmax(detections[0, 0, :, 2])

				# grab the probability associated with the object along
				# with its class label
				conf = detections[0, 0, i, 2]
				label = CLASSES[int(detections[0, 0, i, 1])]

				# filter out weak detections by requiring a minimum
				# confidence
				if conf > confidence and label == labels:
					# compute the (x, y)-coordinates of the bounding box
					# for the object
					box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
					(startX, startY, endX, endY) = box.astype("int")

					# construct a dlib rectangle object from the bounding
					# box coordinates and then start the dlib correlation
					# tracker
					tracker = dlib.correlation_tracker()
					rect = dlib.rectangle(startX, startY, endX, endY)
					tracker.start_track(rgb, rect)

					# draw the bounding box and text for the object
					cv2.rectangle(frame, (startX, startY), (endX, endY),
						(0, 255, 0), 2)
					cv2.putText(frame, label, (startX, startY - 15),
						cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

		# otherwise, we've already performed detection so let's track
		# the object
		else:
			# update the tracker and grab the position of the tracked
			# object
			tracker.update(rgb)
			pos = tracker.get_position()

			# unpack the position object
			startX = int(pos.left())
			startY = int(pos.top())
			endX = int(pos.right())
			endY = int(pos.bottom())

			# draw the bounding box from the correlation object tracker
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				(0, 255, 0), 2)
			cv2.putText(frame, label, (startX, startY - 15),
				cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
   
			cv2.line(frame,(startX,endX),(startY,endY),(255,0,0),)
				
		# check to see if we should write the frame to disk
		if writer is not None:
			writer.write(frame)

		# show the output frame
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

		# update the FPS counter
		fps.update()

	# stop the timer and display FPS information
	fps.stop()
	print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

	# check to see if we need to release the video writer pointer
	if writer is not None:
		writer.release()

	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.release()
objectdetection("cat")


duration = 0.5
freq = 440
engine = pyttsx3.init()
engine.setProperty('rate', 150)
#engine.setProperty('voice', 'english+f1')
def beep() :
	os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
	

# Speech to Text conversion using google API
engine.say("Welcome to the Navigation assistant. Speak help me to activate")
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


