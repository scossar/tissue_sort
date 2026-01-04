"""
Visualization of Decentralized Cell Sorting
Shows how cells autonomously swap with neighbors
"""

from cell_bubble_sort import Cell, CellTissue


def visualize_tissue(tissue, highlight_indices=None):
    """
    Create a visual representation of the tissue showing cell values
    and their connections.

    Args:
        tissue: CellTissue object
        highlight_indices: List of indices to highlight (cells that just swapped)
    """
    values = tissue.to_list()

    # Create a visual representation
    lines = []

    # Top border
    lines.append("┌" + "─" * (len(values) * 6 - 1) + "┐")

    # Values with highlighting
    value_line = "│"
    for i, val in enumerate(values):
        if highlight_indices and i in highlight_indices:
            value_line += f" [{val:2d}] "
        else:
            value_line += f"  {val:2d}  "
    value_line += "│"
    lines.append(value_line)

    # Bottom border
    lines.append("└" + "─" * (len(values) * 6 - 1) + "┘")

    return "\n".join(lines)


def visualize_swap(tissue, cell_index):
    """
    Visualize a single swap operation.

    Args:
        tissue: CellTissue object
        cell_index: Index of the cell that will swap right
    """
    print(f"\n  Cell at index {cell_index} comparing with neighbor...")

    cell = tissue.get_cell_at(cell_index)
    if cell and cell.right_neighbor:
        print(f"  {cell.value} > {cell.right_neighbor.value}? ", end="")
        if cell.should_swap_right():
            print("YES → SWAP!")
            return True
        else:
            print("NO → Stay")
            return False
    return False


def animated_sort(values, delay=0.5):
    """
    Sort with step-by-step animation showing cell decisions.

    Args:
        values: List of values to sort
        delay: Delay between steps (seconds)
    """
    import time

    print("\n" + "=" * 60)
    print("ANIMATED CELL SORTING")
    print("=" * 60)
    print("\nInitial tissue:")

    tissue = CellTissue(values)
    print(visualize_tissue(tissue))
    print(f"\nValues: {tissue.to_list()}")

    time.sleep(delay * 2)

    iteration = 0
    max_iterations = len(values) ** 2

    for iteration in range(max_iterations):
        print(f"\n{'=' * 60}")
        print(f"ITERATION {iteration + 1}")
        print("=" * 60)

        swapped = False
        current = tissue.head
        index = 0

        # Track which cells swap in this iteration
        swap_indices = []

        while current and current.right_neighbor:
            if current.should_swap_right():
                print(f"\nCell {index} deciding:")
                print(
                    f"  Value: {current.value} vs Right neighbor: {current.right_neighbor.value}"
                )
                print(
                    f"  Decision: SWAP! ({current.value} > {current.right_neighbor.value})"
                )

                # Update head if necessary
                if current == tissue.head:
                    tissue.head = current.right_neighbor

                # Remember these indices for highlighting
                swap_indices.extend([index, index + 1])

                current.swap_with_right()
                swapped = True
                time.sleep(delay)

                # Show tissue after swap
                print("\n  After swap:")
                print(visualize_tissue(tissue, swap_indices))

                # Move to next cell
                current = current.right_neighbor
                index += 1
            else:
                current = current.right_neighbor
                index += 1

        print(f"\nState after iteration {iteration + 1}:")
        print(visualize_tissue(tissue))
        print(f"Values: {tissue.to_list()}")

        if not swapped:
            print("\n✓ No swaps occurred - SORTED!")
            break

        time.sleep(delay)

    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    print(visualize_tissue(tissue))
    print(f"Values: {tissue.to_list()}")
    print(f"\nCompleted in {iteration + 1} iterations")


def compare_approaches(values):
    """
    Compare the decentralized cell approach with traditional bubble sort.
    """
    print("\n" + "=" * 60)
    print("COMPARISON: Decentralized Cells vs Traditional Algorithm")
    print("=" * 60)

    print(f"\nInitial array: {values}")

    # Traditional bubble sort
    print("\n--- Traditional Bubble Sort ---")
    print("(Centralized control, algorithm manages all swaps)")

    arr = values.copy()
    iterations_trad = 0
    swaps_trad = 0

    for i in range(len(arr)):
        swapped = False
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                swaps_trad += 1
        iterations_trad += 1
        if not swapped:
            break

    print(f"Result: {arr}")
    print(f"Iterations: {iterations_trad}")
    print(f"Swaps: {swaps_trad}")

    # Cell-based sort
    print("\n--- Decentralized Cell Sort ---")
    print("(Distributed intelligence, each cell decides independently)")

    tissue = CellTissue(values.copy())
    iterations_cell = tissue.sort()

    print(f"Result: {tissue.to_list()}")
    print(f"Iterations: {iterations_cell}")

    print("\n" + "=" * 60)
    print("Analysis:")
    print(f"  Both approaches perform the same number of comparisons")
    print(f"  But the cell-based approach demonstrates 'basal intelligence'")
    print(f"  Each cell is an autonomous agent making local decisions")
    print("=" * 60)


if __name__ == "__main__":
    # Example 1: Small animated sort
    print("\n" + "🧬 " * 20)
    print("EXAMPLE 1: Small Array (Animated)")
    print("🧬 " * 20)
    animated_sort([5, 2, 8, 1, 9], delay=0.3)

    # Example 2: Comparison
    print("\n\n" + "🧬 " * 20)
    print("EXAMPLE 2: Comparing Approaches")
    print("🧬 " * 20)
    compare_approaches([64, 34, 25, 12, 22, 11, 90])

    # Example 3: Larger animated sort (no delays)
    print("\n\n" + "🧬 " * 20)
    print("EXAMPLE 3: Reverse Sorted (Quick)")
    print("🧬 " * 20)
    animated_sort([7, 6, 5, 4, 3, 2, 1], delay=0.0)
