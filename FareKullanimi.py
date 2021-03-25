import cv2

cap = cv2.VideoCapture(0)

circles = []

def mouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN :
             circles.append((x,y))


font = cv2.FONT_HERSHEY_COMPLEX_SMALL
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame",mouse)



while True:
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    cv2.putText(frame, "Silmek icin 'h' ye basin", (5,50), font, 2, (0,0,0))
    for center in circles:
        cv2.circle(frame, center, 20, (255,0,0), 2)

    cv2.imshow("Frame",frame)

    key = cv2.waitKey(5)

    if key == 27:
        break

    elif key == ord('h'):
        circles = []


cap.release()
cv2.destroyAllWindows()