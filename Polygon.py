class Polygon:

    def __init__(self, vertices):
        self.vertices = vertices
        self.point_count = len(self.vertices)

    # returns square of distance between i-th and j-th points of polygon
    def distance(self, i,j):
        p1 = self.vertices[i][0]
        p1 = (p1[0], p1[1])
        p2 = self.vertices[j][0]
        p2 = (p2[0], p2[1])
        return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

    def is_convex(self):
        # Every triangle always is convex
        if self.point_count == 3:
            return True
        positive = False
        negative = False
        for i in range(self.point_count):
            p1 = self.vertices[i][0],
            p2 = self.vertices[(i + 1) % self.point_count][0],
            p3 = self.vertices[(i + 2) % self.point_count][0],
            A = (p1[0][0], p1[0][1])
            B = (p2[0][0], p2[0][1])
            C = (p3[0][0], p3[0][1])
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
        if not self.is_convex():
            return 0
        # Let's find supposed poles
        north = east = south = west = 0
        first_point = self.vertices[0][0]
        min_x, min_y = first_point[0], first_point[1]
        max_x, max_y = min_x, min_y
        for i in range(self.point_count):
            v = self.vertices[i][0]
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
        north, south = self.vertices[north][0], self.vertices[south][0]
        east, west = self.vertices[east][0], self.vertices[west][0]
        north = (north[0], north[1])
        south = (south[0], south[1])
        east = (east[0], east[1])
        west = (west[0], west[1])
        center = (0.5*(west[0] + east[0]), 0.5*(north[1] + south[1]))
        # Let's check if every point lies on ellipse
        for v in self.vertices:
            v = (v[0][0] - center[0], v[0][1] - center[1])
            if abs((v[0]/A)**2 + (v[1]/B)**2 - 1) > epsilon:
                return 0
        # If semi axeses too close - we can decide that its a circle
        if abs(A - B) < 1:
            return 2
        return 1
