import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow("Settings")
cv2.createTrackbar("Lower-Hue", "Settings", 0, 180,nothing)
cv2.createTrackbar("Lower-Saturation", "Settings", 0, 255,nothing)
cv2.createTrackbar("Lower-Value", "Settings", 0, 255,nothing)
cv2.createTrackbar("Upper-Hue", "Settings", 0, 180,nothing)
cv2.createTrackbar("Upper-Saturation", "Settings", 0, 255,nothing)
cv2.createTrackbar("Upper-Value", "Settings", 0, 255,nothing)

font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    lh = cv2.getTrackbarPos("Lower-Hue","Settings")#trackbarın pozisyonunu veriyomuş
    ls = cv2.getTrackbarPos("Lower-Saturation", "Settings")
    lv = cv2.getTrackbarPos("Lower-Value", "Settings")
    uh = cv2.getTrackbarPos("Upper-Hue", "Settings")
    us = cv2.getTrackbarPos("Upper-Saturation", "Settings")
    uv = cv2.getTrackbarPos("Upper-Value", "Settings")
    #Bu degiskenler anlık olarak trackbarların icerigindeki degeri tutacak

    lower_color = np.array([lh,ls,lv]) # tek tek degiskenlerle ugrasmayak diye de array a attık
    upper_color = np.array([uh,us,uv])

    mask = cv2.inRange(hsv, lower_color, upper_color)


    kernel = np.ones((5,5), np.uint8) #maskeledikten sonra beyaz nesneler ustunde olusan siyah noktaları yok etmek icin yaptıgımız bir sey olucak
    mask = cv2.erode(mask,kernel)

    _,contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt) # Alan hesabı yapacak ve 400 degerinden buyuk yerlerde alan hesbı yap diycez
        epsilon = 0.02 * cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        x = approx.ravel()[0]# Bu degerler cokgenlerin konturlarının basladıgı yerler
        y = approx.ravel()[1]

        if area > 400:
            cv2.drawContours(frame, [approx], 0, (0,0,0),5)

            if len(approx) == 3:
                cv2.putText(frame, "Ucgen", (x,y), font, 1, (0,0,0))

            elif len(approx) == 4:
                cv2.putText(frame, "Dikdortgen", (x, y), font, 1, (0, 0, 0))

            elif len(approx) > 6:
                cv2.putText(frame, "Daire", (x, y), font, 1, (0, 0, 0))


    cv2.imshow("mask",mask)
    cv2.imshow("frame",frame)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.waitKey()

