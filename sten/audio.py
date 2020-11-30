import wave


def embed(infile: str, message: str, outfile: str):
    song = wave.open(infile, mode='rb')
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))
    
    message = message + int((len(frame_bytes) - (len(message) * 8 * 8)) / 8) * '#'
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in message])))

    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    frame_modified = bytes(frame_bytes)

    with wave.open(outfile, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)
    song.close()


def extract(file: str):
    song = wave.open(file, mode='rb')
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    message = "".join(chr(int("".join(map(str, extracted[i:i+8])), 2)) for i in range(0, len(extracted), 8))
    decoded = message.split("###")[0]
    song.close()
    return decoded
