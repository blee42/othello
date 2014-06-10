from pprint import pprint
from random import choice
from time import time

# Team Swag

class TeamSwag:

	def __init__(self):
		self.board = [[' '] * 8 for i in range(8)]
		self.size = 8
		self.board[4][4] = 'W'
		self.board[3][4] = 'B'
		self.board[3][3] = 'W'
		self.board[4][3] = 'B'
		self.directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
		self.max_depth = 5

	def copy(self, board):
		return [list(row) for row in board]

	def get(self, coord, board):
		return board[coord[0]][coord[1]]

	def set(self, coord, value, board):
		board[coord[0]][coord[1]] = value

	def add(self, v1, v2):
		return (v1[0] + v2[0], v1[1] + v2[1])

	def sub(self, v1, v2):
		return (v1[0] - v2[0], v1[1] - v2[1])

	def ray(self, v1, v2, a):
		return (v1[0] + a * v2[0], v1[1] + a * v2[1])

	def on_board(self, v):
		return v[0] >= 0 and v[0] < self.size and v[1] >= 0 and v[1] < self.size

	def legal(self, coord, mine, their, board):
		if self.get(coord, board) != ' ':
			return False

		for v in self.directions:
			pos = coord
			next = self.add(pos, v)
			pos = next
			next = self.add(pos, v)
			while self.on_board(next):
				if self.get(pos, board) != their:
					break
				if self.get(next, board) == mine and self.get(pos, board) == their:
					return True
				pos = next
				next = self.add(pos, v)
		return False

	def flip(self, coord, v, distance, mine, board):
		for i in range(distance):
			self.set(self.ray(coord, v, i + 1), mine, board)

	# Alias for interfacing

	def place_piece(self, row, col, mine, their):
		self._place_piece((row, col), mine, their, self.board)

	def _place_piece(self, coord, mine, their, board):
		self.set(coord, mine, board)
		for v in self.directions:
			pos = coord
			pos = self.add(pos, v)
			distance = 0
			while self.on_board(pos):
				if self.get(pos, board) == ' ':
					break
				if self.get(pos, board) == mine:
					self.flip(coord, v, distance, mine, board)
					break
				distance = distance + 1
				pos = self.add(pos, v)

	# Evaluation function

	def evaluate(self, mine, their, board):
		# constants!
		k1 = 10
		k2 = 100
		k3 = 2500
		k4 = 50

		b  = [[99, -8, 8, 6, 6, 8, -8, 99],
		 [-8, --24, -4, -3, -3, -4, --24, -8],
		 [8, -4, 7, 4, 4, 7, -4, 8],
		 [6, -3, 4, 0, 0, 4, -3, 6],
		 [6, -3, 4, 0, 0, 4, -3, 6],
		 [8, -4, 7, 4, 4, 7, -4, 8],
		 [-8, --24, -4, -3, -3, -4, --24, -8],
		 [99, -8, 8, 6, 6, 8, -8, 99]]

		my_pieces = 0
		their_pieces = 0

		pos_score = 0
		for i in range(len(b)):
			for j in range(len(b[i])):
				val = self.get((i, j), board)
				if val == mine:
					pos_score += b[i][j]
					my_pieces += 1
				elif val == their:
					pos_score -= b[i][j]
					their_pieces = 0

		if my_pieces > their_pieces:
			disc_score = 100 * my_pieces / (my_pieces + their_pieces)
		elif my_pieces != their_pieces:
			disc_score = 100 * their_pieces / (my_pieces + their_pieces)
		else:
			disc_score = 0

		if my_pieces + their_pieces > 40:
			k1 = 700

		move_score = len(self.moves(mine, their, board))

		corner_score = 0
		for i in [(0, 0), (0, self.size-1), (self.size-1, 0), (self.size-1, self.size-1)]:
			val = self.get(i, board)
			if val == mine:
				corner_score += 1
			elif val == their:
				corner_score -= 1

		return k1 * disc_score + k2 * move_score + k3 * corner_score + k4 * pos_score + 100000

	def moves(self, mine, their, board):
		options = []
		for i in range(self.size):
			for j in range(self.size):
				coord = (i, j)
				if self.legal(coord, mine, their, board):
					options.append(coord)
		return options

	def minimax(self, curr, mine, their, board, depth, timeout, prune=None):
		if time() > timeout:
			return None, None

		if depth == 0:
			return self.evaluate(mine, their, board), (-1, -1)
		
		if curr == mine: # MAXIMIZE
			moves = self.moves(mine, their, board)
			if len(moves) == 0:
				return self.evaluate(mine, their, board), (-1, -1)
			best_val = None
			best_move = None
			for move in moves:
				new = self.copy(board)
				self._place_piece(move, mine, their, new)

				val = self.minimax(their, mine, their, new, depth - 1, timeout, best_val)[0]

				if val is None:
					return None, None

				if val == -1:
					continue

				# Pruning
				if prune is not None and val >= prune:
					return -1, None

				if best_val is None or val > best_val:
					best_val = val
					best_move = move
			return best_val, best_move
		else: #MINIMIZE
			moves = self.moves(their, mine, board)
			if len(moves) == 0:
				return self.evaluate(mine, their, board), (-1, -1)
			worst_val = None
			worst_move = None
			for move in moves:
				new = self.copy(board)
				self._place_piece(move, their, mine, new)

				val = self.minimax(mine, mine, their, new, depth - 1, timeout, worst_val)[0]

				if val is None:
					return None, None

				if val == -1:
					continue

				# Pruning
				if prune is not None and val <= prune:
					return -1, None

				if worst_val is None or val < worst_val:
					worst_val = val
					worst_move = move
			return worst_val, worst_move

	def play_square(self, prev_row, prev_col, mine, their):
		prev = (prev_row, prev_col)
		if prev != (-1, -1):
			self._place_piece(prev, their, mine, self.board)

		timeout = time() + 1

		move = (-1, -1)

		n = 1
		while n < 64:
			trial = self.minimax(mine, mine, their, self.board, n, timeout)
			if trial[1] is None:
				break
			else:
				move = trial[1]
			n = n + 1


		if move != (-1, -1):
			self._place_piece(move, mine, their, self.board)
		print("Evaluation score: ", self.evaluate(mine, their, self.board))
		print("Depth: ", n)
		return move