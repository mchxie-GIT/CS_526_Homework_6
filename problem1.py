from ast import literal_eval
import sys

from problem2 import MinHeap


def merge_logs(logs):
    queue = MinHeap()
    for register, log in enumerate(logs, start=1):
        if log:
            queue.insert((log[0], register, 0))

    merged = []
    while not queue.is_empty():
        time, register, index = queue.extract_min()
        merged.append((time, register))

        # Only this register can add a new entry to the queue.
        log = logs[register - 1]
        next_index = index + 1
        if next_index < len(log):
            queue.insert((log[next_index], register, next_index))

    return merged


def main():
    logs = [literal_eval(line) for line in sys.stdin]
    merged = merge_logs(logs)
    print(f"Registers: {len(logs)}")
    print(f"Total sales: {len(merged)}")
    print(f"Merged log: {merged}")


if __name__ == "__main__":
    main()
