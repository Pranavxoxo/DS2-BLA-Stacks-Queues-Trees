// ============================================================
// CircularQueue.cpp - Array-based Circular Queue (static array)
// CSC-6021 Data Structures and Algorithms II
// ============================================================
//
// A queue is FIFO (First In, First Out): items are added at the
// REAR (end) and removed from the FRONT (start).
//
// Why circular?
//   In a plain linear array queue, `start` only ever moves
//   forward. After a few dequeues the slots at the front of the
//   array are unused but unreachable, and once `end` hits the
//   last index the queue reports "full" even though the array is
//   half empty. That wasted space is called false overflow.
//
//   A circular queue fixes this with modulo arithmetic:
//        index = (index + 1) % SIZE
//   so the index after the last one wraps back around to 0 and
//   the freed slots get reused.
//
// Why a `count` member?
//   With only start and end, the condition start == end is
//   ambiguous: it is true both when the queue is empty and when
//   it is completely full. Keeping a count of the live elements
//   removes that ambiguity without sacrificing a slot.
// ============================================================

#include <iostream>
using namespace std;

class Queue
{
private:
    static const int SIZE = 5;  // small on purpose so wrap-around happens quickly
    int arr[SIZE];              // the storage
    int start;                  // index of the FRONT element (the next one to leave)
    int end;                    // index of the REAR element (the most recently added)
    int count;                  // how many elements are currently stored

public:
    // An empty queue: start points at slot 0, end sits one slot
    // "behind" it so that the first enqueue lands in slot 0.
    Queue()
    {
        start = 0;
        end = -1;
        count = 0;
    }

    bool isEmpty()
    {
        return count == 0;
    }

    bool isFull()
    {
        return count == SIZE;
    }

    // enqueue(): add to the rear.
    // The modulo is the whole trick - when end is SIZE-1,
    // (SIZE-1 + 1) % SIZE == 0, so we wrap to the front.
    void enqueue(int value)
    {
        if (isFull())
        {
            cout << "  QUEUE OVERFLOW - cannot enqueue " << value
                 << ", all " << SIZE << " slots are in use." << endl;
            return;
        }
        end = (end + 1) % SIZE;
        arr[end] = value;
        count++;
        cout << "  Enqueued " << value << "  -> stored at index " << end
             << "  (start=" << start << ", end=" << end << ", count=" << count << ")" << endl;
    }

    // dequeue(): remove from the front, then wrap start the same way.
    int dequeue()
    {
        if (isEmpty())
        {
            cout << "  QUEUE UNDERFLOW - nothing to dequeue, the queue is empty." << endl;
            return -1;
        }
        int value = arr[start];
        int removedFrom = start;
        start = (start + 1) % SIZE;
        count--;
        cout << "  Dequeued " << value << " <- taken from index " << removedFrom
             << "  (start=" << start << ", end=" << end << ", count=" << count << ")" << endl;
        return value;
    }

    // displayAll(): walk `count` steps from `start`, wrapping as we go.
    // We cannot just loop from start to end, because after a wrap
    // end may be a SMALLER index than start.
    void displayAll()
    {
        if (isEmpty())
        {
            cout << "  Queue contents: (empty)" << endl;
            return;
        }
        cout << "  Queue contents (front -> rear): ";
        for (int i = 0; i < count; i++)
        {
            int index = (start + i) % SIZE;
            cout << arr[index] << "@" << index;
            if (i < count - 1) cout << ", ";
        }
        cout << endl;
    }

    // Helper for the demo: shows the raw array so the wrap is visible.
    void showRawArray()
    {
        cout << "  Raw array slots:  ";
        for (int i = 0; i < SIZE; i++)
        {
            bool live = false;
            for (int j = 0; j < count; j++)
            {
                if ((start + j) % SIZE == i) live = true;
            }
            cout << "[" << i << "]=";
            if (live) cout << arr[i];
            else      cout << "_";
            cout << "  ";
        }
        cout << endl;
    }
};

int main()
{
    Queue q;

    cout << "=== 1. Empty queue ===" << endl;
    q.displayAll();
    cout << "  Attempting to dequeue an empty queue:" << endl;
    q.dequeue();                              // demonstrates UNDERFLOW

    cout << "\n=== 2. Fill the queue completely (end reaches the last index) ===" << endl;
    q.enqueue(10);
    q.enqueue(20);
    q.enqueue(30);
    q.enqueue(40);
    q.enqueue(50);                            // end is now at index 4, the final slot
    q.displayAll();
    q.showRawArray();
    cout << "  isFull() = " << (q.isFull() ? "true" : "false") << endl;
    q.enqueue(60);                            // demonstrates OVERFLOW

    cout << "\n=== 3. Dequeue twice, freeing indices 0 and 1 ===" << endl;
    q.dequeue();
    q.dequeue();
    q.displayAll();
    q.showRawArray();
    cout << "  A LINEAR queue would now be stuck: end is already at the last" << endl;
    cout << "  index, so it would refuse new items even though 2 slots are free." << endl;

    cout << "\n=== 4. WRAP-AROUND: end goes from index 4 back to index 0 ===" << endl;
    q.enqueue(60);                            // (4 + 1) % 5 = 0  -> wraps
    q.enqueue(70);                            // lands in index 1
    q.displayAll();
    q.showRawArray();
    cout << "  60 was stored at index 0 - the array position is reused." << endl;
    cout << "  Note the front (30) is at index 2 and the rear (70) is at index 1," << endl;
    cout << "  so the queue physically wraps past the end of the array." << endl;

    cout << "\n=== 5. Drain the queue - FIFO order is preserved through the wrap ===" << endl;
    while (!q.isEmpty())
    {
        q.dequeue();
    }
    q.displayAll();

    return 0;
}
