import cv2
import sys

img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
if img is None:
  print("failed to read image")
  exit(1)

img = cv2.resize(img, (48, 48))
print("#include <avr/pgmspace.h>")
print("#ifndef IMG_WIDTH")
print("#define IMG_WIDTH", img.shape[1])
print("#endif")
print("#ifndef IMG_HEIGHT")
print("#define IMG_HEIGHT", img.shape[0])
print("#endif")
print("const unsigned int image[IMG_WIDTH * IMG_HEIGHT] PROGMEM = {")
for x in range(0, img.shape[1]):
  print('  /* %2d */' % x, end = ' ')
  for y in range(0, img.shape[0]):
    c = img[y][x]
    c0 = (c[2] & 0xF8) + ((c[1] & 0xE0) >> 5)
    c1 = ((c[1] & 0x1C) << 3) + ((c[0] & 0xF8) >> 3)
    print('0x%02X%02X, ' % (c0, c1), end = ' ')
  print()
print("};")
