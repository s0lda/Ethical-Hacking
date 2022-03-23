from typing import Any
import cv2
import numpy as np

def to_binary(data: str | bytes | int | np.ndarray[Any, Any] | np.uint8) -> str | list[str]:
    """Convert data to binary format as string."""
    if isinstance(data, str):
        return ''.join([format(ord(i), '08b') for i in data])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(i, '08b') for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, '08b')
    else:
        raise TypeError('Type not supported.')

def encode(image_file: str, secret_data: str):
    image = cv2.imread(image_file)
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print(f'Maximum to encode {n_bytes} byte(s).')
    if len(secret_data) > n_bytes:
        raise ValueError('Not enough bytes. Choose bigger image.')
    print('Encoding data...')
    secret_data += '====='
    data_index = 0
    binary_secret_data = to_binary(secret_data)
    data_len = len(binary_secret_data)
    for row in image:
        for pixel in row:
            r, g, b = to_binary(pixel)
            if data_index < data_len:
                pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                pixel[0] = int(g[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                pixel[0] = int(b[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index >= data_len:
                break
    return image

def decode(image_file: str) -> str:
    print('Decoding...')
    image = cv2.imread(image_file)
    binary_data = ''
    for row in image:
        for pixel in row:
            r, g, b = to_binary(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    all_bytes = [binary_data[i : i + 8] for i in range(0, len(binary_data), 8)]
    decoded_data = ''
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] = '=====':
            break
    return decoded_data