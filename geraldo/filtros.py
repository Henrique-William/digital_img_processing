import cv2

if __name__ == "__main__":
    img = cv2.imread("geraldo_ruido.png")
    
    media = cv2.blur(img, (5,5))
    gauss = cv2.GaussianBlur(img, (5,5), 1.0)
    mediana = cv2.medianBlur(img, 5)
    bilateral = cv2.bilateralFilter(img, 9, 75, 75)

    gauss = cv2.GaussianBlur(bilateral, (5,5), 1.0)

    cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Media", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Gauss", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Mediana", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Bilateral", cv2.WINDOW_NORMAL)

    cv2.imshow("Original", img)
    cv2.imshow("Media", media)
    cv2.imshow("Gauss", gauss)
    cv2.imshow("Mediana", mediana)
    cv2.imshow("Bilateral", bilateral)

    cv2.waitKey(0)
    cv2.destroyAllWindows()