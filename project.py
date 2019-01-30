
from game import Game
from node import node_maker
import time

UP = "w"
DOWN = "s"
LEFT = "a"
RIGHT = "d"

class MiniMaxSolver:

    def __init__(self, target):

        self.max_depth = 3
        self.root = node_maker()
        self.hist_states = dict()
        self.target = target

    def build_tree(self, game):
        PLAYER = 0
        CPU = 1

        poshte = []

        root = node_maker()
        root.set_board_key(game.board)
        self.hist_states[root.node_key] = True

        curr_level = 0
        curr_turn = PLAYER

        poshte.append(root)

        while True:
            if len(poshte) == 0:
                return None
            node_baresi = poshte.pop(0)
            #print node_baresi.depth
            if node_baresi.depth > self.max_depth:
                break

            board_baresi = node_baresi.get_board()
            if node_baresi.type == "min":
                poss = game.get_possible_cells(board_baresi)
                for cell in poss:
                    for val in [2,4]:
                        new_board = game.make_computer_move(board_baresi,cell,val)
                        new_node = node_maker()
                        new_node.set_board_key(new_board)

                        new_node.type = "max"
                        new_node.depth = node_baresi.depth + 1
                        node_baresi.children.append(new_node)
                        new_node.parent = node_baresi
                        self.hist_states[new_node.node_key] = True
                        new_node.action=str(val)
                        # print 'make a new node with '+str(new_node.action)
                poshte.extend(node_baresi.children)
            else:
                new_board_left = game.player_turn(LEFT, board_baresi)
                new_board_right = game.player_turn(RIGHT, board_baresi)
                new_board_up = game.player_turn(UP, board_baresi)
                new_board_down = game.player_turn(DOWN, board_baresi)

                poss = [new_board_left, new_board_right, new_board_up, new_board_down]
                actions = [LEFT, RIGHT, UP, DOWN]
                for new_board, action in zip(poss, actions):
                    if new_board == None:
                        continue
                    new_node = node_maker()
                    new_node.set_board_key(new_board)
                    new_node.action = action

                    new_node.type = "min"
                    new_node.depth = node_baresi.depth + 1
                    node_baresi.children.append(new_node)
                    new_node.parent = node_baresi
                    self.hist_states[new_node.node_key] = True
                poshte.extend(node_baresi.children)
        return root

    def perform_minimax_update(self, tree):
        if len(tree.children) == 0:
            if self.target == "smooth":
                return tree.calculate_board_score_smooth()
            elif self.target == "emptiness":
                return tree.calculate_board_score_emptiness()


        if tree.type == "max":
            max = -100000000
            for farzand in tree.children:
                farzand.score = self.perform_minimax_update(farzand)
                # print (farzand.depth*3*' ')+' min ' + str(farzand.action)+' ' + str(farzand.score)+' '+str(farzand.depth)
                # time.sleep(1)
                if farzand.score > max:
                    max = farzand.score
                    tree.action = farzand.action
            tree.score = max
            return tree.score
        else:
            min = 500000
            for farzand in tree.children:
                farzand.score = self.perform_minimax_update(farzand)
                # print (farzand.depth*3*' ')+' max ' + str(farzand.action)+'  ' + str(farzand.score)+' '+str(farzand.depth)
                # time.sleep(1)
                if farzand.score < min:
                    min = farzand.score
            tree.score = min
            return tree.score

    def update_scores(self, tree):
        self.perform_minimax_update(tree)

        return tree


    def run_minimax(self, game):
        max_nodes = None


def main():
    game = Game()
    game.initialize_board()
    game.board = game.computer_turn(game.board)
    target = "smooth"
    allowed_moves = -1
    game.print_board(game.board)
    while True:
        minimax_sol = MiniMaxSolver(target)
        minimax_sol.max_depth = 3

        #print "building tree..."
        tree = minimax_sol.build_tree(game)
        if tree == None:
            break
        #print "updating tree..."
        tree = minimax_sol.update_scores(tree)
        # tree.print_tree()
        # time.sleep(3)

        new_action = tree.action
        print tree.score
        new_move = game.player_turn(new_action, game.board)
        game.board = new_move
        game.board = game.computer_turn(game.board)
        game.print_board(game.board)
        allowed_moves -= 1

        if allowed_moves == 0:

            if target == "smooth":
                target = "smooth"
                allowed_moves = 9*5
    game.print_board(game.board)

if __name__ == "__main__":
    runs = 20

    for i in range(runs):
        main()
        input2 = raw_input()
        if(input2!=''):
            break