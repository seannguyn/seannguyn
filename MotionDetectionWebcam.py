#import
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

# capture the video
videoCapture = VideoStream(src=0).start()
time.sleep(2)

# read the first frame
frame1 = videoCapture.read()

# read the second frame
frame2 = videoCapture.read()

while True:

    # diffFrame = background subtraction between 2 frames
    diffFrame = cv2.absdiff(frame2, frame1)

    # convert diffFrame to greyScaleFrame
    greyScaleFrame = cv2.cvtColor(diffFrame, cv2.COLOR_BGR2GRAY)

    # greyScaleFrame = gaussFrame
    gaussFrame = cv2.GaussianBlur(greyScaleFrame, (21,21), 0)

    # threshold
    _, thresholdFrame = cv2.threshold(gaussFrame, 25, 255, cv2.THRESH_BINARY)

    # dilate
    dilateFrame = cv2.dilate(thresholdFrame, None, iterations=3)

    # find contours
    contours, _ = cv2.findContours(dilateFrame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if (cv2.contourArea(contour) < 500):
            continue

        cv2.rectangle(frame1, (x,y), (x + w, y + h), (0,255,0), 2)
        cv2.putText(frame1, "Status: {}".format("Movement"), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

    # show the video feed
    cv2.imshow("Video Feed", frame1)

    # update frame1, frame2
    frame1 = frame2
    frame2 = videoCapture.read()

    key = cv2.waitKey(1) & 0xFF
    # If the 'q' key is pressed, break from the loop
    if key == ord('q'):
        break

cv2.destroyAllWindows()
videoCapture.release()