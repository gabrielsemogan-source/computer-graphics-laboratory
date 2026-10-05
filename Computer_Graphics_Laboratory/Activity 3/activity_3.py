import math
import random


# ==========================================================
# ACTIVITY 3
# 3D Coordinate Geometry, Distance Metrics & Bounding Volumes
# ==========================================================


# ==========================================================
# TASK 3.1 - POINT 3D
# ==========================================================

class Point3D:

    def __init__(self, x, y, z):

        self.x = x
        self.y = y
        self.z = z

    def distance_to(self, other):

        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )

    def distance_squared(self, other):

        return (
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )

    def dot(self, other):

        return (
            self.x * other.x +
            self.y * other.y +
            self.z * other.z
        )

    def cross(self, other):

        return Point3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def add(self, other):

        return Point3D(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def subtract(self, other):

        return Point3D(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __str__(self):

        return f"({self.x}, {self.y}, {self.z})"


# ==========================================================
# SPHERICAL BOUNDING VOLUME
# ==========================================================

class Sphere3D:

    def __init__(self, center, radius):

        self.center = center
        self.radius = radius

    def contains_point(self, point):

        return (
            self.center.distance_squared(point)
            <= self.radius ** 2
        )

    def intersects_sphere(self, other):

        # Optimization:
        # Compare squared distance instead of calculating sqrt.

        distance_squared = (
            self.center.distance_squared(other.center)
        )

        radius_sum = self.radius + other.radius

        return distance_squared <= radius_sum ** 2


# ==========================================================
# AXIS-ALIGNED BOUNDING BOX
# ==========================================================

class AABB:

    def __init__(self, min_point, max_point):

        self.min_point = min_point
        self.max_point = max_point

    def intersects(self, other):

        x_overlap = (
            self.min_point.x <= other.max_point.x
            and
            self.max_point.x >= other.min_point.x
        )

        y_overlap = (
            self.min_point.y <= other.max_point.y
            and
            self.max_point.y >= other.min_point.y
        )

        z_overlap = (
            self.min_point.z <= other.max_point.z
            and
            self.max_point.z >= other.min_point.z
        )

        return x_overlap and y_overlap and z_overlap


# ==========================================================
# TASK 3.2
# DISTANCE EXAMPLE
# ==========================================================

print("=" * 60)
print("ACTIVITY 3 - 3D COORDINATE GEOMETRY")
print("=" * 60)

print("\nTASK 3.2 - 3D DISTANCE")

P = Point3D(2, -1, 7)
Q = Point3D(1, -3, 5)

distance = P.distance_to(Q)

print(f"P = {P}")
print(f"Q = {Q}")

print(f"Distance = {distance:.3f}")

if math.isclose(distance, 3.0):

    print("Result verified: d = 3.0")


# ==========================================================
# VECTOR OPERATIONS
# ==========================================================

print("\nVECTOR OPERATIONS")

A = Point3D(1, 2, 3)
B = Point3D(4, 5, 6)

print(f"A = {A}")
print(f"B = {B}")

print(f"A + B = {A.add(B)}")
print(f"A - B = {A.subtract(B)}")
print(f"A dot B = {A.dot(B)}")
print(f"A cross B = {A.cross(B)}")


# ==========================================================
# TASK 3.3
# SPHERE EQUATION
# ==========================================================

print("\nTASK 3.3 - SPHERE EQUATION")

print(
    "Equation:"
)

print(
    "x² + y² + z² + 4x - 6y + 2z + 6 = 0"
)

# Completing the square:

center_x = -4 / 2
center_y = -(-6) / 2
center_z = -2 / 2

radius_squared = 8
radius = math.sqrt(radius_squared)

print(f"Center = ({center_x:.0f}, {center_y:.0f}, {center_z:.0f})")
print(f"Radius² = {radius_squared}")
print(f"Radius = {radius:.3f}")


# ==========================================================
# SPHERE TEST
# ==========================================================

print("\nSPHERE TEST")

sphere_a = Sphere3D(
    Point3D(0, 0, 0),
    5
)

sphere_b = Sphere3D(
    Point3D(7, 0, 0),
    3
)

sphere_point = Point3D(2, 1, 1)

print(
    "Point inside Sphere A:",
    sphere_a.contains_point(sphere_point)
)

print(
    "Sphere A intersects Sphere B:",
    sphere_a.intersects_sphere(sphere_b)
)


# ==========================================================
# AABB TEST
# ==========================================================

print("\nAABB TEST")

box_a = AABB(
    Point3D(-2, -2, -2),
    Point3D(2, 2, 2)
)

box_b = AABB(
    Point3D(1, 1, 1),
    Point3D(5, 5, 5)
)

print(
    "Box A intersects Box B:",
    box_a.intersects(box_b)
)


# ==========================================================
# TASK 3.4
# RANDOM 3D SPATIAL OBJECTS
# ==========================================================

print("\nTASK 3.4 - SPATIAL TESTER")

random.seed(42)

objects = []

# Create 100 random spheres
for i in range(100):

    center = Point3D(
        random.uniform(-50, 50),
        random.uniform(-50, 50),
        random.uniform(-50, 50)
    )

    radius = random.uniform(1, 5)

    sphere = Sphere3D(
        center,
        radius
    )

    objects.append(sphere)


print(f"Created {len(objects)} random 3D objects.")


# ==========================================================
# SPHERE BROAD-PHASE COLLISION DETECTION
# ==========================================================

sphere_collisions = 0

for i in range(len(objects)):

    for j in range(i + 1, len(objects)):

        if objects[i].intersects_sphere(objects[j]):

            sphere_collisions += 1


print(
    f"Sphere collision pairs detected: {sphere_collisions}"
)


# ==========================================================
# CREATE AABB FOR EACH OBJECT
# ==========================================================

boxes = []

for sphere in objects:

    r = sphere.radius
    c = sphere.center

    minimum = Point3D(
        c.x - r,
        c.y - r,
        c.z - r
    )

    maximum = Point3D(
        c.x + r,
        c.y + r,
        c.z + r
    )

    boxes.append(
        AABB(minimum, maximum)
    )


# ==========================================================
# AABB BROAD-PHASE COLLISION DETECTION
# ==========================================================

aabb_collisions = 0

for i in range(len(boxes)):

    for j in range(i + 1, len(boxes)):

        if boxes[i].intersects(boxes[j]):

            aabb_collisions += 1


print(
    f"AABB collision pairs detected: {aabb_collisions}"
)


# ==========================================================
# FINISHED
# ==========================================================

print("\n" + "=" * 60)
print("ACTIVITY 3 COMPLETE")
print("=" * 60)