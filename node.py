from puzzle import Puzzle

class Node:

    p = Puzzle()
    # 1 = slide left, 2 = slide right, 3 = flip, 0 = root
    last_m = 0
    parent = None
    child_a = None
    child_b = None
    child_c = None

    count = 0
    depth = 0

    def __init__(self, puzzle, last_m=0, parent=None, root=None):
        self.p = puzzle
        self.last_m = last_m
        self.parent = parent
        if root is None:
            self.root = self
        else:
            self.root = root

    def get_solution(self):
        results = []
        temp_node = self
        while temp_node.parent is not None:
            results.append(temp_node.last_m)
            temp_node = temp_node.parent
        results.append(temp_node.last_m)
        return results

    def is_end_state(self):
        return self.p.is_solution_line()

    def get_children(self):
        if self.last_m != 3:
            self.root.count += 1
            self.__create_child__(3)
        if self.p.slide < 3 and self.last_m != 1:
            self.root.count += 1
            self.__create_child__(2)
        if self.p.slide > 0 and self.last_m != 2:
            self.root.count += 1
            self.__create_child__(1)

    def __create_child__(self, move):
        if self.child_a is None:
            temp_child_puzzle = self.p.clone()
            temp_child_puzzle.move(move)
            self.child_a = Node(temp_child_puzzle, move, self, self.root)
        elif self.child_b is None:
            temp_child_puzzle = self.p.clone()
            temp_child_puzzle.move(move)
            self.child_b = Node(temp_child_puzzle, move, self, self.root)
        else:
            temp_child_puzzle = self.p.clone()
            temp_child_puzzle.move(move)
            self.child_c = Node(temp_child_puzzle, move, self, self.root)

