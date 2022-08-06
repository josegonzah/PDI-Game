# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cv2
import numpy as np
import random

video = cv2.VideoCapture(0)

kernel = np.ones((15, 15), np.uint8)

backGround = cv2.imread('bg2.jpg')
player = cv2.imread('mario.png')
player = cv2.resize(player, (93, 80))
coin = cv2.imread('coin.png')
coin = cv2.resize(coin, (30, 30))
backGroundHeight, backGroundWidth, backGroundCap = backGround.shape
playerHeight, playerWidth, playerCap = player.shape
coinHeight, coinWidth, coinCap = coin.shape
coinPositionYAxis = 0
coinPositionXAxis= random.randint(1,backGroundWidth-coinWidth)
score=0
scoreAux=0
loses = 0

cv2.waitKey(0)
cv2.destroyAllWindows()

while True:
    check,frame=video.read()
    frame=cv2.flip(frame,1)
    processedFrame = frame[:,:,0]
    processedFrame = cv2.subtract(processedFrame, cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY))
    ret, processedFrame = cv2.threshold(processedFrame,100,255,cv2.THRESH_BINARY)
    processedFrame = cv2.blur(processedFrame,(2,2))
    processedFrame = cv2.dilate(processedFrame,kernel,iterations=1)
    processedFrame = cv2.Canny(processedFrame,5,150)
    contornos, cnts = cv2.findContours(processedFrame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    backGround = cv2.imread('bg2.jpg')
    backGround[backGroundHeight-playerHeight:backGroundHeight, contornos[0][0][0][0]:contornos[0][0][0][0]+playerWidth] = player
    if len(contornos)!=0:
        if contornos[0][0][0][0]+playerWidth<=backGroundWidth:
            backGround[backGroundHeight-playerHeight:backGroundHeight, contornos[0][0][0][0]:contornos[0][0][0][0]+playerWidth] = player
            backGround[coinPositionYAxis:coinPositionYAxis+coinHeight, coinPositionXAxis:coinPositionXAxis+coinWidth,:]=coin
            if coinPositionYAxis>=playerHeight and coinPositionXAxis>=contornos[0][0][0][0] and coinPositionXAxis<=contornos[0][0][0][0]+playerWidth:
                score +=1
                scoreAux = score
                if scoreAux > 0:
                    coinPositionYAxis = 0
                    coinPositionXAxis = random.randint(1, backGroundWidth-playerWidth)
                    scoreAux=0
            cv2.putText(backGround, 'SCORE: '+str(score),(10,10), cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
            cv2.putText(backGround, 'LOSES: '+str(loses), (10,30), cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
        else:
            backGround = cv2.imread('bg2.jpg')
    else:
        backGround = cv2.imread('bg2.jpg')
        cv2.putText(backGround, 'COLOCA EL VASO AL FRENTE', (100, 200),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
        cv2.putText(backGround, 'PARA DETECTAR EL MANDO', (120, 250),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
    if score==50 or loses==5:
        break
    cv2.imshow('COIN COLLECTOR',backGround)
    cv2.imshow('',frame)
    key = cv2.waitKey(1)
    if key==ord('q') or key==ord('Q'):
        break
    coinPositionYAxis+=2
    if coinPositionYAxis>=backGroundHeight-1:
        coinPositionYAxis=0
        coinPositionXAxis=random.randint(1,backGroundWidth-playerWidth)
        loses=loses+1
        print(loses)

video.release()
cv2.destroyAllWindows()

if score==50:
    cv2.putText(backGround, 'GANASTE', (250, 50), cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
    (backGround, 'PRESIONA CUALQUIER TECLA PARA SALIR', (200, 450), cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
elif loses==5:
    cv2.putText(backGround, 'PERDISTE', (250, 50), cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
    (backGround, 'PRESIONA CUALQUIER TECLA PARA SALIR', (200, 450), cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
else:
    cv2.putText(backGround, 'SALISTE DEL JUEGO', (250, 50), cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
    (backGround, 'PRESIONA CUALQUIER TECLA PARA SALIR', (200, 450), cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
    
cv2.imshow('RESULTADO', backGround)
cv2.waitKey(0)
cv2.destroyAllWindows()


    
            
