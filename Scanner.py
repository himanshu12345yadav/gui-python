import mapper 
import cv2
import numpy as np
import os

def Scanner(path):
    img_path = os.path.expanduser(path)
    img=cv2.imread(img_path,1)
    img=cv2.resize(img,(600,600))
    # cv2.imshow('original',img)
    orig=img.copy()

    gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#convertig into gray image
    #cv2.imshow('gray',gray_img)

    blur_img=cv2.GaussianBlur(gray_img,(5,5),0)#converting into blurred image
    #cv2.imshow('blur',blur_img)

    edged_img=cv2.Canny(blur_img,30,50)#detecting edges
    #cv2.imshow('edged',edged_img)


    contours,hierarchy=cv2.findContours(edged_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img,contours,-1,(0,255,0),1)   
    contours=sorted(contours,key=cv2.contourArea,reverse=True)

    for c in contours:

        p=cv2.arcLength(c,True)
        approx=cv2.approxPolyDP(c,0.02*p,True)
     
        if len(approx)==4:
           target=approx
           break

    approx=mapper.mapp(target)

    pts=np.float32([[0,0],[600,0],[600,600],[0,600]])


    op=cv2.getPerspectiveTransform(approx, pts)
    dst=cv2.warpPerspective(orig,op,(600,600))

    # cv2.imshow('final',dst)

    #b&w
    imgg=cv2.cvtColor(dst,cv2.COLOR_BGR2GRAY)
    scanned_image=cv2.adaptiveThreshold(imgg,255,1,1,7,2)
    scanned_image=cv2.bitwise_not(scanned_image)
    scanned_image=cv2.medianBlur(scanned_image,3 )
    # cv2.imshow("scanned output",scanned_image)
    return scanned_image

        
scanned = Scanner("./assets/scanner_1.jpg")