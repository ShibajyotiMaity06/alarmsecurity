import cv2
import winsound
import threading
import imutils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)

gray_start = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
gray_start = cv2.GaussianBlur(gray_start, (21, 21), 0)

alarm = False
alarm_mode = False
alarm_counter = 0


def beep():
  global alarm
  while alarm_mode:
    print("Intruder detected!")
    winsound.Beep(2500, 1000)
  alarm = False


while True:
  _, frame = cap.read()
  frame = imutils.resize(frame, width=500)

  if alarm_mode:
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.GaussianBlur(frame_gray, (5, 5), 0)

    diff = cv2.absdiff(frame_gray, gray_start)
    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    gray_start = frame_gray

    if thresh.sum() > 100:
        alarm_counter += 1
    else:
        if alarm_counter > 0:
            alarm_counter -= 1

    cv2.imshow("Threshold", thresh)

  else:
    cv2.imshow("Camera", frame)

  if alarm_counter > 20:
      if not alarm:
          alarm = True
          threading.Thread(target=beep).start()

  key = cv2.waitKey(1) & 0xFF
  if key == ord("q"):
      break
  elif key == ord("s"):
      alarm_mode = not alarm_mode

cap.release()
cv2.destroyAllWindows()