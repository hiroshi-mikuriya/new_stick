import cv2
import sys

size = (48, 48)
print('#include <avr/pgmspace.h>')
print('#ifndef IMG_WIDTH')
print('#define IMG_WIDTH', size[1])
print('#endif')
print('#ifndef IMG_HEIGHT')
print('#define IMG_HEIGHT', size[0])
print('#endif')

for i in range(1, len(sys.argv)):
    img = cv2.imread(sys.argv[i], cv2.IMREAD_COLOR)
    if img is None:
        print('failed to read image', file=sys.stderr)
        exit(1)
    img = cv2.resize(img, size)
    print('// %s' % sys.argv[i])
    print('const uint8_t image%d[IMG_WIDTH * IMG_HEIGHT * 3 / 2] PROGMEM = {' % i)
    for x in range(0, img.shape[1]):
        print('  /* %2d */' % x, end=' ')
        for y in range(0, img.shape[0], 2):
            a0 = img[y][x]
            a1 = img[y + 1][x]
            c0 = (a0[2] & 0xF0) + ((a0[1] & 0xF0) >> 4)
            c1 = (a0[0] & 0xF0) + ((a1[2] & 0xF0) >> 4)
            c2 = (a1[1] & 0xF0) + ((a1[0] & 0xF0) >> 4)
            print('0x%02X,0x%02X,0x%02X,' % (c0, c1, c2), end='  ')
        print()
    print('};')

print('#define COUNT_OF_IMAGES %d' % (len(sys.argv) - 1))
print('const uint8_t * images[COUNT_OF_IMAGES] = {', end = ' ')
for i in range(1, len(sys.argv)):
    print('image%d' % i, end = ', ')
print('};')