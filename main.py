import os
import cv2
import argparse
import cvlib as cv
from cvlib.object_detection import draw_bbox

import numpy as np
import imutils

parser = argparse.ArgumentParser()

parser.add_argument("--input", type=str, dest="input")
parser.add_argument("--output", type=str, dest="output")

args = parser.parse_args()

input_name = args.input
output_name = args.output

cap = cv2.VideoCapture(input_name)
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter(output_name, fourcc, 30.0, (1920,1080))
idx = 0
l = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

while(cap.isOpened()):
    if idx % 100 == 0:
        print(idx,"/",l)
    ret, frame = cap.read()

    if (ret):
        idx += 1
        bbox, label, conf = cv.detect_common_objects(frame)
        for i, cla in enumerate(label):
            if cla == 'car' or cla == 'bus' or cla == 'truck' or cla == 'train':
                blur_h = int((bbox[i][3]-bbox[i][1])*1/3)
                if bbox[i][0] > 0 and bbox[i][1] > 0:
                    blur_area = frame[bbox[i][3]-blur_h:bbox[i][3]+int(blur_h/3),bbox[i][0]:bbox[i][2]]
                    blur_img = cv2.blur(blur_area, (7,7))
                    frame[bbox[i][3]-blur_h:bbox[i][3]+int(blur_h/3),bbox[i][0]:bbox[i][2]] = blur_img
        # draw bounding box over detected objects (검출된 물체 가장자리에 바운딩 박스 그리기)
        # frame = draw_bbox(frame, bbox, label, conf, write_conf=True)

        # display output
        # cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('frame',1100,1500)
        # cv2.imshow("frame", frame)
        out.write(frame)
        # cv2.waitKey(1)  
        # if cv2.waitKey(0) & 0xFF == ord('q'):
        #     break
    else:
        break 
       
out.release()
cap.release()
cv2.destroyAllWindows()