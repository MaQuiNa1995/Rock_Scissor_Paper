from platform import machine
import random
import cv2
import mediapipe

# Camera OpenCV
cap = cv2.VideoCapture(0)
hands = mediapipe.solutions.hands.Hands()
mpDraw = mediapipe.solutions.drawing_utils

# Finger
finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
thumb_Coord = (4,2)

# Rentangle
start_point = (20, 18)
end_point = (500, 50)
black = (0, 0, 0)

options = ["Piedra", "Papel", "Tijera"]

while True:
    success, image = cap.read()
    RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(RGB_image)
    multiLandMarks = results.multi_hand_landmarks

    if multiLandMarks:
        handList = []
        for handLms in multiLandMarks:
            for idx, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                handList.append((cx, cy))

        upCount = 0
        playerElection = ""

        for coordinate in finger_Coord:
            if handList[coordinate[0]][1] < handList[coordinate[1]][1]:
                upCount += 1
        if handList[thumb_Coord[0]][0] > handList[thumb_Coord[1]][0]:
            upCount += 1

        if upCount == 0:
            playerElection = options[0]
        elif upCount == 5:
            playerElection = options[1]
        elif upCount== 2 and handList[8][1] < handList[6][1] and handList[12][1] < handList[10][1]:
            playerElection = options[2]

        image = cv2.rectangle(image, start_point, end_point, black, -1)
        cv2.putText(image, "Estas seguro de elegir: "+str(playerElection), (20,40), cv2.FONT_ITALIC, 1, (0,255,0), 1)

    cv2.imshow("Piedra, Papel, Tijera", image)
    if cv2.waitKey(10) == ord('s') and playerElection != "":
        break

machineElection = random.choice(options)

if (machineElection == playerElection):
    print("He elegido "+ machineElection +" asique Empate")
elif (machineElection == options[0] and playerElection == options[1]):
    print("He elegido "+ machineElection +" y tu " + playerElection + "asique Ganaste")
elif (machineElection == options[1] and playerElection == options[2]):
    print("He elegido "+ machineElection +" y tu " + playerElection + "asique Ganaste")
elif (machineElection == options[2] and playerElection == options[0]):
    print("He elegido "+ machineElection +" y tu " + playerElection + "asique Ganaste")
else:    
    print("He elegido "+ machineElection +" asique Perdiste")