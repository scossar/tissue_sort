from typing import Sequence, Union
import random

random.seed(3)


class CellWithStubborn:
    def __init__(self, value: float, stubborn: bool = False):
        self.value: float = value
        self.stubborn = stubborn
        self.prev: CellWithStubborn | None = None
        self.next: CellWithStubborn | None = None

    def should_swap_next(self) -> bool:
        if not self.next:
            return False
        if self.stubborn:
            return False  # guessing here
        return self.value > self.next.value

    def swap_with_next(self) -> bool:
        if not self.next:
            return False

        # Cell to be swapped with
        next_to_self = self.next

        # outer neighbors: Cells whose prev or next is affected by the swap
        next_to_next = next_to_self.next
        prev_to_self = self.prev

        # update prev/next of outer neighbors
        if prev_to_self:
            prev_to_self.next = next_to_self
        if next_to_next:
            next_to_next.prev = self

        # update next
        next_to_self.prev = prev_to_self
        next_to_self.next = self

        # update self
        self.prev = next_to_self
        self.next = next_to_next

        return True


class CellTissue:
    def __init__(self, values: Sequence[Union[int, float]]):
        cells: list[CellWithStubborn] = [CellWithStubborn(val) for val in values]

        for i in range(len(cells)):
            if i > 0:
                cells[i].prev = cells[i - 1]
            if i < len(cells) - 1:
                cells[i].next = cells[i + 1]

        self.head = cells[0]
        self.size = len(cells)

    def get_cell_at(self, index: int) -> CellWithStubborn | None:
        """Return the cell at a given distance from the linked-list's head."""

        current = self.head
        for _ in range(index):
            if not current:
                return None
            current = current.next

        return current

    def to_list(self) -> Sequence[Union[int, float]]:
        """Convert the linked-list to a list of values."""

        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next

        return result

    def sort_step(self) -> bool:
        """Execute one pass of bubble sort."""
        swapped = False
        current = self.head

        while current and current.next:
            if current.should_swap_next():
                if current == self.head:
                    self.head = current.next
                current.swap_with_next()
                swapped = True
                # don't update current here, current.next has been updated to
                # point to the next node in swap_with_next()
            else:
                current = current.next  # didn't swap, so update current.next

        return swapped

    def sort(self, max_iterations: int | None = None, verbose: bool = False) -> int:
        if not max_iterations:
            max_iterations = self.size**2  # upper bounds for bubble sort
        iterations = 0

        for i in range(max_iterations):
            if not self.sort_step():
                iterations = i  # + 1
                if verbose:
                    print(f"Final: {self.to_list()}")
                    print(f"Sorted in {iterations} iterations")
                    break

            if verbose:
                print(f"Step {i}: {self.to_list()}")

            iterations = i + 1
        else:  # Python for/else (executed if for loop never hits the break statement)
            if verbose:
                print(f"Reached max iterations ({max_iterations})")
        return iterations


def demo():
    values = [3, 1, 12, 9, 8, 100, 6, 111, 2, 10, 7, -4, -100, 5, 4, -1000, 17]
    # values = [1, 3, 8, 9, 12, 100, -4, -1000, -100, 2, 4, 5, 6, 7, 10, 17, 111]
    print(f"len(values): {len(values)}")
    # values = [random.randint(1, 100) for _ in range(13)]
    print(f"Initial values: {values}")
    tissue = CellTissue(values)
    cell1 = tissue.get_cell_at(5)
    cell2 = tissue.get_cell_at(11)
    if cell1 and cell2:
        print(f"stubborn cell.values: {cell1.value}, {cell2.value}")
        cell1.stubborn = True
        cell2.stubborn = True
    tissue.sort(verbose=True)


if __name__ == "__main__":
    demo()
