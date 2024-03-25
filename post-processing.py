import cv2
import numpy as np
import requests
from tqdm import tqdm
import warnings
import matplotlib as mpl
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

# how many images are there?
n_images = 10
img_data = np.empty([n_images, 3, 256, 256, 3])

def blur():
  for n in range(n_images):
    # test image loading
    test=True
    print('test mode ON')
    print('loading image...')
    img = cv2.imread("rgb" + str(n) + ".png", cv2.IMREAD_COLOR)
    print(img.shape)
    img_data[n, 0] = img
    #cv2.imwrite('img_input.png', img)
    print('image loaded')


    # make blur map
    height = img.shape[0]
    width = img.shape[1]
    blur_map = cv2.imread("d" + str(n) + ".png", cv2.IMREAD_COLOR)
    img_data[n, 1] = blur_map
    blur_scale = 30

    for c in range(blur_map.shape[2]):
      for x in tqdm(range(width)):
          for y in range(height):
            blur_map[x, y, c] = min(max((150 - blur_map[x, y, c]) / blur_scale, 0), 254)
    cv2.imwrite('blurmap.png', blur_map );


    # very inefficient blur algorithm!!!
    img_blur = np.copy(img)
    for c in range(img.shape[2]):
      for x in tqdm(range(width)):
          for y in range(height):
              kernel_size = int(blur_map[y, x, 0])

              # no blur applied, then just skip
              if kernel_size == 0:
                  img_blur[y, x, c] = img[y, x, c]
                  continue

              kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
              cut = img[
                  max(0, y - kernel_size):min(height, y + kernel_size),
                  max(0, x - kernel_size):min(width, x + kernel_size),
                  c
              ]

              if cut.shape == kernel.shape:
                  cut = (cut * kernel).mean()
              else:
                  cut = cut.mean()

              img_blur[y, x, c] = cut
    img_data[n, 2] = img_blur
    cv2.imwrite('output' + str(n) + '.png', img_blur);
    print('done')

blur()

plt.axis('off')
f, axarr = plt.subplots(nrows=int(n_images / 2), ncols=6, figsize=(16, 16), tight_layout=True)
n = 0
for n in range(int(n_images / 2)):
  img = plt.imread("rgb" + str(n * 2) + ".png",1)
  blur_map = plt.imread("d" + str(n * 2) + ".png",1)
  output = plt.imread("output" + str(n * 2) + ".png",1)

  axarr[n,0].imshow(img, interpolation='nearest')
  axarr[n,0].set_title("rgb")
  axarr[n,1].imshow(blur_map, interpolation='nearest')
  axarr[n,1].set_title("depth map")
  axarr[n,2].imshow(output, interpolation='nearest')
  axarr[n,2].set_title("blurred rgb")

  axarr[n,0].axis("off")
  axarr[n,1].axis("off")
  axarr[n,2].axis("off")

  img = plt.imread("rgb" + str(n * 2 + 1) + ".png",1)
  blur_map = plt.imread("d" + str(n * 2 + 1) + ".png",1)
  output = plt.imread("output" + str(n * 2 + 1) + ".png",1)

  axarr[n,3].imshow(img, interpolation='nearest')
  axarr[n,3].set_title("rgb")
  axarr[n,4].imshow(blur_map, interpolation='nearest')
  axarr[n,4].set_title("depth map")
  axarr[n,5].imshow(output, interpolation='nearest')
  axarr[n,5].set_title("blurred rgb")

  axarr[n,3].axis("off")
  axarr[n,4].axis("off")
  axarr[n,5].axis("off")
