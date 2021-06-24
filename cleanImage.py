"""
=====================
cleanImage module doc
=====================
    README FIRST:
    1/Use MOUSE RIGHT BUTTON to select background color in 'CLEAN' window
    2/Then you need to hide regions of image (ROI) where pictwin is sure to not
    find any bubbles:
        [Top-left: logo] [Bottom-right: rules] [Bottom: features]
    Use the MOUSE LEFT BUTTON to draw areas on SOURCE window
    3/If you are not proud of your selections, don't be ashamed you are allowed
    to press 'r' to reset your work.
    4/If your are satisfied with your work, press 's' to save the image file
    (saved in dir: ./results/pictwin.png).
        picTwin joue avec Twin-It© (une invention originale de Thomas VUARCHEX)
===============================================================================
"""
import os
import cv2


class Cleaning(object):

    def __init__(self, poster, dirname):
        # Resizeable input windows
        cv2.namedWindow('CLEAN', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('CLEAN', int(poster.shape[0]/2), int(poster.shape[1]/2))
        cv2.moveWindow('CLEAN', 0, 0)
        # Instance variables
        self.img = poster
        self.save = poster
        self.img2 = poster.copy()
        self.dirname = dirname
        self.GREEN = [0, 255, 0]
        self.HIDE = [249, 250, 250]
        self.ix, self.iy = -1, -1
        self.drawing = False

    def getcolor_hide_mouse(self, event, x, y, flags, param):
        # Pick BGR values of the pixel underneath mouse cursor

        if event == cv2.EVENT_RBUTTONDOWN:
            self.ix, self.iy = x, y
        elif event == cv2.EVENT_RBUTTONUP:
            pix = self.img[self.ix, self.iy]
            self.HIDE[0], self.HIDE[1], self.HIDE[2] = int(pix[0]), int(pix[1]), int(pix[2])
            print('BGR values selected:{}'.format(self.HIDE))

        # Draw rectangle
        elif event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix, self.iy = x, y  # stores mouse position in global variables ix,iy
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing is True:
                self.img = self.img2.copy()  # refresh img to draw on clean image
                cv2.rectangle(self.img, (self.ix, self.iy), (x, y), self.GREEN, -1)
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            cv2.rectangle(self.img, (self.ix, self.iy), (x, y), self.HIDE, -1)
            self.img2 = self.img.copy()    # img2 will keep last drawn rectangle

    def clean(self):
        cv2.setMouseCallback('CLEAN', self.getcolor_hide_mouse)
        while True:
            cv2.imshow('CLEAN', self.img)
            k = 0xFF & cv2.waitKey(1)
            # key bindings
            if k == 27:  # esc to exit
                break
            elif k == ord('r'):  # reset all flags
                self.HIDE = [250, 250, 250]
                self.drawing = False
                self.img = self.save
                self.img2 = self.img.copy()
                print(" Values have been reset \n")
            elif k == ord('s'):  # save image
                cv2.imwrite(os.path.join(self.dirname, 'pictwin.png'), self.img)
                print("Saved in {}/pictwin.png".format(self.dirname))
                break
        cv2.destroyWindow('CLEAN')

    def get_image(self):
        return self.img
