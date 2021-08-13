import cv2
import time
import mediapipe as mp
# import os
# import Class_HandTrack as C_HandTrack

# https://www.kiloo.com/subway-surfers/
import pyautogui

wCam, hCam = 640, 480
wCam_Half= int(wCam/2)
hCam_Half= int(hCam/2)
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

MP_Draw_Solu = mp.solutions.drawing_utils
MP_Hands_Solu = mp.solutions.hands

tipIds = [4, 8, 12, 16, 20]
start_game = None
Center_X = None
Center_Y = None
Up_X = None
Up_y = None
Space_P = False
# Down_y = None

Left_Right_Con = [0, 1, 0]
Up_Down_Con = [0,1,0]
Idx_Con_UD=1

Idx_Con = 1
totalFingers_right = 0

Hands = MP_Hands_Solu.Hands(max_num_hands=2, min_tracking_confidence=0.5, min_detection_confidence=0.5)

while True:
    success, image = cap.read()
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results_hands = Hands.process(image)

    LM_list_Right_Hand = []
    LM_list_Left_Hand = []
    finger_count_Right_Hand = []
    hand_type1 = None
    hand_type2 = None

    # try:
    if results_hands.multi_handedness:
        for hand_number, hand_LM in enumerate(results_hands.multi_hand_landmarks):
            if hand_number==0:
                hand_type1 = results_hands.multi_handedness[0].classification[0].label
                if hand_type1 == 'Left':
                    for id, LM in enumerate(hand_LM.landmark):
                        cx, cy = int(LM.x * wCam), int(LM.y * hCam)
                        # cv2.circle(image, (cx, cy), 2, (100, 255, 100), 2)
                        LM_list_Left_Hand.append([id, cx, cy])
                elif hand_type1 == 'Right':
                    for id, LM in enumerate(hand_LM.landmark):
                        cx, cy = int(LM.x * wCam), int(LM.y * hCam)
                        # cv2.circle(image, (cx, cy), 2, (100, 255, 100), 2)
                        LM_list_Right_Hand.append([id, cx, cy])
            if hand_number == 1:
                hand_type2 = results_hands.multi_handedness[1].classification[0].label
                if hand_type2 == 'Left':
                    for id, LM in enumerate(hand_LM.landmark):
                        cx, cy = int(LM.x * wCam), int(LM.y * hCam)
                        # cv2.circle(image, (cx, cy), 2, (100, 255, 100), 2)
                        LM_list_Left_Hand.append([id, cx, cy])
                elif hand_type2 == 'Right':
                    for id, LM in enumerate(hand_LM.landmark):
                        cx, cy = int(LM.x * wCam), int(LM.y * hCam)
                        # cv2.circle(image, (cx, cy), 2, (100, 255, 100), 2)
                        LM_list_Right_Hand.append([id, cx, cy])
        if LM_list_Right_Hand != []:
            # Nhan dang ngon tay cai
            if LM_list_Right_Hand[tipIds[0]][1] < LM_list_Right_Hand[tipIds[0] - 1][1]:
                finger_count_Right_Hand.append(1)
            else:
                finger_count_Right_Hand.append(0)
            # Nhan dang 4 ngon tay con lai co mo hay khong
            for id in range(1, 5):
                if LM_list_Right_Hand[tipIds[id]][2] < LM_list_Right_Hand[tipIds[id] - 2][2]:
                    finger_count_Right_Hand.append(1)
                else:
                    finger_count_Right_Hand.append(0)
            totalFingers_right = finger_count_Right_Hand.count(1)
            # print(totalFingers_right)

            if totalFingers_right == 2 and finger_count_Right_Hand[1]==1 and finger_count_Right_Hand[2]==1 and start_game == None:
                print("Bat dau")
                start_game = 20
                Space_P = True
                xL_C=LM_list_Right_Hand[tipIds[2]][1]
                yL_C=LM_list_Right_Hand[tipIds[2]][2]
                # cv2.circle(image,(xL_C,yL_C),5,(0,0,255),2)

                xR_C = LM_list_Right_Hand[0][1]
                yR_C = LM_list_Right_Hand[0][2]
                # cv2.circle(image, (xR_C, yR_C), 5, (0, 0, 255), 2)
                # cv2.line(image, (xL_C, yL_C), (xR_C, yR_C), (255, 0, 255), 4)

                Center_X = xL_C + int(abs(xL_C - xR_C)/2)
                Center_Y = yR_C - int(abs(yL_C - yR_C)/2)

            if start_game != None:

                cv2.circle(image, (Center_X, Center_Y), 10, (255, 255, 0), 5)

                xL = LM_list_Right_Hand[5][1]
                yL = LM_list_Right_Hand[5][2]

                xR = LM_list_Right_Hand[17][1]
                yR = LM_list_Right_Hand[17][2]

                Up_X = xL + int(abs(xR - xL)/2)
                Up_y = int((yL + yR)/2)
                if finger_count_Right_Hand==3 and finger_count_Right_Hand[0]==1\
                        and finger_count_Right_Hand[1]==1 and finger_count_Right_Hand[2]==1:
                    start_game = None
                    print(start_game)
                if xR < (Center_X-80) and Idx_Con >0 and Left_Right_Con[Idx_Con-1] == 0:
                    Left_Right_Con[Idx_Con] = 0
                    Left_Right_Con[Idx_Con - 1]= 1
                    Idx_Con -=1
                    pyautogui.press('left')
                    print("Left", Left_Right_Con)
                if xL > (Center_X+80) and Idx_Con<2 and Left_Right_Con[Idx_Con+1] ==0:
                    Left_Right_Con[Idx_Con] = 0
                    Left_Right_Con[Idx_Con + 1] = 1
                    Idx_Con += 1
                    pyautogui.press('right')
                    print("Right", Left_Right_Con)
                if xR > (Center_X-40) and xL < (Center_X+40) and Idx_Con==0:
                    Left_Right_Con[Idx_Con]=0
                    Left_Right_Con[Idx_Con+1]=1
                    Idx_Con +=1
                    # pyautogui.press('right')
                    print("Left to Center", Left_Right_Con)
                if xR > (Center_X-40) and xL < (Center_X+40) and Idx_Con==2:
                    Left_Right_Con[Idx_Con] = 0
                    Left_Right_Con[Idx_Con - 1] = 1
                    Idx_Con -= 1
                    # pyautogui.press('left')
                    print("Right to Center", Left_Right_Con)
                # cv2.line(image, (Up_X, Up_y), (Center_X, Center_Y), (255, 255, 255), 2)
                # print(Up_y, Center_Y, Up_y - Center_Y )
                if (Up_y - Center_Y) <= -80 and Idx_Con_UD>0 and Up_Down_Con[Idx_Con_UD-1] == 0:
                    Idx_Con_UD -=1
                    pyautogui.press('up')
                    print("Up")
                if (Up_y - Center_Y) >= 80 and Idx_Con_UD<2 and Up_Down_Con[Idx_Con_UD+1] == 0:
                    Idx_Con_UD +=1
                    pyautogui.press('down')
                    print("Down")
                if ((Up_y - Center_Y) >=-40) and ((Up_y - Center_Y) <=40) and Idx_Con_UD == 0:
                    Idx_Con_UD += 1
                    # pyautogui.press('down')
                    print("Up to Center - Down")
                if ((Up_y - Center_Y) >= -40) and ((Up_y - Center_Y) <= 40) and Idx_Con_UD == 2:
                    Idx_Con_UD -= 1
                    # pyautogui.press('up')
                    print("Down to Center - Up")
                if totalFingers_right == 4 and finger_count_Right_Hand[4] == 1 and Space_P == True:
                    pyautogui.press('space')
                    Space_P = False
                    print("Space press", finger_count_Right_Hand)
                if totalFingers_right == 2 and start_game != None:
                    Space_P = True

    image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imshow("Game", image)
    cv2.waitKey(1)















