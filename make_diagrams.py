#!/usr/bin/env python3
"""Generates the eight required diagrams for the DS2 BLA as standalone SVG files."""

import math
import os

OUT = "/home/claude/bla/diagrams"
os.makedirs(OUT, exist_ok=True)

INK = "#1B2430"
MUTED = "#5B6B7C"
RULE = "#C3CEDA"
PAPER = "#FFFFFF"
ADD = "#0F766E"        # push / enqueue / insert
REMOVE = "#B91C1C"     # pop / dequeue
ROOTC = "#F59E0B"
LEAFC = "#A7F3D0"
LEFTC = "#E0F2FE"
RIGHTC = "#FCE7F3"
GHOST = "#EEF2F6"

FONT = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"


def head(w, h, title, subtitle=None):
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"
     font-family="{FONT}" role="img" aria-label="{title}">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7"
            orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke"/>
    </marker>
  </defs>
  <rect width="{w}" height="{h}" fill="{PAPER}"/>
  <text x="34" y="42" font-size="23" font-weight="600" fill="{INK}">{title}</text>
'''
    if subtitle:
        s += f'  <text x="34" y="66" font-size="14.5" fill="{MUTED}">{subtitle}</text>\n'
    return s


def caption(x, y, lines, w=14, color=None):
    color = color or MUTED
    out = ""
    for i, ln in enumerate(lines):
        out += (f'  <text x="{x}" y="{y + i * 21}" font-size="{w}" fill="{color}">'
                f'{ln}</text>\n')
    return out


def write(name, body):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(body + "</svg>\n")
    print("wrote", name)


# ---------------------------------------------------------------- 1. STACK
def stack_diagram():
    W, H = 980, 560
    s = head(W, H, "Stack: push and pop",
             "Static array of capacity 5. Only the top slot is reachable, and that single "
             "restriction is what makes the structure LIFO.")

    panels = [
        (70,  "Initial state", 2, [11, 22, 33], None),
        (400, "After push(44)", 3, [11, 22, 33, 44], 3),
        (730, "After pop()", 2, [11, 22, 33], None),
    ]
    SW, SH, GAP = 112, 40, 6
    BASE = 430  # y of slot 0

    for px, label, top, vals, hl in panels:
        s += (f'  <text x="{px + SW/2}" y="{132}" font-size="15" font-weight="600" '
              f'text-anchor="middle" fill="{INK}">{label}</text>\n')
        s += (f'  <text x="{px + SW/2}" y="{153}" font-size="13.5" text-anchor="middle" '
              f'fill="{MUTED}">top = {top}</text>\n')
        for i in range(5):
            y = BASE - i * (SH + GAP)
            filled = i < len(vals)
            ghost = (label == "After pop()" and i == 3)
            fill = PAPER
            if filled:
                fill = "#FEF3C7" if hl == i else "#F1F5F9"
            if ghost:
                fill = GHOST
            dash = ' stroke-dasharray="4 3"' if (not filled and not ghost) else ''
            s += (f'  <rect x="{px}" y="{y}" width="{SW}" height="{SH}" rx="4" fill="{fill}" '
                  f'stroke="{RULE}" stroke-width="1.5"{dash}/>\n')
            if filled:
                s += (f'  <text x="{px + SW/2}" y="{y + 26}" font-size="17" font-weight="600" '
                      f'text-anchor="middle" fill="{INK}">{vals[i]}</text>\n')
            elif ghost:
                s += (f'  <text x="{px + SW/2}" y="{y + 26}" font-size="16" text-anchor="middle" '
                      f'fill="#AEBAC6" font-style="italic">44</text>\n')
            s += (f'  <text x="{px - 12}" y="{y + 26}" font-size="12.5" text-anchor="end" '
                  f'fill="{MUTED}">{i}</text>\n')
        ty = BASE - top * (SH + GAP) + 26
        s += (f'  <text x="{px + SW + 10}" y="{ty}" font-size="13" font-weight="600" '
              f'fill="{ADD if label != "After pop()" else INK}">&#8592; top</text>\n')

    s += (f'  <path d="M 240 224 L 380 224" stroke="{ADD}" stroke-width="2.5" fill="none" '
          f'marker-end="url(#arrow)"/>\n')
    s += (f'  <text x="310" y="212" font-size="14.5" font-weight="600" text-anchor="middle" '
          f'fill="{ADD}">push(44)</text>\n')
    s += (f'  <text x="310" y="246" font-size="12.5" text-anchor="middle" fill="{MUTED}">'
          f'top++, then write</text>\n')

    s += (f'  <path d="M 570 224 L 710 224" stroke="{REMOVE}" stroke-width="2.5" fill="none" '
          f'marker-end="url(#arrow)"/>\n')
    s += (f'  <text x="640" y="212" font-size="14.5" font-weight="600" text-anchor="middle" '
          f'fill="{REMOVE}">pop() returns 44</text>\n')
    s += (f'  <text x="640" y="246" font-size="12.5" text-anchor="middle" fill="{MUTED}">'
          f'read, then top--</text>\n')

    s += (f'  <text x="856" y="{BASE - 3*(SH+GAP) + 20}" font-size="11.5" fill="#AEBAC6">'
          f'still in memory,</text>\n')
    s += (f'  <text x="856" y="{BASE - 3*(SH+GAP) + 35}" font-size="11.5" fill="#AEBAC6">'
          f'logically gone</text>\n')

    s += caption(34, 496, [
        "44 was pushed last and popped first: both operations go through the same single "
        "opening, so the ordering falls out of the shape.",
        "pop() never erases the slot; it only moves the top marker down, so the next push overwrites "
        "it. Both operations are O(1).",
    ])
    write("1-stack-push-pop.svg", s)


# ---------------------------------------------------------------- 2. QUEUE
def queue_diagram():
    W, H = 980, 560
    s = head(W, H, "Queue: enqueue and dequeue",
             "Items join at the rear and leave from the front \u2014 FIFO. The same array at two "
             "moments in time.")

    SW, SH = 104, 62
    X0 = 170

    def row(y, vals, start, end, label):
        out = (f'  <text x="34" y="{y - 46}" font-size="14.5" font-weight="600" fill="{INK}">'
               f'{label}</text>\n')
        for i in range(5):
            x = X0 + i * SW
            v = vals[i]
            fill = "#F1F5F9" if v is not None else PAPER
            dash = "" if v is not None else ' stroke-dasharray="4 3"'
            out += (f'  <rect x="{x}" y="{y}" width="{SW}" height="{SH}" fill="{fill}" '
                    f'stroke="{RULE}" stroke-width="1.5"{dash}/>\n')
            if v is not None:
                out += (f'  <text x="{x + SW/2}" y="{y + 39}" font-size="19" font-weight="600" '
                        f'text-anchor="middle" fill="{INK}">{v}</text>\n')
            out += (f'  <text x="{x + SW/2}" y="{y + SH + 19}" font-size="12" '
                    f'text-anchor="middle" fill="{MUTED}">index {i}</text>\n')
        fx = X0 + start * SW + SW / 2
        rx = X0 + end * SW + SW / 2
        out += (f'  <text x="{fx}" y="{y - 14}" font-size="12.5" font-weight="600" '
                f'text-anchor="middle" fill="{ADD}">start / front</text>\n')
        out += (f'  <text x="{rx}" y="{y - 14}" font-size="12.5" font-weight="600" '
                f'text-anchor="middle" fill="{REMOVE}">end / rear</text>\n')
        return out

    # ---- row 1: normal operation
    y1 = 170
    s += row(y1, [10, 20, 30, None, None], 0, 2, "Normal operation: three items waiting")
    s += (f'  <path d="M 150 {y1+31} L 46 {y1+31}" stroke="{REMOVE}" stroke-width="2.5" '
          f'fill="none" marker-end="url(#arrow)"/>\n')
    s += (f'  <text x="98" y="{y1+20}" font-size="13" font-weight="600" text-anchor="middle" '
          f'fill="{REMOVE}">dequeue()</text>\n')
    s += (f'  <text x="98" y="{y1+52}" font-size="12.5" text-anchor="middle" fill="{MUTED}">'
          f'returns 10</text>\n')
    s += (f'  <path d="M 900 {y1+31} L 706 {y1+31}" stroke="{ADD}" stroke-width="2.5" '
          f'fill="none" marker-end="url(#arrow)"/>\n')
    s += (f'  <text x="806" y="{y1+20}" font-size="13" font-weight="600" text-anchor="middle" '
          f'fill="{ADD}">enqueue(40)</text>\n')
    s += (f'  <text x="806" y="{y1+52}" font-size="12.5" text-anchor="middle" fill="{MUTED}">'
          f'lands in index 3</text>\n')

    # ---- row 2: false overflow
    y2 = 370
    s += row(y2, [None, None, 30, 40, 50], 2, 4,
             "Later: the queue filled up, then two items left")
    s += (f'  <rect x="{X0}" y="{y2}" width="{2*SW}" height="{SH}" fill="none" '
          f'stroke="{REMOVE}" stroke-width="1.6" stroke-dasharray="5 4"/>\n')
    s += (f'  <text x="{X0 + SW}" y="{y2 - 14}" font-size="12.5" font-weight="600" '
          f'text-anchor="middle" fill="{REMOVE}">free, but unreachable</text>\n')
    s += (f'  <path d="M 900 {y2+31} L 706 {y2+31}" stroke="{RULE}" stroke-width="2.5" '
          f'fill="none" stroke-dasharray="6 5" marker-end="url(#arrow)"/>\n')
    s += (f'  <text x="806" y="{y2+20}" font-size="13" font-weight="600" text-anchor="middle" '
          f'fill="{MUTED}">enqueue(60)</text>\n')
    s += (f'  <text x="806" y="{y2+52}" font-size="12.5" text-anchor="middle" fill="{REMOVE}">'
          f'refused</text>\n')

    s += caption(34, 496, [
        "The second row is FALSE OVERFLOW: end has reached the last index and can only move "
        "forward, so the queue calls itself full",
        "while 40% of the array sits empty. Shifting everything down would fix it, but that turns "
        "an O(1) operation into O(n).",
    ])
    write("2-queue-enqueue-dequeue.svg", s)


# -------------------------------------------------- 3. CIRCULAR WRAP-AROUND
def circular_diagram():
    W, H = 980, 660
    s = head(W, H, "Circular queue: wrapping from the last slot back to slot 0",
             "State taken from CircularQueue.cpp after the wrap: start = 2, end = 1, count = 5.")

    cx, cy, R, r = 400, 358, 175, 48
    slots = {0: 60, 1: 70, 2: 30, 3: 40, 4: 50}
    pos = {}
    for i in range(5):
        th = math.radians(-90 + 72 * i)
        pos[i] = (cx + R * math.cos(th), cy + R * math.sin(th))

    s += (f'  <circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{RULE}" '
          f'stroke-width="1.5" stroke-dasharray="3 5"/>\n')

    x4, y4 = pos[4]
    x0, y0 = pos[0]
    s += (f'  <path d="M {x4+16:.1f} {y4-44:.1f} Q {(x4+x0)/2 - 20:.1f} {cy-R-56:.1f} '
          f'{x0-50:.1f} {y0-14:.1f}" stroke="{ADD}" stroke-width="3" fill="none" '
          f'marker-end="url(#arrow)"/>\n')
    s += (f'  <text x="{(x4+x0)/2 - 16:.1f}" y="{cy-R-64:.1f}" font-size="15.5" '
          f'font-weight="600" text-anchor="middle" fill="{ADD}">(4 + 1) % 5 = 0</text>\n')

    for i in range(5):
        x, y = pos[i]
        fill, stroke, sw = "#F1F5F9", RULE, 1.8
        if i == 2:
            fill, stroke, sw = "#D1FAE5", ADD, 3
        if i == 1:
            fill, stroke, sw = "#FEE2E2", REMOVE, 3
        s += (f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" '
              f'stroke-width="{sw}"/>\n')
        s += (f'  <text x="{x:.1f}" y="{y + 2:.1f}" font-size="22" font-weight="600" '
              f'text-anchor="middle" fill="{INK}">{slots[i]}</text>\n')
        s += (f'  <text x="{x:.1f}" y="{y + 23:.1f}" font-size="12" text-anchor="middle" '
              f'fill="{MUTED}">index {i}</text>\n')

    x2, y2 = pos[2]
    s += (f'  <text x="{x2:.1f}" y="{y2 + r + 26:.1f}" font-size="13.5" font-weight="600" '
          f'text-anchor="middle" fill="{ADD}">start / front</text>\n')
    x1, y1 = pos[1]
    s += (f'  <text x="{x1 + r + 14:.1f}" y="{y1 + 5:.1f}" font-size="13.5" font-weight="600" '
          f'fill="{REMOVE}">end / rear</text>\n')

    s += (f'  <text x="{cx}" y="{cy - 16}" font-size="13.5" text-anchor="middle" fill="{MUTED}">'
          f'front &#8594; rear</text>\n')
    s += (f'  <text x="{cx}" y="{cy + 10}" font-size="17" font-weight="600" text-anchor="middle" '
          f'fill="{INK}">30, 40, 50, 60, 70</text>\n')
    s += (f'  <text x="{cx}" y="{cy + 32}" font-size="13" text-anchor="middle" fill="{MUTED}">'
          f'count = 5</text>\n')

    s += (f'  <rect x="726" y="180" width="220" height="158" rx="6" fill="#F8FAFC" '
          f'stroke="{RULE}"/>\n')
    s += (f'  <text x="746" y="208" font-size="14" font-weight="600" fill="{INK}">'
          f'The whole trick</text>\n')
    for j, ln in enumerate(["end   = (end + 1) % SIZE;",
                            "start = (start + 1) % SIZE;"]):
        s += (f'  <text x="746" y="{236 + j*22}" font-size="12.5" fill="{ADD}">{ln}</text>\n')
    for j, ln in enumerate(["Freed slots get reused,",
                            "nothing shifts, and both",
                            "operations stay O(1)."]):
        s += (f'  <text x="746" y="{288 + j*19}" font-size="12.5" fill="{MUTED}">{ln}</text>\n')

    s += caption(34, 596, [
        "60 was enqueued after the rear had already reached index 4, so it landed in slot 0 \u2014 "
        "a slot an earlier dequeue had freed.",
        "The rear is now at a lower index than the front, which is why displayAll() steps count "
        "times from start instead of looping start to end.",
    ])
    write("3-circular-queue-wraparound.svg", s)


# ---------------------------------------------------------- tree scaffolding
BST = {
    55: (410, 118), 27: (232, 208), 82: (592, 208),
    19: (146, 298), 41: (322, 298), 70: (502, 298), 96: (682, 298),
    12: (86, 388), 63: (448, 388), 88: (628, 388),
}
EDGES = [(55, 27), (55, 82), (27, 19), (27, 41), (82, 70), (82, 96),
         (19, 12), (70, 63), (96, 88)]
LEAVES = {12, 41, 63, 88}
NR = 27


def draw_tree(fills=None, badges=None, badge_color=ADD, dy=0):
    fills = fills or {}
    out = ""
    for a, b in EDGES:
        ax, ay = BST[a][0], BST[a][1] + dy
        bx, by = BST[b][0], BST[b][1] + dy
        out += (f'  <line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="{RULE}" '
                f'stroke-width="2"/>\n')
    for v, (x, y0) in BST.items():
        y = y0 + dy
        out += (f'  <circle cx="{x}" cy="{y}" r="{NR}" fill="{fills.get(v, PAPER)}" '
                f'stroke="{INK}" stroke-width="2"/>\n')
        out += (f'  <text x="{x}" y="{y + 6}" font-size="17" font-weight="600" '
                f'text-anchor="middle" fill="{INK}">{v}</text>\n')
    if badges:
        for v, n in badges.items():
            x, y = BST[v][0], BST[v][1] + dy
            out += (f'  <circle cx="{x + 26}" cy="{y - 25}" r="14" fill="{badge_color}"/>\n')
            out += (f'  <text x="{x + 26}" y="{y - 20}" font-size="13" font-weight="700" '
                    f'text-anchor="middle" fill="#FFFFFF">{n}</text>\n')
    return out


# ------------------------------------------------- 4. TREE TERMINOLOGY
def terminology_diagram():
    W, H = 900, 600
    DY = 34
    s = head(W, H, "Binary tree terminology",
             "Every node holds a value and two pointers. A pointer that is nullptr means that "
             "subtree does not exist.")

    s += (f'  <rect x="46" y="210" width="316" height="250" rx="10" fill="none" '
          f'stroke="#7C9CB8" stroke-width="1.4" stroke-dasharray="6 5"/>\n')
    s += (f'  <text x="46" y="200" font-size="13" font-weight="600" fill="#4A7593">'
          f'left subtree of the root</text>\n')
    s += (f'  <rect x="452" y="210" width="290" height="250" rx="10" fill="none" '
          f'stroke="#B08099" stroke-width="1.4" stroke-dasharray="6 5"/>\n')
    s += (f'  <text x="452" y="200" font-size="13" font-weight="600" fill="#96566F">'
          f'right subtree of the root</text>\n')

    s += draw_tree(fills={55: "#FEF3C7", 12: LEAFC, 41: LEAFC, 63: LEAFC, 88: LEAFC}, dy=DY)

    def lead(x1, y1, x2, y2):
        return (f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{MUTED}" '
                f'stroke-width="1.2"/>\n')

    s += lead(302, 150, 382, 150)
    s += (f'  <text x="298" y="154" font-size="13" font-weight="600" text-anchor="end" '
          f'fill="{MUTED}">root \u2014 the one node with no parent</text>\n')

    s += lead(244, 206, 238, 216)
    s += (f'  <text x="248" y="200" font-size="13" font-weight="600" fill="{MUTED}">'
          f'parent of 19 and 41</text>\n')

    s += lead(116, 300, 134, 310)
    s += (f'  <text x="112" y="296" font-size="13" font-weight="600" text-anchor="end" '
          f'fill="{MUTED}">left child</text>\n')
    s += lead(354, 300, 336, 310)
    s += (f'  <text x="358" y="296" font-size="13" font-weight="600" fill="{MUTED}">'
          f'right child</text>\n')

    s += lead(86, 462, 86, 478)
    s += (f'  <text x="36" y="496" font-size="13" font-weight="600" fill="{MUTED}">'
          f'leaf \u2014 both pointers are nullptr</text>\n')
    s += (f'  <line x1="322" y1="362" x2="322" y2="478" stroke="{MUTED}" stroke-width="1.2" '
          f'stroke-dasharray="3 3"/>\n')
    s += (f'  <text x="322" y="496" font-size="13" font-weight="600" text-anchor="middle" '
          f'fill="{MUTED}">also a leaf</text>\n')

    s += (f'  <text x="756" y="252" font-size="13" font-weight="600" fill="{MUTED}">'
          f'a subtree is</text>\n')
    for j, ln in enumerate(["a tree in its own", "right, which is why", "every method in the",
                            "class can recurse", "on it"]):
        s += (f'  <text x="756" y="{272 + j*18}" font-size="12.5" fill="{MUTED}">{ln}</text>\n')

    s += caption(34, 540, [
        "A binary tree is only a shape: at most two children per node, with no rule about which "
        "value goes where.",
        "predecessor(41) = 27 and successor(41) = 55 \u2014 the neighbours of 41 in the sorted "
        "(inorder) sequence.",
    ])
    write("4-binary-tree-terminology.svg", s)


# --------------------------------------------------------- 5. COMPLETED BST
def bst_diagram():
    W, H = 980, 610
    DY = 18
    s = head(W, H, "Completed binary search tree",
             "Built from 55, 27, 82, 19, 41, 70, 96, 27, 63, 88, 82, 12 \u2014 inserted in array "
             "order, duplicates rejected.")

    s += (f'  <rect x="52" y="188" width="316" height="280" rx="12" fill="{LEFTC}" '
          f'opacity="0.8"/>\n')
    s += (f'  <rect x="416" y="188" width="316" height="280" rx="12" fill="{RIGHTC}" '
          f'opacity="0.8"/>\n')
    s += (f'  <text x="210" y="454" font-size="13.5" font-weight="600" text-anchor="middle" '
          f'fill="#0369A1">left subtree \u2014 every value &lt; 55</text>\n')
    s += (f'  <text x="574" y="454" font-size="13.5" font-weight="600" text-anchor="middle" '
          f'fill="#9D174D">right subtree \u2014 every value &gt; 55</text>\n')

    s += draw_tree(fills={55: ROOTC, 12: LEAFC, 41: LEAFC, 63: LEAFC, 88: LEAFC}, dy=DY)

    s += (f'  <text x="410" y="94" font-size="13.5" font-weight="600" text-anchor="middle" '
          f'fill="{INK}">root</text>\n')
    s += (f'  <line x1="410" y1="100" x2="410" y2="108" stroke="{INK}" stroke-width="1.5"/>\n')

    s += (f'  <rect x="770" y="188" width="176" height="104" rx="6" fill="#FEF2F2" '
          f'stroke="#F2C9C9"/>\n')
    s += (f'  <text x="786" y="216" font-size="12.5" font-weight="600" fill="{REMOVE}">'
          f'discarded as duplicates</text>\n')
    s += (f'  <text x="786" y="242" font-size="13" fill="{MUTED}">the second 27</text>\n')
    s += (f'  <text x="786" y="262" font-size="13" fill="{MUTED}">the second 82</text>\n')
    s += (f'  <text x="786" y="282" font-size="12.5" fill="{MUTED}">10 of 12 inserted</text>\n')

    lx, ly = 52, 498
    s += (f'  <circle cx="{lx+10}" cy="{ly}" r="10" fill="{ROOTC}" stroke="{INK}" '
          f'stroke-width="1.5"/>\n')
    s += (f'  <text x="{lx+28}" y="{ly+5}" font-size="13" fill="{MUTED}">root</text>\n')
    s += (f'  <circle cx="{lx+110}" cy="{ly}" r="10" fill="{LEAFC}" stroke="{INK}" '
          f'stroke-width="1.5"/>\n')
    s += (f'  <text x="{lx+128}" y="{ly+5}" font-size="13" fill="{MUTED}">'
          f'leaves: 12, 41, 63, 88</text>\n')

    s += caption(34, 540, [
        "The BST rule holds at every node, not just the root. That is what makes lookup O(log n) "
        "in a balanced tree.",
        "predecessor(55) = 41, the rightmost node of the left subtree. successor(55) = 63, the "
        "leftmost node of the right subtree.",
    ])
    write("5-completed-bst.svg", s)


# ------------------------------------------------------------ 6/7/8 TRAVERSALS
def traversal_diagram(name, title, rule, order_map, sequence, why, color):
    W, H = 980, 580
    s = head(W, H, title, rule)
    s += draw_tree(fills={v: "#F8FAFC" for v in BST}, badges=order_map, badge_color=color)

    s += (f'  <text x="34" y="472" font-size="14" font-weight="600" fill="{INK}">'
          f'Visit order</text>\n')
    s += (f'  <text x="34" y="498" font-size="18" font-weight="600" fill="{color}">'
          f'{sequence}</text>\n')
    s += caption(34, 528, why)
    write(name, s)


def traversals():
    traversal_diagram(
        "6-inorder-traversal.svg",
        "Inorder traversal: LEFT \u2192 ROOT \u2192 RIGHT",
        "Numbered badges show the order in which each node is printed.",
        {12: 1, 19: 2, 27: 3, 41: 4, 55: 5, 63: 6, 70: 7, 82: 8, 88: 9, 96: 10},
        "12, 19, 27, 41, 55, 63, 70, 82, 88, 96",
        ["Each node is printed after everything smaller beneath it and before everything larger "
         "beneath it, so the output comes out sorted.",
         "The tree never stores the values in sorted order \u2014 the sortedness falls out of the "
         "insertion rule combined with the visiting rule."],
        "#0F766E")

    traversal_diagram(
        "7-preorder-traversal.svg",
        "Preorder traversal: ROOT \u2192 LEFT \u2192 RIGHT",
        "Each node is printed the moment you arrive at it, before either child is explored.",
        {55: 1, 27: 2, 19: 3, 12: 4, 41: 5, 82: 6, 70: 7, 63: 8, 96: 9, 88: 10},
        "55, 27, 19, 12, 41, 82, 70, 63, 96, 88",
        ["The root comes out first and each parent precedes its whole subtree.",
         "Re-inserting the values in this order rebuilds an identical tree, which is why preorder "
         "serialises or copies a tree."],
        "#1D4ED8")

    traversal_diagram(
        "8-postorder-traversal.svg",
        "Postorder traversal: LEFT \u2192 RIGHT \u2192 ROOT",
        "A node is printed only once both of its children are completely finished.",
        {12: 1, 19: 2, 41: 3, 27: 4, 63: 5, 70: 6, 88: 7, 96: 8, 82: 9, 55: 10},
        "12, 19, 41, 27, 63, 70, 88, 96, 82, 55",
        ["The root comes out last because it is the parent of everything.",
         "Children finish before their parent, which is why destroyHelper() in "
         "BinarySearchTree.cpp is a postorder walk."],
        "#B45309")


if __name__ == "__main__":
    stack_diagram()
    queue_diagram()
    circular_diagram()
    terminology_diagram()
    bst_diagram()
    traversals()
    print("\nAll diagrams written to", OUT)
