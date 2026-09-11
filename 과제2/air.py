import cv2
import numpy as np


def rgb(hsv, col):
    contours = None
    if col == 0:
        lower = np.array([0, 150, 70])
        upper = np.array([10, 255, 255])
        
    elif col == 1:
        lower = np.array([50, 100, 60])
        upper = np.array([70, 255, 255])
        
    else :
        lower = np.array([100, 100, 60])
        upper = np.array([130, 255, 255])
        
    mask = cv2.inRange(hsv, lower, upper)
    dst = cv2.bitwise_not(mask)
    kernel = np.ones((10,10), np.uint8)
    result = cv2.morphologyEx(dst, cv2.MORPH_CLOSE, kernel)
    d = cv2.dilate(result, kernel, iterations=2)
    result1 = cv2.bitwise_not(d)
    contours, hierachy = cv2.findContours(result1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def detect(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    return rgb(hsv,0), rgb(hsv,1), rgb(hsv,2)





SHOW = True

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise SystemExit(f'열 수 없다: {0}. 카메라라면 macOS 터미널에 카메라 권한이 필요하다.')


canvas = None

color = (0,0,0)

def getColor(r,b):
    if r == 0:
        return (255 if b else 0,0,0)
    elif r == 1:
        return (0,255 if b else 0,0)
    else:
        return (0,0,255 if b else 0)
    return color
bbb = True
while True:
    ok, frame = cap.read()
    if not ok:
        break
    frame = cv2.flip(frame, 1)   # 거울처럼 보이게 하는 것뿐이고 검출 결과와는 무관하다

    if canvas is None:
        canvas = np.zeros_like(frame)   # frame 과 같은 크기·채널의 검은 이미지

    r,g,b = detect(frame)

    # 캔버스에 누적한다. 지우지 않으므로 이전에 그린 것이 그대로 남는다.
    cv2.drawContours(canvas, r, -1, getColor(0,bbb), -1)
    cv2.drawContours(canvas, g, -1, getColor(1,bbb), -1)
    cv2.drawContours(canvas, b, -1, getColor(2,bbb),-1)

    # 캔버스에서 칠해진 픽셀만 골라 frame 위에 덮는다.
    # any(axis=2) 는 B,G,R 셋 중 하나라도 0 이 아니면 True - 즉 "칠해진 자리"다.
    painted = canvas.any(axis=2)
    frame[painted] = canvas[painted]

    if SHOW:
        cv2.imshow("subject", frame)
        key = cv2.waitKey(1) & 0xFF
        if key in (ord('q'), 66):
            break
        if key in (ord('c'), 74):      # 캔버스 지우기
            canvas[:] = 0
        if key in (ord('g'), 28):
            print(key)
            if bbb :
                bbb = False
            else :
                bbb = True

cap.release()
if SHOW:
    cv2.destroyAllWindows()
