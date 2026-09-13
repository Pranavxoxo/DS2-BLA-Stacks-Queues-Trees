// ============================================================
// Stack.cpp - Array-based Stack (static array, no STL)
// CSC-6021 Data Structures and Algorithms II
// ============================================================
//
// A stack is a LIFO (Last In, First Out) container. Everything
// happens at ONE end of the array, which is why every operation
// below is O(1) - no shifting of elements is ever required.
//
// The whole class is really just an array plus one integer
// (`top`) that remembers the index of the most recently pushed
// element. top == -1 means "nothing in here yet".
// ============================================================

#include <iostream>
using namespace std;

class Stack
{
private:
    static const int SIZE = 5;  // fixed capacity - chosen small so overflow is easy to demonstrate
    int arr[SIZE];              // the storage; memory is reserved once, at compile time
    int top;                    // index of the top element; -1 when the stack is empty

public:
    // Constructor: an empty stack has no top element yet.
    Stack()
    {
        top = -1;
    }

    // No elements have been pushed, or every element has been popped.
    bool isEmpty()
    {
        return top == -1;
    }

    // The last usable index is SIZE - 1, so that index means "no room left".
    bool isFull()
    {
        return top == SIZE - 1;
    }

    // push(): add a value on top.
    // Guard against STACK OVERFLOW first - writing to arr[SIZE]
    // would be out of bounds and is undefined behaviour in C++.
    void push(int value)
    {
        if (isFull())
        {
            cout << "  STACK OVERFLOW - cannot push " << value
                 << ", the array is full (capacity " << SIZE << ")." << endl;
            return;
        }
        top = top + 1;      // move the marker up one slot
        arr[top] = value;   // then store the value there
        cout << "  Pushed " << value << "  (top index is now " << top << ")" << endl;
    }

    // pop(): remove and return the top value.
    // Guard against STACK UNDERFLOW - popping from an empty stack.
    // Note we do not erase the old value; we simply move `top` down,
    // so the slot is logically gone and will be overwritten by the
    // next push. That is why pop is O(1).
    int pop()
    {
        if (isEmpty())
        {
            cout << "  STACK UNDERFLOW - nothing to pop, the stack is empty." << endl;
            return -1;      // sentinel value meaning "no data"
        }
        int value = arr[top];
        top = top - 1;
        cout << "  Popped " << value << " (top index is now " << top << ")" << endl;
        return value;
    }

    // peek()/top(): look at the top value WITHOUT removing it.
    int peek()
    {
        if (isEmpty())
        {
            cout << "  Stack is empty - nothing to peek at." << endl;
            return -1;
        }
        return arr[top];
    }

    // displayAll(): print from the top down, because that is the
    // order in which the elements would actually come off.
    void displayAll()
    {
        if (isEmpty())
        {
            cout << "  Stack contents: (empty)" << endl;
            return;
        }
        cout << "  Stack contents (top -> bottom): ";
        for (int i = top; i >= 0; i--)
        {
            cout << arr[i];
            if (i > 0) cout << ", ";
        }
        cout << endl;
    }
};

int main()
{
    Stack s;

    cout << "=== 1. Empty stack ===" << endl;
    s.displayAll();
    cout << "  isEmpty() = " << (s.isEmpty() ? "true" : "false") << endl;
    cout << "  Attempting to pop an empty stack:" << endl;
    s.pop();                                  // demonstrates UNDERFLOW

    cout << "\n=== 2. Pushing values ===" << endl;
    s.push(11);
    s.push(22);
    s.push(33);
    s.displayAll();
    cout << "  peek() = " << s.peek() << "  (value is still on the stack)" << endl;
    s.displayAll();

    cout << "\n=== 3. Filling the stack to capacity ===" << endl;
    s.push(44);
    s.push(55);
    cout << "  isFull() = " << (s.isFull() ? "true" : "false") << endl;
    s.displayAll();
    cout << "  Attempting one more push:" << endl;
    s.push(66);                               // demonstrates OVERFLOW

    cout << "\n=== 4. Popping values (LIFO order) ===" << endl;
    s.pop();
    s.pop();
    s.displayAll();
    cout << "  Notice 55 and 44 came off first - they went on last." << endl;

    cout << "\n=== 5. Emptying the stack completely ===" << endl;
    while (!s.isEmpty())
    {
        s.pop();
    }
    s.displayAll();
    cout << "  isEmpty() = " << (s.isEmpty() ? "true" : "false") << endl;

    return 0;
}
