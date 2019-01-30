import time
SIZE = 4
class node_maker:

    def __init__(self):
        self.action = None
        self.type = "max"
        self.score = 0
        self.children = []
        self.node_key = ""
        self.parent = None
        self.depth = 0



    def set_board_key(self, board):
        self.node_key = ';'.join([' '.join([str(num) for num in row]) for row in board])

    def get_board(self):
        return [[int(num) for num in row.split()] for row in self.node_key.split(';')]

    def print_node(self):
        # print self.node_key,
        if self.action:
            print str(self.score)+ " " + self.action
        else:
            print str(self.score)

    def print_tree(self):
        print "Level:%d"%self.depth,
        time.sleep(1)
        for i in range(self.depth):
            print "\t",
        self.print_node()
        print "\n",
        for child in self.children:
            child.print_tree()

    def get_empty_cells(self, board):
        count = 0
        for row in board:
            for col in row:
                if col < 2:
                    count += 1

        return count
    def score_simple_snake(self,board):
        if board[0][0] == (board[0][1]*2) and board[0][1] == (board[0][2]*2) and board[0][2] == (board[0][3]*2):
            return 250
        else:
            return 0
    def get_gradient_score(self, board):
        grad = [[32, 2,      2, 0.125],
                [16,  4,       1,  0.250],
                [16,  4,       1,  0.250],
                [8,  8,       0.5, 0.5]]
        grad = [[32, 16,      16, 8],
                [16,  4,       1,  0.250],
                [16,  4,       1,  0.250],
                [8,  8,       0.5, 0.5]]
        score = 0
        total = 0

        for num_radif, row in enumerate(board):
            for num_soton, val in enumerate(row):
                score += (board[num_radif][num_soton]*grad[num_radif][num_soton])
                total += board[num_radif][num_soton]

        return score/(1.0)
    def get_gradient_emptiness_score(self, board):
        grad = [[ 6,  -1,       -1, -1],
                [-1,  -1,       -1, -1],
                [-1,  -1,       -1, -1],
                [-1,  -1,       -1, -1]]
        score = 0

        for num_radif, row in enumerate(board):
            for num_soton, val in enumerate(row):
                score += (board[num_radif][num_soton]*grad[num_radif][num_soton])

        return score

    def get_double(self, board):
        smooth = 1
        max = 0
        for num_radif, row in enumerate(board):
            for num_soton, val in enumerate(row):
                if num_soton + 1 < SIZE:
                    if val == 2*board[num_radif][num_soton+1]:
                        smooth += 1
                if num_radif - 1 >= 0:
                    if val == 2*board[num_radif-1][num_soton]:
                        smooth += 1
                if num_soton - 1 >= 0:
                    if val == 2*board[num_radif][num_soton-1]:
                        smooth += 1
                if num_radif + 1 < SIZE:
                    if val == 2*board[num_radif+1][num_soton]:
                        smooth += 1


        return (smooth)/(4*1.0)

    def get_edges(self, board):
        outer = 1
        inner = 1
        for num_radif, row in enumerate(board):
            for num_soton, val in enumerate(row):
                if num_soton == 0 or num_soton == SIZE - 1 or num_radif == 0 or num_radif == SIZE - 1:
                    outer += val
                else:
                    inner += val


        return outer/(inner*1.0)


        return (smooth)/(4*1.0)
    def get_smoothness(self, board):
        smooth = 1
        max = 0
        for num_radif, row in enumerate(board):
            for num_soton, val in enumerate(row):
                if val == 0:
                    continue
                if num_soton + 1 < SIZE and (board[num_radif][num_soton+1] != 0):
                    right_delta = abs(val - board[num_radif][num_soton+1])
                    smooth += right_delta
                if num_radif - 1 >= 0 and (board[num_radif-1][num_soton] != 0):
                    up_delta = abs(val - board[num_radif-1][num_soton])
                    smooth += up_delta
                if num_soton - 1 >= 0 and (board[num_radif][num_soton-1] != 0):
                    left_delta = abs(val - board[num_radif][num_soton-1])
                    smooth += left_delta
                if num_radif + 1 < SIZE  and (board[num_radif+1][num_soton] != 0):
                    down_delta = abs(val - board[num_radif+1][num_soton])
                    smooth += down_delta
                if val > max:
                    max = val

        return (smooth)
    def get_smoothness_snake(self, board):
        smooth = 1
        max = 0
        for num_radif, row in enumerate(board):
            for num_soton, val in enumerate(row):
                if val == 0:
                    continue

                if num_radif + 1 < SIZE  and (board[num_radif+1][num_soton] != 0):
                    down_delta = abs(val - board[num_radif+1][num_soton])
                    smooth += down_delta
                if num_soton - 1 < SIZE:
                    if val > board[num_radif][num_soton-1]:
                        left_delta = abs(val - board[num_radif][num_soton-1])
                        smooth += (left_delta)
                if val > max:
                    max = val

        return (smooth) + abs(board[SIZE-1][0] - board[SIZE-1][1]) + abs(board[0][1] - board[0][2]) + abs(board[SIZE-1][2] - board[SIZE-1][3])

    def get_monot(self, board):

        max_row = 0
        max_id = 0
        max = 0
        for num_radif, row in enumerate(board):
            for num_soton, val in enumerate(row):
                if val > max:
                    max = val
                    max_row = num_radif
                    max_col = num_soton
        if max_row < (SIZE/2):
            dir_rows = 1
        else:
            dir_rows = 0

        if max_col < (SIZE/2):
            dir_cols = 1
        else:
            dir_cols = 0

        monot_rows = [4]*SIZE
        monot_cols = [4]*SIZE
        for num_radif, row in enumerate(board):
            for num_soton, val in enumerate(row):

                if num_radif - 1 >= 0 :
                    if dir_rows == 1:
                        check_rows = (val > board[num_radif-1][num_soton])
                    else:
                        check_rows = (val < board[num_radif-1][num_soton])

                if num_soton + 1 < SIZE :
                    if dir_cols == 1:
                        check_cols = (val < board[num_radif][num_soton+1])
                    else:
                        check_cols = (val > board[num_radif][num_soton+1])

                if num_soton + 1 < SIZE :
                    if check_cols:

                        monot_rows[num_radif] -= 1

                if num_radif - 1 >= 0 :
                    if check_rows:

                        monot_cols[num_soton] -= 1

        return (sum(monot_rows) + sum(monot_cols))/(1.0)
    def get_largest(self, board):
        max_row = 0
        max_id = 0
        max = 0
        for num_radif, row in enumerate(board):
            for num_soton, val in enumerate(row):
                if val > max:
                    max = val
                    max_row = num_radif
                    max_col = num_soton

        return max
        if (max_row != 0) or (max_col != 0):
            return 10000
        else:
            return 0

        return max, sum/(1.0*total)
    def get_large_nums(self, board):
        sum = 0
        total = 0
        max = 0
        for num_radif, row in enumerate(board):
            for num_soton, val in enumerate(row):
                if val > max:
                    max = val
                if val >= 2:
                    total += 1
                sum += val

        return max, sum/(1.0*total)


    def calculate_board_score_smooth(self):
        board = self.get_board()
        grad_score = self.get_smoothness_snake(board)
        empty_cell = self.get_empty_cells(board)

        monot_factor = self.get_monot(board)
        largest = self.get_largest(board)
        score = self.get_gradient_score(board)
        penalty = 0
        if largest != board[0][0]:
            penalty = 5*largest
        #penalty = 0
        #if empty_cell < 6:
        #    penalty = 100

        return   score - (largest*grad_score/10.0) + (largest*empty_cell) + (largest*largest)# - penalty# - grad_score + monot_factor + largest

    # def calculate_board_score_emptiness(self):
    #     board = self.get_board()
    #
    #     #grad_factor = self.get_gradient_score(board)
    #     #grad_emptiness = self.get_gradient_emptiness_score(board)
    #     #snake_factor = self.score_simple_snake(board)
    #     empty_cell = self.get_empty_cells(board)
    #     #smooth_factor = self.get_smoothness(board)
    #     #max_factor, sum_factor = self.get_large_nums(board)
    #     #double_factor = self.get_double(board)
    #     #edges = self.get_edges(board)
    #     #smooth_weight = 1
    #     #emptiness_weight = 1
    #
    #     #penalty = 0
    #     #if empty_cell < 1:
    #     #    penalty = 50000
    #     #if empty_cell != 0:
    #     #    ratio = smooth_factor/(-1.0*empty_cell)
    #     #    if empty_cell < 12:
    #     #        emptiness_weight = 16-empty_cell
    #     #        smooth_weight = 5
    #     #else:
    #     #    emptiness_weight = 16
    #     #    smooth_weight = 10
    #
    #
    #     #print "grad: ",
    #     #print grad_factor
    #     #print "snake: ",
    #     #print snake_factor
    #     #print "cells: ",
    #     #print empty_cell
    #     #print "*******"
    #
    #     return  empty_cell