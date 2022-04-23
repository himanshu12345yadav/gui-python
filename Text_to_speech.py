#####TextExtraction
import cv2
import pytesseract

def text_to_speech(img_path): 
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

    ####Text to speech
    from gtts import gTTS
    import os

    myText = extracted_text

    language = 'en'

    output = gTTS(text=myText, lang=language,slow =False)

    output.save("output.mp3")

    os.system("start output.mp3")


#text_to_speech('screenshot.jpg')




    ####Reading input from a file and speaking it

    #fh = open("test.txt","r")
    #myText = fh.read().replace("\n", " ")

    #language = 'en'
    #output = gTTS(text=myText, lang=language, slow=False)

    #output.save("output.mp3")
    #fh.close()
    #os.system("start output.mp3")
