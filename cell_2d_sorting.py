"""
2D Cell Sorting - Extended Cell Intelligence
Cells can sort 2D points (x,y) using different comparison strategies
"""

import math


class Cell2D:
    """
    A cell that holds 2D values (x, y) and can compare using different strategies.
    This demonstrates how cells can have different 'cognitive models' for decision-making.
    """

    def __init__(self, x, y=None):
        """
        Initialize with either:
        - x, y as separate args
        - (x, y) as a tuple/list
        """
        if y is None and isinstance(x, (tuple, list)):
            self.x, self.y = x
        else:
            self.x = x
            self.y = y if y is not None else 0

        self.left_neighbor = None
        self.right_neighbor = None

    def get_value(self):
        """Return the 2D value as a tuple."""
        return (self.x, self.y)

    def distance_from_origin(self):
        """Calculate Euclidean distance from origin."""
        return math.sqrt(self.x**2 + self.y**2)

    def should_swap_right(self, compare_method="distance"):
        """
        Decision function with multiple comparison strategies.

        Args:
            compare_method: One of 'distance', 'x_first', 'y_first', 'sum'

        Returns:
            True if this cell should swap with its right neighbor
        """
        if not self.right_neighbor:
            return False

        right = self.right_neighbor

        if compare_method == "distance":
            # Compare by distance from origin
            return self.distance_from_origin() > right.distance_from_origin()

        elif compare_method == "x_first":
            # Compare by x, then y
            if self.x > right.x:
                return True
            elif self.x == right.x and self.y > right.y:
                return True
            return False

        elif compare_method == "y_first":
            # Compare by y, then x
            if self.y > right.y:
                return True
            elif self.y == right.y and self.x > right.x:
                return True
            return False

        elif compare_method == "sum":
            # Compare by sum of coordinates
            return (self.x + self.y) > (right.x + right.y)

        else:
            raise ValueError(f"Unknown comparison method: {compare_method}")

    def swap_with_right(self):
        """Execute a swap with the right neighbor."""
        if not self.right_neighbor:
            return False

        right = self.right_neighbor

        # Save the neighbors beyond the swap pair
        left_of_self = self.left_neighbor
        right_of_right = right.right_neighbor

        # Update the outer neighbors to point to the swapped cells
        if left_of_self:
            left_of_self.right_neighbor = right
        if right_of_right:
            right_of_right.left_neighbor = self

        # Swap the cells' positions
        right.left_neighbor = left_of_self
        right.right_neighbor = self
        self.left_neighbor = right
        self.right_neighbor = right_of_right

        return True

    def __repr__(self):
        return f"({self.x},{self.y})"


class Tissue2D:
    """A 1D tissue array of 2D cells."""

    def __init__(self, points):
        """
        Initialize tissue with 2D points.

        Args:
            points: List of (x,y) tuples or Cell2D objects
        """
        if not points:
            self.head = None
            self.size = 0
            return

        # Create cells from points
        cells = []
        for p in points:
            if isinstance(p, Cell2D):
                cells.append(p)
            else:
                cells.append(Cell2D(p))

        # Link them together
        for i in range(len(cells)):
            if i > 0:
                cells[i].left_neighbor = cells[i - 1]
            if i < len(cells) - 1:
                cells[i].right_neighbor = cells[i + 1]

        self.head = cells[0]
        self.size = len(cells)

    def to_list(self):
        """Convert to list of (x,y) tuples."""
        result = []
        current = self.head
        while current:
            result.append(current.get_value())
            current = current.right_neighbor
        return result

    def sort_step(self, compare_method="distance"):
        """Execute one sorting pass using the specified comparison method."""
        swapped = False
        current = self.head

        while current and current.right_neighbor:
            if current.should_swap_right(compare_method):
                if current == self.head:
                    self.head = current.right_neighbor

                current.swap_with_right()
                swapped = True
                current = current.right_neighbor
            else:
                current = current.right_neighbor

        return swapped

    def sort(self, compare_method="distance", max_iterations=None, verbose=False):
        """
        Sort the tissue using the specified comparison method.

        Args:
            compare_method: 'distance', 'x_first', 'y_first', or 'sum'
            max_iterations: Maximum iterations (None for unlimited)
            verbose: Print progress if True

        Returns:
            Number of iterations
        """
        if max_iterations is None:
            max_iterations = self.size**2

        if verbose:
            print(f"\nSorting by: {compare_method}")
            print(f"Initial: {self.to_list()}")

        iterations = 0
        for i in range(max_iterations):
            if not self.sort_step(compare_method):
                iterations = i + 1
                break
            iterations = i + 1

        if verbose:
            print(f"Final:   {self.to_list()}")
            print(f"Iterations: {iterations}\n")

        return iterations


def demonstrate_2d_sorting():
    """Demonstrate 2D cell sorting with different comparison methods."""

    print("=" * 70)
    print("2D CELL SORTING - Different Cognitive Models")
    print("=" * 70)
    print("\nEach cell can use different strategies to compare with neighbors:")
    print("  1. Distance from origin")
    print("  2. X-coordinate first, then Y")
    print("  3. Y-coordinate first, then X")
    print("  4. Sum of coordinates")
    print()

    # Sample 2D points
    points = [(5, 2), (1, 4), (3, 1), (2, 5), (4, 3), (1, 1), (6, 0)]

    print(f"Original points: {points}")
    print()

    # Sort using different methods
    methods = ["distance", "x_first", "y_first", "sum"]

    for method in methods:
        print("-" * 70)
        tissue = Tissue2D(points.copy())
        tissue.sort(compare_method=method, verbose=True)

    print("=" * 70)


def visualize_2d_sorting():
    """Create a visual representation of 2D point sorting."""

    print("\n" + "=" * 70)
    print("VISUAL 2D SORTING DEMONSTRATION")
    print("=" * 70)

    points = [(8, 2), (3, 7), (5, 4), (2, 1), (9, 8), (1, 3)]

    print(f"\nOriginal points: {points}")

    # Sort by distance
    print("\n--- Sorting by Distance from Origin ---")
    tissue = Tissue2D(points.copy())

    iteration = 0
    while tissue.sort_step("distance"):
        iteration += 1
        current_points = tissue.to_list()

        # Calculate distances for display
        distances = [math.sqrt(x**2 + y**2) for x, y in current_points]

        print(f"Step {iteration}:")
        for point, dist in zip(current_points, distances):
            print(f"  {point} → distance: {dist:.2f}")
        print()

        if iteration >= 20:  # Safety limit
            break

    print(f"Final sorted by distance: {tissue.to_list()}")

    # Show distances of final result
    print("\nFinal distances:")
    for point in tissue.to_list():
        dist = math.sqrt(point[0] ** 2 + point[1] ** 2)
        print(f"  {point} → {dist:.2f}")


def compare_cell_intelligence():
    """
    Compare how different 'intelligence' (comparison methods)
    affects the sorting behavior.
    """
    print("\n" + "=" * 70)
    print("CELL INTELLIGENCE COMPARISON")
    print("=" * 70)
    print("\nThe same cells with different 'cognitive models'")
    print("produce different organizational patterns.\n")

    # Points in a grid pattern
    points = [(i, j) for i in range(3) for j in range(3)]
    import random

    random.shuffle(points)

    print(f"Random initial arrangement:")
    print(f"{points}\n")

    results = {}

    for method in ["distance", "x_first", "y_first", "sum"]:
        tissue = Tissue2D(points.copy())
        iterations = tissue.sort(compare_method=method)
        results[method] = {"sorted": tissue.to_list(), "iterations": iterations}

    # Display results
    print("-" * 70)
    for method, data in results.items():
        print(f"\n{method.upper()}:")
        print(f"  Result: {data['sorted']}")
        print(f"  Iterations: {data['iterations']}")

    print("\n" + "=" * 70)
    print("INSIGHT: Same cells, same data, different 'intelligence' →")
    print("         Different emergent organizational structures!")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_2d_sorting()
    visualize_2d_sorting()
    compare_cell_intelligence()
