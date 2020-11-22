import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2

val = [255 for i in range(3000000)]
datain = np.array(val, dtype=np.int8)
# print(datain)
datam = datain.reshape(1000, 1000, 3)
# print(datam)
img = Image.fromarray(datam, 'RGB')
img.show()
