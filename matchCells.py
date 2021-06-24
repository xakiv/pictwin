import math
import os

import numpy as np
import cv2

import identify


class Matching(object):

    def __init__(self, image, dirname):
        # Instance variables
        self.img = image
        self.dirname = dirname
        self.BLUE = [255, 18, 0]  # color for query area
        self.RED = [0, 0, 255]  # color for matched areas

    def find(self):
        process = identify.Identify(self.img, self.dirname)
        contours, _ = process.contour()
        for i in range(0, len(contours)):
            cnt = contours[i]
            x, y, w, h = cv2.boundingRect(cnt)
            cropped_cell = process.extract_cell_rgb(i)
            img_hidden = process.hidden_rgb(i)

            # Match cropped cell template and masked image: Greyscale
            res = cv2.matchTemplate(
                img_hidden, cropped_cell, cv2.TM_CCOEFF_NORMED)
            threshold = 0.50
            # Return the tuple condition.nonzero(): the indices where condition is True
            loc = np.where(res >= threshold)
            nbMatch = 0
            img_rgb = self.img.copy()
            # Unpacking Argument Lists of loc
            cv2.rectangle(img_rgb, (x, y), (x + w, y + h), self.BLUE, 5)
            for pt in zip(*loc[::-1]):
                nbMatch = nbMatch + 1
                # Draw rect on matched area
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), self.RED, 5)
                if (nbMatch > 10):
                    match_file_name = 'Match-' + str(i) + '.png'
                    cv2.imwrite(os.path.join(
                        self.dirname, match_file_name), img_rgb)
                    break

    def find_id(self, cell_id, th):
        """
        Test function for returning matching results on an image where query cell is hide
        """
        process = identify.Identify(self.img, self.dirname)
        contours, _ = process.contour()
        print(cell_id)
        cnt = contours[cell_id]
        x, y, w, h = cv2.boundingRect(cnt)
        # Select a cell
        cropped_cell = process.extract_cell_rgb(cell_id)
        # Use an image where query cell was hide
        img_hidden = process.hidden_rgb(cell_id)
        # Match cropped cell template and masked image: Greyscale
        res = cv2.matchTemplate(img_hidden, cropped_cell, cv2.TM_CCOEFF_NORMED)
        threshold = th
        # Return the tuple condition.nonzero(): the indices where condition is True
        loc = np.where(res >= threshold)
        nbMatch = 0
        img_rgb = self.img.copy()
        cv2.rectangle(img_rgb, (x, y), (x + w, y + h), self.BLUE, 6)
        # Unpacking Argument Lists of loc
        for pt in zip(*loc[::-1]):
            nbMatch = nbMatch + 1
            # Draw rect of matched area
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), self.RED, 3)
        print('{} matched areas'.format(nbMatch))
        return img_rgb

    def find_me(self, cell_id, th):
        """
        Matching function & discard results regarding distance between query cell
        and matched cells
        """
        def distance(xa, ya, xb, yb):
            return math.sqrt((xb - xa)**2 + (yb - ya)**2)
        process = identify.Identify(self.img, self.dirname)
        contours, _ = process.contour()
        cnt = contours[cell_id]
        x, y, w, h = cv2.boundingRect(cnt)
        (centre_cnt_x, centre_cnt_y), radius = cv2.minEnclosingCircle(cnt)
        cell = self.img[y:y + h, x:x + w]
        img_rgb = self.img.copy()

        # Match cropped cell template and masked image: Greyscale
        res = cv2.matchTemplate(self.img, cell, cv2.TM_CCOEFF_NORMED)
        threshold = th
        loc = np.where(res >= threshold)
        nbMatch = 0
        # Show query cell in blue
        cv2.rectangle(img_rgb, (x, y), (x + w, y + h), self.BLUE, 6)

        # Unpacking Argument Lists of loc
        for pt in zip(*loc[::-1]):
            nbMatch = nbMatch + 1
            # Get the center of current matching rectangle
            centerTx = ((2 * pt[0] + w) / 2)
            centerTy = ((2 * pt[1] + h) / 2)
            # Distance between both center
            calc_dist = distance(
                centre_cnt_x, centre_cnt_y, centerTx, centerTy)
            # Only draw matching area
            if calc_dist > radius:
                # Draw rect of matched area
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), self.RED, 3)
        print('{} matched areas'.format(nbMatch))
        return img_rgb
