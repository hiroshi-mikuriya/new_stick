import cv2
import sys

img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
if img is None:
  print("failed to read image")
  exit(1)

img = cv2.resize(img, (50, 43))
print("#include <avr/pgmspace.h>")
print("#define IMG_WIDTH", img.shape[1])
print("#define IMG_HEIGHT", img.shape[0])
print("const uint8_t image[IMG_WIDTH * IMG_HEIGHT * 3] PROGMEM = {")
for x in range(0, img.shape[1]):
  print('  ', end = '')
  for y in range(0, img.shape[0]):
    c = img[y][x]
    print('0x%02X, 0x%02X, 0x%02X, ' % (c[0], c[1], c[2]), end = ' ')
  print()
print("};")
