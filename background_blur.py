"""License MIT
Copyright 2020 HIMANSHU YADAV
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import cv2
import os
import numpy as np
import sys
from string import Template

face_cascade = cv2.CascadeClassifier(os.path.expanduser('haarcascade_frontalface_default.xml'))

scale_factor = 1.1
min_neighbors = 3
min_size = (30, 30)
flags = cv2.CASCADE_SCALE_IMAGE

def blur_image(img_path):
    image_path = os.path.expanduser(img_path)
    image = cv2.imread(image_path)
    image2 = cv2.imread(image_path)
    dmage = ''
    faces = face_cascade.detectMultiScale(
        image, scaleFactor=scale_factor, minNeighbors=min_neighbors, minSize=min_size, flags=flags)

    for(x, y, w, h) in faces:
        blurred_img = cv2.GaussianBlur(image, (31, 31), 0)
        mask = np.zeros((512, 512, 3), dtype=np.uint8)
        mask = cv2.rectangle(
            image, (x, y), (x + w, y + h), (255, 255, 255), -1)
        dmage = np.where(mask == np.array(
            [255, 255, 255]), image2, blurred_img)
        

    return dmage
