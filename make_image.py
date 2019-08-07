import cv2
import sys

img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
if img is None:
  print("failed to read image")
  exit(1)

print(img.shape)
for x in range(0, img.shape[1]):
  print("{ ", end = "")
  for y in range(0, img.shape[0]):
    c = img[y][x]
    print(c[0], end = ", ")
    print(c[1], end = ", ")
    print(c[2], end = ", ")
  print("},")
