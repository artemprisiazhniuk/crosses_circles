import math


class Game:
    def __init__(self, n, k, mode):
        self.field = [[0] * n for _ in range(n)]
        self.n = n
        self.k = k
        self.mode = mode
        self.player = 2
        self.counter = 0
        self.human = 2
        self.computer = 1

    def initialize_players(self, human, computer):
        self.human = human
        self.computer = computer

    def swap_player(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def swap_roles(self):
        if self.mode == 2:
            self.human = 3 - self.human
            self.computer = 3 - self.computer

    def make_turn(self, x, y):
        if self.field[x][y] != 0:
            print('Cell already filled. Try choosing another cell')
            return False
        self.field[x][y] = self.player
        return True

    def display(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.field[i][j] == 0:
                    print('.', end=' ')
                elif self.field[i][j] == 1:
                    print('x', end=' ')
                else:
                    print('o', end=' ')
            print()
        print()

    def compute(self, board, player, depth=0):
        if depth > self.n:
            return [(len(board)//2, len(board)//2), 0]
        win = self.win_check(board, self.human)
        if win:
            if win == 2:
                return [(len(board)//2, len(board)//2), 0]
            return [(len(board)//2, len(board)//2), -10]
        elif self.win_check(board, self.computer):
            return [(len(board)//2, len(board)//2), 10]

        moves = []
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != 0:
                    continue
                move = [(i, j), 0]
                board[i][j] = player
                result = self.compute(board, 3 - player, depth+1)
                move[1] = result[1]
                board[i][j] = 0
                moves.append(move)

        best_move = 0
        if player == self.computer:
            best_score = -math.inf
            for i in range(len(moves)):
                if moves[i][1] > best_score:
                    best_score = moves[i][1]
                    best_move = i
        else:
            best_score = math.inf
            for i in range(len(moves)):
                if moves[i][1] < best_score:
                    best_score = moves[i][1]
                    best_move = i

        return moves[best_move]

    def win_check(self, board, player):
        # [up, right, diagr, diagl]
        res = [0, 0, 0, 0]
        table = [[0, 0, 0, 0] * self.n for _ in range(self.n)]
        counter = 0
        for i in range(0, self.n):
            for j in range(self.n-1, -1, -1):
                if board[i][j] == player:
                    table[i][4*j] = 1
                    table[i][4*j+1] = 1
                    table[i][4*j+2] = 1
                    if i-1 > -1:
                        if board[i-1][j] == player:
                            table[i][4*j] += table[i-1][4*j]
                            res[0] = max(res[0], table[i][4 * j])
                    if j+1 < len(board):
                        if board[i][j+1] == player:
                            table[i][4*j+1] += table[i][4*(j+1)+1]
                            res[1] = max(res[1], table[i][4 * j + 1])
                    if i-1 > -1 and j+1 < len(board):
                        if board[i-1][j+1] == player:
                            table[i][4*j+2] += table[i-1][4*(j+1)+2]
                            res[2] = max(res[2], table[i][4 * j + 2])
                    if i-1 > -1 and j-1 > -1 < len(board):
                        if board[i-1][j-1] == player:
                            table[i][4*j+3] += table[i-1][4*(j-1)+3]
                            res[3] = max(res[3], table[i][4 * j + 3])
                if board[i][j] != 0:
                    counter += 1

                if max(res) >= self.k:
                    return 1
                elif counter == len(board) * len(board):
                    return 2
        return 0
