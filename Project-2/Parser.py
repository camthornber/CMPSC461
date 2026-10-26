from ASTNodeDefs import *
from typing import List, Tuple, Union
import re


"""
This is the skeleton code for the Parser with a Lexer
Feel free to modify anything in this file as needed
To run tests, use Verify.py

P2 note: base imported from my P1 submission
"""


class Lexer:
    """
    The Lexer (also known as a tokenizer or scanner) is responsible for breaking
    the raw source code string into a stream of meaningful tokens.
    """

    def __init__(self, code: str):
        self.code = code
        self.tokens: List[Tuple[str, str]] = []  # List of (token_type, token_value)
        self.token_specs = [
            #symbols
            ("ASSIGN", r":="),
            ("COLON", r":"),
            ("SEMICOLON", r";"),
            ("LEQ", r"<="),
            ("GEQ", r">="),
            ("NEQ", r"/="),
            ("EQ", r"="),
            ("LT", r"<"),
            ("GT", r">"),
            ("PLUS", r"\+"),
            ("MINUS", r"-"),
            ("MULTIPLY", r"\*"),
            ("DIVIDE", r"/"),
            ("LEFT_BRACKET", r"\("),
            ("RIGHT_BRACKET", r"\)"),
            ("RANGE", r"\.\."),

            #commands
            ("PUT", r"\bPut\b"),
            ("VAR", r"\bvar\b"),
            ("IF", r"\bif\b"),
            ("THEN", r"\bthen\b"),
            ("ELSE", r"\belse\b"),
            ("END", r"\bend\b"),
            ("WHILE", r"\bwhile\b"),
            ("FOR", r"\bfor\b"),
            ("IN", r"\bin\b"),
            ("LOOP", r"\bloop\b"),
            ("OR", r"\bor\b"),
            ("AND", r"\band\b"),
            ("MODULO", r"\bmod\b"),
            ("TRUE", r"\bTrue\b"),
            ("FALSE", r"\bFalse\b"),

            #types 
            ("INTEGER_TYPE", r"\bInteger\b"),
            ("BOOLEAN_TYPE", r"\bBoolean\b"),

            #terms 
            ("INTEGER", r"[0-9]+"),
            ("ID", r"[a-zA-Z_][a-zA-Z0-9_]*"),

            #etc 
            ("SKIP", r"[ \t\n]+"),
            ("MISMATCH", r".")
         
        ]
        self.token_regex = re.compile(
            "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in self.token_specs)
        )

    def tokenize(self) -> List[Tuple[str, str]]:
        """
        Tokenizes the input code into a list of tokens.
        Each token is represented as a tuple (token_type, token_value).
        """
        for mo in self.token_regex.finditer(self.code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == "SKIP":
                continue
            elif kind == "MISMATCH":
                raise RuntimeError(f"Unexpected character: {value}")
            else:
                self.tokens.append((kind, value))
        self.tokens.append(("EOF", ""))  # End-of-file token
        return self.tokens


class Parser:
    def __init__(self, tokens: List[Tuple[str, str]]):
        self.tokens = tokens
        self.pos = 0  # Current position in the token list
        self.scopes = [{}]
        self.valid = True 

    def current_token(self) -> Tuple[str, str]:
        # Returns the current token without consuming it
        return self.tokens[self.pos]

    def advance(self) -> None:
        # Advances to the next token
        self.pos += 1

    def expect(self, token_type: str) -> Tuple[str, str]:
        # Consumes the current token if it matches the expected type and returns it
        current_type, current_value = self.current_token()
        if current_type == token_type:
            self.advance()
            return (current_type, current_value)
        else:
            raise RuntimeError(
                f"Expected token type {token_type}, got type {current_type}"
            )
        
    def enter_scope(self) -> None: 
        self.scopes.append({})
    
    def exit_scope(self) -> None: 
        if len(self.scopes) > 1:
            self.scopes.pop()
    
    def declare(self, name, var_type) -> bool:
        current_scope = self.scopes[-1]
        if name in current_scope:
            self.valid = False 
            return False 
        current_scope[name] = var_type 
        return True 
    
    def lookup(self, name): 
        for scope in reversed(self.scopes):
            if name in scope: 
                return scope[name]
        self.valid = False 
        return None 

    def parse(self) -> ASTNode:
        block = self.parse_block()
        self.expect("EOF")
        if not self.valid: 
            return Error()
        return block

    def parse_block(self) -> Block:
        #put statements in a list: <stmt>*
        statements = [] 
        #statement keywords: <assign-stmt> | <put-stmt> | <if-stmt> | (<while-loop> | <for-loop> | <decl-stmt>)
        while self.current_token()[0] in ["ID", "PUT", "IF", "WHILE", "FOR", "VAR"]:
            statements.append(self.parse_statement())
        return Block(statements)

    def parse_statement(self) -> Union[Assign, Put, If, WhileLoop, ForLoop]:
        if self.current_token()[0] == "ID": 
            return self.parse_assign_stmt() 
        elif self.current_token()[0] == "PUT":
            return self.parse_put_stmt() 
        elif self.current_token()[0] == "IF": 
            return self.parse_if_stmt() 
        elif self.current_token()[0] == "WHILE":
            return self.parse_while_loop() 
        elif self.current_token()[0] == "FOR": 
            return self.parse_for_loop()  
        elif self.current_token()[0] == "VAR":
            return self.parse_decl_stmt()

    #statements
    #<assign-stmt> ::= <id> ':=" <expr> ";"
    def parse_assign_stmt(self) -> Assign: 
        id = self.expect("ID")[1]
        self.expect("ASSIGN")
        expr = self.parse_expr() 
        self.expect("SEMICOLON")

        if self.lookup(id) != self.get_type(expr):
            self.valid = False 

        return Assign(Identifier(id), expr)
    
    #<put-stmt> ::== "Put" "(" <expr> ")" ";"
    def parse_put_stmt(self) -> Put:
        self.expect("PUT")
        self.expect("LEFT_BRACKET")
        expr = self.parse_expr() 
        self.expect("RIGHT_BRACKET")
        self.expect("SEMICOLON")
        return Put(expr)
    
    #<if-stmt> ::== "if" <expr> "then" <block> ("else" <block>)? "end" "if" ";"
    def parse_if_stmt(self) -> If:
        self.expect("IF")
        expr = self.parse_expr()

        if self.get_type(expr) != "Boolean":
            self.valid = False
        
        self.expect("THEN")

        self.enter_scope()
        then_block = self.parse_block() 
        self.exit_scope()

        else_block = None
        if self.current_token()[0] == "ELSE": 
            self.expect("ELSE")
            self.enter_scope()
            else_block = self.parse_block() 
            self.exit_scope()
        self.expect("END") 
        self.expect("IF")
        self.expect("SEMICOLON")
        return If(expr, then_block, else_block)

    #<while-loop> ::== "while" <expr> "loop" <block> "end" "loop" ";"
    def parse_while_loop(self) -> WhileLoop:
        self.expect("WHILE")
        expr = self.parse_expr()

        if self.get_type(expr) != "Boolean":
            self.valid = False

        self.expect("LOOP")
        self.enter_scope()
        block = self.parse_block() 
        self.exit_scope()
        self.expect("END")
        self.expect("LOOP")
        self.expect("SEMICOLON")
        return WhileLoop(expr, block)

    #<for-loop> ::== "for" <expr> "loop" <block> "end" "loop" ";"
    def parse_for_loop(self) -> ForLoop:
        self.expect("FOR")
        id = self.expect("ID")[1]
        self.expect("IN")
        start_expr = self.parse_expr() 
        self.expect("RANGE")
        end_expr = self.parse_expr()

        if self.lookup(id) != "Integer" or self.get_type(start_expr) != "Integer" or self.get_type(end_expr) != "Integer":
            self.valid = False 

        self.expect("LOOP")
        self.enter_scope()
        block = self.parse_block() 
        self.exit_scope()
        self.expect("END")
        self.expect("LOOP")
        self.expect("SEMICOLON")
        return ForLoop(Identifier(id), start_expr, end_expr, block)

    #<decl-stmt> ::= "var" <id> ":" <type> (":=" <expr>)? ":"
    def parse_decl_stmt(self) -> Decl: 
        self.expect("VAR")
        id = self.expect("ID")[1]
        self.expect("COLON")
        
        if self.current_token()[0] == "INTEGER_TYPE":
            type_val = "Integer"
            type_node = Type("Integer")
            self.advance() 
        elif self.current_token()[0] == "BOOLEAN_TYPE":
            type_val = "Boolean"
            type_node = Type("Boolean")
            self.advance() 
        
        expr = None 
        if self.current_token()[0] == "ASSIGN":
            self.expect("ASSIGN")
            expr = self.parse_expr()
            if self.get_type(expr) != type_val:
                self.valid = False
        
        self.declare(id, type_val)
        self.expect("SEMICOLON")
        return Decl(Identifier(id), type_node, expr)

    #expressions
    #<expr> ::== <conjunction> ("or" <conjunction>)*
    def parse_expr(self):
        conjunctions = [self.parse_conjunction()]
        while self.current_token()[0] == "OR": 
            self.expect("OR")
            conjunctions.append(self.parse_conjunction())
        if len(conjunctions) == 1: 
            return conjunctions[0]
        else:
            return Or(conjunctions)
    
    #<conjunction> ::= <comparison> ("and" <comparison>)*
    def parse_conjunction(self):
        comparisons = [self.parse_comparison()]
        while self.current_token()[0] == "AND": 
            self.expect("AND")
            comparisons.append(self.parse_comparison())
        if len(comparisons) == 1: 
            return comparisons[0]
        else:
            return And(comparisons)
    
    #<comparison> ::= <term> (("=" | "/=" | "<" | ">" | "<=" | ">=" <term>))?
    def parse_comparison(self): 
        left_term = self.parse_term()
        if self.current_token()[0] in ["EQ", "NEQ", "LT", "GT", "LEQ", "GEQ"]:
            op = self.current_token()[1] 
            self.advance() 
            right_term = self.parse_term()
            return Comparison(left_term, op, right_term)
        return left_term
    
    #terms 
    #<term> ::= <factor> (("+"|"-") <factor>)*
    def parse_term(self): 
        factor = [self.parse_factor()]
        op = [] 
        while self.current_token()[0] in ["PLUS", "MINUS"]: 
            op_val = self.current_token()[1]
            self.advance() 
            op.append(op_val)
            factor.append(self.parse_factor())
        if len(op) == 0: 
            return factor[0]
        else:
            return Term(factor, op)

    #factor ::= <primary> (("*" | "/" | "mod") <primary>)   
    def parse_factor(self): 
        primary = [self.parse_primary()]
        op = [] 
        while self.current_token()[0] in ["MULTIPLY", "DIVIDE", "MODULO"]: 
            op_val = self.current_token()[1]
            self.advance() 
            op.append(op_val)
            primary.append(self.parse_primary())
        if len(op) == 0: 
            return primary[0]
        else:
            return Factor(primary, op)
        
    def parse_primary(self): 
        if self.current_token()[0] == "INTEGER": 
            tok = self.current_token()[1]
            self.advance()
            return Integer(tok)
        if self.current_token()[0] in ["TRUE", "FALSE"]: 
            tok = self.current_token()[1]
            self.advance()
            return Boolean(tok)
        if self.current_token()[0] == "ID": 
            self.lookup(self.current_token()[1])
            tok = self.current_token()[1]
            self.advance()
            return Identifier(tok)
        if self.current_token()[0] == "LEFT_BRACKET": 
            self.expect("LEFT_BRACKET")
            expr = self.parse_expr() 
            self.expect("RIGHT_BRACKET")
            return expr
        
    def get_type(self, node): 
        if type(node) == Integer: 
            return "Integer" 
        elif type(node) == Boolean:
            return "Boolean"
        elif type(node) == Identifier: 
            return self.lookup(node.name)
        elif type(node) == Term: 
            for factor in node.factors: 
                if self.get_type(factor) != "Integer":
                    self.valid = False 
                    return None 
            return "Integer"
        elif type(node) == Factor: 
            for primary in node.primaries: 
                if self.get_type(primary) != "Integer": 
                    self.valid = False 
                    return None 
            return "Integer"
        elif type(node) == Comparison:
            if self.get_type(node.left) == "Integer" and self.get_type(node.right) == "Integer": 
                return "Boolean"
            self.valid = False 
            return None 
        elif type(node) == And: 
            for comparison in node.comparisons: 
                if self.get_type(comparison) != "Boolean": 
                    self.valid = False 
                    return None 
            return "Boolean"
        elif type(node) == Or: 
            for comparison in node.conjunctions: 
                if self.get_type(comparison) != "Boolean": 
                    self.valid = False 
                    return None 
            return "Boolean"
        
    # More parsing methods as needed
