# 13 - April - 2019
# Created by Guru Sarath

import pygame
import sys
import time
import random
import copy
from os import system, name 


#Define the colors (R,G,B)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
Top_padding_COLOR = (244,66,66)

SingleCoin_side = 50
separatorLine_width = 1
Top_padding = 100
ConnectX = 8
Display_WIDTH = (SingleCoin_side * ConnectX)
Display_HEIGHT = (SingleCoin_side * ConnectX) + Top_padding
ExitGame = False

  

# GUI
def createPyGameText(textX, sizeX, colorX, antiAliasing = True):
    TextFontSettings = pygame.font.Font('freesansbold.ttf', sizeX)
    TextSurface = TextFontSettings.render(textX, antiAliasing, colorX)
    TextRect = TextSurface.get_rect()
    return TextSurface, TextRect

# Create the GUI
def init_game():

	global clock, Main_Window_surfaceObject

	pygame.init()
	Main_Window_surfaceObject = pygame.display.set_mode((Display_WIDTH, Display_HEIGHT))
	pygame.display.set_caption('Connect Four Game ')
	clock = pygame.time.Clock()

	# Background color of the surface
	Main_Window_surfaceObject.fill(WHITE)
	# Status bar
	pygame.draw.rect(Main_Window_surfaceObject, Top_padding_COLOR, (0, 0, Display_WIDTH,Top_padding) )

	#Display Title
	text_surf, text_rect = createPyGameText('Connect 4', 50, BLACK)
	Main_Window_surfaceObject.blit(text_surf, (Display_WIDTH / 6, 5))

	#Draw horizontal lines
	for i in range(ConnectX):
		pygame.draw.line( Main_Window_surfaceObject, BLACK, (0, i*SingleCoin_side + Top_padding) , (Display_WIDTH,  i*SingleCoin_side + Top_padding) , separatorLine_width)

	#Draw vertical lines
	for i in range(ConnectX):
		pygame.draw.line( Main_Window_surfaceObject, BLACK, (i * SingleCoin_side, Top_padding) , (i * SingleCoin_side, Display_HEIGHT) , separatorLine_width)

	pygame.display.update()
	clock.tick(60)

#Create the coins
def createCoin(CoinX):
	coin = None

	if CoinX == 'blue':
		coin = pygame.image.load('Coin_blue.png')
	else:
		coin = pygame.image.load('Coin_red.png')

	coin = pygame.transform.scale(coin, (SingleCoin_side, SingleCoin_side))
	#Main_Window_surfaceObject.blit(blue_coin, (0, 0))
	return coin

#Place the coin at a particular location
def placeCoin(locationOfCoinDrop, CoinX):
	row, col = locationOfCoinDrop
	x = (col - 1) * SingleCoin_side
	y = ((row - 1) * SingleCoin_side) + Top_padding
	coin = createCoin(CoinX)
	Main_Window_surfaceObject.blit(coin, (x,y))

# MAIN GAME LOOP
def game_loop(gameXObj):

	while not ExitGame:

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()


		if gameXObj.currentPlayer == gameXObj.players[0]:
			clear()
			print('Computer\'s Turn - ')
			#Wait for computer player
			gameXObj.ComputerPlay(gameXObj.MonteCarloPlayer)

		else:
			clear()
			print('Your Turn')
			# Wait for human player
			gameXObj.HoomanPlay()

		# Exit game if winner found
		if gameXObj.Winner:
			if gameXObj.Winner == gameXObj.players[0]:
				print('You Lose')
				text_surf, text_rect = createPyGameText('You Lose', 50, BLUE)
			elif gameXObj.Winner == gameXObj.players[1]:
				print('You Win')
				text_surf, text_rect = createPyGameText('You Win', 50, BLUE)
			else:
				text_surf, text_rect = createPyGameText('Tie!!', 50, BLUE)

			Main_Window_surfaceObject.blit(text_surf, (Display_WIDTH / 6, 50))
			pygame.display.update()
			time.sleep(5) # Wait for 5 sec before exit
			pygame.quit()
			sys.exit()


		pygame.display.update()
		clock.tick(60)


# Clears the command prompt window 
def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 


# =======================================================================
# Main Game Class
# =======================================================================
class Connect4:

	players = (1,2)
	players_names = ['Computer', 'Player 2']
	players_printFace = ['X', 'O']
	currentPlayer = players[0]
	currentPlayer_name = players_names[0]
	DifficultyLevel = 4
	Hooman_Turn_and_Hooman_Did_not_Play = False

	NumberOfMovesPlayed = 0
	Winner = None
	board = ([0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0])

	#Format Col:Number Of coins that can be inserted in that column
	availableMovesDict = {1:8,2:8,3:8,4:8,5:8,6:8,7:8,8:8}

	def __init__(self, currentPlayer = 1):
		self.NumberOfMovesPlayed = 0
		self.currentPlayer = self.players[currentPlayer - 1]
		self.currentPlayer_name = self.players[currentPlayer - 1]


	# Prints the current status of the game
	# USED IN CLI VERSION OF THE GAME
	# NOT REQUIRED IN GUI VERSION !!!!!
	def printStatus(self):
		print('============================================================================')
		print('Player', self.players_names[self.currentPlayer - 1], '\'s turn ', end='')
		print('| Total Number of Moves played - ', self.NumberOfMovesPlayed, end='')
		print('| Difficulty Level - ', self.DifficultyLevel)
		print('============================================================================')

	# Switch players 1 to 2 or 2 to 1
	def switchPlayer(self):

		if self.currentPlayer == self.players[0]:
			self.currentPlayer = self.players[1]
			self.currentPlayer_name = self.players_names[1]
		else:
			self.currentPlayer = self.players[0]
			self.currentPlayer_name = self.players_names[0]


	# Return the locations at which a coin can be placed
	# Returns a list with locations as tuples
	# ex: [(1,3),(7,2)] 
	def availableMoves(self):

		NextMoves = []

		i = 0
		for col in self.availableMovesDict:

			if self.availableMovesDict[col] > 0:
				NextMoves.append(   (self.availableMovesDict[col] - 1, col - 1)  )
				i += 1
			else:
				pass

		return NextMoves


	# Insert a coin in a particular column
	def executeMove(self, Move, PrintBoard = False):
		# execute move only needs the column number to insert coin
		# c is actual array index
		c = Move

		# Return false if invalid column number is passed
		if c > 7 or c < 0 :
			return False

		#Execute move only if there is an empty spot
		if self.availableMovesDict[c + 1] > 0:
			Location = (self.availableMovesDict[c + 1] - 1 , c )
			boardListForm = list(self.board)
			boardListForm[ self.availableMovesDict[c + 1] - 1 ][c] = self.currentPlayer
			self.board = tuple(boardListForm)
			self.availableMovesDict[c + 1] -= 1
			self.NumberOfMovesPlayed += 1

			if PrintBoard: self.printBoard()

			#This function return the row and column in which element was inserted
			return Location
		else:
			# Return False if a move cant be made
			return False


	# When it is human player's turn
	def HoomanPlay(self):

		if self.currentPlayer == self.players[1]:
			# c is actual array index
			Hooman_Turn_and_Hooman_Did_not_Play = True

		CoinLocation_x = 0

		# This loop will exits only when the user clicks a location on the screen
		while True:

			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				# If mouse pressed and released
				if event.type == pygame.MOUSEBUTTONUP:
					x, y = pygame.mouse.get_pos()
					CoinLocation_x = 0

					# This loop finds the column at wihich the user clicked (1 to 8)
					for location in range(ConnectX + 1):

						# Check in what x range the mouse click 
						if (x < SingleCoin_side * location) and (x > SingleCoin_side * (location-1)):
							CoinLocation_x = location
							print(CoinLocation_x) # For debugging purpose
							break;

				if CoinLocation_x: break; #Break the loop if location to insert coin is found

			if CoinLocation_x: break; #Break the loop if location to insert coin is found

		
		MoveX = self.executeMove(CoinLocation_x - 1) # Execute that move # internal record

		if MoveX:
			placeCoin( (self.availableMovesDict[CoinLocation_x] + 1, CoinLocation_x ) , 'red') # Place the coin at that location
			self.checkCompletion(MoveX)
			self.switchPlayer()
			return True
		else:
			print('Invalid Move !!')
			self.HoomanPlay()

	# When it is computer player's turn
	# AI_Agent - is a function that returns a move
	def ComputerPlay(self, AI_Agent):

		if self.currentPlayer == self.players[0]:
			#Get the from the agent
			# MoveX is a location tuple (row, col)
			print('\nThinking ... ... ...')
			MoveX = AI_Agent() 
			
			if MoveX:
				placeCoin( (MoveX[0]+1,MoveX[1]+1) , 'blue') # Place the coin at that location returned by AI agent
				MoveX = self.executeMove(MoveX[1]) #Execute move only requires the column to insert
				self.checkCompletion(MoveX)
				self.switchPlayer()
				Hooman_Turn_and_Hooman_Did_not_Play = False
				return True
			else:
				Hooman_Turn_and_Hooman_Did_not_Play = False
				return False

	# Agent random player
	def randomPlayer(self):
		PossibleNextMoves = self.availableMoves()
		MoveX = random.choice(PossibleNextMoves)

		if MoveX:
			return MoveX
		else:
			return False

	# Agent Monte carlo player
	def MonteCarloPlayer(self):

		# Number of simulations to run on each Next possible moves 
		# More the simulations = Better the decision
		Simulations_each = 1000

		# Set the number of simulations based on difficulty level
		if self.DifficultyLevel >= 4:
			Simulations_each = 1000 #Super hard
		elif self.DifficultyLevel >= 3:
			Simulations_each = 200 #Hard
		elif self.DifficultyLevel >= 2:
			Simulations_each = 50 #Easy
		elif self.DifficultyLevel >= 1:
			Simulations_each = 5 #Baby



		GameX_CurrentState = self.makeCopy() #Make a copy of current game, for simulation purpose
		PossibleNextMoves_CurrentState = GameX_CurrentState.availableMoves() #Find all the next possible moves from the current state
		NumberOfPossibleMoves = len(PossibleNextMoves_CurrentState)

		#Create a dictionary with key as next possible moves
		# ex: {(7,1):0, (7,3):0, (4,6):0}
		# The value corresponding to the particular key value is the number of wins through that move
		# This value is used to select the next best move
		Move_probability_dict = { PossibleNextMoves_CurrentState[i] : 0 for i in range(NumberOfPossibleMoves)}

		# Run the simulation for all the possible moves
		for i in range(NumberOfPossibleMoves):

			Wins = 0 # In this move we won 0 times (at the start)
			GameX_Simulation_level_0 = self.makeCopy()
			MoveX_immediate_next = GameX_Simulation_level_0.executeMove(PossibleNextMoves_CurrentState[i][1], PrintBoard = False)
			GameX_Simulation_level_0.checkCompletion(MoveX_immediate_next)

			# If a immediate next move leads to a win
			# then return that move and Win the game
			if GameX_Simulation_level_0.Winner == self.players[0]:
				return MoveX_immediate_next

			GameX_Simulation_level_0.switchPlayer()
			GameX_Simulation_level_1 = copy.deepcopy(GameX_Simulation_level_0)

			# Run 'Simulations_each = 1000' number of simulations on each move
			for TrialX in range(Simulations_each):

				GameX_Simulation_level_X = copy.deepcopy(GameX_Simulation_level_1)
				while not GameX_Simulation_level_X.Winner:
					# Expand the board
					PossibleNextMoves = GameX_Simulation_level_X.availableMoves()
					MoveX = None

					if PossibleNextMoves:
						# Select a random move
						MoveX = random.choice(PossibleNextMoves)

					if MoveX:
						# Execute that move
						MoveX = GameX_Simulation_level_X.executeMove(MoveX[1], PrintBoard = False) #Execute move only requires the column to insert
						GameX_Simulation_level_X.checkCompletion(MoveX)
						GameX_Simulation_level_X.switchPlayer()
					else:
						# May be Tie
						break;


					if GameX_Simulation_level_X.Winner == GameX_Simulation_level_X.players[0]:
						#If the computer won 
						#then increment the winnig count
						Wins += 1

			# Record the winning count for this i th move
			Move_probability_dict[MoveX_immediate_next] = Wins


		# Find the move with maximum wins and retun it
		Best = None # Move with Max Win
		Max = 0 # Max win record

		# Loop through the dict to find the max winning move
		for i in range(NumberOfPossibleMoves):
			if Move_probability_dict[ PossibleNextMoves_CurrentState[i] ] >= Max:
				Max = Move_probability_dict[ PossibleNextMoves_CurrentState[i] ]
				Best = PossibleNextMoves_CurrentState[i]

		#print(Move_probability_dict)

		#Return the Best move
		return Best



	# Makes an identical copy of the current game state
	def makeCopy(self):
		NewGame = Connect4() # New Object of the game
		NewGame.players = copy.deepcopy(self.players)
		NewGame.players_names = copy.deepcopy(self.players_names)
		NewGame.players_printFace = copy.deepcopy(self.players_printFace)
		NewGame.currentPlayer = copy.deepcopy(self.currentPlayer)
		NewGame.currentPlayer_name = copy.deepcopy(self.currentPlayer_name)
		NewGame.NumberOfMovesPlayed = copy.deepcopy(self.NumberOfMovesPlayed)
		NewGame.Winner = copy.deepcopy(self.Winner)
		NewGame.board = copy.deepcopy(self.board)
		NewGame.availableMovesDict = copy.deepcopy(self.availableMovesDict)

		return NewGame


	# Check if the last move caused the game to end (Win, lose or Tie)
	def checkCompletion(self, lastMove):

		#Uses actual array index
		r_center,c_center = lastMove

		# HORIZONTAL CHECK
		#--------------------------------------------------------

		count = 0
		r = r_center
		c = c_center
		while self.board[r][c] == self.board[r_center][c_center]:
			count += 1
			c += 1
			if r < 0 or r > 7 or c < 0 or c > 7:
				break

		r = r_center
		c = c_center
		while self.board[r][c] == self.board[r_center][c_center]:
			count += 1
			c -= 1
			if r < 0 or r > 7 or c < 0 or c > 7:
				break

		if count == 5:
			self.Winner = self.board[r_center][c_center]
			return self.board[r_center][c_center]

		# VERTICAL CHECK
		#--------------------------------------------------------

		count = 0
		r = r_center
		c = c_center
		while self.board[r][c] == self.board[r_center][c_center]:
			count += 1
			r += 1
			if r < 0 or r > 7 or c < 0 or c > 7:
				break

		r = r_center
		c = c_center
		while self.board[r][c] == self.board[r_center][c_center]:
			count += 1
			r -= 1
			if r < 0 or r > 7 or c < 0 or c > 7:
				break

		if count == 5:
			self.Winner = self.board[r_center][c_center]
			return self.board[r_center][c_center]

		# DIAGONAL1 CHECK
		#--------------------------------------------------------

		count = 0
		r = r_center
		c = c_center
		while self.board[r][c] == self.board[r_center][c_center]:
			count += 1
			r -= 1
			c += 1
			if r < 0 or r > 7 or c < 0 or c > 7:
				break

		r = r_center
		c = c_center
		while self.board[r][c] == self.board[r_center][c_center]:
			count += 1
			r += 1
			c -= 1
			if r < 0 or r > 7 or c < 0 or c > 7:
				break

		if count == 5:
			self.Winner = self.board[r_center][c_center]
			return self.board[r_center][c_center]

		# DIAGONAL2 CHECK
		#--------------------------------------------------------

		count = 0
		r = r_center
		c = c_center
		while self.board[r][c] == self.board[r_center][c_center]:
			count += 1
			r += 1
			c += 1
			if r < 0 or r > 7 or c < 0 or c > 7:
				break

		r = r_center
		c = c_center
		while self.board[r][c] == self.board[r_center][c_center]:
			count += 1
			r -= 1
			c -= 1
			if r < 0 or r > 7 or c < 0 or c > 7:
				break

		if count == 5:
			self.Winner = self.board[r_center][c_center]
			return self.board[r_center][c_center]


		# Check TIE
		#--------------------------------------------------------

		if self.NumberOfMovesPlayed >= 64:
			self.Winner = 64
			return 64 #Tie
		else:
			self.Winner = None
			return None #InProgress

	# Print the board in a good format
	# USED IN CLI VERSION OF THE GAME
	# NOT REQUIRED IN GUI VERSION !!!!!
	def printBoard(self):

		clear()

		# Print column numbers
		for row in self.board:
			i = 0
			print(' ',end='')
			for point in row:
				i += 1
				print(' | ' + str(i), end='')
			print(' |')
			break;

		# Print a line after column numbers
		for row in self.board:
			i = 0
			print(' ',end='')
			for point in row:
				i += 1
				print(' | ' + '_', end='')
			print(' |')
			break;

		# Print the board
		i=0
		for row in self.board:
			i += 1
			print(i, end='')
			for point in row:
				if point == self.players[0]:
					print(' | ' + str(self.players_printFace[0]) , end='')
				elif point == self.players[1]:
					print(' | ' + str(self.players_printFace[1]) , end='')
				else:
					print(' | ' + ' ' , end='')

			print(' |')

		return None


	# Print winner after the game comes to an end
	# USED IN CLI VERSION OF THE GAME
	# NOT REQUIRED IN GUI VERSION !!!!!
	def printWinner(self):

		if self.Winner == self.players[0]:
			print('\n------------------- YOU LOSE --------------------')
		elif self.Winner == self.players[1]:
			print('\n------------------- YOU WIN --------------------')
		else:
			print('\n------------------- TIE --------------------')


	# Start the game with this function
	def play(self):

		# Get the player's name
		self.players_names[1] = 'You'

		self.currentPlayer = self.players[1]

		self.DifficultyLevel = 4

		clear()

		init_game() # initiate the GUI
		game_loop(self) # start GUI game

		self.printWinner()

# Create a new game
gameX = Connect4()
#Start the Game
gameX.play()

