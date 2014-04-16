#Kairavi Chahal
#kchahal@andrew.cmu.edu

from Tkinter import *

def unflipPieces():
	board = canvas.data.board
	lastPiecesFlipped = canvas.data.lastPiecesFlipped
	for (row, col) in lastPiecesFlipped:
		flipPiece(board, row, col)

def undoMove():
	if (canvas.data.undoCount <=1):
		row = canvas.data.lastRow
		col = canvas.data.lastCol
		board = canvas.data.board
		board[row][col] = None
		canvas.data.player = canvas.data.lastPlayer
		unflipPieces()
		redrawAll()
	else:
		drawError("Cannot undo more than once.")

def instructions():
	canvas.data.instructions = True
	canvasWidth = canvas.data.canvasWidth
	canvasHeight = canvas.data.canvasHeight
	canvas.create_rectangle(15, 50, canvasWidth-15, canvasHeight-50, fill="#029743")
	canvas.create_text(canvasWidth/2, canvasHeight/5+10, text="HOW TO PLAY", font=("Times New Roman", 32, "bold"))
	canvas.create_text(canvasWidth/2, canvasHeight/2, text="Each player's objective is to have as many disks one's own color as possible. Click on a square to make your move. A move consists of  \"outflanking\" your opponent's discs, then flipping the outflanked discs to your color. To outflank means to place a disc on the board so that your opponent's row (or rows) of  discs are bordered at each end by a disc of your color.", font=("Arial", 12), justify="center", width=300)
	canvas.create_text(canvasWidth/2, canvasHeight/2+120, text="H for hints | Z to undo | S to skip\nR to restart | Q to quit\nClick to return to main menu.", font=("Arial", 12), justify="center", width=320)

def drawHints(validMoves):
	topMargin = canvas.data.topMargin
	margin = canvas.data.margin
	cellSize = canvas.data.cellSize
	for (row, col) in validMoves:
		left = margin + col * cellSize
		right = left + cellSize
		top = topMargin + row * cellSize
		bottom = top + cellSize
		canvas.create_rectangle(left, top, right, bottom, fill="black")
		canvas.create_rectangle(left+1, top+1, right-1, bottom-1, fill="gray")

def getHints():
	board = canvas.data.board
	validMoves = []
	for row in xrange(8):
		for col in xrange(8):
			if (board[row][col] == None):
				if (isValidMove(board, row, col) == True):
					validMoves += [(row, col)]
	if (len(validMoves) == 0):
		drawError("No more valid moves. Press S to skip.")
	else:
		drawHints(validMoves)
	canvas.data.hintMode = False

def piecesToFlip(board, row, col, xdir, ydir):
	player = canvas.data.player
	if (player == "black"):
		otherPlayer = "white"
	elif (player == "white"):
		otherPlayer = "black"
	piecesToFlip = []
	row += xdir
	col += ydir
	while ((row >= 0) and (row < 8) and (col >= 0) and (col < 8)) and (board[row][col] != player):
		if (board[row][col] == None):
			break
		if (board[row][col] == otherPlayer):
			piecesToFlip += [(row, col)]
		row += xdir
		col += ydir
	canvas.data.lastPiecesFlipped += piecesToFlip
	for (row, col) in piecesToFlip:
		flipPiece(board, row, col)

def isBoardFull():
	board = canvas.data.board
	boardFull = True
	for row in xrange(8):
		for col in xrange(8):
			if (board[row][col] == None):
				boardFull = False
	return boardFull

def searchDirection(row, col, xdir, ydir):
	board = canvas.data.board
	while ((row+xdir >= 0) and (row+xdir < 8) and (col+ydir >= 0) and (col+ydir < 8)):
		row += xdir
		col += ydir
		if (board[row][col] == None):
			return False
		elif (board[row][col] == canvas.data.player):
			return True

def isValidMove(board, row, col):
	player = canvas.data.player
	validMove = False
	if (player == "black"):
		otherPlayer = "white"
	elif (player == "white"):
		otherPlayer = "black"
	for (dx, dy) in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
		if (row+dx >= 0) and (row+dx < 8) and (col+dy >= 0) and (col+dy < 8):
			if (board[row+dx][col+dy] == otherPlayer):
				(xdir, ydir) = (dx, dy)
				if (searchDirection(row+dx, col+dy, xdir, ydir) == True):
					validMove = True
					if (canvas.data.hintMode == False):
						piecesToFlip(board, row, col, xdir, ydir)
	return validMove

def nextPlayer():
	if (canvas.data.player == "black"):
		canvas.data.player = "white"
	elif (canvas.data.player == "white"):
		canvas.data.player = "black"

def flipPiece(board, row, col):
	if (board[row][col] == "black"):
		board[row][col] = "white"
	elif (board[row][col] == "white"):
		board[row][col] = "black"
	

def winner():
	if (canvas.data.blackScore > canvas.data.whiteScore):
		canvas.data.winner = "Black wins!\nClick to restart."
	elif (canvas.data.blackScore < canvas.data.whiteScore):
		canvas.data.winner = "White wins!\nClick to restart."
	elif (canvas.data.blackScore == canvas.data.whiteScore):
		canvas.data.winner = "Tie!\nClick to restart."
			
def gameOver():
	winner()
	cx = canvas.data.canvasWidth/2
	cy = canvas.data.canvasHeight/2
	canvas.create_rectangle(cx-120, cy-50, cx+120, cy+50, fill="white", outline="black", width=3)
	canvas.create_text(cx, cy, text=canvas.data.winner, font=("Arial", 18), fill="black", justify="center", width=220)
	canvas.data.gameOver = True

def drawError(message):
	cx = canvas.data.canvasWidth/2
	canvas.create_rectangle(cx-160, 5, cx+160, 46, fill="white", outline="#9F1E0B", width=3)
	canvas.create_text(cx, 25, text=message, font=("Arial", 12), fill="#9F1E0B", justify="center", width=220)

def mousePressed(event):
	canvas = event.widget.canvas
	canvasWidth = canvas.data.canvasWidth
	canvasHeight = canvas.data.canvasHeight
	canvas.data.lastPiecesFlipped = []
	if (canvas.data.splashScreen == False) and (canvas.data.instructions == False):
		board = canvas.data.board
		player = canvas.data.player
		cellSize = canvas.data.cellSize
		topMargin = canvas.data.topMargin
		margin = canvas.data.margin
		row = (event.y - topMargin)/cellSize
		canvas.data.lastRow = row
		col = (event.x - margin)/cellSize
		canvas.data.lastCol = col
		canvas.data.lastPlayer = canvas.data.player
		if (canvas.data.gameOver == False) and (isBoardFull() == False):
			if (event.x < margin) or (event.x > (margin+cellSize*8)) or (event.y < topMargin) or (event.y > topMargin+cellSize*8):
				drawError("Please click on the board.")
			elif (board[row][col] != None):
				drawError("You cannot place a piece on another piece.")
			elif (isValidMove(board, row, col) == False):
				drawError("That is not a valid move.")
			else:
				board[row][col] = player
				nextPlayer()
				canvas.data.undoCount = 0
				redrawAll()
		elif (canvas.data.gameOver == True):
			init()
	elif (canvas.data.splashScreen == True):
		if (event.x > canvasWidth/2-80) and (event.y > canvasHeight/4+80) and (event.x < canvasWidth/2+80) and (event.y < canvasHeight/4+120):
			canvas.data.splashScreen = False
			init()
		elif (event.x > canvasWidth/2-80) and (event.y > canvasHeight/4+140) and (event.x < canvasWidth/2+80) and (event.y < canvasHeight/4+180):
			canvas.data.splashScreen = False
			instructions()
	elif (canvas.data.instructions == True):
		canvas.data.instructions = False
		splashScreen()

def keyPressed(event):
	canvas = event.widget.canvas
	if (canvas.data.splashScreen == False) and (canvas.data.instructions == False):
		if (event.char == "q"):
			gameOver()
			splashScreen()
		elif (event.char == "r"):
			init()
		elif (event.char == "h"):
			canvas.data.hintMode = True
			getHints()
		elif (event.char == "z"):
			canvas.data.undoCount += 1
			undoMove()
		elif (event.char == "s"):
			nextPlayer()
			redrawAll()
		#elif (event.char == "p"):
			#can be used for debugging
	elif (canvas.data.splashScreen == True):
		if (event.char == "i"):
			canvas.data.splashScreen = False
			instructions()
		elif (event.keysym == "space"):
			canvas.data.splashScreen = False
			init()
	elif (canvas.data.instructions == True):
		if (event.char == "b"):
			canvas.data.instructions = False
			splashScreen()

def drawPlayerTurn():
	cx = canvas.data.canvasWidth/2
	cy = canvas.data.canvasHeight - canvas.data.topMargin/2 + 5
	if (canvas.data.player == "black"):
			canvas.create_text(cx, cy, text="Black's turn", font=("Helvetica", 32))
	elif (canvas.data.player == "white"):
			canvas.create_text(cx, cy, text="White's turn", font=("Helvetica", 32))

def drawScore():
	blackScore = canvas.data.blackScore
	whiteScore = canvas.data.whiteScore
	cx = canvas.data.canvasWidth/2
	cy = canvas.data.topMargin/2 + 10
	canvas.create_text(cx, cy, text="Black: %d\t\tWhite: %d" % (blackScore, whiteScore), font=("Helvetica", 18))

def getScore():
	board = canvas.data.board
	blackScore = 0
	whiteScore = 0
	for row in xrange(8):
		for col in xrange(8):
			if (board[row][col] == "black"):
				blackScore += 1
			elif (board[row][col] == "white"):
				whiteScore += 1
	canvas.data.blackScore = blackScore
	canvas.data.whiteScore = whiteScore

def drawDisc(board, row, col):
	topMargin = canvas.data.topMargin
	margin = canvas.data.margin
	cellSize = canvas.data.cellSize
	left = (margin + col * cellSize) + 5
	right = (left + cellSize) - 10
	top = (topMargin + row * cellSize) + 5
	bottom = (top + cellSize) - 10
	canvas.create_oval(left, top, right, bottom, fill="black")
	canvas.create_oval(left+1, top+1, right-1, bottom-1, fill=board[row][col])

def drawCell(board, row, col):
	topMargin = canvas.data.topMargin
	margin = canvas.data.margin
	cellSize = canvas.data.cellSize
	left = margin + col * cellSize
	right = left + cellSize
	top = topMargin + row * cellSize
	bottom = top + cellSize
	canvas.create_rectangle(left, top, right, bottom, fill="black")
	canvas.create_rectangle(left+1, top+1, right-1, bottom-1, fill="#029743")
	if (board[row][col] != None):
		drawDisc(board, row, col)

def drawBoard():
	board = canvas.data.board
	for row in xrange(8):
		for col in xrange(8):
			drawCell(board, row, col)

def redrawAll():
	if (isBoardFull() == True):
		canvas.delete(ALL)
		drawBoard()
		getScore()
		drawScore()
		gameOver()
	else:
		canvas.delete(ALL)
		drawBoard()
		getScore()
		drawScore()
		drawPlayerTurn()

def init():
	canvas.data.gameOver = False
	canvas.data.hintMode = False
	canvas.data.splashScreen = False
	canvas.data.undoCount = 0
	board = []
	for row in xrange(8):
		board += [[None]*8]
	board[3][3] = "black"
	board[3][4] = "white"
	board[4][3] = "white"
	board[4][4] = "black"
	canvas.data.board = board
	canvas.data.player = "black"
	redrawAll()

def splashScreen():
	canvas.delete(ALL)
	canvas.data.splashScreen = True
	canvasWidth = canvas.data.canvasWidth
	canvasHeight = canvas.data.canvasHeight
	canvas.create_rectangle(15, 50, canvasWidth-15, canvasHeight-50, fill="#029743")
	canvas.create_text(canvasWidth/2, canvasHeight/5+30, text="OTHELLO", font=("Times New Roman", 42, "bold"))
	canvas.create_rectangle(canvasWidth/2-80, canvasHeight/4+80, canvasWidth/2+80, canvasHeight/4+120, fill="white", width=3)
	canvas.create_text(canvasWidth/2, canvasHeight/4+100, text="Start game", font=("Arial", 22), justify="center", fill="black")
	canvas.create_rectangle(canvasWidth/2-80, canvasHeight/4+140, canvasWidth/2+80, canvasHeight/4+180, fill="white", width=3)
	canvas.create_text(canvasWidth/2, canvasHeight/4+160, text="How to play", font=("Arial", 22), justify="center", fill="black")

def run():
	global canvas
	root = Tk()
	root.title("OTHELLO")
	topMargin = 50
	margin = 15
	cellSize = 40
	canvasWidth = (8*cellSize) + (2*margin)
	canvasHeight = (8*cellSize) + (2*topMargin)
	canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
	canvas.pack()
	root.resizable(width=0, height=0)
	root.canvas = canvas.canvas = canvas
	class Struct(): pass
	canvas.data = Struct()
	canvas.data.topMargin = topMargin
	canvas.data.margin = margin
	canvas.data.cellSize = cellSize
	canvas.data.canvasWidth = canvasWidth
	canvas.data.canvasHeight = canvasHeight
	canvas.data.splashScreen = False
	canvas.data.instructions = False
	splashScreen()
	root.bind("<Button-1>", mousePressed)
	root.bind("<Key>", keyPressed)
	root.mainloop()

run()
