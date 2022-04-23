import cv2
import pytesseract

def Text_detection(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    #print(pytesseract.image_to_string(img))

    #Detecting characters
    hImg,wImg,_ = img.shape
    boxes = pytesseract.image_to_boxes(img)
    for b in boxes.splitlines():
        #print(b)
        b = b.split(' ')
        #print(b)
        x,y,w,h = int(b[1]),int(b[2]),int(b[3]),int(b[4])
        cv2.rectangle(img,(x,hImg-y),(w,hImg-h),(0,0,255),3)
        cv2.putText(img,b[0],(x,hImg-y+25),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2)

    # #Detecting Words
    # hImg,wImg,_= img.shape
    # boxes = pytesseract.image_to_data(img)
    # #print(boxes)
    # for x,b in enumerate(boxes.splitlines()):
    #     if x!=0:
    #         b = b.split()
    #         print(b)
    #         if len(b)==12:
    #              x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
    #              cv2.rectangle(img,(x,y),(w+x,h+y),(0,0,255),3)
    #              cv2.putText(img,b[11],(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2)
    #

    # #Detecting characters of digits only
    # hImg,wImg,_ = img.shape
    # cong = r' --oem 3 --psm 6 outputbase digits'
    # boxes = pytesseract.image_to_boxes(img,config=cong)
    # for b in boxes.splitlines():
    #     #print(b)
    #     b = b.split(' ')
    #     #print(b)
    #     x,y,w,h = int(b[1]),int(b[2]),int(b[3]),int(b[4])
    #     cv2.rectangle(img,(x,hImg-y),(w,hImg-h),(0,0,255),3)
    #     cv2.putText(img,b[0],(x,hImg-y+25),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2)

    # #Detecting Words only
    # hImg,wImg,_= img.shape
    # cong = r' --oem 3 --psm 6 outputbase digits'
    # boxes = pytesseract.image_to_data(img, config=cong)
    # #print(boxes)
    # for x,b in enumerate(boxes.splitlines()):
    #     if x!=0:
    #         b = b.split()
    #         print(b)
    #         if len(b)==12:
    #              x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
    #              cv2.rectangle(img,(x,y),(w+x,h+y),(0,0,255),3)
    #              cv2.putText(img,b[11],(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2)

    #cv2.imshow('Result',img)
    cv2.waitKey(0)

    return img


#Text_detection('screenshot.jpg')
#cv2.imshow('Result',Text_detection('screenshot.jpg'))










