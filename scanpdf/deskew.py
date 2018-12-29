# import cv2
import numpy as np
import scipy
import scipy.misc
import random
from operator import itemgetter
import skimage.filters

def deskew_fft(image):
    #import cv2
    #image = cv2.GaussianBlur(image,(3,3),0)
    skimage.filters.gaussian(image, 3)
    ft = np.fft.fft2(image)
    ftshift = np.fft.fftshift(ft)
    spek = 20 * np.log(np.abs(ftshift))
    spect_center = (spek[np.uint32(spek.shape[0]/2)-np.uint32(spek.shape[0]/6):np.uint32(spek.shape[0]/2)+np.uint32(spek.shape[0]/6),np.uint32(spek.shape[1]/2)-np.uint32(spek.shape[1]/14):np.uint32(spek.shape[1]/2)+np.uint32(spek.shape[1]/14)])

    maxS = 0
    uhel = 0
    for i in range(-15,15):
        imr = scipy.misc.imrotate(spect_center, i*0.1)
        temp = np.max(np.sum(imr,0))
        if temp > maxS:
            maxS = temp
            uhel = i*0.1
    return uhel


def measure(image, size=512):
    px = random.randint(0, image.shape[1] - size)
    py = random.randint(0, image.shape[0] - size)
    part = image[py:py + size, px:px + size]
    angle = deskew_fft(part)
    return angle


def deskew_mean(image, echo=False):
    zmean = 0
    n = 100
    for i in range(n):
        z = measure(image)
        zmean = zmean + z
        if echo:
            print('measurement', i, 'angle', zmean/float(i+1))
    return zmean / float(n)

def deskew(image):
    angle = deskew_mean(image)
    return angle

def rotate(image, angle):
    temp_image = np.ones([image.shape[0] * 2, image.shape[1] * 2], dtype=np.uint8) * np.mean(image)
    ymin = int(temp_image.shape[0] / 2.0 - image.shape[0] / 2.0)
    ymax = int(temp_image.shape[0] / 2.0 + image.shape[0] / 2.0)
    xmin = int(temp_image.shape[1] / 2.0 - image.shape[1] / 2.0)
    xmax = int(temp_image.shape[1] / 2.0 + image.shape[1] / 2.0)
    temp_image[ymin: ymax, xmin: xmax] = image
    temp_image = scipy.misc.imrotate(temp_image, angle, 'bicubic')
    image = temp_image[ymin: ymax, xmin: xmax]
    return image

'''
 Nova verze, ktera vybira casti obrazu deterministicky
'''

def deskew_determ(gray):
    tiles = []
    for y in range(0, 3504 - 219, 73):
        y2 = y + 219
        for x in range(0, 2480 - 248, 124):
            x2 = x + 248
            tiles.append((y, y2, x, x2, np.mean(gray[y:y2, x:x2])))
    tiles.sort(key=itemgetter(4))
    zmean = 0
    n = int(len(tiles) / 8)
    for i in range(n):
        part = gray[tiles[i][0]:tiles[i][1], tiles[i][2]:tiles[i][3]]
        z = deskew_fft(part)
        zmean = zmean + z
    #cv2.destroyAllWindows()
    angle = zmean / float(n)
    return angle

def deskew_determ_small(gray):
    tiles = []
    if gray.shape[0] < 100:
        return 0
    for y in range(0, gray.shape[0] - gray.shape[0]/5, gray.shape[0]/10):
        y2 = y + 219
        for x in range(0, 2480 - 248, 124):
            x2 = x + 248
            tiles.append((y, y2, x, x2, np.sum(gray[y:y2, x:x2])))
    tiles.sort(key=itemgetter(4))
    zmean = 0
    if tiles < 8:
        return 0
    n = len(tiles)/8
    for i in range(n+1):
        part = gray[tiles[i][0]:tiles[i][1], tiles[i][2]:tiles[i][3]]
        z = deskew_fft(part)
        zmean = zmean + z

    angle = zmean / float(n)

    return angle