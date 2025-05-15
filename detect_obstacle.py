import cv2
import numpy as np
# from playsound import playsound  # Optional: Uncomment if you want sound alerts

# Load the game area image
img = cv2.imread("game_area.png")

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply inverted threshold to highlight dark obstacles
_, thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY_INV)

# Define Region of Interest (ROI) in front of the player
roi = thresh[300:370, 440:510]  # (y1:y2, x1:x2)

# Draw the ROI on the original image for visual feedback
cv2.rectangle(img, (440, 300), (510, 370), (0, 255, 0), 2)

# Find contours in the ROI
contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

obstacle_detected = False

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 300:  # Filter out small noise
        obstacle_detected = True
        x, y, w, h = cv2.boundingRect(cnt)
        
        # Classify obstacle: jump or slide
        if h > 25:  # Adjust this value based on testing
            action = "🚨 Obstacle ahead! Jump!"
            color = (0, 0, 255)
        else:
            action = "⚠️ Obstacle ahead! Slide!"
            color = (0, 255, 255)
        
        # Optional: play sound
        # playsound("alert.mp3")
        
        # Draw feedback text on the image
        cv2.putText(img, action, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        break

if not obstacle_detected:
    cv2.putText(img, "✅ Path is clear!", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Show images
cv2.imshow("Thresholded", thresh)
cv2.imshow("Region of Interest", img)
cv2.imshow("ROI", roi)

cv2.waitKey(0)
cv2.destroyAllWindows()
