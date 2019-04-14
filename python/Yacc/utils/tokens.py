QUOTE = r'(\'|")'


tokens = (
	'SEMI',
	'COLON',
	'COMMA',
	'DOT',
	'LPAREN',
	'RPAREN',
	'LT',
	'GT',
	'EQ',
	'MINUS',
	'PLUS',
	'TIMES',
	'COLEQ',
	'LE',
	'GE',
	'NE',
	'ID',
	'ICONST',
	'CCONST',
	'SCONST',
	'AND',
	'ARRAY',
	'BEGIN',
	'DIV',
	'DOWNTO',
	'ELSE',
	'ELSIF',
	'END',
	'ENDIF',
	'ENDLOOP',
	'FOR',
	'FUNCTION',
	'IF',
	'LOOP',
	'NOT',
	'OF',
	'OR',
	'PROCEDURE',
	'PROGRAM',
	'RECORD',
	'REPEAT',
	'RETURN',
	'THEN',
	'TO',
	'TYPE',
	'UNTIL',
	'VAR',
	'WHILE',
	'INTEGER',
	'CHAR',
	'STRING',
)


# Regular statement rules for tokens.
t_DOT			= r"\."

t_COLEQ			= r":="
t_SEMI			= r";"
t_COLON			= r":"
t_COMMA			= r","

t_PLUS			= r"\+"
t_MINUS			= r"\-"
t_TIMES			= r"\*"

t_EQ			= r"\="
t_NE			= r"\<\>"
t_LT			= r"\<"
t_GT			= r"\>"
t_LE			= r"\<\="
t_GE			= r"\>\="


t_LPAREN		= r"\("
t_RPAREN		= r"\)"
#t_LBRACKET		= r"\["
#t_RBRACKET		= r"\]"

t_CCONST		= r"\'.\'"
t_SCONST		= r"\'.{2,}\'"
t_ICONST		= r"(\-)*[0-9]+"


reserved_keywords = {
	'program':	'PROGRAM',
	'var':		'VAR',
	'begin':	'BEGIN',
	'end':		'END',
	'array':	'ARRAY',

	'if':		'IF',
	'then':		'THEN',
	'else':		'ELSE',
	'for':		'FOR',
	'while':	'WHILE',
	'repeat':	'REPEAT',
	'do':		'DO',
	'to':		'TO',
	'downto':	'DOWNTO',
	'until':	'UNTIL',
	'elsif':	'ELSIF',
	'endif':	'ENDIF',
	'loop':		'LOOP',
	'endloop':	'ENDLOOP',

	'and':		'AND',
	'or':		'OR',

	'div':		'DIV',
	
	'procedure':'PROCEDURE',
	'function':	'FUNCTION',

	'integer':	'INTEGER',
	'string':	'STRING',
	'char':	'CHAR',
}

def t_ID(t):
	r"[a-zA-Z]([a-zA-Z0-9])*"
	if t.value.lower() in reserved_keywords:
		t.type = reserved_keywords[t.value.lower()]
	return t


def t_COMMENT(t):
	r"\(\*.*\*\)"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs).
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])


if __name__ == '__main__':
	# Build the lexer
	from ply import lex
	import sys 
	
	lex.lex()
	
	data = open('../tests/test.pasc', 'r').read()
	
	lex.input(data)
	
	# Tokenize
	while 1:
	    tok = lex.token()
	    if not tok: break      # No more input
	    print(tok)
	

