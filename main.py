import cv2
import pickle
import numpy as np
import cvzone

#dimensions
width, height= 107,48

#Video feed import
cap=cv2.VideoCapture('carPark.mp4')

with open('carParkpos', 'rb') as f:
    poslist = pickle.load(f)
def checkparkingspace(imgPro):
    availablespace = 0
    availablespace_dict = {}
    for pos in poslist:
        x,y =pos

        imgcrop=imgPro[y:y+height,x:x+width]
        #cv2.imshow(str(x*y),imgcrop)
        count=cv2.countNonZero(imgcrop)

        # This converts coordinates to index
        element = pos
        index = poslist.index(element)+1

        #print(index)
        #cvzone.putTextRect(img,str(count),(x,y+height-10),scale=1,offset=0,thickness=1)

        if count <900:
            color=(0,255,0)
            thickness=5
            availablespace +=1

            availablespace_dict[index]=pos


            #this displays the index on the image
            cvzone.putTextRect(img, str(index), (x, y + height - 10), scale=2, offset=0, thickness=1)

            #freespaces_index = {}
            #freespaces_index[index] = pos[]




        else:
            color=(0,0,255)
            thickness=2


        #This creates the red or green rectangle according to vacancy of parking space
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color,thickness)

        #This displays the id of the parking space defined
        #cvzone.putTextRect(img, str(index), (x, y + height - 10), scale=2, offset=0, thickness=1)


        freespaces_index = {}

        freespaces_index[index]=pos
        #print(freespaces_index)

    #this gives the total number of parkings vs empty
    cvzone.putTextRect(img, f'Free:{availablespace}/{len(poslist)}', (100,50), scale=5, offset=0, thickness=3,colorR=(0,200,0))

    #this displays the available spaces number and their coordinates
    print("available spaces dict")
    print(availablespace_dict)
    print(len(availablespace_dict))

while True:



    if cap.get(cv2.CAP_PROP_POS_FRAMES)== cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    success, img = cap.read()
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur=cv2.GaussianBlur(imgGray,(3,3),1)
    imgThreshold=cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV,25,16)
    imgMedian=cv2.medianBlur(imgThreshold,5)
    kernel=np.ones((3,3),np.uint8)
    imgDilate=cv2.dilate(imgMedian,kernel,iterations=1)

    checkparkingspace(imgDilate)
   # for pos in poslist:
      #  cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)






    cv2.imshow("Image",img)
    #cv2.imshow("ImageBlur",imgBlur)
   #cv2.imshow("imgathresh",imgThreshold)
    cv2.waitKey(30000)