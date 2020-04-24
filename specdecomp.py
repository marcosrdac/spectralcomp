#!/usr/bin/env python3

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def normalize(img):
    '''
    Normalizes array with values ranging from 0 to 1.
    '''
    imgmax = img.max()
    imgmin = img.min()
    normalized = (img - imgmin) / (imgmax - imgmin)
    return(normalized)


def spectral_composition(img, axis=0, ratio_power=4):
    '''
    Create an RGB composition of frequencies.
    '''
    # passing image to Fourier domain
    imgfour = np.fft.rfft(img, axis=axis)
    # deriving limits to separate frequencies
    rg = int((1/4)**ratio_power * imgfour.shape[0])
    gb = int((2/4)**ratio_power * imgfour.shape[0])
    # creating channels in fouorier domain
    channelsfour = np.zeros((imgfour.shape[0], imgfour.shape[1], 3),
                            dtype=np.complex)
    # puts contents of
    if axis == 0:
        channelsfour[:rg, :, 0] = imgfour[:rg, :]
        channelsfour[rg:gb, :, 1] = imgfour[rg:gb, :]
        channelsfour[gb:, :, 2] = imgfour[gb:, :]
    else:
        channelsfour[:, :rg,   0] = imgfour[:, :rg]
        channelsfour[:, rg:gb, 1] = imgfour[:, rg:gb]
        channelsfour[:, gb:,   2] = imgfour[:, gb:]
    channels = np.fft.irfft(channelsfour, axis=axis)
    for i in range(3):
        channels[:, :, i] = normalize(channels[:, :, i])
    return(channels)


if __name__ == '__main__':
    filename = '/home/marcosrdac/Dropbox/pictures/wallpapers/favorites/water_drop_on_leaf.jpg'
    axis = 1
    ratio_power = 5

    img = np.mean(np.array(Image.open(filename)), axis=-1)

    compostion = spectral_composition(img, axis=axis, ratio_power=ratio_power)

    fig, ax = plt.subplots(1,2, figsize=(8,3))

    ax[0].set_title('Original Image')
    ax[0].imshow(img, cmap='Greys_r')

    ax[1].set_title('RGB spectral composition')
    ax[1].imshow(compostion)

    fig.tight_layout()

    fig.savefig('asdk.png')
    plt.show()
