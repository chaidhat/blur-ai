import numpy as np
from scipy import ndimage
from PIL import Image
from os import listdir
from os.path import isfile, join
from os import system


OUTPUT_IMAGE_SIZE = (256, 256)

def pil2numpy(path, img: Image = None) -> np.ndarray:
    """
    Convert an HxW pixels RGB Image into an HxWx3 numpy ndarray
    """

    if img is None:
        img = Image.open(path)
        img = img.resize(OUTPUT_IMAGE_SIZE)	# resize to 256, 256

    np_array = np.asarray(img)
    return np_array


def numpy2pil(np_array: np.ndarray) -> Image:
    """
    Convert an HxWx3 numpy array into an RGB Image
    """

    assert_msg = 'Input shall be a HxWx3 ndarray'
    assert isinstance(np_array, np.ndarray), assert_msg

    if (len(np_array.shape) == 2):
        img = Image.fromarray(np_array, 'L')
        return img
    else:
        assert len(np_array.shape) == 3, assert_msg
        assert np_array.shape[2] == 3, assert_msg
        img = Image.fromarray(np_array, 'RGB')
        return img


path = "./cv-project-raw/"
files = [f for f in listdir(path) if isfile(join(path, f))]

for f in files:
    p = f.split(".")[0]
    ext = ""
    pre = ""
    if p.split("-")[1] == "rgb":
        pre = "features/"
        ext = ".jpg"
    else:
        pre = "predictions/"
        ext = ".jpeg"
    print(p + ext)
    try:
        image = pil2numpy("./cv-project-raw/" + p + ext)
        img = numpy2pil(image)
        img.save("./cv-project-preprocessed/" + pre + p.split("-")[0] + ".png")
    except:
        print("oops" + p)

#image = pil2numpy()
#img = numpy2pil(image)
#img.save("yay.png")