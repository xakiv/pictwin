import cv2

import matchCells
import identify


class Result(object):

    def __init__(self, image, dirname):
        self.img = image
        self.dirname = dirname

    def play(self):
        """play() function doc

            Display matching areas found for a given cell #id

            Use trackbars to setup values for cells #id and Accurateness level
            NB: You can use NUMPAV keys also:
                8 and 2  for cell #id
                4 and 6  for Accurateness level

            Press 'm' to display matching area
        """
        match_getter = matchCells.Matching(self.img, self.dirname)
        contours_getter = identify.Identify(self.img, self.dirname)
        Contours, _ = contours_getter.contour()
        nb_Contours = len(Contours) - 1

        def nothing(x):
            pass

        # Create a black image, a window
        disp = self.img
        # Display debugging
        cv2.namedWindow('picTwin', cv2.WINDOW_KEEPRATIO)
        cv2.moveWindow('picTwin', 0, 0)
        cv2.resizeWindow('picTwin', 800, 1200)
        # Identify Cells
        labels = contours_getter.print_id(mode=None)
        cv2.namedWindow('Cell labels', cv2.WINDOW_NORMAL)
        cv2.imshow('Cell labels', labels)
        # create trackbars for cell id selection
        cv2.createTrackbar('Cell #Id', 'picTwin', 0, nb_Contours, nothing)
        # create trackbars for threshold selection
        cv2.createTrackbar('Precision', 'picTwin', 0, 20, nothing)
        cv2.imshow('picTwin', disp)
        while (1):
            cv2.imshow('picTwin', disp)
            k = 0xFF & cv2.waitKey(1)
            # key bindings
            if k == 27:         # esc to exit
                break
            elif k == ord('m'):  # matching
                cellId = cv2.getTrackbarPos('Cell #Id', 'picTwin')
                step = cv2.getTrackbarPos('Precision', 'picTwin')
                th = step / float(20)
                disp = match_getter.find_me(cellId, th)
                print("Results for Cell #{} and similarity level= {}% \n".format(
                    cellId, th * 100))
            elif k == ord('8'):
                pos = cv2.getTrackbarPos('Cell #Id', 'picTwin')
                pos = pos + 1
                cv2.setTrackbarPos('Cell #Id', 'picTwin', pos)
            elif k == ord('2'):
                pos = cv2.getTrackbarPos('Cell #Id', 'picTwin')
                pos = pos - 1
                cv2.setTrackbarPos('Cell #Id', 'picTwin', pos)
            elif k == ord('6'):
                pos = cv2.getTrackbarPos('Precision', 'picTwin')
                pos = pos + 1
                cv2.setTrackbarPos('Precision', 'picTwin', pos)
            elif k == ord('4'):
                pos = cv2.getTrackbarPos('Precision', 'picTwin')
                pos = pos - 1
                cv2.setTrackbarPos('Precision', 'picTwin', pos)

            elif k == ord('r'):  # reset
                disp = self.img

        cv2.destroyAllWindows()
