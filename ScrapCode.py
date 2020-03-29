# from imutils.video import VideoStream
# import argparse
# import datetime
# import imutils
# import time
# import cv2
#
# parse = argparse.ArgumentParser();
# parse.add_argument("-v", "--video", help="Path to a video file");
#
# args_dict = vars(parse.parse_args())
#
# # capture the video
# vid = cv2.VideoCapture(0)
# # vid = VideoStream(src=0).start()
# time.sleep(2)
# first_frame = None
# # infinite loop, keep reading the frame
# while True:
#     _, frame = vid.read()
#     text = "No Motion"
#
#     grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     gaus_frame = cv2.GaussianBlur(grey_frame, (21,21), 0)
#
#     if (first_frame is None):
#         first_frame = grey_frame
#
#     diff = cv2.absdiff(first_frame, gaus_frame)
#     thresh = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY)[1]
#
#     dilate_image = cv2.dilate(thresh, None, iterations=2)
#
#     # cnt = cv2.findContours(dilate_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
#     # # contours gives 3 diffrent ouputs image, contours and hierarchy, so using [1] on end means contours = [1](cnt)
#     # # cv2.CHAIN_APPROX_SIMPLE saves memory by removing all redundent points and comppressing the contour, if you have a rectangle
#     # # with 4 straight lines you dont need to plot each point along the line, you only need to plot the corners of the rectangle
#     # # and then join the lines, eg instead of having say 750 points, you have 4 points.... look at the memory you save!
#     #
#     # for c in cnt:
#     #     if cv2.contourArea(c) > 800:  # if contour area is less then 800 non-zero(not-black) pixels(white)
#     #         (x, y, w, h) = cv2.boundingRect(c)  # x,y are the top left of the contour and w,h are the width and hieght
#     #
#     #         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0),
#     #                       2)  # (0, 255, 0) = color R,G,B = lime / 2 = thickness(i think?)(YES IM RITE!)
#     #         # image used for rectangle is frame so that its on the secruity feed image and not the binary/threshold/foreground image
#     #         # as its already used the threshold/(binary image) to find the contours this image/frame is what image it will be drawed on
#     #
#     #         text = 'Occupied'
#     #         # text that appears when there is motion in video feed
#     #     else:
#     #         pass
#     #
#     # ''' now draw text and timestamp on security feed '''
#     # font = cv2.FONT_HERSHEY_SIMPLEX
#     #
#     # cv2.putText(frame, '{+} Room Status: %s' % (text),
#     #             (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
#     # # frame is the image on wich the text will go. 0.5 is size of font, (0,0,255) is R,G,B color of font, 2 on end is LINE THICKNESS! OK :)
#     #
#     # cv2.putText(frame, datetime.datetime.now().strftime('%A %d %B %Y %I:%M:%S%p'),
#     #             (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255),
#     #             1)  # frame.shape[0] = hieght, frame.shape[1] = width,ssssssssssssss
#     # # using datetime to get date/time stamp, for font positions using frame.shape() wich returns a tuple of (rows,columns,channels)
#     # # going 10 accross in rows/width so need columns with frame.shape()[0] we are selecting columns so how ever many pixel height
#     # # the image is - 10 so oppisite end at bottom instead of being at the top like the other text
#
#     cv2.imshow("Live Video", frame)
#     cv2.imshow('Threshold(foreground mask)', dilate_image)
#     cv2.imshow('Frame_delta', diff)
#
#     key = cv2.waitKey(1) & 0xFF # If the 'q' key is pressed, break from the loop
#     if key == ord('q'):
#         cv2.destroyAllWindows()
#         break

# Import all the packages we will be using for our program. We can come back and later add packages if needed
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="Path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="Minimum area size")
args = vars(ap.parse_args())

# If the video argument is None, let us start reading from the web cam
if args.get("video", None) is None:
    vs = VideoStream(src=0).start()
    time.sleep(2.0)

# Otherwise, if we have the video file argument, let us read from the video file
else:
    vs = cv2.VideoCapture(args["video"])

# Initialise the first frame in the video
firstFrame = None

# Start looping over the frames of the video/webcam
while True:
    # Grab the current frame and initialise the occupied/unoccupied text
    frame = vs.read()
    frame = frame if args.get("video", None) is None else frame[1]
    text = "No motion"

    # If we were not able to read the file, then we have reached the end of the video
    if frame is None:
        break

    # Resize the frame, convert it to grayscale and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # If the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    # Compute the absolute difference between the current frame and the first frame that we have already stored
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # Dilate the threshold image to fill in holes, then find contours on the thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Now that we have all the contours, let us loop over the contours
    for c in cnts:
        # If the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue

        # Compute the bounding box of the contour and draw it on the frame. Update the text accordingly
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Motion is detected"

    # Draw the text and the timestamp of when it happened on the frame
    cv2.putText(frame, "Motion status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # Show the frame and record if the user presses a key

    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame delta", frameDelta)
    cv2.imshow("Video feed", frame)

    key = cv2.waitKey(1) & 0xFF
    # If the 'q' key is pressed, break from the loop
    if key == ord('q'):
        break

# Clean up the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
