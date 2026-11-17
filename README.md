Running the programs

Keep the three Python files together. Put the input files you want to
test in the same folder.

    Get-Content merge_input1.txt | python problem1.py
    Get-Content heap_input1.txt | python problem2.py
    Get-Content median_input1.txt | python problem3.py

Here is the first command in Bash.

    python problem1.py < merge_input1.txt

Problem 1:
I use the min-heap from Problem 2 as the priority queue. I start by
putting the first sale from each nonempty register into the heap. An
entry holds the sale time, register number, and index in that log.
The heap compares time first and register number second, so ties go
to the lower-numbered register.

I remove the smallest entry, add its (time, register) pair to the
result, and add the next sale from that same register if there is one.
Each log is already sorted, so only its first remaining sale could be
next. The heap holds at most one sale from each register.

With k registers and N sales, this takes O(k + N log(k + 1)) time.
The queue uses O(k) extra space.


Problem 2:
Each node has links to its parent, left child, and right child. To find a
position, I skip the first 1 in its binary number. A 0 then means left
and a 1 means right. For example, position 6 is 110, so I go right,
then left.

I insert at the next open position and swap the value with its parent
while it is smaller. To remove a value, I use the last node's value to
fill the spot, detach the last node, and move the replacement up or
down as needed. The build method links all the nodes and fixes the
heap from the bottom up. The heap_sort method removes the values from
a copy of the heap, smallest first.


Problem 3:
I use two min-heaps from Problem 2. The upper heap stores the
larger sales and gives me the smallest one at its root. The lower heap
stores the smaller sales as negatives. With 3 and 8 in the lower half,
-8 is at the root. Flipping its sign gives me the largest sale in that
half.

I compare each new sale with the largest sale in the lower half to pick
a heap. After each sale, two things have to be true.

    1. Every sale in the lower half is at most every sale in the upper half.
    2. The heaps have the same size, or the lower heap has one extra sale.

If the sizes are off, I move the root of the larger heap to the smaller
one. With equal sizes, I average the two root values after flipping the
lower root's sign. Otherwise, I use the largest sale in the lower half.
Reading the roots takes O(1) time. Adding and rebalancing takes O(log n)
per sale, so processing n sales takes O(n log n) time.
