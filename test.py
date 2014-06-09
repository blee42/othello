from TeamSwag import TeamSwag

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

def color(text, code):
	return code + text + ENDC

def print_board(board):
		# Print board
		print '   1 2 3 4 5 6 7 8'
		print ' +' + '-' * 16 + '+'
		n = 1
		for row in board:
			string = str(n) + '|' + ''.join(map(lambda x: color(' #', OKGREEN) if x == 'W' else (color(' O', OKBLUE) if x =='B' else '  '), row)) + '|'
			print string
			n = n + 1
		print ' +' + '-' * 16 + '+'

x = TeamSwag()
x.max_depth = 3

print_board(x.board)

x.play_square(-1, -1, 'W', 'B')

print_board(x.board)
