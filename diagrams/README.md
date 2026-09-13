# Diagrams

Eight original diagrams, generated as SVG by `../make_diagrams.py`. PNG copies at 2x are in
`png/` for use in slides, the video, and the LinkedIn post.

| # | File | Covers |
|---|---|---|
| 1 | `1-stack-push-pop.svg` | One push and one pop on a capacity-5 array stack, with the `top` index tracked |
| 2 | `2-queue-enqueue-dequeue.svg` | FIFO operation, and the false-overflow state of a linear array queue |
| 3 | `3-circular-queue-wraparound.svg` | The same five slots as a ring, showing `end` moving from index 4 to index 0 |
| 4 | `4-binary-tree-terminology.svg` | Root, parent, child, left/right child, leaf, subtree, left/right subtree |
| 5 | `5-completed-bst.svg` | The finished BST, with root, leaves, both subtrees and the rejected duplicates |
| 6 | `6-inorder-traversal.svg` | Visit order 1–10 for LEFT → ROOT → RIGHT |
| 7 | `7-preorder-traversal.svg` | Visit order 1–10 for ROOT → LEFT → RIGHT |
| 8 | `8-postorder-traversal.svg` | Visit order 1–10 for LEFT → RIGHT → ROOT |

All values shown match the program output in `../documentation/sample-output.txt`, so the
diagrams and the code cannot drift apart. Change the dataset in `BinarySearchTree.cpp` and the
`BST` dictionary in `make_diagrams.py` needs the same change.

Regenerate with:

```bash
pip install cairosvg     # only needed for the PNG export
python3 make_diagrams.py
```
