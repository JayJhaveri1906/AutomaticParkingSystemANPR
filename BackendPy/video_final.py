# importing libraries 
import cv2
import numpy as np
import imutils
import sys
import pytesseract
import pandas as pd
import time
import argparse
import os.path
import sqlite3
from sqlite3 import Error
import pyperclip
# import trialtrial
from PyQt5 import QtCore, QtGui, QtWidgets
import compare

global final
final = 0
# Estatablising Database
conn = sqlite3.connect('database.db')
c1 = conn.cursor()
# Initialize the parameters
confThreshold = 0.5  # Confidence threshold
nmsThreshold = 0.4  # Non-maximum suppression threshold
inpWidth = 416  # 608     #Width of network's input image
inpHeight = 416  # 608     #Height of network's input image

currentFrame = 0

# Give the configuration and weight files for the model and load the network using them.

modelConfiguration = "darknet-yolov3.cfg";
modelWeights = "lapi.weights";

net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


# Searching in Database
def read(text):
    conn = sqlite3.connect('database.db')
    c1 = conn.cursor()
    c1.execute('SELECT * FROM number_plate where plate_number=?', (text,))
    r = c1.fetchone()
    if (r != None):
        print("Number Plate Detected")
        print("The details of the Car Owner are as follows:")
        print("1. Number_Plate = " +r[0])
        print("2. Name Of the Car Owner : " +r[1])
        print("3. Phone_number : " +str(r[2]))
        print("4. Address : " +r[3])
        # trialtrial.Ui_Dialog().lineEdit_2.setText("Number Plate Detected\n" +
        #                                              "The details of the Car Owner are as follows:\n" +
        #                                              "1. Number_Plate = " + r[0] + "\n" +
        #                                              "2. Name Of the Car Owner : " + r[1] + "\n" +
        #                                              "3. Phone_number : " + str(r[2]) + "\n" +
        #                                              "4. Address : " + r[3])


    else:
        print("Unauthorized vehicle")


# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


# Draw the predicted bounding box
def drawPred(frame, classId, conf, left, top, right, bottom,myFlag):
    # Draw a bounding box.
    # cv2.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 3)
    print(top, left, bottom, right)
    # Display the resulting frame 
    cv2.imshow('Frame', frame.astype(np.uint8))
    name = 'frame' + str(currentFrame) + '.jpg'
    # frame[y:y+h, x:x+w]
    cv2.imwrite('D:\\Main projectssssss\\sih\\tempProgs\\final\\Frames\\' + name, frame[top:bottom, left:right])
    image = cv2.imread("D:\\Main projectssssss\\sih\\tempProgs\\final\\Frames\\" + name)
    cv2.imshow("Original Image", image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    pytesseract.pytesseract.tesseract_cmd = 'D:\\softwares\\Tesseract-ocr\\tesseract.exe'
    # Run tesseract OCR on image
    text = pytesseract.image_to_string(gray, lang='eng')

    # initializing bad_chars_list 
    # bad_chars = [";", ':', '!', "*", ',', '.', ' ']
    bad_chars = [";", ':', '!', "*", ',', '.', ' ', '/', '\\', '@', '#', '$', '`', '~', '%',
                 '^', '&', '(', ')', '-', '+', '<', '>', '?', '\'', '\"', ' ', "“", "=", "[","]",
                 "{","}","~",'‘']
    text = ''.join(i for i in text if not i in bad_chars)
    text = text[-1:-11:-1]
    text = text[::-1]
    # Print recognized text
    # print("recognised: -", text)
    # Searching in database

    # read(text)
    print("Plate : ", text)
    # flagEntryExit = 0
    global final
    if myFlag==1:
        final = compare.whenEntery(text)
        # return flagEntryExit
    else :
        final = compare.whenExit(text)
        # return flagEntryExit


# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs, path, myFlag):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    classIds = []
    confidences = []
    boxes = []
    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        print("out.shape : ", out.shape, end=" ")
        for detection in out:
            # if detection[4]>0.001:
            scores = detection[5:]
            classId = np.argmax(scores)
            # if scores[classId]>confThreshold:
            confidence = scores[classId]
            if detection[4] > confThreshold:
                print(detection[4], " - ", scores[classId], " - th : ", confThreshold)
                print(detection)
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        if myFlag==1:
            drawPred(frame, classIds[i], confidences[i], left, top, left + width, top + height, myFlag)
        else :
            drawPred(frame, classIds[i], confidences[i], left, top, left + width, top + height, myFlag)


def main(path,myFlag):
    currentFrame = 0

    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture(path)

    # Check if camera opened successfully 
    if (cap.isOpened() == False):
        print("Error opening video  file")

    # Read until video is completed 
    while (cap.isOpened()):
        cap.set(cv2.CAP_PROP_POS_MSEC, 200 * currentFrame + 200)
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:

            # Create a 4D blob from a frame.
            blob = cv2.dnn.blobFromImage(frame, 1 / 255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)

            # Sets the input to the network
            net.setInput(blob)

            # Runs the forward pass to get output of the output layers
            outs = net.forward(getOutputsNames(net))

            scale_percent = 45  # percent of original size
            width = 1055
            height = 349
            dim = (width, height)
            # resize image
            resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            winname = "Frame"
            cv2.namedWindow(winname)  # Create a named window
            cv2.moveWindow(winname, 424, 559)  # Move it to (40,30)
            cv2.imshow(winname, resized)
            cv2.imshow('Frame', resized)
            # Remove the bounding boxes with low confidence
            # flagFinal = postprocess(frame, outs, path)
            postprocess(frame, outs, path, myFlag)
            global final
            if final == 1:
                print("successssss :)")
                final=0
                break

            # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the timings for each of the layers(in layersTimes)
            t, _ = net.getPerfProfile()
            label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
            # cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
            currentFrame += 1

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    # When everything done, release  
    # the video capture object 
    cap.release()

    # Closes all the frames 
    cv2.destroyAllWindows()

def forDesign(button):
    # path = "D:\\Main projectssssss\\sih\\sampleStuff\\vid\\20200117_131656_1.mp4"
    # path = 0
    path = "D:\\Main projectssssss\\sih\\sampleStuff\\vid\\workingVid.mp4"
    main(path, button)

# main()
if __name__=="__main__":
    while True:
        print("press entry/exit(1/0) button")
        # path = "D:\\Main projectssssss\\sih\\sampleStuff\\vid\\20200117_131656_1.mp4"
        # path = 0
        path = "D:\\Main projectssssss\\sih\\sampleStuff\\vid\\workingVid.mp4"
        button = int(input())
        # if else is not needed am dumb
        if button == 1:
            main(path,button)
        else :
            main(path,button)
