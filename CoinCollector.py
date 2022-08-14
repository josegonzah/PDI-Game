# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
import cv2
import numpy as np
import random

#Inicializo las variables con las que trabajaremos en el programa
video = cv2.VideoCapture(0)
kernel = np.ones((30, 30), np.uint8)
backGround = cv2.imread('bg2.jpg')
player = cv2.imread('mario.png')
player = cv2.resize(player, (93, 80))
coin = cv2.imread('coin.png')
coin = cv2.resize(coin, (30, 30))
backGroundHeight, backGroundWidth, backGroundCap = backGround.shape
playerHeight, playerWidth, playerCap = player.shape
coinHeight, coinWidth, coinCap = coin.shape
coinPositionYAxis = coinHeight
coinPositionXAxis= random.randint(1,backGroundWidth-coinWidth)
score=0
scoreAux=0
loses = 0
#Limpiamos las ventanas
cv2.waitKey(0)
cv2.destroyAllWindows()
#Ciclo principal que procesa constatemente las imagenes y permite jugar el juego
while True:
    #Leo los frames y extraigo la informacion significativa para luego propecesarlo
    check,frame=video.read()
    frame=cv2.flip(frame,1)
    processedFrame = frame[:,:,0]
    processedFrame = cv2.subtract(processedFrame, cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY))
    ret, processedFrame = cv2.threshold(processedFrame,100,250,cv2.THRESH_BINARY)
    processedFrame = cv2.blur(processedFrame,(4,4))
    processedFrame = cv2.dilate(processedFrame,kernel,iterations=1)
    processedFrame = cv2.Canny(processedFrame,100,250)
    contornos, cnts = cv2.findContours(processedFrame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    backGround = cv2.imread('bg2.jpg')
    if len(contornos)!=0:
        backGround[backGroundHeight-playerHeight:backGroundHeight, contornos[0][0][0][0]:contornos[0][0][0][0]+playerWidth] = player
        if coinPositionYAxis+4>=backGroundHeight: #Checkeo si la moneda aun esta dentro del recuadro
            coinPositionYAxis=coinHeight #Inicializo la poscion de la moneda en el inicio del fondo
            coinPositionXAxis=random.randint(1,backGroundWidth-playerWidth)#Le damos un valor aleatorio en el eje X
            loses=loses+1 #Sumamos una perdida
            backGround[coinPositionYAxis-coinHeight:coinPositionYAxis, coinPositionXAxis:coinPositionXAxis+coinWidth]=coin #Actualizo la imagen de la moneda
        if contornos[0][0][0][0]+playerWidth<=backGroundWidth and coinPositionYAxis<backGroundHeight-2: #Si la moneda aun esta en juego pinto
            backGround[backGroundHeight-playerHeight:backGroundHeight, contornos[0][0][0][0]:contornos[0][0][0][0]+playerWidth] = player
            backGround[coinPositionYAxis-coinHeight:coinPositionYAxis, coinPositionXAxis:coinPositionXAxis+coinWidth]=coin
            if coinPositionYAxis>=playerHeight and coinPositionXAxis>=contornos[0][0][0][0] and coinPositionXAxis<=contornos[0][0][0][0]+playerWidth:
                #En caso de anotar elimino la moneda y sumo un punto
                score +=1
                scoreAux = score
                if scoreAux > 0:
                    coinPositionYAxis = coinHeight
                    coinPositionXAxis = random.randint(1, backGroundWidth-playerWidth)
                    scoreAux=0
            cv2.putText(backGround, 'SCORE: '+str(score),(10,10), cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
            cv2.putText(backGround, 'LOSES: '+str(loses), (10,30), cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
        else:
            backGround = cv2.imread('bg2.jpg')
        coinPositionYAxis+=4
    else:
        #El juego no inicia hasta que el programa no detecte el color azul
        backGround = cv2.imread('bg2.jpg')
        cv2.putText(backGround, 'COLOCA EL VASO AL FRENTE', (100, 200),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
        cv2.putText(backGround, 'PARA DETECTAR EL MANDO', (120, 250),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
    if score==30 or loses==10:
        #El juego termina cuando pierde 10 veces o agarra 30 monedas
        break
    cv2.imshow('COIN COLLECTOR',backGround)
    cv2.imshow('',frame)
    key = cv2.waitKey(1)
    if key==ord('q') or key==ord('Q'):
        break
    

video.release()
cv2.destroyAllWindows()

#Mensajes en caso de terminar el juego
if score==30:
    cv2.putText(backGround, 'GANASTE', (250, 50), cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
    (backGround, 'PRESIONA CUALQUIER TECLA PARA SALIR', (200, 450), cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
elif loses==10:
    cv2.putText(backGround, 'PERDISTE', (250, 50), cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
    (backGround, 'PRESIONA CUALQUIER TECLA PARA SALIR', (200, 450), cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
else:
    cv2.putText(backGround, 'SALISTE DEL JUEGO', (250, 50), cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
    (backGround, 'PRESIONA CUALQUIER TECLA PARA SALIR', (200, 450), cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
    
cv2.imshow('RESULTADO', backGround)
cv2.waitKey(0)
cv2.destroyAllWindows()


    
            
