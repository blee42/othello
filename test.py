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
		print '+' + '-' * 16 + '+'
		for row in board:
			string = '|' + ''.join(map(lambda x: color('[]', OKGREEN) if x == 'W' else (color('[]', OKBLUE) if x =='B' else '  '), row)) + '|'
			print string
		print '+' + '-' * 16 + '+'

x = TeamSwag()

print_board(x.board)