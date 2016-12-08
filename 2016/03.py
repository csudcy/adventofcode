INPUT = open('03.txt').read()

def convert_triangle(input):
    return map(int, input.split())

def convert_triangles(input):
    return [
        triangle
        for triangle in map(convert_triangle, input.split('\n'))
    ]

def is_valid_triangle(triangle):
    a, b, c = triangle
    return all([
        (a + b > c),
        (a + c > b),
        (b + c > a),
    ])

def filter_valid_triangles(triangles):
    return filter(is_valid_triangle, triangles)

def count_valid_triangles(input):
    return len(
        filter_valid_triangles(
            convert_triangles(input)
        )
    )

assert count_valid_triangles('3 4 5') == 1
assert count_valid_triangles('5 10 25') == 0
assert count_valid_triangles('3 4 5\n5 10 25') == 1
print count_valid_triangles(INPUT)



def transpose_triangles(triangles):
    for row in xrange(0, len(triangles), 3):
        # Transpose the 3 rows starting at row e.g.
        #   (row+0, 0) (row+0, 1) (row+0, 2)
        #   (row+1, 0) (row+1, 1) (row+1, 2)
        #   (row+2, 0) (row+2, 1) (row+2, 2)
        #
        # Becomes:
        #   (row+0, 0) (row+1, 0) (row+2, 0)
        #   (row+0, 1) (row+1, 1) (row+2, 1)
        #   (row+0, 2) (row+1, 2) (row+2, 2)
        #
        # I.E. swap:
        #   (row+0, 1) <-> (row+1, 0)
        #   (row+0, 2) <-> (row+2, 0)
        #   (row+1, 2) <-> (row+2, 1)
        triangles[row+0][1], triangles[row+1][0] = triangles[row+1][0], triangles[row+0][1]
        triangles[row+0][2], triangles[row+2][0] = triangles[row+2][0], triangles[row+0][2]
        triangles[row+1][2], triangles[row+2][1] = triangles[row+2][1], triangles[row+1][2]
    return triangles

def count_valid_transposed_triangles(input):
    return len(
        filter_valid_triangles(
            transpose_triangles(
                convert_triangles(input)
            )
        )
    )

TRANSPOSE_TEST = """3 6 12
4 8 16
5 10 20"""

assert count_valid_triangles(TRANSPOSE_TEST) == 0
assert count_valid_transposed_triangles(TRANSPOSE_TEST) == 3
print count_valid_transposed_triangles(INPUT)
