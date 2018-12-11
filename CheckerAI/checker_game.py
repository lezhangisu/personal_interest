from random import shuffle
import copy

class Game:
    newBoard = [[ 0, -1,  0, -1,  0, -1,  0, -1],
                [-1,  0, -1,  0, -1,  0, -1,  0],
                [ 0, -1,  0, -1,  0, -1,  0, -1],
                [ 0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0],
                [1, 0, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0]]

    def __init__(self, board, player, depth, alpha, beta):
        self.board = copy.deepcopy(board)
        self.player = player # player 'b' is player, 'r' is AI
        self.depth = depth

        self.moveList = self.getMoveList()
        # self.availablePieceList = self.get_piece_list()

        self.alpha = alpha
        self.beta = beta

        self.winner = "";

    def reset(self, board, player, depth, alpha, beta):
        self.board = board
        self.player = player # player 'b' is player, 'r' is AI
        self.depth = depth

        self.moveList = self.getMoveList()

        self.alpha = alpha
        self.beta = beta

        self.winner = "";

    def switchSide(self):
        if self.player == 'b':
            self.player = 'r'
        elif self.player == 'r':
            self.player = 'b'

    def cntPieces(self):
        cnt_b = 0
        cnt_r = 0
        for row in self.board:
            for pos in row:
                if pos < 0:
                    cnt_r += 1
                elif pos > 0:
                    cnt_b += 1
        return cnt_b, cnt_r

    def finish(self):
        if len(self.moveList) < 1:
            self.switchSide()
            self.winner = self.player
            return True

        cnt_b, cnt_r = self.cntPieces()
        if cnt_b == 0:
            self.winner = 'r'
            return True
        elif cnt_r == 0:
            self.winner = 'b'
            return True
        return False

    def evaluate(self):
        cnt_b = 0
        cnt_r = 0
        for row in self.board:
            for pos in row:
                if pos < 0:
                    cnt_r -= pos
                elif pos > 0:
                    cnt_b += pos
        # cnt_b, cnt_r = self.cntPieces()
        return cnt_r - cnt_b

    def getMoveList(self):

        list_ = [] # [(from_coordinates, to_coordinates, possible_killed_piece_coordinates),...]

        if self.player == 'r': # AI move predictions
            for y in xrange(len(self.board)):
                for x in xrange(len(self.board[y])):
                    if self.board[y][x] <0:
                        if x-1 >= 0 and y+1 < 8:
                            if self.board[y+1][x-1] == 0: # basic move
                                list_.append(((x,y),(x-1, y+1)))
                            elif self.board[y+1][x-1] > 0: # kill move
                                if x-2 >= 0 and y+2 < 8 and self.board[y+2][x-2] == 0:
                                    list_.append(((x,y), (x-2, y+2), (x-1, y+1)))

                        if x+1 < 8 and y+1 < 8:
                            if self.board[y+1][x+1] == 0: # basic move
                                list_.append(((x,y),(x+1, y+1)))
                            elif self.board[y+1][x+1] > 0: # kill move
                                if x+2 < 8 and y+2 < 8 and self.board[y+2][x+2] == 0:
                                    list_.append(((x,y), (x+2, y+2), (x+1, y+1)))

                    if self.board[y][x] < -1:
                        if x-1 >= 0 and y-1 >= 0:
                            if self.board[y-1][x-1] == 0: # basic move
                                list_.append(((x,y),(x-1, y-1)))
                            elif self.board[y-1][x-1] > 0: # kill move
                                if x-2 >= 0 and y-2 >= 0 and self.board[y-2][x-2] == 0:
                                    list_.append(((x,y), (x-2, y-2), (x-1, y-1)))

                        if x+1 < 8 and y-1 >=0:
                            if self.board[y-1][x+1] == 0: # basic move
                                list_.append(((x,y),(x+1, y-1)))
                            elif self.board[y-1][x+1] > 0: # kill move
                                if x+2 < 8 and y-2 >= 0 and self.board[y-2][x+2] == 0:
                                    list_.append(((x,y), (x+2, y-2), (x+1, y-1)))

        else: # player move predictions
            for y in xrange(len(self.board)):
                for x in xrange(len(self.board[y])):
                    if self.board[y][x] > 0:
                        if x-1 >= 0 and y-1 >= 0:
                            if self.board[y-1][x-1] == 0: # basic move
                                list_.append(((x,y),(x-1, y-1)))
                            elif self.board[y-1][x-1] < 0: # kill move
                                if x-2 >= 0 and y-2 >=0 and self.board[y-2][x-2] == 0:
                                    list_.append(((x,y), (x-2, y-2), (x-1, y-1)))

                        if x+1 < 8 and y-1 >= 0:
                            if self.board[y-1][x+1] == 0: # basic move
                                list_.append(((x,y),(x+1, y-1)))
                            elif self.board[y-1][x+1] < 0: # kill move
                                if x+2 < 8 and y-2 >= 0 and self.board[y-2][x+2] == 0:
                                    list_.append(((x,y), (x+2, y-2), (x+1, y-1)))

                    if self.board[y][x] > 1:
                        if x-1 >= 0 and y+1 < 8:
                            if self.board[y+1][x-1] == 0: # basic move
                                list_.append(((x,y),(x-1, y+1)))
                            elif self.board[y+1][x-1] < 0: # kill move
                                if x-2 >= 0 and y+2 < 8 and self.board[y+2][x-2] == 0:
                                    list_.append(((x,y), (x-2, y+2), (x-1, y+1)))

                        if x+1 < 8 and y+1 < 8:
                            if self.board[y+1][x+1] == 0: # basic move
                                list_.append(((x,y),(x+1, y+1)))
                            elif self.board[y+1][x+1] < 0: # kill move
                                if x+2 < 8 and y+2 < 8 and self.board[y+2][x+2] == 0:
                                    list_.append(((x,y), (x+2, y+2), (x+1, y+1)))

            # print ""
        jump_list = []
        for mov in list_:
            if len(mov) > 2:
                jump_list.append(mov)
        if len(jump_list) > 0:
            shuffle(jump_list)
            return jump_list
        shuffle(list_) # shuffle to eliminate impact of order
        return list_

    def updateBoard(self, mov):
        piece = self.board[mov[0][1]][mov[0][0]]
        self.board[mov[0][1]][mov[0][0]] = 0

        if piece == 1 and mov[1][1] < 1:
            self.board[mov[1][1]][mov[1][0]] = 2
        elif piece == -1 and mov[1][1] > 6:
            self.board[mov[1][1]][mov[1][0]] = -2
        else:
            self.board[mov[1][1]][mov[1][0]] = piece

        if len(mov) > 2:
            self.board[mov[2][1]][mov[2][0]] = 0
            l = self.getMoveList()
            ret = []
            if len(l) > 0 and len(l[0]) > 2: # when jumped, if next move is a jump
                for m in l:
                    if m[0] == mov[1]: # if next jump is the same piece
                        ret.append(m)
                if ret:
                    return ret
        # switch player
        self.switchSide()
        return self.getMoveList()

    def makeMove(self, mov):
        if mov in self.moveList:
            self.moveList = self.updateBoard(mov)
            return True
        return False

    def alphaBeta(self):
        if self.depth == 0:
            return self.evaluate(), 0

        index = 0
        if self.player == "r": # max value

            for i, mov in enumerate(self.moveList):
                childGame = Game(self.board, self.player, self.depth-1, self.alpha, self.beta)
                childGame.makeMove(mov)
                score, ind = childGame.alphaBeta()

                if score > self.alpha:
                    self.alpha = score
                    index = i

            return self.alpha, index

        else: # min value

            for i, mov in enumerate(self.moveList):
                childGame = Game(self.board, self.player, self.depth-1, self.alpha, self.beta)
                childGame.makeMove(mov)
                childGame.moveList = self.moveList
                score, ind = childGame.alphaBeta()

                if score < self.beta:
                    self.beta = score
                    index = i

            return self.beta, index

    def abMove(self):
        score, index = self.alphaBeta()

        self.makeMove(self.moveList[index])

    def getValidPos(self):
        valid_pos = []
        for mov in self.moveList:
            valid_pos.append(mov[0])
        return valid_pos

    def ab2(self):
        if self.depth == 0:
            return self.evaluate()

    def randMove(self):
        self.makeMove(self.moveList[0])
        return

    def printBoard(self):
        for row in self.board:
            for c in row:
                print str(c)+'\t',
            print '\n'

#
