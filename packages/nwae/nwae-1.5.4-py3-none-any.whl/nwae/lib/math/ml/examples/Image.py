
import numpy as np
import cv2
from matplotlib import pyplot as plt

img_path = '/Users/mark/Desktop/opencv.png'

img = cv2.imread(img_path)
print('Image type "' + str(type(img)) + '"dtype "' + str(img.dtype) + '", shape ' + str(img.shape))

px = img[100,100]
print('Pixel = ' + str(px))

plt.imshow(
    img,
    #cmap = 'gray',
    #interpolation = 'bicubic'
)
#plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()
