# Human Player

class Human:

	def __init__(self):
		self.board = [[' '] * 8 for i in range(8)]
		self.size = 8
		self.board[4][4] = 'W'
		self.board[3][4] = 'B'
		self.board[3][3] = 'W'
		self.board[4][3] = 'B'
		# a list of unit vectors (row, col)
		self.directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

	def get(self, coord):
		return self.board[coord[0]][coord[1]]

	def set(self, coord, value):
		self.board[coord[0]][coord[1]] = value

	def add(self, v1, v2):
		return (v1[0] + v2[0], v1[1] + v2[1])

	def sub(self, v1, v2):
		return (v1[0] - v2[0], v1[1] - v2[1])

	def ray(self, v1, v2, a):
		return (v1[0] + a * v2[0], v1[1] + a * v2[1])

	def on_board(self, v):
		return v[0] >= 0 and v[0] < self.size and v[1] >= 0 and v[1] < self.size

	def legal(self, coord, mine, their):
		if self.get(coord) != ' ':
			return False

		for v in self.directions:
			pos = coord
			next = self.add(pos, v)
			pos = next
			next = self.add(pos, v)
			while self.on_board(next):
				if self.get(pos) != their:
					break
				if self.get(next) == mine and self.get(pos) == their:
					return True
				pos = next
				next = self.add(pos, v)
		return False

	def flip(self, coord, v, distance, mine):
		for i in range(distance):
			self.set(self.ray(coord, v, i + 1), mine)

	def place_piece(self, row, col, mine, their):
		self._place_piece((row, col), mine, their)

	def _place_piece(self, coord, mine, their):
		self.set(coord, mine)
		for v in self.directions:
			pos = coord
			pos = self.add(pos, v)
			distance = 0
			while self.on_board(pos):
				if self.get(pos) == ' ':
					break
				if self.get(pos) == mine:
					self.flip(coord, v, distance, mine)
					break
				distance = distance + 1
				pos = self.add(pos, v)

	def play_square(self, prev_row, prev_col, mine, their):
		prev = (prev_row, prev_col)
		if prev != (-1, -1):
			self._place_piece(prev, their, mine)
		coord = (-1, -1)
		while not self.legal(coord, mine, their):
			try:
				coord = (int(raw_input('Row: ')) - 1, int(raw_input('Col: ')) - 1)
				if coord[0] < 0 or coord[0] > self.size or coord[1] < 0 or coord[1] > self.size:
					raise ValueError()
			except KeyboardInterrupt:
				raise SystemExit(0)
			except ValueError:
				pass
		if not coord == (-1, -1):
			self._place_piece(coord, mine, their)
		return coord