# DS2-BLA-Stacks-Queues-Trees

**Name:** Pranav
**Course:** CSC-6021 — Data Structures and Algorithms II
**Instructor:** Dr. Victor Govindaswamy
**Assignment:** BLA — Stacks, Queues, Circular Queues, Binary Trees and Binary Search Trees

**YouTube video:** _(paste link)_
**LinkedIn post:** _(paste link)_

---

## About this project

Three data structures implemented from scratch in C++ — no STL containers — each with a demonstration program that prints its internal state as it runs, so the behaviour is visible rather than just asserted.

1. **Array-based stack** built on a static array, showing LIFO ordering plus deliberate overflow and underflow.
2. **Array-based circular queue** showing FIFO ordering and the modulo wrap-around that lets freed slots be reused.
3. **Pointer-based binary search tree** built from a 12-value dataset containing duplicates, showing duplicate rejection and all three traversals.

The written research, diagrams and explanations are in [`documentation/BLA-Writeup.md`](documentation/BLA-Writeup.md).

## Repository structure

```
DS2-BLA-Stacks-Queues-Trees/
|
+-- README.md
+-- Stack/
|   +-- Stack.cpp
+-- Queue/
|   +-- CircularQueue.cpp
+-- Tree/
|   +-- BinarySearchTree.cpp
+-- diagrams/
+-- documentation/
    +-- BLA-Writeup.md
    +-- sample-output.txt
```

## Compilation

Each program is standalone with its own `main()`. Requires a C++11 compiler (g++, clang, or MSVC).

```bash
g++ -std=c++11 -Wall -o stack_demo Stack/Stack.cpp
g++ -std=c++11 -Wall -o queue_demo Queue/CircularQueue.cpp
g++ -std=c++11 -Wall -o bst_demo   Tree/BinarySearchTree.cpp
```

All three compile clean with `-Wall`.

The binaries are named `*_demo` rather than `stack` and `queue` because macOS and Windows
use case-insensitive filesystems, where an output file called `stack` collides with the
`Stack/` source directory and the link step fails.

## Execution

```bash
./stack_demo    # Windows: stack_demo.exe
./queue_demo
./bst_demo
```

No input is required; each program runs a scripted demonstration. Full expected output is saved in `documentation/sample-output.txt`.

---

## Stack

A stack restricts access to one end. Items are added and removed at the top only, which makes it **LIFO — Last In, First Out**.

The implementation is a static array plus a single integer `top` holding the index of the most recent element, with `top == -1` meaning empty. `push` increments `top` then writes; `pop` reads then decrements. Nothing shifts, so every operation is O(1).

Two error conditions are guarded explicitly:

- **Overflow** — `push` when `top == SIZE - 1`. Unchecked, this writes past the end of the array (undefined behaviour).
- **Underflow** — `pop` or `peek` on an empty stack, which would read `arr[-1]`.

Capacity is set to 5 so both conditions can be triggered inside a short demonstration.

## Queue and Circular Queue

A queue adds at the rear and removes from the front — **FIFO — First In, First Out**.

A plain linear array queue suffers from **false overflow**: once `end` reaches the last index it refuses new items even though dequeues have freed slots at the front. The fix is modulo arithmetic, treating the array as a ring:

```cpp
end   = (end + 1) % SIZE;
start = (start + 1) % SIZE;
```

Freed slots are reused, nothing shifts, and both operations stay O(1).

The class keeps `start`, `end` and a `count`. The count is needed because `start == end` is ambiguous with only two indices — it is true both when the queue is empty and when it is full.

The demonstration deliberately fills all 5 slots so `end` lands on the final index, dequeues twice, then enqueues again to force the wrap from index 4 back to index 0.

## Binary Search Tree

A binary tree allows at most two children per node. A **binary search tree** adds the ordering rule that smaller values go left and larger values go right, at every node. That is what makes lookup O(log n) in a balanced tree — each comparison discards one entire side.

Each node holds an `int data`, a `Node* left` and a `Node* right`, with `nullptr` marking a missing subtree. Two `nullptr` children is the definition of a leaf, and it is also the base case for every recursive method in the class.

**Dataset used:** `55, 27, 82, 19, 41, 70, 96, 27, 63, 88, 82, 12`

The second `27` and the second `82` are detected during insertion — when the new value compares equal to the current node, the function returns without allocating — and are discarded, leaving 10 nodes.

**Traversals produced:**

| Traversal | Order | Output |
|---|---|---|
| Inorder | L → Root → R | 12 19 27 41 55 63 70 82 88 96 |
| Preorder | Root → L → R | 55 27 19 12 41 82 70 63 96 88 |
| Postorder | L → R → Root | 12 19 41 27 63 70 88 96 82 55 |

Inorder comes out sorted because each node is visited after everything smaller beneath it and before everything larger beneath it — a direct consequence of the insertion rule.

## Diagrams

See the `diagrams/` folder:

- Stack push/pop
- Queue enqueue/dequeue
- Circular queue wrap-around
- Binary tree terminology
- Completed BST
- Inorder, preorder and postorder traversal illustrations
