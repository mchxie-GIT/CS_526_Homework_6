from ast import literal_eval
import sys


class Node:
    def __init__(self, value, parent=None):
        self.value = value
        self.left = None
        self.right = None
        self.parent = parent


class MinHeap:
    def __init__(self):
        self.root = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def _node_at(self, position):
        node = self.root
        # Skip the 0b prefix and the leading 1, which represents the root.
        for direction in bin(position)[3:]:
            if direction == "0":
                node = node.left
            else:
                node = node.right
        return node

    def _sift_up(self, node):
        while node.parent is not None and node.value < node.parent.value:
            parent = node.parent
            node.value, parent.value = parent.value, node.value
            node = parent

    def _sift_down(self, node):
        while node.left is not None:
            smaller = node.left
            if node.right is not None and node.right.value < smaller.value:
                smaller = node.right
            if not smaller.value < node.value:
                break
            node.value, smaller.value = smaller.value, node.value
            node = smaller

    def insert(self, value):
        position = self._size + 1
        if position == 1:
            self.root = Node(value)
        else:
            parent = self._node_at(position // 2)
            node = Node(value, parent)
            if position % 2 == 0:
                parent.left = node
            else:
                parent.right = node
            self._sift_up(node)
        self._size += 1

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from an empty heap")
        return self.root.value

    def extract_min(self):
        value = self.peek()
        self._remove_node(self.root)
        return value

    def _remove_node(self, node):
        last = self._node_at(self._size)
        if last.parent is None:
            self.root = None
        elif last.parent.left is last:
            last.parent.left = None
        else:
            last.parent.right = None
        self._size -= 1

        if node is not last:
            node.value = last.value
            if node.parent is not None and node.value < node.parent.value:
                self._sift_up(node)
            else:
                self._sift_down(node)

    def _find(self, node, value):
        if node is None or node.value == value:
            return node
        found = self._find(node.left, value)
        if found is not None:
            return found
        return self._find(node.right, value)

    def delete(self, value):
        node = self._find(self.root, value)
        if node is None:
            return False
        self._remove_node(node)
        return True

    def build(self, values):
        # Finish both subtrees before sifting their parent down.
        def build_subtree(position, parent):
            if position > len(values):
                return None
            node = Node(values[position - 1], parent)
            node.left = build_subtree(2 * position, node)
            node.right = build_subtree(2 * position + 1, node)
            self._sift_down(node)
            return node

        self.root = build_subtree(1, None)
        self._size = len(values)

    def heap_sort(self):
        def copy_subtree(node, parent):
            if node is None:
                return None
            new_node = Node(node.value, parent)
            new_node.left = copy_subtree(node.left, new_node)
            new_node.right = copy_subtree(node.right, new_node)
            return new_node

        heap_copy = MinHeap()
        heap_copy.root = copy_subtree(self.root, None)
        heap_copy._size = self._size
        values = []
        while not heap_copy.is_empty():
            values.append(heap_copy.extract_min())
        return values

    def print_heap(self):
        if self.is_empty():
            return

        # Assign columns in inorder and use every other row for the branches.
        rows = ["" for _ in range(2 * self._size.bit_length() - 1)]
        column = 0

        def draw(node, row):
            nonlocal column
            if node.left is not None:
                left_center = draw(node.left, row + 2)
                rows[row + 1] = rows[row + 1].ljust(left_center + 1) + "/"

            label = str(node.value)
            center = column + len(label) // 2
            rows[row] = rows[row].ljust(column) + label
            column += len(label) + 3

            if node.right is not None:
                right_center = draw(node.right, row + 2)
                rows[row + 1] = rows[row + 1].ljust(right_center - 1) + "\\"
            return center

        draw(self.root, 0)
        for row in rows:
            print(row)


def main():
    values = literal_eval(sys.stdin.read().strip())
    heap = MinHeap()
    print(f"Input values: {values}")
    for value in values:
        heap.insert(value)
        print(f"\nAfter insert({value}):")
        heap.print_heap()


if __name__ == "__main__":
    main()
