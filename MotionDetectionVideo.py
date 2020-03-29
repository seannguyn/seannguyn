from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

# open the clip
videoCapture = cv2.VideoCapture("Untitled.mp4")
# videoCapture = VideoStream(src=0).start()

# read frame1
_, frame1 = videoCapture.read()

# read frame2
_, frame2 = videoCapture.read()

# while the clip is still running
while videoCapture.isOpened():

    # diff
    diff = cv2.absdiff(frame1, frame2)

    # convert to grey scale
    greyScale = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # gausSmooth to remove all the noise
    gaussFrame = cv2.GaussianBlur(greyScale, (5,5), 0)

    # threshold
    _, threthold = cv2.threshold(gaussFrame, 25, 255, cv2.THRESH_BINARY)

    # dilate
    dilate = cv2.dilate(threthold, None, iterations=3)

    # contours = findcontours
    contours, _ = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 500:
            continue

        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)

    cv2.imshow("feed", frame1)

    # update frame1, frame2
    frame1 = frame2
    _, frame2 = videoCapture.read()

    key = cv2.waitKey(1) & 0xFF
    # If the 'q' key is pressed, break from the loop
    if key == ord('q'):
        break

cv2.destroyAllWindows()
videoCapture.release()