import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Get screen size for mapping
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False  # Disable failsafe for smooth operation

# Initialize variables
smoothening = 7
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0
click_threshold = 40  # Distance between fingers for click detection
scroll_threshold = 50  # Distance for scroll detection
last_click_time = 0
click_cooldown = 0.5  # Cooldown between clicks in seconds

def get_finger_distance(landmarks, idx1, idx2, frame_width, frame_height):
    """Calculate distance between two landmarks in pixels."""
    x1, y1 = landmarks[idx1].x * frame_width, landmarks[idx1].y * frame_height
    x2, y2 = landmarks[idx2].x * frame_width, landmarks[idx2].y * frame_height
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

try:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Error: Could not read frame.")
            break

        # Flip the frame horizontally for natural movement
        frame = cv2.flip(frame, 1)
        frame_height, frame_width = frame.shape[:2]

        # Convert to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks on the frame
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get index and middle finger tip coordinates
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                # Map index finger tip to screen coordinates
                x = int(index_tip.x * frame_width)
                y = int(index_tip.y * frame_height)

                # Smooth cursor movement
                curr_x = prev_x + (x - prev_x) / smoothening
                curr_y = prev_y + (y - prev_y) / smoothening

                # Map to screen coordinates
                screen_x = np.interp(curr_x, [100, frame_width-100], [0, screen_width])
                screen_y = np.interp(curr_y, [100, frame_height-100], [0, screen_height])

                # Move mouse
                pyautogui.moveTo(screen_x, screen_y)
                prev_x, prev_y = curr_x, curr_y

                # Detect click (index and thumb close together)
                thumb_index_dist = get_finger_distance(hand_landmarks, 
                                                    mp_hands.HandLandmark.INDEX_FINGER_TIP,
                                                    mp_hands.HandLandmark.THUMB_TIP,
                                                    frame_width, frame_height)

                if thumb_index_dist < click_threshold:
                    current_time = time.time()
                    if current_time - last_click_time > click_cooldown:
                        pyautogui.click()
                        last_click_time = current_time

                # Detect scroll (index and middle finger distance)
                index_middle_dist = get_finger_distance(hand_landmarks,
                                                      mp_hands.HandLandmark.INDEX_FINGER_TIP,
                                                      mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                                                      frame_width, frame_height)

                if index_middle_dist > scroll_threshold:
                    # Scroll up if middle finger is above index finger
                    if middle_tip.y < index_tip.y:
                        pyautogui.scroll(10)
                    else:
                        pyautogui.scroll(-10)

        # Display the frame
        cv2.imshow('Virtual Mouse', frame)

        # Exit on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Program terminated by user.")

finally:
    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    hands.close()