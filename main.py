import cv2
import numpy as np
import math
import mediapipe as mp
import pyautogui
import time

# Initialize volume control parameters
volume = 50  # Initial volume level
max_volume = 100
min_volume = 0
vol_increment = 5  # Volume increment percentage
vol_range = max_volume - min_volume

# Initialize hand tracking
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize webcam
cap = cv2.VideoCapture(0)

# Set screen width and height
screen_width, screen_height = pyautogui.size()

# Define hand landmarks for volume control
thumb_tip_id = 4
index_finger_tip_id = 8
middle_finger_tip_id = 12
ring_finger_tip_id = 16
thumb_base_id = 2
index_finger_base_id = 5

# Define gesture thresholds
gesture_distance_threshold = 50
next_track_distance_threshold = 40  # Threshold for next track gesture
prev_track_distance_threshold = 40  # Threshold for previous track gesture

# Initialize gesture variables
previous_gesture = None
gesture_start_time = time.time()

while True:
    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a mirrored view
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and detect hands
    results = hands.process(image_rgb)

    # Draw hand landmarks on the frame
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get coordinates for volume and play/pause gestures
            thumb_tip = hand_landmarks.landmark[thumb_tip_id]
            index_finger_tip = hand_landmarks.landmark[index_finger_tip_id]
            middle_finger_tip = hand_landmarks.landmark[middle_finger_tip_id]
            ring_finger_tip = hand_landmarks.landmark[ring_finger_tip_id]

            # Convert thumb, index, middle, and ring finger coordinates to screen coordinates
            thumb_x, thumb_y = int(thumb_tip.x * screen_width), int(thumb_tip.y * screen_height)
            index_x, index_y = int(index_finger_tip.x * screen_width), int(index_finger_tip.y * screen_height)
            middle_x, middle_y = int(middle_finger_tip.x * screen_width), int(middle_finger_tip.y * screen_height)
            ring_x, ring_y = int(ring_finger_tip.x * screen_width), int(ring_finger_tip.y * screen_height)

            # Calculate distance between thumb and index finger for volume control
            distance = math.sqrt((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2)

            # Calculate distances for next and previous track gestures
            thumb_middle_distance = math.sqrt((middle_x - thumb_x) ** 2 + (middle_y - thumb_y) ** 2)
            thumb_ring_distance = math.sqrt((ring_x - thumb_x) ** 2 + (ring_y - thumb_y) ** 2)

            # Map the distance to the volume range
            volume = np.interp(distance, [0, screen_width], [min_volume, max_volume])
            volume = int(volume)

            # Determine the gesture based on the distance
            if distance < gesture_distance_threshold:
                current_gesture = 'CLOSED'
            else:
                current_gesture = 'OPEN'

            # Perform actions based on gestures
            if current_gesture != previous_gesture:
                if current_gesture == 'CLOSED':
                    gesture_start_time = time.time()
                elif current_gesture == 'OPEN':
                    gesture_duration = time.time() - gesture_start_time

                    if gesture_duration < 1.0:  # Play/pause if gesture duration is short
                        pyautogui.press('playpause')
                    elif gesture_duration > 1.0 and gesture_duration < 4:  # Adjust volume if gesture duration is medium
                        vol_change = (vol_range * vol_increment) / 100
                        pyautogui.press('volumeup', presses=int(vol_change))
                    else:  # Volume down gesture for long hold
                        vol_change = (vol_range * vol_increment) / 100
                        pyautogui.press('volumedown', presses=int(vol_change))

            # Perform next track action based on thumb and middle finger distance
            if thumb_middle_distance < next_track_distance_threshold and current_gesture == 'OPEN':
                pyautogui.press('nexttrack')


            # Perform previous track action based on thumb and ring finger distance
            if thumb_ring_distance < prev_track_distance_threshold and current_gesture == 'OPEN':
                pyautogui.press('prevtrack')


            previous_gesture = current_gesture

    # Show the frame
    cv2.imshow('Hand Gesture Media Control', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy windows
cap.release()
cv2.destroyAllWindows()
