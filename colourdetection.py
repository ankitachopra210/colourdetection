import cv2 as cv
import numpy as np 
from PIL import Image as img

pink= [203, 192, 255]  
cap = cv.VideoCapture(0)
def get_limits(color):
    c = np.uint8([[color]])  # Convert BGR to NumPy array
    hsvC = cv.cvtColor(c, cv.COLOR_BGR2HSV)  # Convert to HSV
    hue = hsvC[0][0][0]  # Get the hue value

    # Handle red hue wrap-around
    if hue >= 165:  
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 15:  
        lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    else:
        lowerLimit = np.array([max(hue - 10, 0), 100, 100], dtype=np.uint8)
        upperLimit = np.array([min(hue + 10, 180), 255, 255], dtype=np.uint8)

    return lowerLimit, upperLimit
while True:
    ret,frame= cap.read()
    hsvimage= cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    lowerLimit,upperLimit= get_limits(color=pink)
   
    mask = cv.inRange(hsvimage, lowerLimit, upperLimit)

    mask_ = img.fromarray(mask)

    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox

        frame = cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    cv.imshow('frame', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv.destroyAllWindows()

