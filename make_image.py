import cv2
import sys

size = (48, 48)
image_t = 'uint16_t'
print('#include <avr/pgmspace.h>')
print('#ifndef IMG_WIDTH')
print('#define IMG_WIDTH', size[1])
print('#endif')
print('#ifndef IMG_HEIGHT')
print('#define IMG_HEIGHT', size[0])
print('#endif')
print('typedef %s image_t;' % image_t)
for i in range(1, len(sys.argv)):
    img = cv2.imread(sys.argv[i], cv2.IMREAD_COLOR)
    if img is None:
        print('failed to read image', file=sys.stderr)
        exit(1)
    img = cv2.resize(img, size)
    print('// %s' % sys.argv[i])
    print('const image_t image%d[IMG_WIDTH * IMG_HEIGHT] PROGMEM = {' % i)
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            a = img[y][x]
            c = ((a[2] & 0b11111000) << 8) + ((a[1] & 0b11111100) << 3) + (
                (a[0] & 0b11111000) >> 3)
            print('/* %2d-%d */ 0x%04X' % (x, y, c), end=', ')
        print()
    print('};')

print('#define COUNT_OF_IMAGES %d' % (len(sys.argv) - 1))
print('const image_t* images[COUNT_OF_IMAGES] = {', end=' ')
for i in range(1, len(sys.argv)):
    print('image%d' % i, end=', ')
print('};')
