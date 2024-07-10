from math import sqrt

from computed_property import computed_property


class Vector:
    def __init__(self, x, y, z, color=None):
        self.x, self.y, self.z = x, y, z
        self.color = color

    @computed_property("x", "y", "z")
    def magnitude(self):
        print("computing magnitude")
        return sqrt(self.x**2 + self.y**2 + self.z**2)


v = Vector(9, 2, 6)
print(v.magnitude)

v.color = "red"
print(v.magnitude)

v.y = 18
print(v.magnitude)


class Circle:
    def __init__(self, radius=1):
        self.radius = radius

    @computed_property("radius", "area")
    def diameter(self):
        print("computing diameter")
        return self.radius * 2


circle = Circle()
print(circle.diameter)

circle.area = 6
print(circle.diameter)

print(circle.diameter)


class Circle:
    def __init__(self, radius=1):
        self.radius = radius

    @computed_property("radius")
    def diameter(self):
        print("computing diameter")
        return self.radius * 2

    @diameter.setter
    def diameter(self, diameter):
        self.radius = diameter / 2

    @diameter.deleter
    def diameter(self):
        self.radius = 0


circle = Circle()
print(circle.diameter)

circle.diameter = 3
print(circle.radius)

del circle.diameter
print(circle.radius)


class Circle:
    def __init__(self, radius=1):
        self.radius = radius

    @computed_property("radius")
    def diameter(self):
        """Circle diameter from radius"""
        print("computing diameter")
        return self.radius * 2


print(help(Circle))
