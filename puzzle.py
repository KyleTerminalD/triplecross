from random import randint
import copy
import numpy as np


class Puzzle:

    slide = 1
    left_up = True

    left = np.array([0, 0], np.int8)
    right = np.array([0, 0], np.int8)

    board = np.array([[0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0]], np.int8)

    def __init__(self, default=False):
        if default:
            self.board = np.array([[1, 2, 0, 0, 0, 0, 0], [3, 4, 0, 0, 5, 6, 7]], np.int8)

    def move(self, move):
        if move == 1:
            self.slide_left()
        elif move == 2:
            self.slide_right()
        elif move == 3:
            self.flip()

    def slide_left(self):
        if self.slide == 2:
            return False
        else:
            self.slide += 1
            return True

    def slide_right(self):
        if self.slide == 0:
            return False
        else:
            self.slide -= 1
            return True

    def flip(self):
        if self.left_up:
            temp_left = self.left[:]
            self.left = copy.deepcopy(self.board[1][self.slide:self.slide + 2])
            self.board[1][self.slide] = self.board[0][self.slide]
            self.board[1][self.slide + 1] = self.board[0][self.slide + 1]
            self.board[0][self.slide] = temp_left[0]
            self.board[0][self.slide + 1] = temp_left[1]

            temp_right = self.right[:]
            self.right = copy.deepcopy(self.board[0][self.slide + 3:self.slide + 5])
            self.board[0][self.slide + 3] = self.board[1][self.slide + 3]
            self.board[0][self.slide + 4] = self.board[1][self.slide + 4]
            self.board[1][self.slide + 3] = temp_right[0]
            self.board[1][self.slide + 4] = temp_right[1]

            self.left_up = False
        else:
            temp_left = self.left[:]
            self.left = copy.deepcopy(self.board[0][self.slide:self.slide + 2])
            self.board[0][self.slide] = self.board[1][self.slide]
            self.board[0][self.slide + 1] = self.board[1][self.slide + 1]
            self.board[1][self.slide] = temp_left[0]
            self.board[1][self.slide + 1] = temp_left[1]

            temp_right = self.right[:]
            self.right = copy.deepcopy(self.board[1][self.slide + 3:self.slide + 5])
            self.board[1][self.slide + 3] = self.board[0][self.slide + 3]
            self.board[1][self.slide + 4] = self.board[0][self.slide + 4]
            self.board[0][self.slide + 3] = temp_right[0]
            self.board[0][self.slide + 4] = temp_right[1]

            self.left_up = True
        return True

    def scramble(self, moves=20):
        for i in range(0, moves):
            move = randint(0, 3)
            if move == 0:
                self.slide_left()
            elif move == 1:
                self.slide_right()
            else:
                self.flip()

    def is_solution(self):
        if self.is_solution_line() and self.is_solution_circle():
            return True
        else:
            return False

    def is_solution_circle(self):
        if self.left_up:
            if (self.left == [1, 2]).all() and self.board[0][self.slide] == 3 and self.board[0][self.slide + 1] == 4:
                return True
            elif (self.right == [3, 4]).all() and self.board[1][self.slide + 3] == 1 and self.board[1][self.slide + 4] == 2:
                return True
        else:
            if (self.left == [3, 4]).all() and self.board[1][self.slide] == 1 and self.board[1][self.slide + 1] == 2:
                return True
            elif (self.right == [1, 2]).all() and self.board[0][self.slide + 3] == 3 and self.board[0][self.slide + 4] == 4:
                return True

        for x in range(0, 7):
            if (self.board[0][x:x+2] == [1, 2]).all() and (self.board[1][x:x+2] == [3, 4]).all():
                return True
        return False

    def is_solution_line(self):
        for y in range(0, 2):
            for x in range(0, 5):
                if self.board[y][x] >= 5:
                    if self.board[y][x + 1] >= 5 and self.board[y][x + 2] >= 5:
                        return True
        return False

    def clone(self):
        temp_p = Puzzle()
        temp_p.slide = self.slide
        temp_p.left_up = self.left_up
        temp_p.left = self.left[:]
        temp_p.right = self.right[:]
        temp_p.board = copy.deepcopy(self.board)
        return temp_p

    def __str__(self):
        results = ""
        if self.left_up:
            for i in range(0, self.slide):
                results += " "
            results += str(self.left[0]) + str(self.left[1])
        else:
            for i in range(0, self.slide + 3):
                results += " "
            results += str(self.right[0]) + str(self.right[1])

        results += "\n"
        for y in range(0, 2):
            for x in range(0, 7):
                results += str(self.board[y][x])
            results += "\n"

        if not self.left_up:
            for i in range(0, self.slide):
                results += " "
            results += str(self.left[0]) + str(self.left[1])
        else:
            for i in range(0, self.slide + 3):
                results += " "
            results += str(self.right[0]) + str(self.right[1])
        return results

    def bin3bit(self, num):
        if num > 7 or num < 0:
            raise IndexError
        results = bin(num)[2:]
        while results.__len__() < 3:
            results = "0" + results
        return results

    def puzzle_to_integer(self):
        if self.left_up:
            results = "1"
        else:
            results = "0"

        bslide = bin(self.slide)[2:]

        while bslide.__len__() < 2:
            bslide = "0" + bslide

        results += bslide

        for i in self.left:
            results += self.bin3bit(i)
        for r in self.board:
            for i in r:
                results += self.bin3bit(i)
        for i in self.right:
            results += self.bin3bit(i)

        return int(results, 2)

    def integer_to_puzzle(self, num):
        bnum = bin(num)[2:]
        while bnum.__len__() < 57:
            bnum = "0" + bnum
        if int(bnum[:1], 2) == 0:
            self.left_up = False
        else:
            self.left_up = True

        self.slide = int(bnum[])