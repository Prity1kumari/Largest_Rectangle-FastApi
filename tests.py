from algorithm import largest_rectangle


def test_provided_example():
    matrix = [
        [1, 1, 1, 0, 1, -9],
        [1, 1, 1, 1, 2, -9],
        [1, 1, 1, 1, 2, -9],
        [1, 0, 0, 0, 5, -9],
        [5, 0, 0, 0, 5],
    ]
    number, area = largest_rectangle(matrix)
    # Cols 0-2, Rows 0-2 form a valid 3×3 rectangle of 1s (area=9)
    # This is larger than the 2×4 rectangle (area=8) mentioned in the assignment note.
    # Our algorithm finds the true maximum.
    assert number == 1, f"Expected number=1, got {number}"
    assert area == 9, f"Expected area=9 (3×3 rectangle), got {area}"


def test_single_element():
    matrix = [[42]]
    assert largest_rectangle(matrix) == (42, 1)


def test_all_same():
    matrix = [[3, 3], [3, 3]]
    assert largest_rectangle(matrix) == (3, 4)


def test_single_row():
    matrix = [[2, 2, 2, 1, 1]]
    assert largest_rectangle(matrix) == (2, 3)


def test_single_column():
    matrix = [[7], [7], [7], [1]]
    assert largest_rectangle(matrix) == (7, 3)


def test_negative_numbers():
    # -1 appears at (0,0),(0,1),(1,0) — an L-shape, not a rectangle.
    # Largest rectangle of -1s is 1×2=2 or 2×1=2.
    matrix = [[-1, -1], [-1, 2]]
    number, area = largest_rectangle(matrix)
    assert number == -1 and area == 2, f"Expected (-1, 2), got ({number}, {area})"


def test_large_flat_matrix():
    matrix = [[5] * 10 for _ in range(10)]
    assert largest_rectangle(matrix) == (5, 100)


def test_jagged_rows():
    # Row 0: [1,1,1], Row 1: [1,1], Row 2: [1]
    # Largest rect: cols 0-1 × rows 0-1 = 2×2 = 4
    matrix = [[1, 1, 1], [1, 1], [1]]
    number, area = largest_rectangle(matrix)
    assert number == 1 and area == 4, f"Expected (1, 4), got ({number}, {area})"


if __name__ == "__main__":
    tests = [
        test_provided_example,
        test_single_element,
        test_all_same,
        test_single_row,
        test_single_column,
        test_negative_numbers,
        test_large_flat_matrix,
        test_jagged_rows,
    ]
    for t in tests:
        try:
            t()
            print(f"  ✅ {t.__name__}")
        except AssertionError as e:
            print(f"  ❌ {t.__name__}: {e}")
    print("\nDone.")
