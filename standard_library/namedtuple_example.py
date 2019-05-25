from collections import namedtuple

Point = namedtuple('Point', ['x', 'y', 'z'])

p = Point(10, 20, 30)
print(p)
print(f'p.y = {p.y}')
print(f'p[1] = {p[1]}')
print(f'p.y is p[1] {p.y is p[1]}')
