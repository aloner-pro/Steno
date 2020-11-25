import numpy as np
from PIL import Image

val = [150 for i in range(3000000)]
array = np.array(val, dtype=np.int8).reshape(1000, 1000, 3)
total_pixels = array.size//3

data = input('Enter your message:')
mess = "".join([format(ord(i), '08b') for i in data])
req_pixels = len(mess)

if req_pixels > total_pixels:
    print("ERROR! File's size is not sufficient for your message.")
    quit()
else:
    index = 0
    for j in range(total_pixels):
        for k in range(0, 3):
            if index < req_pixels:
                array[j][k] = int(bin(array[j][k])[2:9] + data[index], 2)
                index += 1

array2 = array.reshape(1000, 1000, 3)
img = Image.fromarray(array, mode='RGB')
img.show()
