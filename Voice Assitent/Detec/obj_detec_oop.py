# USAGE
# python obj_detec.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel
# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())


# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

class Model:
	def __init__(self):
		# load our serialized model from disk
		print("[INFO] loading model...")
		self.net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
		print("[INFO] starting video stream...")
		self.vs = VideoStream(src=0).start()
		time.sleep(2.0)
		self.fps = FPS().start()
	def Obj_Detec(self):
		# loop over the frames from the video stream
		while True:
			self.frame = self.vs.read()
			self.frame = imutils.resize(self.frame, width=400)
			# grab the frame dimensions and convert it to a blob
			(h, w) = self.frame.shape[:2]
			blob = cv2.dnn.blobFromImage(cv2.resize(self.frame, (300, 300)),
			0.007843, (300, 300), 127.5)
			self.net.setInput(blob)
			detections = self.net.forward()
			# loop over the detections
			for i in np.arange(0, detections.shape[2]):
				confidence = detections[0, 0, i, 2]
				if confidence > args["confidence"]:
					# extract the index of the class label from the
			        # `detections`, then compute the (x, y)-coordinates of
			        # the bounding box for the object
					idx = int(detections[0, 0, i, 1])
					box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
					(startX, startY, endX, endY) = box.astype("int")
					label = "{}: {:.2f}%".format(CLASSES[idx],confidence * 100)
					cv2.rectangle(self.frame, (startX, startY), (endX, endY),
					COLORS[idx], 2)
					y = startY - 15 if startY - 15 > 15 else startY + 15
					cv2.putText(self.frame, label, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
			# show  he output frame
			cv2.imshow("Frame", self.frame)
			key = cv2.waitKey(1) & 0xFF
			# if the `q` key was pressed, break from the loop
			if key == ord("q"):
				break
			# update the FPS counter
			self.fps.update()
	    # stop the timer and display FPS information
		self.fps.stop()
		print("[INFO] elapsed time: {:.2f}".format(self.fps.elapsed()))
		print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()))
		# do a bit of cleanup
		cv2.destroyAllWindows()
		self.vs.stop()

def main():
	obj = Model()
	obj.Obj_Detec()

if __name__ == "__main__":
	main()
