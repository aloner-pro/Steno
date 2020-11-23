import numpy as np
from PIL import Image

data = input('Enter your message:')
datalist = [ord(i) for i in data]
val = [150 for i in range(3000000)]
datain = np.array(val, dtype=np.int64)
datam = datain.reshape(1000, 1000, 3)
img = Image.fromarray(datam, 'RGB')
img.show()
