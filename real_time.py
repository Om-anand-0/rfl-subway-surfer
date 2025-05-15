import cv2
import numpy as np
import mss
import time

# Define screen region to capture (tune based on your monitor & game window)
monitor = {
    "top": 150,      # Y position
    "left": 300,     # X position
    "width": 600,    # Width of capture
    "height": 400    # Height of capture
}

# Define ROI relative to the monitor box
roi_top = 200
roi_left = 260
roi_height = 70
roi_width = 70

with mss.mss() as sct:
    while True:
        start = time.time()
        screenshot = np.array(sct.grab(monitor))

        frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY_INV)

        # Extract ROI
        roi = thresh[roi_top:roi_top+roi_height, roi_left:roi_left+roi_width]
        cv2.rectangle(frame, (roi_left, roi_top), (roi_left+roi_width, roi_top+roi_height), (0, 255, 0), 2)

        # Detect obstacle
        contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        obstacle_detected = False

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 300:
                x, y, w, h = cv2.boundingRect(cnt)
                obstacle_detected = True
                if h > 25:
                    text = "🚨 JUMP!"
                    color = (0, 0, 255)
                else:
                    text = "⚠️ SLIDE!"
                    color = (0, 255, 255)
                break

        if not obstacle_detected:
            text = "✅ CLEAR"
            color = (0, 255, 0)

        cv2.putText(frame, text, (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.imshow("Game Detection", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        # Print FPS (optional)
        # print("FPS:", round(1 / (time.time() - start), 2))

cv2.destroyAllWindows()
