# A basic (but broken for now) multithread implementation
import threading
import time
import random


class ThreadedCell(threading.Thread):
    def __init__(self, value, index, cells, lock, stubborn=False):
        threading.Thread.__init__(self)
        self.value = value
        self.index = index
        self.cells = cells  # shared array of all cells
        self.lock = lock  # shared lock
        self.stubborn = stubborn
        self.active = True
        self.daemon = True  # thread dies when main program exits

    def should_swap_with(self, neighbor_index):
        """Check if we should swap with neighbor."""
        if self.stubborn:
            return False
        if neighbor_index < 0 or neighbor_index >= len(self.cells):
            return False
        neighbor = self.cells[neighbor_index]
        return self.value > neighbor.value

    def run(self):
        """Main loop - runs continuously in its own thread."""
        while self.active:
            self.lock.acquire()  # Get exclusive access
            try:
                # Randomly check left or right
                direction = random.choice([-1, 1])
                neighbor_index = self.index + direction

                if self.should_swap_with(neighbor_index):
                    # Swap positions in the array
                    neighbor = self.cells[neighbor_index]
                    self.cells[self.index], self.cells[neighbor_index] = neighbor, self
                    self.index, neighbor.index = neighbor.index, self.index

            finally:
                self.lock.release()  # Always release lock

            time.sleep(0.01)  # Brief pause to let other threads run

    def stop(self):
        self.active = False


class ParallelCellTissue:
    def __init__(self, values):
        self.lock = threading.Lock()
        self.cells = [
            ThreadedCell(val, i, None, self.lock) for i, val in enumerate(values)
        ]
        # Update cells array reference for all cells
        for cell in self.cells:
            cell.cells = self.cells

    def start_sorting(self):
        """Start all cell threads."""
        for cell in self.cells:
            cell.start()

    def stop_sorting(self):
        """Stop all cell threads."""
        for cell in self.cells:
            cell.stop()
        for cell in self.cells:
            cell.join()  # Wait for threads to finish

    def get_values(self):
        """Get current state."""
        self.lock.acquire()
        try:
            return [cell.value for cell in self.cells]
        finally:
            self.lock.release()

    def is_sorted(self):
        """Check if sorted."""
        values = self.get_values()
        return all(values[i] <= values[i + 1] for i in range(len(values) - 1))


# Usage
def demo_parallel():
    values = [3, 1, 12, 9, 8, 100, 6, 111, 2, 10, 7, -4, -100]
    tissue = ParallelCellTissue(values)

    # Make index 5 stubborn
    tissue.cells[5].stubborn = True

    print(f"Initial: {tissue.get_values()}")

    tissue.start_sorting()

    # Monitor progress
    for i in range(20):
        time.sleep(0.5)
        current = tissue.get_values()
        print(f"Step {i}: {current}")
        if tissue.is_sorted():
            print("Sorted!")
            break

    tissue.stop_sorting()
    print(f"Final: {tissue.get_values()}")


if __name__ == "__main__":
    demo_parallel()
