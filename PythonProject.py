"""
Group Members:
1.Himanshu(2019KUEC2009)
2.Ayush Kumar Gupta(2019KUEC2018)
3.Krishankant Garg(2019KUEC2025)
4.Deepak Gurjar(2019KUEC2027)
@copyright 2021
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import sys
from PyQt5.QtWidgets import QApplication,QFileDialog,QMessageBox, QStyle, QLabel,QSizePolicy, QWidget, QPushButton ,QHBoxLayout, QGroupBox, QDialog, QVBoxLayout,QColorDialog
from PyQt5.QtGui import QIcon, QFont , QImage , QPixmap
from PyQt5.QtCore import pyqtSlot , QSize , Qt
from background_blur import blur_image
import numpy as np;
import cv2
import os
from Scanner import Scanner
from Text_detection import Text_detection
from Text_extraction import ocr_text
from Hindi_translator import Hindi_translate
from Text_to_speech import text_to_speech

from detect_face_image import facedetectImage
from detect_face_video import facedetectVideo

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "ImagiFy"
        self.left = 200
        self.top = 100
        self.width = 800
        self.height = 650
        self.initUI()
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('./assets/logo.png'))
        self.createHorizontalLayout()
        self.setStyleSheet("""QToolTip { 
                           padding: 5px;
                           }
                           QWidget{
                           background-color: #f9b8ff;
                           color: white;
                           font-family: 'Roboto';
                           
                           }
                           QPushButton{
                           background-color: #333;
                           color: white;
                           padding: 10px;
                           font-family: 'Roboto';
                           font-size: 20px;
                           border:3px solid;
                           }""")

        #color = QColorDialog.getColor()
        #code starting for headre main
        self.label=QLabel(self)
        self.pixmap = QPixmap('./assets/features.png')
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.width(), self.pixmap.height())
	#code ending for header main
        
	#code start for footer main
        self.label1=QLabel(self)
        self.pixmap=QPixmap('./assets/libraries.png')
        self.label1.setPixmap(self.pixmap)
        self.label1.resize(self.pixmap.width(), self.pixmap.height())
        self.label1.move(0,402)
         #code ending for footer main

        self.label2=QLabel(self)
        self.label2.setText("Click Below:-")
        self.label2.setStyleSheet("""
		color:black;
		padding:0px;
		font-size:18px;
		width:500px;
		""")
        
        self.label2.move(100,260)
        
        
        self.show()
    def createHorizontalLayout(self):
        layout = QHBoxLayout()
        scanner_btn = QPushButton("Scanner", self)
        scanner_btn.setToolTip("Click here to scan document")
        scanner_btn.clicked.connect(self.handleScanner)
        layout.addWidget(scanner_btn)

        image_edit = QPushButton("Image Editor", self)
        image_edit.setToolTip("Click Here for Image Edit")
        image_edit.clicked.connect(self.handleImageEdit)
        layout.addWidget(image_edit)

        image_ocr = QPushButton("OCR", self)
        image_ocr.setToolTip("Click here for OCR")
        image_ocr.clicked.connect(self.handleImageOcr)
        layout.addWidget(image_ocr)
        
        Face_detection = QPushButton("Face Detection", self)
        Face_detection.setToolTip("Click Here for Face Detection")
        Face_detection.clicked.connect(self.handleFacedetection)
        layout.addWidget(Face_detection)
        self.setLayout(layout)

    @pyqtSlot()
    def handleScanner(self):
        self.cams = ScannerWindow(self) 
        self.cams.show()
        self.close()
    @pyqtSlot()
    def handleImageEdit(self):
        self.cams = ImageEditWindow(self) 
        self.cams.show()
        self.close()
    @pyqtSlot()
    def handleImageOcr(self):
        self.cams = ImageOCRWindow(self) 
        self.cams.show()
        self.close()
    @pyqtSlot()
    def handleFacedetection(self):
        self.cams = FacedetectionWindow(self) 
        self.cams.show()
        self.close()

       
class ScannerWindow(QDialog):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        # Code for the Scanner Window
        self.setWindowTitle('Scanner')
        self.setGeometry(value.left, value.top, value.width, value.height)
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))
        self.setStyleSheet("""QToolTip { 
                           padding: 5px;
                           }
                           QWidget{
                           background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #fc00ff, stop:1 #00dbde);
                           color: white;
                           font-family: 'Roboto';
                           
                           }
                           
                           QPushButton{
                           
                           color: white;
                           padding: 10px;
                           font-family: 'Roboto';
                           font-size: 20px;
                           
                           background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #525252 , stop:1 #3d72b4);
                           
                           }""")
        
        label1 = QLabel("Scanner App")
        self.button = QPushButton()
        self.button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.button.setIcon(QIcon('./assets/image_dialog.png'))
        self.button.setIconSize(QSize(170, 170))
        self.button.clicked.connect(self.getScanned)
        
        layoutV = QVBoxLayout()
        self.pushButton = QPushButton(self)
        self.pushButton.setStyleSheet('background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #136a8a, stop:1 #267871);')
        self.pushButton.setText('Back')
        self.pushButton.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.pushButton.setIconSize(QSize(20, 20))
        self.pushButton.clicked.connect(self.goMainWindow)
        layoutV.addWidget(self.pushButton)
        
        layoutH = QHBoxLayout()
        layoutV.addWidget(label1)
        label1.setFont(QFont('Roboto', 20))
        label1.setAlignment(Qt.AlignCenter)
        # closing button
        layoutH.addWidget(self.button)
        layoutV.addLayout(layoutH)
        self.setLayout(layoutV)
      

    def getScanned(self):
        # To fetch the scanner image
        options = QFileDialog.Options()
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Image files (*.jpg *.gif *.png)", options=options)
        imagePath = fname[0]

        if imagePath:
            scanned = Scanner(imagePath)
            cv2.imshow("Scanned Image", scanned)
            cv2.moveWindow("Scanned Image", 200, 50)
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            ret = QMessageBox.question(self, 'Save Image', "Do You want to save this Scanned Image ?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
            if ret == QMessageBox.Yes:
                outfname = "scanned_image.jpg"
                cv2.imwrite(os.path.expanduser(outfname), scanned)


    def goMainWindow(self):
        self.cams = App()
        self.cams.show()
        self.close() 
        
    
class ImageEditWindow(QDialog):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Image Editor')
        # Here value is the super class object
        # Main Window
        self.setGeometry(value.left, value.top, value.width, value.height)
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))


        self.setStyleSheet("""QToolTip { 
                           padding: 5px;
                           }
                           QWidget{
                           background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #fc00ff, stop:1 #00dbde);
                           color: white;
                           font-family: 'Roboto';
                           
                           }
                           
                           QPushButton{
                           
                           color: white;
                           padding: 10px;
                           font-family: 'Roboto';
                           font-size: 20px;
                           
                           background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #525252 , stop:1 #3d72b4);
                           
                           }""")
        # App Label
        label_2 = QLabel("Image Editor")

        # Main Content
        self.button = QPushButton()
        self.button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.button.setIcon(QIcon('./assets/image_dialog.png'))
        self.button.setStyleSheet('background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #525252 , stop:1 #3d72b4);')
        self.button.setIconSize(QSize(200, 200))
        self.button.clicked.connect(self.getImage)
        
        layoutV = QVBoxLayout() # Vertical Layout For the App Flow
        # Back Button
        self.pushButton = QPushButton(self)
        self.pushButton.setStyleSheet('background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #136a8a, stop:1 #267871);')
        self.pushButton.setText('Back')
        self.pushButton.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.pushButton.setIconSize(QSize(20, 20))
        self.pushButton.clicked.connect(self.goMainWindow)
        layoutV.addWidget(self.pushButton)
        
        layoutH = QHBoxLayout() # Horizontal Layout for Main Content
        layoutV.addWidget(label_2)
        label_2.setFont(QFont('Roboto', 20))
        label_2.setAlignment(Qt.AlignCenter)
        layoutH.addWidget(self.button)
        layoutV.addLayout(layoutH)
        self.setLayout(layoutV)
        self.previewImage = QLabel()
        self.previewImage.setAlignment(Qt.AlignCenter)
        layoutV.addWidget(self.previewImage)

    def getImage(self):
        options = QFileDialog.Options()
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Image files (*.jpg *.gif *.png)", options=options)
        imagePath = fname[0]
        if imagePath:
            cvImg = blur_image(imagePath)
            blurred_img = cvImg.copy()
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(cvImg, 'Modified', (100 , 100), font, 3, (0,0,0), 2, cv2.LINE_AA)
            original_image = cv2.imread(imagePath)
            font = cv2.FONT_HERSHEY_SIMPLEX 
            cv2.putText(original_image, 'Original', (100 , 100), font, 3, (0,0,0), 2, cv2.LINE_AA)
            output_result = np.concatenate((original_image, cvImg), axis=1)
            height, width, channel = output_result.shape
            bytesPerLine = 3 * width
            qImg = QImage(output_result.data, width, height, bytesPerLine, QImage.Format_BGR888)
            pixmap = QPixmap(qImg)
            self.previewImage.setPixmap(pixmap.scaled(pixmap.width()//3, pixmap.height()//2, Qt.KeepAspectRatio, Qt.FastTransformation))
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            ret = QMessageBox.question(self, 'Save Image', "Do You want to save this blurred Image ?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
            if ret == QMessageBox.Yes:
                outfname = "blurred_img.jpg"
                cv2.imwrite(os.path.expanduser(outfname), blurred_img)


    def goMainWindow(self):
        self.cams = App()
        self.cams.show()
        self.close()    
        
   
class ImageOCRWindow(QDialog):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Image OCR')
        self.setGeometry(value.left, value.top, value.width, value.height)
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))

        self.setStyleSheet("""QToolTip { 
                           padding: 5px;
                           }
                           QWidget{
                           background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #fc00ff, stop:1 #00dbde);
                           color: white;
                           font-family: 'Roboto';
                           
                           }
                           
                           QPushButton{
                           
                           color: white;
                           padding: 10px;
                           font-family: 'Roboto';
                           font-size: 20px;
                           
                           background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #525252 , stop:1 #3d72b4);
                           
                           }""")

        # label_3 = QLabel("Image OCR")
        self.button = QPushButton()
        self.button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.button.setIcon(QIcon('./assets/image_dialog.png'))
        self.button.setIconSize(QSize(200, 200))
        self.button.clicked.connect(self.image_input)
        
        layoutV = QVBoxLayout()
        self.pushButton = QPushButton(self)
        self.pushButton.setStyleSheet('background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #136a8a, stop:1 #267871);')
        self.pushButton.setText('Back')
        self.pushButton.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.pushButton.setIconSize(QSize(20, 20))
        self.pushButton.clicked.connect(self.goMainWindow)
        layoutV.addWidget(self.pushButton)
        
        layoutH = QHBoxLayout()
        # layoutV.addWidget(label_3)
        # label_3.setFont(QFont('Roboto', 20))
        # label_3.setAlignment(Qt.AlignCenter)
        layoutH.addWidget(self.button)
        self.layoutH = layoutH
        self.layoutV = layoutV
        self.button.clicked.connect(self.createHorizontalLayout)
        layoutV.addLayout(layoutH)
        self.setStyleSheet("""QToolTip { 
                           padding: 5px;
                           }
                           QPushButton{
                           background-color: #333;
                           color: white;
                           padding: 10px;
                           font-family: 'Roboto';
                           font-size: 14px;
                           }""")
        self.setLayout(layoutV)
    def image_input(self):
        options = QFileDialog.Options()
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Image files (*.jpg *.gif *.png)", options=options)
        imagePath = fname[0]

        if imagePath:
            # Get the image
            #ocr = OCR(imagePath)
            self.image_path = imagePath
            self.layoutH.removeWidget(self.button)
            self.button.deleteLater()
            self.button = None
            pixmap = QPixmap(imagePath)
            self.preview = QLabel()
            self.preview.setPixmap(pixmap)
            self.preview.setPixmap(pixmap.scaled(pixmap.width()//5, pixmap.height()//3, Qt.KeepAspectRatio, Qt.FastTransformation))
            self.layoutH.addWidget(self.preview)
            self.preview.setAlignment(Qt.AlignCenter)




    def createHorizontalLayout(self):
        layout = QHBoxLayout()
        text_detect = QPushButton("Text Detection", self)
        text_detect.setToolTip("Click here to detect Text")
        text_detect.clicked.connect(self.handleTextDetect)
        layout.addWidget(text_detect)

        text_extract = QPushButton("Text Extraction", self)
        text_extract.setToolTip("Click Here to extract Text")
        text_extract.clicked.connect(self.handleTextExtract)
        layout.addWidget(text_extract)

        tts = QPushButton("Text To Speech", self)
        tts.setToolTip("Click here to speak the text")
        tts.clicked.connect(self.handleTTS)
        layout.addWidget(tts)

        hindi_text = QPushButton("Get Hindi Text", self)
        hindi_text.setToolTip("Click here to get the hindi text")
        hindi_text.clicked.connect(self.getHindiText)
        layout.addWidget(hindi_text)
        self.layoutV.addLayout(layout)
        self.text = QLabel("", self)
        self.layoutV.addWidget(self.text)
        self.text.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""QLabel { 
                           padding: 5px;
                           font-size: 14px;
                           }
                           QPushButton{
                           background-color: #333;
                           color: white;
                           padding: 10px;
                           font-family: 'Roboto';
                           font-size: 14px;
                           }""")
        self.text.setWordWrap(True)

    def handleTextExtract(self):
        # Handles the text extraction , gets the text string
        extracted_text = ocr_text(self.image_path)
        #extracted_text = "Hello this is extracted text"
        self.text.setText(extracted_text)

    def handleTextDetect(self):
        # Handles the text detect, get the final image
        text_detect = Text_detection(self.image_path)
        text_detect = cv2.resize(text_detect, (960, 540))
        cv2.imshow('Detected Text',text_detect)
        cv2.moveWindow("Detected Text", 200, 100)
        #height, width, channel = text_detect.shape
        #bytesPerLine = 3 * width
        #qImg = QImage(text_detect.data, width, height, bytesPerLine, QImage.Format_BGR888)
        #pixmap = QPixmap(qImg)
        #self.detected_text.setPixmap(pixmap.scaled(pixmap.width()//3, pixmap.height()//2, Qt.KeepAspectRatio, Qt.FastTransformation))
        #pixmap = QPixmap(self.image_path)
        #self.detectedText = QLabel()
        #self.detectedText.setPixmap(pixmap)
        #self.detectedText.setPixmap(pixmap.scaled(pixmap.width()//1, pixmap.height()//2, Qt.KeepAspectRatio, Qt.FastTransformation))
        #self.layoutV.addWidget(self.detectedText)
        #self.detectedText.setAlignment(Qt.AlignCenter)
        
    def handleTTS(self):
        # handle TTS
        # play the converted audio
        tts = text_to_speech(self.image_path)

    def getHindiText(self):
        extracted_text = Hindi_translate(self.image_path)
        # extracted_text = "Hello this is Hindi extracted text"
        self.text.setText(extracted_text)
        # self.layoutV.addWidget(self.text)

    def goMainWindow(self):
        self.cams = App()
        self.cams.show()
        self.close()




class FacedetectionWindow(QDialog):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Face Detection')
        self.setGeometry(value.left, value.top, value.width, value.height)
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))

        self.setStyleSheet("""QToolTip { 
                           padding: 5px;
                           }
                           QWidget{
                           background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #fc00ff, stop:1 #00dbde);
                           color: white;
                           font-family: 'Roboto';
                           
                           }
                           
                           QPushButton{
                           
                           color: white;
                           padding: 10px;
                           font-family: 'Roboto';
                           font-size: 20px;
                           
                           background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #525252 , stop:1 #3d72b4);
                           
                           }""")

        # label_3 = QLabel("Image OCR")
        self.button = QPushButton()
        self.button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.button.setIcon(QIcon('./assets/image_dialog.png'))
        self.button.setIconSize(QSize(200, 200))
        self.button.clicked.connect(self.image_input)
        
        layoutV = QVBoxLayout()
        self.pushButton = QPushButton(self)
        self.pushButton.setStyleSheet('background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #136a8a, stop:1 #267871);')
        self.pushButton.setText('Back')
        self.pushButton.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.pushButton.setIconSize(QSize(20, 20))
        self.pushButton.clicked.connect(self.goMainWindow)
        layoutV.addWidget(self.pushButton)
        
        layoutH = QHBoxLayout()
        # layoutV.addWidget(label_3)
        # label_3.setFont(QFont('Roboto', 20))
        # label_3.setAlignment(Qt.AlignCenter)
        layoutH.addWidget(self.button)
        self.layoutH = layoutH
        self.layoutV = layoutV
        self.button.clicked.connect(self.createHorizontalLayout)
        layoutV.addLayout(layoutH)
        self.setStyleSheet("""QToolTip { 
                           padding: 5px;
                           }
                           QPushButton{
                           background-color: #333;
                           color: white;
                           padding: 10px;
                           font-family: 'Roboto';
                           font-size: 14px;
                           }""")
        self.setLayout(layoutV)
    def image_input(self):
        options = QFileDialog.Options()
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Image files (*.jpg *.gif *.png *.jpeg)", options=options)
        imagePath = fname[0]

        if imagePath:
            # Get the image
            #ocr = Face detect(imagePath)
            self.image_path = imagePath
            self.layoutH.removeWidget(self.button)
            self.button.deleteLater()
            self.button = None
            pixmap = QPixmap(imagePath)
            self.preview = QLabel()
            self.preview.setPixmap(pixmap)
            self.preview.setPixmap(pixmap.scaled(pixmap.width()//1, pixmap.height()//2, Qt.KeepAspectRatio, Qt.FastTransformation))
            self.layoutH.addWidget(self.preview)
            self.preview.setAlignment(Qt.AlignCenter)




    def createHorizontalLayout(self):
        layout = QHBoxLayout()
        face_detect = QPushButton("Face Detection in Image", self)
        face_detect.setToolTip("Click here to detect face in an iamge")
        face_detect.clicked.connect(self.handleFaceDetect)
        layout.addWidget(face_detect)

        tts = QPushButton("Face detection in video", self)
        tts.setToolTip("Click here to detect face in a video")
        tts.clicked.connect(self.handleVideodetect)
        layout.addWidget(tts)
        self.layoutV.addLayout(layout)
        self.text = QLabel("", self)
        self.layoutV.addWidget(self.text)


    def handleFaceDetect(self):
        # Handles the text detect, get the final image
        image_detect = facedetectImage(self.image_path)
        cv2.imshow('Result',image_detect)
        #height, width, channel = text_detect.shape
        #bytesPerLine = 3 * width
        #qImg = QImage(text_detect.data, width, height, bytesPerLine, QImage.Format_BGR888)
        #pixmap = QPixmap(qImg)
        #self.detected_text.setPixmap(pixmap.scaled(pixmap.width()//3, pixmap.height()//2, Qt.KeepAspectRatio, Qt.FastTransformation))
        #pixmap = QPixmap(self.image_path)
        #self.detectedText = QLabel()
        #self.detectedText.setPixmap(pixmap)
        #self.detectedText.setPixmap(pixmap.scaled(pixmap.width()//1, pixmap.height()//2, Qt.KeepAspectRatio, Qt.FastTransformation))
        #self.layoutV.addWidget(self.detectedText)
        #self.detectedText.setAlignment(Qt.AlignCenter)
        
    def handleVideodetect(self):
        facedetectVideo()

    

    def goMainWindow(self):
        self.cams = App()
        self.cams.show()
        self.close()

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App();
    sys.exit(app.exec_());


    
