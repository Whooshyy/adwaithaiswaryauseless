import cv2
import pygame
import mediapipe as mp
import random
import time

pygame.mixer.init()

goofyaah_sounds = [
    ("67.mp3", cv2.resize(cv2.imread("67.jpeg"), (220, 220))),
    ("faah.mp3", cv2.resize(cv2.imread("sadge.jpeg"), (220, 220))),
    ("sus.mp3", cv2.resize(cv2.imread("rock.jpeg"), (220, 220))),
    ("metalpipe.mp3", cv2.resize(cv2.imread("steelpipe.jpeg"), (220, 220))),
]

cam = cv2.VideoCapture(0)
hand_detect = mp.solutions.hands
hands = hand_detect.Hands(max_num_hands=2, min_detection_confidence=0.7)
pose = mp.solutions.pose
mp_pose = pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6)
baseline_nose_y = None
slouch_threshold = 60
calibration_end_time = time.time() + 3

last_trigger_time = 0
cooldown = 2
current_image = None
current_text = ""
alert_timer_end = 0

while cam.isOpened():
    success, frame = cam.read()
    if not success:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgbframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pose_results = mp_pose.process(rgbframe)
    results = hands.process(rgbframe)
    current_time = time.time()
    
    slouch_detected = False
    if pose_results.pose_landmarks:
        nose_y = int(pose_results.pose_landmarks.landmark[0].y * h)
        if current_time < calibration_end_time:
            baseline_nose_y = nose_y
        elif baseline_nose_y is not None and nose_y > baseline_nose_y + slouch_threshold:
            slouch_detected = True

    hands_detected = results.multi_hand_landmarks is not None
    violation = hands_detected or slouch_detected

    if violation and (current_time - last_trigger_time > cooldown):
        chosen_sound, chosen_image = random.choice(goofyaah_sounds)
        try:
            pygame.mixer.music.load(chosen_sound)
            pygame.mixer.music.play()
        except Exception as e:
            print("Audio error:", e)

        current_image = chosen_image
        alert_timer_end = current_time + 2.0
        last_trigger_time = current_time

    if current_time < alert_timer_end and current_image is not None:
        frame[30:250, -250:-30] = current_image

    if results.multi_hand_landmarks:
        cv2.putText(
            frame,
            "KEEP YOUR HANDS TO YOURSELF GNG!!",
            (30, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 0, 255),
            3,
        )

    cv2.imshow("im going to the HR SIMULATOR", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
pygame.quit()