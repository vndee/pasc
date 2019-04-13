from .utils.yacc import  yacc
from .utils.rules import *
from .utils.semantic import *

parser = yacc()
f = open('./Lexical/Test05.txt', 'r')
raw_input = f.read()
result = parser.parse(raw_input)
print(result)
