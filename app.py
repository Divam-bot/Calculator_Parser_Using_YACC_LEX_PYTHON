import ply.lex as lex
import ply.yacc as yacc
# List of token names.   This is always required
tokens = (
    'INT',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'NAME',
    'DIV',
 )

 # Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

 # A regular expression rule with some action code


def t_INT(t):
    r'[0-9]+'
    t.value = int(t.value)    
    return t
 # Rule for variable
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type='NAME'
    return t
 # Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
 
 # A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
 
 # Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
 

lexer = lex.lex()
 

precedence = (
    ( 'left', 'PLUS', 'MINUS' ),
    ( 'left', 'TIMES', 'DIVIDE' ),
    ( 'nonassoc', 'UMINUS' )
)

def p_add( p ) :
    'expr : expr PLUS expr'
    p[0] = p[1] + p[3]

def p_sub( p ) :
    'expr : expr MINUS expr'
    p[0] = p[1] - p[3]

def p_expr2uminus( p ) :
    'expr : MINUS expr %prec UMINUS'
    p[0] = - p[2]

def p_mult_div( p ) :
    '''expr : expr TIMES expr
            | expr DIVIDE expr'''

    if p[2] == '*' :
        p[0] = p[1] * p[3]
    else :
        if p[3] == 0 :
            print("Can't divide by 0")
            raise ZeroDivisionError('integer division by 0')
        p[0] = p[1] / p[3]

def p_expr2NUM( p ) :
    'expr : INT'
    p[0] = p[1]

def p_parens( p ) :
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]

def p_error( p ):
    print("Syntax error in input!")

parser = yacc.yacc()

#data = '''34 + 4 * 9'''

#print(parser.parse(data))
 




from flask import Flask,render_template, request,redirect,url_for,Response , jsonify


app = Flask(__name__)


@app.route("/",methods=["GET","POST"])
def index():
    res=""
    if(request.method == "POST"):
        
        data = request.form.get("input")
        res+=str(parser.parse(data))
        
    return render_template("index.html",res=res)

if __name__ == "__main__":
    app.run()