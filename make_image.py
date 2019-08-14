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
    print('const uint16_t image%d[IMG_WIDTH * IMG_HEIGHT] PROGMEM = {' % i)
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            a = img[y][x]
            c = ((a[2] & 0xF1) << 8) + ((a[1] & 0xFC) << 3) + (
                (a[0] & 0xF8) >> 3)
            print('/* %2d-%d */ 0x%04X' % (x, y, c), end=', ')
        print()
    print('};')

print('#define COUNT_OF_IMAGES %d' % (len(sys.argv) - 1))
print('const uint16_t * images[COUNT_OF_IMAGES] = {', end=' ')
for i in range(1, len(sys.argv)):
    print('image%d' % i, end=', ')
print('};')
