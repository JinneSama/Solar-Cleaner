import cv2
import numpy as np

aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
aruco_params = cv2.aruco.DetectorParameters_create()
cap = cv2.VideoCapture("rtsp://192.168.0.194/live/ch00_1")

if not cap.isOpened():
    print("Could not open webcam")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error reading frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)

    cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    if ids is not None and len(ids) > 0:
        centers = []

        for i in range(len(ids)):
            c = corners[i][0]
            x = int((c[0][0] + c[2][0]) / 2)
            y = int((c[0][1] + c[2][1]) / 2)
            centers.append((x, y))
            cv2.circle(frame, (x, y), 10, (0, 255, 0), 2)
            
        if len(ids) == 4:
            centers = sorted(centers, key=lambda x: x[0])

            group1 = [centers[0], centers[1]]
            group2 = [centers[2], centers[3]]

            pts = np.array(group1 + group2, np.int32)
            pts = pts.reshape((-1, 1, 2))
            mask = np.zeros_like(frame)

            # fill the region outside the polygon with black color
            cv2.fillPoly(mask, [pts], (255, 255, 255))
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
            masked_frame[mask == 0] = (0, 0, 0)

            # convert to HSV color space for brown color detection
            hsv = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2HSV)

            # define brown color range in HSV
            brown_lower = np.array([10, 50, 20])
            brown_upper = np.array([30, 255, 200])

            # threshold the image to get the brown color region
            brown_mask = cv2.inRange(hsv, brown_lower, brown_upper)

            # find contours in the brown mask
            contours, _ = cv2.findContours(brown_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # draw contours on the original frame
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 100:
                    cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)

            cv2.polylines(frame, [pts], True, (0, 255, 255), 2)

    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()