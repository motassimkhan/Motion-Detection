import cv2
import numpy as np

# get video from webcam
cap = cv2.VideoCapture(0)

# Read the first frame for motion detection and manually convert it to greyscale
_, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

while True:
    # Read the current frame
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Edge detection using Sobel and Laplacian
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5) 
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5) 
    sobel = sobelx + sobely
    sobel = cv2.convertScaleAbs(sobel)  
    sobel_color = cv2.cvtColor(sobel, cv2.COLOR_GRAY2BGR) 

    # Motion detection using frame differencing
    diff = cv2.absdiff(prev_gray, gray)
    _, motion = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    motion_color = cv2.cvtColor(motion, cv2.COLOR_GRAY2BGR)

    # Update the previous frame
    prev_gray = gray

    # Combine edges and motion
    combined = cv2.addWeighted(sobel_color, 0.5, motion_color, 0.5, 0)

    cv2.imshow("Original", frame)
    cv2.imshow("Sobel Combined", sobel)
    cv2.imshow("Motion", motion)
    cv2.imshow("Combined (Edges + Motion)", combined)

    # 'Esc' key to exit
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
