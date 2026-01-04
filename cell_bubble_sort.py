"""
Decentralized Bubble Sort Implementation
Based on Michael Levin's research on basal intelligence in algorithms.

Each "cell" in the array has its own agency to decide whether to swap
with its neighbor, implementing a distributed sorting algorithm.
"""


class Cell:
    """
    A cell in a 1D tissue array that can autonomously decide to swap
    with its right neighbor based on local comparison rules.
    """

    def __init__(self, value):
        self.value = value
        self.left_neighbor: Cell | None = None
        self.right_neighbor: Cell | None = None

    def should_swap_right(self):
        """
        Decision function: Should this cell swap with its right neighbor?
        This is the cell's 'intelligence' - it can make local decisions.
        """
        if not self.right_neighbor:
            return False
        return self.value > self.right_neighbor.value

    def swap_with_right(self):
        """
        Execute a swap with the right neighbor by updating the linked list pointers.
        This is the cell's 'action' - it can modify its own connections.
        """
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


class CellTissue:
    """
    A 1D tissue array that manages a collection of cells.
    The tissue provides the infrastructure, but cells make their own decisions.
    """

    def __init__(self, values):
        """Initialize the tissue with a list of values."""
        if not values:
            self.head = None
            self.size = 0
            return

        # Create cells
        cells = [Cell(val) for val in values]

        # Link them together
        for i in range(len(cells)):
            if i > 0:
                cells[i].left_neighbor = cells[i - 1]
            if i < len(cells) - 1:
                cells[i].right_neighbor = cells[i + 1]

        self.head = cells[0]
        self.size = len(cells)

    def get_cell_at(self, index):
        """Get the cell at a specific index (for visualization/debugging)."""
        current = self.head
        for _ in range(index):
            if not current:
                return None
            current = current.right_neighbor
        return current

    def to_list(self):
        """Convert the linked list to a Python list for easy viewing."""
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.right_neighbor
        return result

    def sort_step(self):
        """
        Execute one pass of the bubble sort.
        Each cell checks if it should swap with its right neighbor.
        Returns True if any swaps occurred.
        """
        swapped = False
        current = self.head

        while current and current.right_neighbor:
            if current.should_swap_right():
                # If this cell swaps, we need to update head if necessary
                if current == self.head:
                    self.head = current.right_neighbor

                current.swap_with_right()
                swapped = True
                # After swap, current is now to the right of where it was,
                # so we move to the next cell (which is now current.right_neighbor)
                current = current.right_neighbor
            else:
                # No swap, just move to next cell
                current = current.right_neighbor

        return swapped

    def sort(self, max_iterations=None, verbose=False):
        """
        Sort the tissue by repeatedly letting cells make local decisions.

        Args:
            max_iterations: Maximum number of passes (None for unlimited)
            verbose: Print each step if True

        Returns:
            Number of iterations taken
        """
        if max_iterations is None:
            max_iterations = self.size**2  # Upper bound for bubble sort

        iterations = 0

        for i in range(max_iterations):
            if verbose:
                print(f"Step {i}: {self.to_list()}")

            if not self.sort_step():
                # No swaps occurred, we're done
                iterations = i + 1
                if verbose:
                    print(f"Final: {self.to_list()}")
                    print(f"Sorted in {iterations} iterations")
                break
            iterations = i + 1
        else:
            if verbose:
                print(f"Reached max iterations ({max_iterations})")

        return iterations


def demonstrate_cell_sorting():
    """Demonstrate the decentralized bubble sort."""

    print("=" * 60)
    print("DECENTRALIZED BUBBLE SORT")
    print("Each cell autonomously decides whether to swap")
    print("=" * 60)
    print()

    # Example 1: Small array
    print("Example 1: Small array")
    print("-" * 40)
    values = [64, 34, 25, 12, 22, 11, 90]
    print(f"Initial: {values}")

    tissue = CellTissue(values)
    iterations = tissue.sort(verbose=True)
    print()

    # Example 2: Reverse sorted
    print("\nExample 2: Reverse sorted array")
    print("-" * 40)
    values = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    print(f"Initial: {values}")

    tissue = CellTissue(values)
    iterations = tissue.sort(verbose=True)
    print()

    # Example 3: Already sorted
    print("\nExample 3: Already sorted")
    print("-" * 40)
    values = [1, 2, 3, 4, 5]
    print(f"Initial: {values}")

    tissue = CellTissue(values)
    iterations = tissue.sort(verbose=True)
    print()

    # Example 4: Random values
    print("\nExample 4: Random values")
    print("-" * 40)
    import random

    values = [random.randint(1, 100) for _ in range(15)]
    print(f"Initial: {values}")

    tissue = CellTissue(values)
    iterations = tissue.sort()
    print(f"Final: {tissue.to_list()}")
    print(f"Sorted in {iterations} iterations")
    print()


if __name__ == "__main__":
    demonstrate_cell_sorting()
