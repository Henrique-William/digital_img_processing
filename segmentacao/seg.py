import cv2
import numpy as np

if __name__ == "__main__":
    img = cv2.imread("cachorro_green.png")
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    baixo_verde = np.array([35, 80, 80])
    alto_verde = np.array([85, 255, 255])

    mascara_verde = cv2.inRange(hsv, baixo_verde, alto_verde)
    mascara_objeto = cv2.bitwise_not(mascara_verde)

    kernel = np.ones((5, 5), np.uint8)
    mascara_objeto = cv2.morphologyEx(mascara_objeto, cv2.MORPH_OPEN, kernel)
    mascara_objeto = cv2.morphologyEx(mascara_objeto, cv2.MORPH_CLOSE, kernel)

    resultado = cv2.bitwise_and(img, img, mask = mascara_objeto)

    cv2.imshow("mascara verde", mascara_verde)
    cv2.imshow("mascara objeto", mascara_objeto)
    cv2.imshow("resultado", resultado)

    cv2.waitKey(0)
    cv2.destroyAllWindows