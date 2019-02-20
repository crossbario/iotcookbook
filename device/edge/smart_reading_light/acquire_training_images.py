## capture a sequence of images from a webcam

import numpy as np
import cv2

cap = cv2.VideoCapture(1)

j = 0
for i in range(100):
    ret, frame = cap.read()
    if j >= 5:
        cv2.imwrite('img_{}.png'.format(i), frame)
        j =0
    j +=1
exit()

# When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()
