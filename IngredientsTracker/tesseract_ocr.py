import cv2
import pytesseract


def scan_image():
    testing_image_read_in = cv2.imread('image/path')

    # change image to gray scake
    gray_image = cv2.cvtColor(testing_image_read_in, cv2.COLOR_BGR2GRAY)

    # do adaptive threshold on gray image
    thresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 15)

    ocr_result = pytesseract.image_to_string(thresh)