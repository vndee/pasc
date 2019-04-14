from .ast import Node
import sys

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES'),
    ('left', 'DIV'),
    ('left', 'EQ', 'NE', 'LE', 'LT', 'GT', 'GE'),
    ('left', 'OR', 'AND'),
)


def p_program_start(args):
	"""program : header SEMI block DOT
	| statement_sequence
	"""
	if len(args) == 2:
		args[0] = Node('program', args[1])
	else:
		args[0] = Node('program',args[1],args[3])


def p_header(args):
    'header : PROGRAM identifier'
    args[0] = args[2]


def p_block(args):
    """block : variable_declaration_part procedure_or_function statement_part
	"""
    args[0] = Node('block', args[1], args[2], args[3])


def p_variable_declaration_part(args):
    """variable_declaration_part : VAR variable_declaration_list
	 |
	"""
    if len(args) > 1:
        args[0] = args[2]


def p_variable_declaration_list(args):
    """variable_declaration_list : variable_declaration variable_declaration_list
	 | variable_declaration
	"""
    # function and procedure missing here
    if len(args) == 2:
        args[0] = args[1]
    else:
        args[0] = Node('var_list', args[1], args[2])


def p_variable_declaration(args):
    """variable_declaration : variable_identifier COLON type SEMI"""
    args[0] = Node('var', args[1], args[3])

def p_variable_identifier(args):
	"""variable_identifier : identifier COMMA variable_identifier
	| identifier"""
	if len(args) > 2:
		args[0] = Node('id_list', args[1], args[3])
	else:
		args[0] = Node('id_list', args[1])

def p_procedure_or_function(args):
    """procedure_or_function : proc_or_func_declaration SEMI procedure_or_function
		| """

    if len(args) == 4:
        args[0] = Node('function_list', args[1], args[3])


def p_proc_or_func_declaration(args):
    """ proc_or_func_declaration : procedure_declaration
               | function_declaration """
    args[0] = args[1]


def p_procedure_declaration(args):
    """procedure_declaration : procedure_heading SEMI block"""
    args[0] = Node("procedure", args[1], args[3])


def p_procedure_heading(args):
    """ procedure_heading : PROCEDURE identifier
	| PROCEDURE identifier LPAREN parameter_list RPAREN"""

    if len(args) == 3:
        args[0] = Node("procedure_head", args[2])
    else:
        args[0] = Node("procedure_head", args[2], args[4])


def p_function_declaration(args):
    """ function_declaration : function_heading SEMI block"""
    args[0] = Node('function', args[1], args[3])


def p_function_heading(args):
    """ function_heading : FUNCTION type
	 	| FUNCTION identifier COLON type
		| FUNCTION identifier LPAREN parameter_list RPAREN COLON type"""
    if len(args) == 3:
        args[0] = Node("function_head", args[2])
    elif len(args) == 5:
        args[0] = Node("function_head", args[2], args[3])
    else:
        args[0] = Node("function_head", args[2], args[4], args[7])


def p_parameter_list(args):
    """ parameter_list : parameter COMMA parameter_list
	| parameter"""
    if len(args) == 4:
        args[0] = Node("parameter_list", args[1], args[3])
    else:
        args[0] = args[1]


def p_parameter(args):
    """ parameter : identifier COLON type"""
    args[0] = Node("parameter", args[1], args[3])


def p_type(args):
    """ type : STRING
	| INTEGER
	| CHAR
	"""
    args[0] = Node('type', args[1].lower())


def p_statement_part(args):
    """statement_part : BEGIN statement_sequence END"""
    args[0] = args[2]


def p_statement_sequence(args):
    """statement_sequence : statement SEMI statement_sequence
	 | statement"""
    if len(args) == 2:
        args[0] = args[1]
    else:
        args[0] = Node('statement_list', args[1], args[3])


def p_statement(args):
    """statement : assignment_statement
	 | statement_part
	 | if_statement
	 | while_statement
	 | repeat_statement
	 | for_statement
	 | procedure_or_function_call
	 |
	"""
    if len(args) > 1:
        args[0] = args[1]


def p_procedure_or_function_call(args):
    """ procedure_or_function_call : identifier LPAREN param_list RPAREN
	| identifier """

    if len(args) == 2:
        args[0] = Node("function_call", args[1])
    else:
        args[0] = Node("function_call", args[1], args[3])


def p_param_list(args):
    """ param_list : param_list COMMA param
	 | param """
    if len(args) == 2:
        args[0] = args[1]
    else:
        args[0] = Node("parameter_list", args[1], args[3])


def p_param(args):
    """ param : expression """
    args[0] = Node("parameter", args[1])


def p_if_statement(args):
    """if_statement : IF expression THEN statement ELSE statement ENDIF
	| IF expression THEN statement ELSIF statement ENDIF
	| IF expression THEN statement ENDIF
	"""

    if len(args) == 5:
        args[0] = Node('if', args[2], args[4])
    else:
        args[0] = Node('if', args[2], args[4], args[6])


def p_while_statement(args):
    """while_statement : WHILE expression LOOP statement ENDLOOP"""
    args[0] = Node('while', args[2], args[4])


def p_repeat_statement(args):
    """repeat_statement : REPEAT statement UNTIL expression"""
    args[0] = Node('repeat', args[2], args[4])


def p_for_statement(args):
    """for_statement : FOR assignment_statement TO expression LOOP statement ENDLOOP
	| FOR assignment_statement DOWNTO expression LOOP statement ENDLOOP
	"""
    args[0] = Node('for', args[2], args[3], args[4], args[6])


def p_assignment_statement(args):
    """assignment_statement : identifier COLEQ expression"""
    args[0] = Node('assign', args[1], args[3])


def p_expression(args):
    """expression : expression and_or expression_m
	| expression_m
	"""
    if len(args) == 2:
        args[0] = args[1]
    else:
        args[0] = Node('op', args[2], args[1], args[3])


def p_expression_m(args):
    """ expression_m : expression_s
	| expression_m sign expression_s"""
    if len(args) == 2:
        args[0] = args[1]
    else:
        args[0] = Node('op', args[2], args[1], args[3])


def p_expression_s(args):
    """ expression_s : element
	| expression_s psign element"""
    if len(args) == 2:
        args[0] = args[1]
    else:
        args[0] = Node('op', args[2], args[1], args[3])


def p_and_or(args):
    """ and_or : AND
	| OR """
    args[0] = Node('and_or', args[1])


def p_psign(args):
    """psign : TIMES
	| DIV"""
    args[0] = Node('sign', args[1])


def p_sign(args):
    """sign : PLUS
	| MINUS
	| EQ
	| NE
	| LT
	| LE
	| GT
	| GE
	"""
    args[0] = Node('sign', args[1])


def p_element(args):
    """element : identifier
	| integer
	| string
	| char
	| LPAREN expression RPAREN
	| NOT element
	"""
    if len(args) == 2:
        args[0] = Node("element", args[1])
    elif len(args) == 3:
        # not e
        args[0] = Node('not', args[2])
    else:
        # ( e )
        args[0] = Node('element', args[2])


def p_identifier(args):
    """ identifier : ID """
    args[0] = Node('identifier', str(args[1]).lower())


def p_integer(args):
    """ integer : ICONST """
    args[0] = Node('integer', args[1])


def p_string(args):
    """ string : SCONST """
    args[0] = Node('string', args[1])


def p_char(args):
    """ char : CCONST """
    args[0] = Node('char', args[1])


def p_error(args):
    print("Syntax error in input, in line %d:" % t.lineno, t)
    sys.exit()
