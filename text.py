import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image


width = 48
height = 48
font = ImageFont.truetype('ヒラギノ角ゴシック W9.ttc', 32)
char_list = list('ようこそこんにちは')
# REDは人によっては見えづらいことがあるので入れない
colors = [(0xFF, 0x00, 0x00), (0xFF, 0xFF, 0x00), (0x00, 0xFF, 0x00), (0x00, 0xFF, 0xFF), (0xFF, 0x00, 0xFF)]

for i in range(len(char_list)):
  c = char_list[i]
  rgb = colors[i % len(colors)]
  img = np.zeros((height, width, 3), np.uint8)
  # 画像を変換し、テキストを描画
  img_pil = Image.fromarray(img)
  draw = ImageDraw.Draw(img_pil)
  draw.text((5, 5), c, font = font, fill = rgb)
  # 描画したイメージをnumpyの配列に戻して出力
  img = np.array(img_pil)
  cv2.imwrite(str(i) + '.png', img)
