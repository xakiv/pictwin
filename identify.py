import os

import cv2
import numpy as np


class Identify(object):

    def __init__(self, image, dirname):
        # Instance variables
        self.img = image
        self.dirname = dirname

    def mask(self, mode=None):
        """Creat a mask of a given image:
        Use cv2.threshold() with cv2.THRESH_BINARY_INV mode to get a binary image
        with white forground and black background
        Use cv2.morphologyEx() with cv2.MORPH_OPEN option to remove BG noises
        """
        # Convert original image to grayscale option
        img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        # Bounding detection:
        # Threshold = 249, as brightness background area between 250 and 255
        ret, mask_inv = cv2.threshold(
            img_gray, 249, 255, cv2.THRESH_BINARY_INV)  # FG=White BG=Black
        # Morphological Gradient
#        kernel = np.ones((3,3),np.uint8)
        kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.uint8)
        gradient_mask_inv = cv2.morphologyEx(mask_inv, cv2.MORPH_OPEN, kernel)
        if mode is None:
            return gradient_mask_inv
        else:
            cv2.imwrite(os.path.join(
                self.dirname, "mask Result.png"), gradient_mask_inv)
            cv2.imwrite(os.path.join(
                self.dirname, "threshold249.png"), mask_inv)
            cv2.imwrite(os.path.join(self.dirname, "img_gray.png"), img_gray)

    def contour(self):
        # Copy gradient_mask_inv into gradient_mask_inv2:
        # findContours function modifies the source image
        gradient_mask_inv2 = self.mask()
        # Find countour
        contours, hierarchy = cv2.findContours(
            gradient_mask_inv2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # return values using a tuple
        return (contours, hierarchy)

    def print_id(self, mode=None):
        img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        # To draw colored id on grayscal img
        img_gray_3chan = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
        contours, hierarchy = self.contour()
        # Cell iteration
        for i in range(0, len(contours)):
            cnt = contours[i]
            (centre_cnt_x, centre_cnt_y), radius = cv2.minEnclosingCircle(cnt)
            # Draw labels on
            font = cv2.FONT_HERSHEY_SIMPLEX
            im_with_label = cv2.putText(img_gray_3chan, str(
                i), (int(centre_cnt_x), int(centre_cnt_y)), font, 1, (72, 33, 242), 3)
        if mode is None:
            return im_with_label
        else:
            cv2.imwrite(os.path.join(
                self.dirname, "Cells ID.png"), im_with_label)

    def extract_cell_gray(self, i, mode=None):
        """Extract one cell from self.img with #id = i argument

            Call contour() to get all contours
            Get position and dimension of query cell's rectangle w/ cv2.boundingRect()
            Creat an array filled w/ zeros (black) and the same shape of the grayscaled image
            Fill-in the body of the query cell (w/ white) and draw it in previous array
            Creat an array filled w/ zeros (black) and the same shape of the grayscaled image
                out[contours_img == 255] = img_gray[contours_img == 255]
            We select the region of img_gray that corresponds to our mask in contours_img
            (as cell filled-in w/ 255)
            This selected region will be transferred on our 'out' array in same position
            We crop the cell's rectangle on a black background
            The purpose is to only use the texture of the query cell for matching and avoid s
            surrounding cells part

            If 'mode' is not 'None' extract_cell)() will write image's file in current directory
        """
        img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        contours, _ = self.contour()
        cnt = contours[i]
        x, y, w, h = cv2.boundingRect(cnt)
        # Crop internal area of current cell
        # Return a new array of given shape and type, filled with zeros.
        contours_img = np.zeros(img_gray.shape, np.uint8)
        cv2.drawContours(contours_img, [cnt], 0, (255, 255, 255), -1)
        # Same as np.zeros() but return an array w/ same dtype as the given array
        out = np.zeros_like(img_gray)
        out[contours_img == 255] = img_gray[contours_img == 255]
        cropped_cell = out[y:y + h, x:x + w]
        if mode is None:
            return cropped_cell
        else:
            cropped_cell_file = 'cropped_cell-' + str(i) + '.png'
            cv2.imwrite(os.path.join(
                self.dirname, cropped_cell_file), cropped_cell)

    def extract_cell_rgb(self, i, mode=None):
        contours, hierarchy = self.contour()
        cnt = contours[i]
        x, y, w, h = cv2.boundingRect(cnt)
        # Crop internal area of current cell
        # Return a new array of given shape and type, filled with zeros.
        contours_img = np.zeros(self.img.shape, np.uint8)
        cv2.drawContours(contours_img, [cnt], 0, (255, 255, 255), -1)
        # Return a new array of given shape and type, filled with zeros.
        out = np.zeros_like(self.img)
        out[contours_img == 255] = self.img[contours_img == 255]
        cropped_cell = out[y:y + h, x:x + w]
        if mode is None:
            return cropped_cell
        else:
            cropped_cell_file = 'cropped_cell-' + str(i) + '.png'
            cv2.imwrite(os.path.join(
                self.dirname, cropped_cell_file), cropped_cell)

    def extract_all_cells(self):
        img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        # Copy gradient_mask_inv into gradient_mask_inv2:
        # findContours function modifies the source image
        gradient_mask_inv2 = self.mask()
        # Find countour
        imCont, contours, hierarchy = cv2.findContours(
            gradient_mask_inv2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # makeDir for cropped cells
        dirCroppedCells = str(self.dirname) + '/croppedDB'
        os.mkdir(dirCroppedCells)
        # Cell iteration
        for i in range(0, len(contours)):
            cnt = contours[i]
            x, y, w, h = cv2.boundingRect(cnt)
            # Return a new array of given shape and type, filled with zeros.
            contours_img = np.zeros(img_gray.shape, np.uint8)
            cv2.drawContours(contours_img, [cnt], 0, (255, 255, 255), -1)
            # Return a new array of given shape and type, filled with zeros.
            out = np.zeros_like(img_gray)
            out[contours_img == 255] = img_gray[contours_img == 255]
            cropped_cell = out[y:y + h, x:x + w]
            cropped_cell_file = 'cropped_cell-' + str(i) + '.png'
            cv2.imwrite(os.path.join(dirCroppedCells,
                                     cropped_cell_file), cropped_cell)

    def extract_all_cells_rgb(self):
        # Copy gradient_mask_inv into gradient_mask_inv2:
        # findContours function modifies the source image
        gradient_mask_inv2 = self.mask()
        # Find countour
        imCont, contours, hierarchy = cv2.findContours(
            gradient_mask_inv2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # makeDir for cropped cells
        dirCroppedCells = str(self.dirname) + '/croppedDBrgb'
        os.mkdir(dirCroppedCells)
        # Cell iteration
        for i in range(0, len(contours)):
            cnt = contours[i]
            x, y, w, h = cv2.boundingRect(cnt)
            # Return a new array of given shape and type, filled with zeros.
            contours_img = np.zeros(self.img.shape, np.uint8)
            cv2.drawContours(contours_img, [cnt], 0, (255, 255, 255), -1)
            # Return a new array of given shape and type, filled with zeros.
            out = np.zeros_like(self.img)
            out[contours_img == 255] = self.img[contours_img == 255]
            cropped_cell = out[y:y + h, x:x + w]
            cropped_cell_file = 'cropped_cell-' + str(i) + '.png'
            cv2.imwrite(os.path.join(dirCroppedCells,
                                     cropped_cell_file), cropped_cell)

    def hide_cell(self):
        # Copy gradient_mask_inv into gradient_mask_inv2:
        # findContours function modifies the source image
        gradient_mask_inv2 = self.mask()
        # Find countour
        imCont, contours, hierarchy = cv2.findContours(
            gradient_mask_inv2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Creat directory
        dirHiddenCells = str(self.dirname) + '/hiddenDB'
        os.mkdir(dirHiddenCells)
        # Cell iteration
        for i in range(0, len(contours)):
            cnt = contours[i]
            # Return a new array of given shape and type, filled with zeros.
            contours_img = np.zeros(self.img.shape, np.uint8)
            cv2.drawContours(contours_img, [cnt], 0, (255, 255, 255), -1)
            removed = cv2.add(self.img, contours_img)
            removed_img_file = 'removed_cell-' + str(i) + '.png'
            cv2.imwrite(os.path.join(dirHiddenCells,
                                     removed_img_file), removed)

    def hidden_rgb(self, i):
        # Copy gradient_mask_inv into gradient_mask_inv2:
        # findContours function modifies the source image
        gradient_mask_inv2 = self.mask()
        # Find countour
        imCont, contours, hierarchy = cv2.findContours(
            gradient_mask_inv2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[i]
        copy = self.img.copy()
        cv2.drawContours(copy, [cnt], 0, (255, 255, 255), -1)
        return copy

    def hidden_gray(self, i):
        img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        # Copy gradient_mask_inv into gradient_mask_inv2:
        # findContours function modifies the source image
        gradient_mask_inv2 = self.mask()
        # Find countour
        imCont, contours, hierarchy = cv2.findContours(
            gradient_mask_inv2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[i]
        cv2.drawContours(img_gray, [cnt], 0, (255, 255, 255), -1)
        return img_gray
