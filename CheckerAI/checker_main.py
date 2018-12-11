
"""
Oct. 2018
Written by Le Zhang for ComS 572 Lab2
Run:
    python checker_main.py

"""


try:
    # for Python2
    import Tkinter as tk   ## notice capitalized T in Tkinter
except ImportError:
    # for Python3
    import tkinter as tk

import checker_game as ab
import time

PIECE_SIZE = 10

click_x = 0
click_y = 0


person_flag = 1
game_over = False
piece_color = "black"

game = None

init_board = []

# event monitoring
def coorBack(event):
    global click_x, click_y
    click_x = event.x
    click_y = event.y
    coorJudge()

def pushMessage():
    if game.winner == 'r':
        var1.set("Red Win!")
    elif game.winner == 'b':
        var1.set("Black Win!")
    var2.set("Game Over")

def judge():
    global game_over
    if game_over:
        pushMessage()

# place piece logic
def coorJudge():
    global game_over
    if game_over:
        return

    global click_x, click_y
    moves = game.moveList
    valid_pos = game.getValidPos()

    item = canvas.find_closest(click_x, click_y)
    tags_tuple = canvas.gettags(item)
    sel_tags = canvas.gettags(canvas.find_withtag("select"))

    if len(tags_tuple) > 2 and len(tags_tuple[1]) == 8 and str(tags_tuple[1]).startswith('piece'):
        sel_x = int(tags_tuple[1][5])
        sel_y = int(tags_tuple[1][6])
        color = str(tags_tuple[1][7])
        if color == game.player and (sel_x, sel_y) in valid_pos:
            if tags_tuple[2] == 'king':
                king = 'king'
            else:
                king = 'no'
            canvas.delete("select")
            selectPiece(sel_x, sel_y, color, king)
    elif len(sel_tags) > 2:
        sel_x = int(sel_tags[1][6])
        sel_y = int(sel_tags[1][7])
        color = str(sel_tags[1][8])


        clk_x = (click_x-20)/60
        clk_y = (click_y-20)/60

        for mov in moves:
            if (sel_x, sel_y) == mov[0] and (clk_x, clk_y) == mov[1]:
                cont = game.makeMove(mov)
                canvas.delete("select")
                show_board(game.board)
                game_over = game.finish()
                judge()
                # mov_flag = True
                canvas.update()
                if game.player == 'r':
                    aiMove()

def aiMove():
    global game_over
    if game_over:
        return
    time.sleep(0.5)
    # cont = game.randMove()
    game.abMove()
    show_board(game.board)
    canvas.update()
    game_over = game.finish()
    judge()
    if game.player == 'r':
        aiMove()


# place read piece, input with center coordinates X, Y (grid number 0-7)
def placeRedPiece(x, y):
    canvas.create_oval(50+x*60-25, 50+y*60-25, 50+x*60+25, 50+y*60+25, width = 3, outline="#660000", fill = '#b20000', tags = ("piece", "piece"+str(x)+str(y)+"r"))

def placeRedPieceKing(x, y):
    canvas.create_oval(50+x*60-25, 50+y*60-25, 50+x*60+25, 50+y*60+25, width = 3, outline="#660000", fill = '#b20000', tags = ("piece", "piece"+str(x)+str(y)+"r", "king"))
    canvas.create_polygon(50+x*60+10, 50+y*60+10, 50+x*60+16, 50+y*60-10, 50+x*60+8, 50+y*60, 50+x*60, 50+y*60-10
        , 50+x*60-8, 50+y*60, 50+x*60-16, 50+y*60-10, 50+x*60-10, 50+y*60+10, width = 0, fill = '#ff9999', tags = ("piece", "piece"+str(x)+str(y)+"r", "king"))

def placeBlkPiece(x, y):
    canvas.create_oval(50+x*60-25, 50+y*60-25, 50+x*60+25, 50+y*60+25, width = 3, outline="#191919", fill = '#323232', tags = ("piece", "piece"+str(x)+str(y)+"b"))

def placeBlkPieceKing(x, y):
    canvas.create_oval(50+x*60-25, 50+y*60-25, 50+x*60+25, 50+y*60+25, width = 3, outline="#191919", fill = '#323232', tags = ("piece", "piece"+str(x)+str(y)+"b", "king"))
    canvas.create_polygon(50+x*60+10, 50+y*60+10, 50+x*60+16, 50+y*60-10, 50+x*60+8, 50+y*60, 50+x*60, 50+y*60-10
        , 50+x*60-8, 50+y*60, 50+x*60-16, 50+y*60-10, 50+x*60-10, 50+y*60+10, width = 0, fill = '#999999', tags = ("piece", "piece"+str(x)+str(y)+"b" , "king"))

def selectPiece(x, y, color, king):
    canvas.create_oval(50+x*60-25, 50+y*60-25, 50+x*60+25, 50+y*60+25, width = 3, outline="#ffff00", tags = ("select", "select"+str(x)+str(y)+color, king))

def show_board(board):
    canvas.delete("piece")
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == 1:
                placeBlkPiece(x, y)
            if board[y][x] == 2:
                placeBlkPieceKing(x, y)
            if board[y][x] == -1:
                placeRedPiece(x, y)
            if board[y][x] == -2:
                placeRedPieceKing(x, y)
    cnt_b, cnt_r = game.cntPieces()
    var.set(str(cnt_r)+"\t    "+str(cnt_b))

def resetBoard():
    new_board = []
    new_board.append([0, -1, 0, -1, 0, -1, 0, -1])
    new_board.append([-1, 0, -1, 0, -1, 0, -1, 0])
    new_board.append([0, -1, 0, -1, 0, -1, 0, -1])
    new_board.append([0, 0, 0, 0, 0, 0, 0, 0])
    new_board.append([0, 0, 0, 0, 0, 0, 0, 0])
    new_board.append([1, 0, 1, 0, 1, 0, 1, 0])
    new_board.append([0, 1, 0, 1, 0, 1, 0, 1])
    new_board.append([1, 0, 1, 0, 1, 0, 1, 0])
    return new_board

def newGame():
    global game_over, game, init_board
    game_over = False
    var1.set("")
    var2.set("")
    game.reset(resetBoard(), 'b', 4, -1000, 1000)
    show_board(game.board)



"""main window"""
root = tk.Tk()

root.title("Checkers")
root.geometry("760x525")

# """pieces count board"""
side_canvas = tk.Canvas(root, width = 220, height = 70)
side_canvas.grid(row = 0, column = 1)
side_canvas.create_oval(30, 10, 80, 60, width = 3, outline="#660000", fill = '#b20000', tags = ("show_piece"))
side_canvas.create_oval(140, 10, 190, 60, width = 3, outline="#191919", fill = '#323232', tags = ("show_piece"))


# """piece count"""
var = tk.StringVar()
var.set("")
person_label = tk.Label(root, textvariable = var, width = 12, anchor = tk.CENTER,
                        font = ("Arial", 20) )
person_label.grid(row = 1, column = 1)

#
"""win-lose board"""
var1 = tk.StringVar()
var1.set("")
result_label = tk.Label(root, textvariable = var1, width = 12, height = 4,
                        anchor = tk.CENTER, fg = "red", font = ("Arial", 25) )
result_label.grid(row = 2, column = 1, rowspan = 2)

"""game over board"""
var2 = tk.StringVar()
var2.set("")
game_label = tk.Label(root, textvariable = var2, width = 12, height = 4,
                        anchor = tk.CENTER, font = ("Arial", 18) )
game_label.grid(row = 4, column = 1)


reset_button = tk.Button(root, text = "Restart", font = 20,
                          width = 8, command = newGame)
reset_button.grid(row = 5, column = 1)


"""draw board"""
# background
canvas = tk.Canvas(root, bg = "saddlebrown", width = 520, height = 520)
canvas.bind("<Button-1>", coorBack)  #click event
canvas.grid(row = 0, column = 0, rowspan = 6)

# fill
for i in range(4):
    for j in range(8):
        if j%2 >0:
            shift = 60
        else:
            shift = 0
        canvas.create_rectangle(shift+20+i*120, 20+j*60, shift+80+i*120, 80+j*60, outline="#000", fill="#fb0")

#lines
for i in range(9):
    canvas.create_line(20, (60 * i + 20), 500, (60 * i + 20))
    canvas.create_line((60 * i + 20), 20, (60 * i + 20), 500)


board = []
board.append([0, -1, 0, -1, 0, -1, 0, -1])
board.append([-1, 0, -1, 0, -1, 0, -1, 0])
board.append([0, -1, 0, -1, 0, -1, 0, -1])
board.append([0, 0, 0, 0, 0, 0, 0, 0])
board.append([0, 0, 0, 0, 0, 0, 0, 0])
board.append([1, 0, 1, 0, 1, 0, 1, 0])
board.append([0, 1, 0, 1, 0, 1, 0, 1])
board.append([1, 0, 1, 0, 1, 0, 1, 0])
#
# board.append([0, 0, 0, -1, 0, 0, 0, 0])
# board.append([0, 0, -1, 0, -1, 0, 0, 0])
# board.append([0, 0, 0, -1, 0, 1, 0, 0])
# board.append([0, 0, 0, 0, 0, 0, 0, 0])
# board.append([0, 0, 0, 1, 0, 2, 0, 0])
# board.append([0, 0, 1, 0, 0, 0, 0, 0])
# board.append([0, 0, 0, 0, 0, 0, 0, 0])
# board.append([0, 0, 0, 0, 0, 0, 0, 0])

init_board = board

game = ab.Game(init_board, 'b', 4, -1000, 1000)

show_board(game.board)

"""show main window"""
root.mainloop()
