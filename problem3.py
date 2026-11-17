from ast import literal_eval
import sys

from problem2 import MinHeap


def running_medians(sales):
    lower = MinHeap()  # Store negative values so its root gives the largest sale.
    upper = MinHeap()
    medians = []

    for sale in sales:
        if lower.is_empty() or sale <= -lower.peek():
            lower.insert(-sale)
        else:
            upper.insert(sale)

        if len(lower) > len(upper) + 1:
            upper.insert(-lower.extract_min())
        elif len(upper) > len(lower):
            lower.insert(-upper.extract_min())

        if len(lower) == len(upper):
            medians.append((-lower.peek() + upper.peek()) / 2)
        else:
            medians.append(float(-lower.peek()))

    return medians


def main():
    sales = literal_eval(sys.stdin.read().strip())
    print(running_medians(sales))


if __name__ == "__main__":
    main()
