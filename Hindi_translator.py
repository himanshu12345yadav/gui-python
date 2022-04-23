# Text extraction

import cv2
import pytesseract
def Hindi_translate(img_path):
    def ocr_core(img):
        text = pytesseract.image_to_string(img)
        return text

    img = cv2.imread(img_path)

    #Get grayscale image
    def get_grayscale(image):
        return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    #noise removal
    def remove_noise(image):
        return cv2.medianBlur(image,5)

    #thresholding
    def thresholding(image):
        return cv2.threshold(image,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    img = get_grayscale(img)
    img = thresholding(img)
    img = remove_noise(img)

    extracted_text = ocr_core(img)
    #print(extracted_text)

        
    # english to hindi

    from translate import Translator
    String = str(extracted_text)
    sentence = String[0:500]
    translator = Translator(to_lang = "Hindi")
    translation = translator.translate(sentence)
    #print(translation)

    return translation

#Hindi_translate('screenshot.jpg')
