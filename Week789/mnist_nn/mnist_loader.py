import numpy as np
import struct

def load_images(filename):
    with open(filename, 'rb') as f:
        magic, num, rows, cols = struct.unpack(">IIII", f.read(16))
        images = np.frombuffer(f.read(), dtype=np.uint8)
        images = images.reshape(num, rows*cols)
        images = images / 255.0  # 归一化
        return images

def load_labels(filename):
    with open(filename, 'rb') as f:
        magic, num = struct.unpack(">II", f.read(8))
        labels = np.frombuffer(f.read(), dtype=np.uint8)
        return labels

def load_mnist(path='./', flatten=True):
    X_train = load_images(path + 'train-images-idx3-ubyte')
    y_train = load_labels(path + 'train-labels-idx1-ubyte')
    X_test = load_images(path + 't10k-images-idx3-ubyte')
    y_test = load_labels(path + 't10k-labels-idx1-ubyte')
    return X_train, y_train, X_test, y_test
