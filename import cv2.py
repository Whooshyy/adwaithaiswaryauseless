import cv2
import pygame
import mediapipe as mp
import random
import time

pygame.mixer.init()
goofyaah_sounds = ["67.mp3","faah.mp3","sus.mp3"]

cam = cv2.VideoCapture(0)
hand_detect = mp.solutions.hands
hands = hand_detect.Hands(max_num_hands=2, min_detection_confidence=0.7)

last_trigger_time = 0
cooldown = 2

while cam.isOpened():
    success, frame = cam.read()
    if not success:
        break
    frame = cv2.flip(frame, 1)
    rgbframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgbframe)
    current_time = time.time()

    if results.multi_hand_landmarks:
        cv2.putText(frame, "KEEP YOUR HANDS TO YOURSELF GNG!!", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
    
        if current_time - last_trigger_time > cooldown:
            sound_play = random.choice(goofyaah_sounds)
            pygame.mixer.music.load(sound_play)
            pygame.mixer.music.play()
            last_trigger_time = current_time

    cv2.imshow("im going to the HR SIMULATOR", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cam.release()
cv2.destroyAllWindows()
pygame.quit()




