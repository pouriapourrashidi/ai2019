import random

SIZE = 4

UP = "w"
DOWN = "s"
LEFT = "a"
RIGHT = "d"

class Game:
    def __init__(self):
        self.board = [0]*SIZE

    def initialize_board(self):
        for idx, row in enumerate(self.board):
            self.board[idx] = [0]*SIZE
        radif = random.randint(0,SIZE-1)
        soton = random.randint(0,SIZE-1)

        self.board[radif][soton] = 2

    def count_empty_cells(self, board):
        count = 0
        for row in board:
            for val in row:
                if val < 2:
                    count += 1
        return count
    def print_board(self, board):
        print "**************************"
        for row in board:
            for val in row:
                if val > 0:
                    print "%d\t"%val,
                else:
                    print " \t",
            print "\n",

    def get_possible_cells(self, board):
        araye = []
        for radif, row in enumerate(board):
            for soton, val in enumerate(row):
                if val < 2:
                    poss = (radif, soton)
                    araye.append(poss)

        return araye

    def make_computer_move(self, board, cell, value):
        board_Jadid = [0]*SIZE
        for idx, row in enumerate(board_Jadid):
            board_Jadid[idx] = [0]*SIZE

        for radif, row in enumerate(board):
            for soton, val in enumerate(row):
                board_Jadid[radif][soton] = board[radif][soton]

        board_Jadid[cell[0]][cell[1]] = value

        return board_Jadid

    def transpose(self,board):
        board_Jadid = [0]*SIZE
        for idx, row in enumerate(board_Jadid):
            board_Jadid[idx] = [0]*SIZE

        for radif, row in enumerate(board):
            for soton, val in enumerate(row):
                board_Jadid[soton][radif] = board[radif][soton]

        return board_Jadid

    def reverse(self,board):
        board_Jadid = [0]*SIZE
        for idx, row in enumerate(board_Jadid):
            board_Jadid[idx] = [0]*SIZE

        for radif, row in enumerate(board):
            for soton, val in enumerate(row):
                board_Jadid[radif][SIZE - soton - 1] = board[radif][soton]

        return board_Jadid

    def merge_left(self,board):
        board_Jadid = [0]*SIZE
        for idx, row in enumerate(board_Jadid):
            board_Jadid[idx] = [0]*SIZE

        for radif, row in enumerate(board):
            for soton, val in enumerate(row):
                if val < 2:
                    continue
                if soton + 1 < SIZE:
                    if board[radif][soton+1] == val:
                        board_Jadid[radif][soton] = board[radif][soton] + board[radif][soton+1]
                        board[radif][soton+1] = 0
                    else:
                        board_Jadid[radif][soton] = board[radif][soton]
                else:
                    board_Jadid[radif][soton] = board[radif][soton]
        return board_Jadid

    def compress_left(self,board):
        board_Jadid = [0]*SIZE
        for idx, row in enumerate(board_Jadid):
            board_Jadid[idx] = [0]*SIZE

        for radif, row in enumerate(board):
            new_col = 0
            for soton, val in enumerate(row):
                if val >= 2:
                    board_Jadid[radif][new_col] = val
                    new_col += 1

        return board_Jadid

    def get_board_key(self, board):
        #self.score = self.calculate_board_score(board)
        return ';'.join([' '.join([str(num) for num in row]) for row in board])
    def player_turn(self, direction, board):

        old_key = self.get_board_key(board)
        if direction == LEFT:
            board_Jadid = self.compress_left(board)
            board_Jadid = self.merge_left(board_Jadid)
            board_Jadid = self.compress_left(board_Jadid)
        elif direction == UP:
            board_Jadid = self.transpose(board)
            board_Jadid = self.compress_left(board_Jadid)
            board_Jadid = self.merge_left(board_Jadid)
            board_Jadid = self.transpose(self.compress_left(board_Jadid))
        elif direction == DOWN:
            board_Jadid = self.transpose(board)
            board_Jadid = self.reverse(board_Jadid)
            board_Jadid = self.compress_left(board_Jadid)
            board_Jadid = self.merge_left(board_Jadid)
            board_Jadid = self.transpose(self.reverse(self.compress_left(board_Jadid)))
        elif direction == RIGHT:
            board_Jadid = self.reverse(board)
            board_Jadid = self.compress_left(board_Jadid)
            board_Jadid = self.merge_left(board_Jadid)
            board_Jadid = self.reverse(self.compress_left(board_Jadid))
        new_key = self.get_board_key(board_Jadid)

        if new_key != old_key:
            return board_Jadid
        else:
            return None

    def computer_turn(self, board):

        board_Jadid = [0]*SIZE
        for idx, row in enumerate(board_Jadid):
            board_Jadid[idx] = [0]*SIZE
        for radif, row in enumerate(board):
            for soton, val in enumerate(row):
                board_Jadid[radif][soton] = board[radif][soton]

        araye = self.get_possible_cells(board)
        possible_values = [2,4]

        chosen_cell_idx = random.randint(0,len(araye) - 1)
        chosen_val_idx = random.randint(0,len(possible_values) - 1)

        chosen_cell = araye[chosen_cell_idx]
        chosen_value = possible_values[chosen_val_idx]

        board_Jadid[chosen_cell[0]][chosen_cell[1]] = chosen_value

        return board_Jadid

def main():
    new_game = Game()
    new_game.initialize_board()
    while(True):
        board_Jadid = new_game.computer_turn(new_game.board)
        new_game.board = board_Jadid
        new_game.print_board(new_game.board)
        x = raw_input("Enter a direction: ")
        board_Jadid = new_game.player_turn(x, new_game.board)
        new_game.board = board_Jadid
        print "**************************"

if __name__ == "__main__":
    main()