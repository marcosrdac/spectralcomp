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


def view_amplitudes(imgfour, axis):
    amp = np.sum(np.abs(imgfour), axis=1-axis)
    fig, ax = plt.subplots()
    ax.plot(np.arange(1, amp.size+1), amp)
    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.show()


def spectralcomp(img, axis=0, rg=None, gb=None,
                 rgp=None, gbp=None, interactive=False,
                 ratio_power=4):
    '''
    Create an RGB composition of frequencies.
    '''
    # passing image to Fourier domain
    imgfour = np.fft.rfft(img, axis=axis)
    # deriving limits to separate frequencies
    if interactive:
        view_amplitudes(imgfour, axis)
        rg = int(input('red-green limit at frquency: '))
        gb = int(input('green-blue limit at frquency: '))
    else:
        if rg is None or gb is None:
            if rgp is not None and gbp is not None:
                rg = int(rgp * imgfour.shape[axis])
                gb = int(gbp * imgfour.shape[axis])
            else:
                rg = int((1/3)**ratio_power * imgfour.shape[axis])
                gb = int((2/3)**ratio_power * imgfour.shape[axis])
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
    filename = '/home/marcosrdac/Dropbox/pictures/wallpapers/favorites/pebbles_in_beach_sunset.jpg'
    filename = '/home/marcosrdac/Dropbox/documents/personal/photos/agua25l.png'
    filename = '/home/marcosrdac/Dropbox/pictures/wallpapers/favorites/water_drop_on_leaf.jpg'
    filename = '/home/marcosrdac/Dropbox/pictures/wallpapers/favorites/white_tiger_chun_lo.png'

    axis = 1
    saveas = 'test.png'

    # opening image, making it grayscale
    filename = os.path.expanduser(filename)
    img = np.mean(np.array(Image.open(filename)), axis=-1)

    # decomposing image
    compostion = spectralcomp(img, axis=axis, interactive=True)

    # plotting results
    fig, ax = plt.subplots(1, 2, figsize=(8, 3))

    ax[0].set_title('Original Image')
    ax[0].imshow(img, cmap='Greys_r')

    ax[1].set_title('RGB spectral composition')
    ax[1].imshow(compostion)

    fig.tight_layout()

    fig.savefig(saveas)
    plt.show()
