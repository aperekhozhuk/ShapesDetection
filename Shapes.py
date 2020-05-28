import numpy as np
import cv2
from Polygon import Polygon

class ShapeDetector:

    def __init__(self, img_path):
        # Reading image
        self.img = cv2.imread(img_path, cv2.IMREAD_COLOR)

        # Reading same image in another variable and
        # converting to gray scale.
        self.img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        # Converting image to a binary image
        _,self.img_binary = cv2.threshold(self.img_gray, 110, 255, cv2.THRESH_BINARY)
        self.contours = None
        # On result image we'll highlight every kind of figure in some color
        # 1 - ellipses, 2 - circles, 0 - other unclassified figures
        self.colors = {0: (0, 0, 255), 1: (255, 0, 0), 2: (0, 255, 0)}

    def show_image(self):
        cv2.imshow('Output', self.img)

    def find_contours(self):
        # Detecting shapes in image by selecting region
        # with same colors or intensity.
        self.contours,_= cv2.findContours(
            image = self.img_binary,
            mode=cv2.RETR_TREE,
            method=cv2.CHAIN_APPROX_SIMPLE
        )

    def draw_contours(self):
        if not self.contours:
            self.find_contours()
        # Searching through every region selected to
        # find the required polygon
        for i, cnt in enumerate(self.contours) :
            approx_polygon = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), closed = True)
            contour_type = self.analyze_polygon(approx_polygon)
            color = self.colors[contour_type]
            cv2.drawContours(self.img, [approx_polygon], 0, color, 3)
                    
    def analyze_polygon(self, verticies):
        # If passed vertices present polygon, that too close
        # to some ellipse - return 1, if it circle - return 2
        polygon = Polygon(verticies)
        is_ellipse = polygon.is_ellipse()
        if is_ellipse:
            return is_ellipse
        return 0


if __name__ == "__main__":
    img_path = 'blob.jpg'
    shape_detector = ShapeDetector(img_path)

    # Recognition operations
    shape_detector.draw_contours()

    # Displaying result
    shape_detector.show_image()

    # Exiting the window if 'q' is pressed on the keyboard.
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()