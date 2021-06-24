import os
import shutil

import cv2

import cleanImage
import identify
import display

IMAGE_PATH = 'data/twinit-sample.png'

if __name__ == '__main__':

    dirname = 'results'
    if os.path.exists(dirname):
        shutil.rmtree(dirname, ignore_errors=True)
    os.mkdir(dirname)

    # Read original file:
    poster = cv2.imread(IMAGE_PATH, 1)

    print('Poster dim. and channels: {}'.format(poster.shape))

    # Cleaning poster
    print(cleanImage.__doc__)
    start = cleanImage.Cleaning(poster, dirname)
    start.clean()
    img = start.get_image()

    # Save contours Id & mask
    keep_roll = identify.Identify(img, dirname)
    keep_roll.mask(mode=1)
    keep_roll.print_id(mode=1)

    # Match Cells and display results
    finish = display.Result(img, dirname)
    print(display.Result.play.__doc__)
    finish.play()

    # Close all window
    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()
