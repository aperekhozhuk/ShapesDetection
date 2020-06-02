import numpy as np

class Polygon:

    def __init__(self, vertices, area, perimeter):
        self.point_count = len(vertices)
        # Here we receive accurate area and perimeter of contour
        self.area = area
        self.perimeter = perimeter
        # convert np.ndarray to np.array for easier accessing
        self.vertices = np.empty((self.point_count,2), dtype = np.int32)
        for i, x in enumerate(vertices):
            self.vertices[i] = x[0]

    # returns square of distance between i-th and j-th points of polygon
    def distance(self, i,j):
        p1 = self.vertices[i]
        p1 = (p1[0], p1[1])
        p2 = self.vertices[j]
        p2 = (p2[0], p2[1])
        return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

    # Return bool vector ("polygon is chain?", "polygon is a period")
    def is_chain(self, thickness = 4):
        length = None
        is_chain = (self.area/self.perimeter) < thickness
        is_period = False
        if is_chain and (self.point_count == 2):
            is_period = True
            length = self.distance(0,1)**0.5
        # If polygon is actually chain
        if is_chain and not is_period:
            length = 0
            # It length = sum of length of segments
            for i in range(self.point_count):
                length += (self.distance(i, (i+1)%self.point_count))**(0.5)
            length = length/2
        return is_chain, is_period, length

    # Return True if polygon is trianlge
    def is_triangle(self):
        return self.point_count == 3

    # Return -2 if rectangle, -1 if square, 0 else
    def is_rectangle(self, epsilon = 0.01):
        if self.point_count == 4:
            d1 = self.distance(0,1)
            d2 = self.distance(0,2)
            d3 = self.distance(0,3)
            d1, d3, summ = min(d1,d2,d3), max(d1,d2,d3), d1+d2+d3
            d2 = summ - d1 - d3
            if abs((d1 + d2 - d3)/d3) <= epsilon:
                if abs((d1 - d2)/d2) <= epsilon:
                    return -1
                return -2
        return 0

    def is_convex(self):
        # Every triangle always is convex
        if self.point_count == 3:
            return True
        positive = False
        negative = False
        for i in range(self.point_count):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % self.point_count]
            p3 = self.vertices[(i + 2) % self.point_count]
            A = (p1[0], p1[1])
            B = (p2[0], p2[1])
            C = (p3[0], p3[1])
            BA = (A[0] - B[0], A[1] - B[1])
            BC = (C[0] - B[0], C[1] - B[1])
            cross_procuct = BA[0]*BC[1] - BA[1]*BC[0]
            if cross_procuct < 0:
                negative = True
            elif cross_procuct > 0:
                positive = True
            if positive and negative:
                return False
        return True

    # If circle - return 2, ellipse - 1, else - 0
    def is_ellipse(self, epsilon = 0.05):
        # Not convex figures we mark as Zero contour type
        if not self.is_convex():
            return 0
        # Let's find supposed poles
        north = east = south = west = 0
        first_point = self.vertices[0]
        min_x, min_y = first_point[0], first_point[1]
        max_x, max_y = min_x, min_y
        for i in range(self.point_count):
            v = self.vertices[i]
            x, y = v[0], v[1]
            if x < min_x:
                min_x = x
                east = i
            elif x > max_x:
                max_x = x
                west = i
            if y < min_y:
                min_y = y
                north = i
            elif y > max_y:
                max_y = y
                south = i
        # semi axeses
        A = (self.distance(east, west))**(0.5) / 2
        B = (self.distance(north, south))**(0.5) / 2
        # finding center
        north, south = self.vertices[north], self.vertices[south]
        east, west = self.vertices[east], self.vertices[west]
        north = (north[0], north[1])
        south = (south[0], south[1])
        east = (east[0], east[1])
        west = (west[0], west[1])
        center = (0.5*(west[0] + east[0]), 0.5*(north[1] + south[1]))
        # Let's check if every point lies on ellipse
        for v in self.vertices:
            v = (v[0] - center[0], v[1] - center[1])
            if abs((v[0]/A)**2 + (v[1]/B)**2 - 1) > epsilon:
                # We find that contour is not ellipse, so let's return 4
                # It mean, that figure just convex
                return 4
        # If semi axeses too close - we can decide that its a circle
        if abs(A - B) < 1:
            return 2
        return 1
