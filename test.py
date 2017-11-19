from puzzle import Puzzle
from node import Node
from collections import deque
import numpy as np
import time



p = Puzzle(True)
p.slide = 1
p.left_up = False
p.left = np.array([3, 5], np.int8)
p.right = np.array([6, 0], np.int8)
p.board = np.array([[7, 1, 2, 0, 0, 0, 0], [0, 0, 4, 0, 0, 0, 0]])
print(p)

current_node = Node(p)
queue = deque([current_node])
start = time.time()
count = 0
while True:
    current_node.get_children()
    if current_node.child_a is not None:
        if current_node.child_a.is_end_state():
            current_node = current_node.child_a
            break
        else:
            queue.append(current_node.child_a)
    if current_node.child_b is not None:
        if current_node.child_b.is_end_state():
            current_node = current_node.child_b
            break
        else:
            queue.append(current_node.child_b)
    if current_node.child_c is not None:
        if current_node.child_c.is_end_state():
            current_node = current_node.child_c
            break
        else:
            queue.append(current_node.child_c)
    current_node = queue.popleft()

    count += 1
    if count % 10000 == 0:
        print(count)
        print("\n" + str(current_node.p) + "\n")
        print("Node count: " + str(current_node.root.count))
        print("Queue size: " + str(queue.__len__()))
end = time.time()
print(end - start)
print(current_node.p)
print(current_node.get_solution())
