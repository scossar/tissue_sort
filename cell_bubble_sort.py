from typing import Sequence, Union
import random

random.seed(1)


class Cell:
    def __init__(self, value: float):
        self.value: float = value
        self.prev: Cell | None = None
        self.next: Cell | None = None

    def should_swap_next(self):
        if not self.next:
            return False
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
        cells: list[Cell] = [Cell(val) for val in values]

        for i in range(len(cells)):
            if i > 0:
                cells[i].prev = cells[i - 1]
            if i < len(cells) - 1:
                cells[i].next = cells[i + 1]

        self.head = cells[0]
        self.size = len(cells)

    def get_cell_at(self, index: int) -> Cell | None:
        current = self.head
        for _ in range(index):
            if not current:
                return None
            current = current.next

        return current

    def to_list(self) -> Sequence[Union[int, float]]:
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
                current = current.next
            else:
                current = current.next

        return swapped

    def sort(self, max_iterations: int | None = None, verbose: bool = False) -> int:
        if not max_iterations:
            max_iterations = self.size**2  # upper bounds for bubble sort
        iterations = 0

        for i in range(max_iterations):
            if not self.sort_step():
                iterations = i + 1
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
    values = [4, 2, 124, 3]
    tissue = CellTissue(values)
    tissue.sort(verbose=True)


values = [random.randint(1, 100) for _ in range(12)]
tissue = CellTissue(values)
for i in range(10):
    tissue.sort(verbose=True, max_iterations=1)
    fourth_cell = tissue.get_cell_at(3)
    if fourth_cell:
        print(f"First cell value: {fourth_cell.value}")

# if __name__ == "__main__":
#     demo()
