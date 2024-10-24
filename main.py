from matplotlib import pyplot as plt
from device import Devices
# from ocr.ocr import ocrDefault
import cv2
import numpy as np
from skimage import filters
import time
if __name__=="__main__":
  # simulator = input('请输入模拟器地址')
  simulator = '127.0.0.1:62001'
  d = Devices(simulator)
  start = time.time()
  img = d.screenshot()
  edges = cv2.Canny(img, 100, 200)
  lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=800, maxLineGap=20)
  print(lines)
  # 在原图上绘制检测到的线条
  if lines is not None:
      for line in lines:
          x1, y1, x2, y2 = line[0]
          cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

  # 显示结果
  plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
  plt.axis('off')
  plt.show()
  # r = ocrDefault(img)
  # print(r)
