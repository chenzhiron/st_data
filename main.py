import time
from device import Devices
from ocr.ocr import ocr_format_val
import cv2
import numpy as np
from utils import formatDate

from collections import defaultdict

def loopinfo(img):
      resarr = []

      edges = cv2.Canny(np.array(img.crop([120, 195, 1760, 1050])), 100, 200)
      lines = cv2.HoughLinesP(edges, 2, np.pi / 180, threshold=200, minLineLength=1200, maxLineGap=20)
      lines = lines.squeeze()

      sorted_lines = lines[np.argsort(lines[:, 1])]
      # 初始化过滤后的结果
      filtered_lines = [sorted_lines[0]]  # 保留第一个线条
      # 遍历排序后的线条，过滤掉相邻线条之间 y 值差距小于 100 的线条
      for i in range(1, len(sorted_lines)):
         if sorted_lines[i][1] - sorted_lines[i-1][1] >= 100:
            filtered_lines.append(sorted_lines[i])

      # 转换为 NumPy 数组
      filtered_lines = np.array(filtered_lines)
      #  print(filtered_lines)
      for v in filtered_lines:
         current = {}
         # print('lines:', v) 

         # 名字
         r = ocr_format_val(np.array(img.crop([568,v[1] + 195,820, v[1] + 195 + 70])))
         if r == None:
            r = ocr_format_val(np.array(img.crop([568,v[1] + 195 - 70,820, v[1] + 195])))
         if r != None and current.get("name",None) ==None:
            current["name"] = r
            
         print('name:',r)

         # 战报时间
         times = formatDate(ocr_format_val(np.array(img.crop([800,v[1] + 195 + 300,1072, v[1] + 195 + 300+50]))))
         if times == None:
            times = formatDate(ocr_format_val(np.array(img.crop([800,v[1] + 195 + 230,1072, v[1] + 195 + 230 + 50]))))
         current["times"] = 0
         if times != None and current.get("times",None) == None:
            current["times"] = times
         print('times:', times)
         # 单次战斗数量
         battles = ocr_format_val(np.array(img.crop([1770, v[1] + 195 + 130, 1830,  v[1] + 195 + 200])))
         if battles== None:
            battles = ocr_format_val(np.array(img.crop([1770, v[1] + 195 + 70, 1830,  v[1] + 195 + 130])))
         if battles== None:
            battles = 0
         if battles != None and current.get("battles",None) == None:
            current["battles"] = int(battles) + 1
         else:
            current["battles"] += int(battles) + 1
         print('battles:',battles)
         resarr.append(current)
      return resarr

if __name__=="__main__":
  # simulator = input('请输入模拟器地址')
  simulator = '127.0.0.1:16384'
  d = Devices(simulator)
  rr = []
  rr_end = []
  for v in range(5):
      r2 = loopinfo(d.screenshot())
      if(r2.__len__() == rr_end.__len__()):   
          status = 0
          l = r2.__len__()
          for v in range(l):
             print(v)
             origin = rr[-(v+1)]
             comparison = r2[-(v+1)]
             if origin["name"] == comparison["name"] and \
                  origin["battles"] == comparison["battles"] and origin["times"] == comparison['times']:
                status += 1
          if status == l:
              break

      for v in r2:
          rr.append(v)
      d.swipe(950,1030,950,100)
      time.sleep(1)
      rr_end = r2
  print(rr)
