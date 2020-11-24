from PIL import Image
import numpy as np


def encode(message, src, out):
    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n, m = 3, 0
    elif img.mode == 'RGBA':
        n, m = 4, 1
    total_pixels = array.size//n

    message += "~$@#OK"
    dat = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(dat)

    if req_pixels > total_pixels:
        print("ERROR! File's size is not sufficient for your message.")
        quit()
    else:
        index = 0
        for j in range(total_pixels):
            for k in range(m, n):
                if index < req_pixels:
                    array[j][k] = int(bin(array[j][k])[2:9] + dat[index], 2)
                    index += 1

    array = array.reshape(height, width, n)
    enc_img = Image.fromarray(array.astype("int8"), img.mode)
    enc_img.save(out)
    print("Encoding Successful.")


def decode(src):

    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
        m = 0
    elif img.mode == 'RGBA':
        n = 4
        m = 1

    total_pixels = array.size//n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(m, n):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == "~$@#OK":
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if "~$@#OK" in message:
        print("Hidden Message:", message[:-6])
    else:
        print("No Hidden Message Found")


def main():
    print("===Steno===", "1: Encode", "2: Decode", sep="\n")

    usr = input("Enter your option[1 or 2]:")
    if usr == '1':
        src = input("Enter image path:")
        message = input("Enter the message you want to hide:")
        output = input("Enter the path where you want to save new image:")
        encode(src=src, message=message, out=output)
    elif usr == '2':
        src = input("Enter path of image:")
        decode(src)
    else:
        print('Invalid Choice!!!')
        main()


if __name__ == '__main__':
    main()


