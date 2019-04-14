from ply import lex, yacc
import argparse
from utils.tokens import *
from utils.graph import graph
from utils.rules import *

def main(filename):
	logger = yacc.NullLogger()
	yacc.yacc()

	data = open(filename, 'r').read()
	ast = yacc.parse(data,lexer = lex.lex())
	graph(ast, filename)

if __name__ == '__main__':
	parser = argparse.ArgumentParser("""
	    *** PASC (Mini Pascal) lang                  ***
	    *** 502057 (Programming Language Concepts)   ***
	    *** Spring 2018-2019 assignment.             ***
	""")

	parser.add_argument('-i', '--input', help="Input path. Example: ./Test.txt")

	args = parser.parse_args()
	if not args.input:
		print("Missing argument: `python3 parser.py -h` for more detail.")
		exit(0)

	main(filename=args.input)
