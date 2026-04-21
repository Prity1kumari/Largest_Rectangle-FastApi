from typing import List, Tuple


def largest_rectangle(matrix: List[List[int]]) -> Tuple[int, int]:
    """
    Find the largest rectangle formed by similar numbers in a matrix.

    Uses a histogram-based approach per unique number:
    For each value, build a binary height matrix and run the
    'largest rectangle in histogram' algorithm on each row.

    :param matrix: A 2D matrix of integers
    :return: (number, area) — the value and area of the largest rectangle
    """
    if not matrix or not matrix[0]:
        return (0, 0)

    rows = len(matrix)
    # Handle jagged rows
    cols = max(len(row) for row in matrix)

    # Collect all unique values
    unique_values = set()
    for row in matrix:
        unique_values.update(row)

    best_area = 0
    best_number = 0

    for value in unique_values:
        # Build height matrix for this value
        heights = [0] * cols

        for r in range(rows):
            for c in range(cols):
                cell = matrix[r][c] if c < len(matrix[r]) else None
                if cell == value:
                    heights[c] += 1
                else:
                    heights[c] = 0

            area = _max_histogram_area(heights)
            if area > best_area:
                best_area = area
                best_number = value

    return (best_number, best_area)


def _max_histogram_area(heights: List[int]) -> int:
    """
    Compute the maximum rectangular area in a histogram using a stack.
    Standard O(n) algorithm.
    """
    stack = []  # stores indices
    max_area = 0
    n = len(heights)

    for i in range(n + 1):
        h = heights[i] if i < n else 0
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    return max_area
