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
        # 1 - ellipses, 2 - circles, 3 - triangles, -1 - squares, -2 - rectangles,
        # -3 - chains, -4 periods, 4 - convex polygons (> 4 vertices)
        # 0 - other unclassified figures
        self.colors = {
            -4: (121, 50, 168),
            -3: (9, 9, 235),
            -2: (66, 81, 245),
            -1: (66, 150, 245),
             0: (66, 233, 245),
             1: (66, 245, 170),
             2: (138, 245, 66),
             3: (245, 212, 66),
             4: (227, 20, 55)
        }

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

    def process(self):
        if not self.contours:
            self.find_contours()
        # Searching through every region selected to
        # find the required polygon
        for i, cnt in enumerate(self.contours) :
            # calculate area and perimeter of countour
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt,True)
            # approximation by polygon
            approx_polygon = cv2.approxPolyDP(cnt, 0.009 * perimeter, closed = True)
            contour_info = self.analyze_polygon(approx_polygon, area, perimeter)
            # If contour is a chain or period - we also receive it length
            if contour_info[0] <= -3:
                contour_length = contour_info[1]
            # Highlighting contour
            color = self.colors[contour_info[0]]
            cv2.drawContours(self.img, [approx_polygon], 0, color, 3)
                    
    def analyze_polygon(self, verticies, area, perimeter):
        # If passed vertices present polygon, that too close
        # to some ellipse - return 1, if it circle - return 2
        polygon = Polygon(verticies, area, perimeter)
        # Check if contour is close to chain or period
        # If thats it - we also receive length as 3rd argument
        is_chain, is_period, length = polygon.is_chain()
        if is_period:
            return -4, length
        if is_chain:
            return -3, length
        # If triangle - contour_type is 3
        if polygon.is_triangle():
            return (3, None)
        # If rectangle - contour_type is -2, square — -1
        is_rectangle = polygon.is_rectangle()
        if is_rectangle:
            return (is_rectangle, None)
        # ellipse - 1, circle - 2
        is_ellipse = polygon.is_ellipse()
        if is_ellipse:
            return (is_ellipse, None)
        # Other - contour type is zero
        return (0, None)


if __name__ == "__main__":
    img_path = 'blob.jpg'
    shape_detector = ShapeDetector(img_path)

    # Recognition operations
    shape_detector.process()

    # Displaying result
    shape_detector.show_image()

    # Exiting the window if 'q' is pressed on the keyboard.
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()