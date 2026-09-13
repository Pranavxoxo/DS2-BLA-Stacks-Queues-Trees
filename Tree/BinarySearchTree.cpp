// ============================================================
// BinarySearchTree.cpp - Class/pointer-based BST
// CSC-6021 Data Structures and Algorithms II
// ============================================================
//
// A binary tree is any tree where each node has at most two
// children. A BINARY SEARCH TREE adds an ordering rule:
//
//        value < node  -> goes in the LEFT subtree
//        value > node  -> goes in the RIGHT subtree
//        value == node -> duplicate, rejected in this assignment
//
// That single rule is what makes searching fast: at every node
// you discard one whole side of the tree, so a balanced BST
// searches in O(log n) instead of O(n).
// ============================================================

#include <iostream>
using namespace std;

// ---- The Node -------------------------------------------------
// data  : the integer stored at this position
// left  : pointer to the root of the LEFT subtree (smaller values)
// right : pointer to the root of the RIGHT subtree (larger values)
// A pointer is nullptr when that subtree does not exist, which is
// also how we recognise a leaf (both pointers nullptr).
class Node
{
public:
    int data;
    Node* left;
    Node* right;

    Node(int value)
    {
        data = value;
        left = nullptr;
        right = nullptr;
    }
};

class BinarySearchTree
{
private:
    Node* root;         // entry point to the whole tree; nullptr when empty
    int   nodeCount;
    int   rejectedCount;

    // Recursive insert helper.
    // Returns the (possibly new) subtree root so the parent can
    // link it in. This is the standard way to attach a new node
    // without needing a separate "parent" pointer.
    Node* insertHelper(Node* current, int value, bool& inserted)
    {
        if (current == nullptr)             // found the empty spot
        {
            inserted = true;
            return new Node(value);
        }

        if (value < current->data)
        {
            current->left = insertHelper(current->left, value, inserted);
        }
        else if (value > current->data)
        {
            current->right = insertHelper(current->right, value, inserted);
        }
        else
        {
            // value == current->data  -> DUPLICATE DETECTED.
            // We simply return without creating a node, so the
            // tree is left exactly as it was.
            inserted = false;
        }
        return current;
    }

    // Inorder: LEFT -> ROOT -> RIGHT
    // Because everything smaller is visited before the node and
    // everything larger after it, the output comes out SORTED.
    void inorderHelper(Node* current)
    {
        if (current == nullptr) return;
        inorderHelper(current->left);
        cout << current->data << " ";
        inorderHelper(current->right);
    }

    // Preorder: ROOT -> LEFT -> RIGHT
    // Visits a node before its children, so replaying this order
    // through insert() rebuilds the identical tree shape.
    void preorderHelper(Node* current)
    {
        if (current == nullptr) return;
        cout << current->data << " ";
        preorderHelper(current->left);
        preorderHelper(current->right);
    }

    // Postorder: LEFT -> RIGHT -> ROOT
    // Children are finished before the parent, which is why this
    // is the order used to delete/free a tree safely.
    void postorderHelper(Node* current)
    {
        if (current == nullptr) return;
        postorderHelper(current->left);
        postorderHelper(current->right);
        cout << current->data << " ";
    }

    // Rightmost node of a subtree = largest value in it.
    Node* findMax(Node* current)
    {
        while (current != nullptr && current->right != nullptr)
            current = current->right;
        return current;
    }

    // Leftmost node of a subtree = smallest value in it.
    Node* findMin(Node* current)
    {
        while (current != nullptr && current->left != nullptr)
            current = current->left;
        return current;
    }

    Node* findNode(Node* current, int value)
    {
        if (current == nullptr || current->data == value) return current;
        if (value < current->data) return findNode(current->left, value);
        return findNode(current->right, value);
    }

    void printLeavesHelper(Node* current)
    {
        if (current == nullptr) return;
        if (current->left == nullptr && current->right == nullptr)
            cout << current->data << " ";
        printLeavesHelper(current->left);
        printLeavesHelper(current->right);
    }

    // Sideways picture of the tree: read it with your head tilted
    // to the left. Right subtree prints above, left subtree below.
    void printTreeHelper(Node* current, int depth)
    {
        if (current == nullptr) return;
        printTreeHelper(current->right, depth + 1);
        for (int i = 0; i < depth; i++) cout << "        ";
        cout << current->data << endl;
        printTreeHelper(current->left, depth + 1);
    }

    // Free every node, children first (postorder).
    void destroyHelper(Node* current)
    {
        if (current == nullptr) return;
        destroyHelper(current->left);
        destroyHelper(current->right);
        delete current;
    }

public:
    BinarySearchTree()
    {
        root = nullptr;
        nodeCount = 0;
        rejectedCount = 0;
    }

    ~BinarySearchTree()
    {
        destroyHelper(root);
    }

    void insert(int value)
    {
        bool inserted = false;
        root = insertHelper(root, value, inserted);
        if (inserted)
        {
            nodeCount++;
            cout << "  Inserted " << value << endl;
        }
        else
        {
            rejectedCount++;
            cout << "  DUPLICATE " << value << " detected - discarded, tree unchanged" << endl;
        }
    }

    void inorder()   { cout << "  Inorder   (L-Root-R): "; inorderHelper(root);   cout << endl; }
    void preorder()  { cout << "  Preorder  (Root-L-R): "; preorderHelper(root);  cout << endl; }
    void postorder() { cout << "  Postorder (L-R-Root): "; postorderHelper(root); cout << endl; }

    void printTree()
    {
        cout << "  (rotate 90 degrees clockwise to read normally)" << endl << endl;
        printTreeHelper(root, 0);
    }

    void printLeaves()
    {
        cout << "  Leaves (no children): ";
        printLeavesHelper(root);
        cout << endl;
    }

    void printRoot()
    {
        if (root == nullptr) { cout << "  Tree is empty." << endl; return; }
        cout << "  Root: " << root->data << endl;
        cout << "  Left subtree of root  starts at: "
             << (root->left  ? to_string(root->left->data)  : "none") << endl;
        cout << "  Right subtree of root starts at: "
             << (root->right ? to_string(root->right->data) : "none") << endl;
    }

    // Predecessor = largest value smaller than this node.
    // Successor   = smallest value larger than this node.
    // If the node has the matching subtree, the answer lives there;
    // otherwise we track it on the way down from the root.
    void predecessorAndSuccessor(int value)
    {
        Node* target = findNode(root, value);
        if (target == nullptr)
        {
            cout << "  " << value << " is not in the tree." << endl;
            return;
        }

        // Case 1: the answer lives inside the node's own subtree.
        //   predecessor = rightmost node of the LEFT subtree
        //   successor   = leftmost node of the RIGHT subtree
        Node* pred = (target->left  != nullptr) ? findMax(target->left)  : nullptr;
        Node* succ = (target->right != nullptr) ? findMin(target->right) : nullptr;

        // Case 2: no such subtree, so the answer is an ancestor.
        // Walking down from the root: every time we turn RIGHT the
        // node we left behind is smaller (a predecessor candidate),
        // and every time we turn LEFT it is larger (a successor
        // candidate). The LAST candidate recorded is the closest one.
        Node* predAncestor = nullptr;
        Node* succAncestor = nullptr;
        Node* current = root;
        while (current != nullptr && current->data != value)
        {
            if (value > current->data) { predAncestor = current; current = current->right; }
            else                       { succAncestor = current; current = current->left;  }
        }
        if (pred == nullptr) pred = predAncestor;
        if (succ == nullptr) succ = succAncestor;

        cout << "  Node " << value
             << " -> predecessor: " << (pred ? to_string(pred->data) : "none")
             << ",  successor: "    << (succ ? to_string(succ->data) : "none") << endl;
    }

    int  getNodeCount()     { return nodeCount; }
    int  getRejectedCount() { return rejectedCount; }
};

int main()
{
    // ---- My dataset: 12 values, with 27 and 82 appearing twice ----
    int values[] = {55, 27, 82, 19, 41, 70, 96, 27, 63, 88, 82, 12};
    int n = sizeof(values) / sizeof(values[0]);

    cout << "=== 1. Original array (" << n << " values) ===" << endl << "  ";
    for (int i = 0; i < n; i++) cout << values[i] << (i < n - 1 ? ", " : "\n");

    cout << "\n=== 2. Inserting in array order; duplicates rejected ===" << endl;
    BinarySearchTree tree;
    for (int i = 0; i < n; i++) tree.insert(values[i]);

    cout << "\n  Nodes actually inserted: " << tree.getNodeCount() << endl;
    cout << "  Duplicate occurrences discarded: " << tree.getRejectedCount()
         << "  (the second 27 and the second 82)" << endl;

    cout << "\n=== 3. The completed BST ===" << endl;
    tree.printTree();

    cout << "\n=== 4. Structure ===" << endl;
    tree.printRoot();
    tree.printLeaves();

    cout << "\n=== 5. Predecessor and successor ===" << endl;
    tree.predecessorAndSuccessor(55);
    tree.predecessorAndSuccessor(70);
    tree.predecessorAndSuccessor(12);
    tree.predecessorAndSuccessor(41);

    cout << "\n=== 6. Traversals ===" << endl;
    tree.inorder();
    tree.preorder();
    tree.postorder();
    cout << "\n  The inorder output is in ascending order. The BST rule puts every" << endl;
    cout << "  smaller value in the left subtree, so visiting left before the node" << endl;
    cout << "  and the node before the right subtree emits values smallest first." << endl;

    return 0;
}
