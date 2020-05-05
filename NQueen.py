import sys
import pygame
from pygame.sprite import Sprite


class MyRectangle(Sprite):
    def __init__(self, screen, x, y, width=100, height=100, color=(0, 0, 0)):
        super(MyRectangle, self).__init__()
        self.screen = screen
        self.__width = width
        self.__height = height
        self.__rect = pygame.Rect(0, 0, self.__width, self.__height)
        self.__rect.y = y * height
        self.__rect.x = x * width
        self.__color = color

    def blit_me(self):
        pygame.draw.rect(self.screen, self.__color, self.__rect)


class Board:
    def __init__(self, n):
        self.n = n
        self.__board = [[0 for x in range(self.n)] for y in range(self.n)]
        self.__points = []
        self.__rectangles = []
        self.__prepare_board()
        self.__prepare_rectangles()

    def __prepare_board(self):
        flag = True
        for x in range(len(self.__board)):
            for y in range(len(self.__board[x])):
                if flag:
                    if y % 2 == 0:
                        self.__board[x][y] = 1
                        self.__points.append((x, y))
                else:
                    if y % 2 == 1:
                        self.__board[x][y] = 1
                        self.__points.append((x, y))
            flag = not flag

    def __prepare_rectangles(self):
        for x in self.__points:
            TMP = MyRectangle(screen, x[0], x[1], int((800/self.n)), int((800/self.n)))
            self.__rectangles.append(TMP)

    def display_screen(self):
        for x in self.__rectangles:
            x.blit_me()


class Queen:
    def __init__(self, screen, q, n):
        self.screen = screen
        self.__queens = q
        self.__n = n
        self.__points = []
        self.__prepare()

    def __prepare(self):
        for z in range(len(self.__queens)):
            for x in range(len(self.__queens[z])):
                for y in range(len(self.__queens[x])):
                    if self.__queens[x][y]:
                        self.__points.append((x, y))

    def display_queens(self):
        for x in range(len(self.__points)):
            tmp = MyRectangle(screen, self.__points[x][0], self.__points[x][1], int(800/self.__n), int(800/self.__n),
                              (255, 0, 0))
            tmp.blit_me()


class Solve:
    def __init__(self, size):
        self.n = size
        self.board = [[0 for x in range(self.n)] for y in range(self.n)]

    def solve(self):
        self.__n_het(0, self.n)

    def __check(self, y, x):
        for i in range(0, y):
            if self.board[i][x]:
                return False
        for i, j in zip(range(y, -1, -1), range(x, -1, -1)):
            if self.board[i][j]:
                return False
        for i, j in zip(range(y, -1, -1), range(x, self.n)):
            if self.board[i][j]:
                return False
        return True

    def __n_het(self, y, n):
        if y == n:
            return True
        for x in range(n):
            if self.__check(y, x):
                self.board[y][x] = 1
                if self.__n_het(y+1, n):
                    return True
                self.board[y][x] = 0

        return False


class Facade:
    def __init__(self, screen, size):
        self.solve = Solve(size)
        self.solve.solve()
        self.board = Board(size)
        self.solution = self.solve.board
        self.queens = Queen(screen, self.solution, size)

    def display(self):
        self.board.display_screen()
        self.queens.display_queens()


class User:
    def __init__(self, number=4,):
        self.size = number

    def give_me_size(self):
        while True:
            self.size = int(input("Give me size of board from 4 to 16 (to quit press 1)"))
            if self.size in range(4, 17):
                break
            elif self.size == 1:
                sys.exit()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


if __name__ == '__main__':
    pygame.init()
    info = "This is simple solution of N Queen problem. Queens has got red color."
    U = User()
    print(info)
    U.give_me_size()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("NxN Queen")
    bg_color = (255, 255, 255)
    facade = Facade(screen, U.size)
    while True:
        screen.fill(bg_color)
        U.check_events()
        facade.display()
        pygame.display.flip()


