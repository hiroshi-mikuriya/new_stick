import cv2
import sys

img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
if img is None:
    print("failed to read image", file=sys.stderr)
    exit(1)

img = cv2.resize(img, (48, 48))
print("#include <avr/pgmspace.h>")
print("#ifndef IMG_WIDTH")
print("#define IMG_WIDTH", img.shape[1])
print("#endif")
print("#ifndef IMG_HEIGHT")
print("#define IMG_HEIGHT", img.shape[0])
print("#endif")
print("const uint8_t image[IMG_WIDTH * IMG_HEIGHT * 3 / 2] PROGMEM = {")
for x in range(0, img.shape[1]):
    print('  /* %2d */' % x, end=' ')
    for y in range(0, img.shape[0], 2):
        a0 = img[y][x]
        a1 = img[y + 1][x]
        c0 = (a0[2] & 0xF0) + ((a0[1] & 0xF0) >> 4)
        c1 = (a0[0] & 0xF0) + ((a1[2] & 0xF0) >> 4)
        c2 = (a1[1] & 0xF0) + ((a1[1] & 0xF0) >> 4)
        print('0x%02X,0x%02X,0x%02X,' % (c0, c1, c2), end='  ')
    print()
print("};")
