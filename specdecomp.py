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


def spectralcomp(img, axis=0, rgp=None, gbp=None, ratio_power=4):
    '''
    Create an RGB composition of frequencies.
    '''
    # passing image to Fourier domain
    imgfour = np.fft.rfft(img, axis=axis)
    # deriving limits to separate frequencies
    if rgp is None or gbp is None:
        rg = int((1/3)**ratio_power * imgfour.shape[axis])
        gb = int((2/3)**ratio_power * imgfour.shape[axis])
    else:
        rg = int(rgp * imgfour.shape[axis])
        gb = int(gbp * imgfour.shape[axis])
    # creating channels in fouorier domain
    channelsfour = np.zeros((imgfour.shape[0], imgfour.shape[1], 3),
                            dtype=np.complex)
    # puts contents of
    if axis == 0:
        channelsfour[:rg, :, 0] = imgfour[:rg, :]
        channelsfour[rg:gb, :, 1] = imgfour[rg:gb, :]
        channelsfour[gb:, :, 2] = imgfour[gb:, :]
    else:
        channelsfour[:, :rg, 0] = imgfour[:, :rg]
        channelsfour[:, rg:gb, 1] = imgfour[:, rg:gb]
        channelsfour[:, gb:, 2] = imgfour[:, gb:]
    channels = np.fft.irfft(channelsfour, axis=axis)
    for i in range(3):
        channels[:, :, i] = normalize(channels[:, :, i])
    return(channels)




if __name__ == '__main__':
    import os

    # parameters
    filename = '/home/marcosrdac/Dropbox/documents/personal/photos/agua25l.png'
    axis = 1
    ratio_power = 4

    # opening image, making it grayscale
    filename = os.path.expanduser(filename)
    img = np.mean(np.array(Image.open(filename)), axis=-1)

    # decomposing image
    compostion = spectralcomp(img, axis=axis, ratio_power=ratio_power)

    # plotting results
    fig, ax = plt.subplots(1, 2, figsize=(8, 3))

    ax[0].set_title('Original Image')
    ax[0].imshow(img, cmap='Greys_r')

    ax[1].set_title('RGB spectral composition')
    ax[1].imshow(compostion)

    fig.tight_layout()

    #fig.savefig('me.png')
    plt.show()
