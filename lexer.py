# ---------------------------------------------------------
# Assignment: Compiler Construction - Assignment 1
# Student Name: Aurangzeb Abbas
# Roll No: S23NDOCS1M01044
# Class: BsCs
# Submitted to: Iffat Maa'am
# Project: Design and Implement a Robust Lexical Analyzer for MiniLang
# ---------------------------------------------------------

import re
import os

class Token:
    """Represents a single token identified during lexical analysis."""
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        # Format requirements: <LINE X> <TYPE, VALUE>
        return f"<LINE {self.line}>  <{self.type}, {self.value}>"

class LexicalAnalyzer:
    """A lexical analyzer for the MiniLang programming language."""
    def __init__(self):
        self.keywords = {
            'int', 'float', 'char', 'if', 'else', 'for', 'while', 'return', 'break', 'continue'
        }
        
        # Token specifications using Regular Expressions
        self.token_specification = [
            ('COMMENT_MULTI',   r'/\*[\s\S]*?\*/'),            # Multi-line comment
            ('ERROR_COMMENT',   r'/\*[\s\S]*'),                # UNCLOSED Multi-line comment (no matching */)
            ('COMMENT_SINGLE',  r'//.*'),                      # Single-line comment
            ('FLOAT_LITERAL',   r'\d+\.\d+'),                  # Float literal
            ('INVALID_ID',      r'\d+[A-Za-z_][A-Za-z0-9_]*'), # Invalid identifiers like 9var (MUST be before INT)
            ('INTEGER_LITERAL', r'\d+'),                       # Integer literal (must be after FLOAT and INVALID_ID)
            ('STRING_LITERAL',  r'"[^"\n]*"'),                 # String literal
            ('ERROR_STRING',    r'"[^"\n]*'),                  # UNCLOSED String literal
            ('CHARACTER_LITERAL', r"'[^'\n]'"),                # Character literal
            ('OPERATOR',        r'\+\+|--|==|!=|<=|>=|\+=|-=|\*=|\/=|&&|\|\||[+\-*/%=<>=!&|]'), # Operators
            ('SYMBOL',          r'[(){}\[\] ,;]'),              # Delimiters & Symbols
            ('IDENTIFIER',      r'[A-Za-z_][A-Za-z0-9_]*'),    # Valid Identifiers
            ('NEWLINE',         r'\n'),                        # Line endings
            ('SKIP',            r'[ \t\r]+'),                  # Skip whitespace
            ('MISMATCH',        r'.'),                         # Any other character (error)
        ]
        
        self.tokens = []
        self.errors = []
        self.symbol_table = {}  # {name: {type, category, value}}
        self.stats = {
            'KEYWORDS': 0,
            'IDENTIFIERS': 0,
            'LITERALS': 0,
            'OPERATORS': 0,
            'SYMBOLS': 0
        }

    def tokenize(self, code):
        """Processes source code and breaks it into tokens."""
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)
        line_num = 1
        line_start = 0
        
        for mo in re.finditer(tok_regex, code):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start + 1
            
            if kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
                continue
            elif kind == 'SKIP':
                continue
            elif kind == 'COMMENT_SINGLE' or kind == 'COMMENT_MULTI':
                if kind == 'COMMENT_MULTI':
                    line_num += value.count('\n')
                    last_newline = value.rfind('\n')
                    if last_newline != -1:
                        line_start = mo.start() + last_newline + 1
                continue
            elif kind == 'IDENTIFIER':
                if value in self.keywords:
                    kind = 'KEYWORD'
                    self.stats['KEYWORDS'] += 1
                else:
                    self.stats['IDENTIFIERS'] += 1
                    # Add identifiers to symbol table if not present
                    if value not in self.symbol_table:
                        self.symbol_table[value] = {'type': 'variable', 'category': 'identifier', 'value': '--'}
            elif kind.endswith('_LITERAL'):
                self.stats['LITERALS'] += 1
                lit_type = kind.split('_')[0].lower()
                if value not in self.symbol_table:
                    self.symbol_table[value] = {'type': lit_type, 'category': 'literal', 'value': value}
            elif kind == 'OPERATOR':
                self.stats['OPERATORS'] += 1
            elif kind == 'SYMBOL':
                self.stats['SYMBOLS'] += 1
            elif kind == 'INVALID_ID':
                self.errors.append(f"Lexical Error (line {line_num}, col {column}): Invalid identifier '{value}'")
                continue
            elif kind == 'ERROR_STRING':
                self.errors.append(f"Lexical Error (line {line_num}, col {column}): Unterminated string literal")
                continue
            elif kind == 'ERROR_COMMENT':
                self.errors.append(f"Lexical Error (line {line_num}, col {column}): Unclosed multi-line comment")
                continue
            elif kind == 'MISMATCH':
                self.errors.append(f"Lexical Error (line {line_num}, col {column}): Invalid character '{value}'")
                continue

            self.tokens.append(Token(kind, value, line_num, column))

    def save_output(self, token_file="tokens.txt", symbol_file="symbol_table.txt"):
        """Saves generated tokens and symbol table to files."""
        with open(token_file, 'w') as f:
            for token in self.tokens:
                f.write(str(token) + '\n')
        
        with open(symbol_file, 'w') as f:
            f.write(f"{'Name':<15} | {'Type':<15} | {'Category':<15} | {'Value':<15}\n")
            f.write("-" * 65 + "\n")
            for name, info in self.symbol_table.items():
                f.write(f"{name:<15} | {info['type']:<15} | {info['category']:<15} | {info['value']:<15}\n")

    def print_cleaned_source(self, code):
        """Returns the source code with all comments removed."""
        cleaned = re.sub(r'//.*', '', code)
        cleaned = re.sub(r'/\*[\s\S]*?\*/', '', cleaned)
        return cleaned

def main():
    lexer = LexicalAnalyzer()
    input_file = 'test.mini'
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    with open(input_file, 'r') as f:
        code = f.read()

    print(f"\nProcessing file: {input_file}...")
    lexer.tokenize(code)
    lexer.save_output()
    print("Tokens saved to tokens.txt")
    print("Symbol table saved to symbol_table.txt")

    while True:
        print("\n" + "="*40)
        print("   MiniLang Lexical Analyzer CLI   ")
        print("="*40)
        print("1. View Token Stream")
        print("2. View Symbol Table")
        print("3. View Cleaned Source (No Comments)")
        print("4. View Statistical Summary")
        print("5. View Error Log")
        print("6. Exit")
        print("="*40)
        
        choice = input("Select an option (1-6): ")
        
        if choice == '1':
            print("\n>>> Token Stream:")
            for t in lexer.tokens:
                print(t)
        elif choice == '2':
            print("\n>>> Symbol Table:")
            print(f"{'Name':<15} | {'Type':<15} | {'Category':<15} | {'Value':<15}")
            print("-" * 65)
            for name, info in lexer.symbol_table.items():
                print(f"{name:<15} | {info['type']:<15} | {info['category']:<15} | {info['value']:<15}")
        elif choice == '3':
            print("\n>>> Cleaned Source Code:")
            print(lexer.print_cleaned_source(code))
        elif choice == '4':
            print("\n>>> Analysis Statistics:")
            for k, v in lexer.stats.items():
                print(f"{k:<15}: {v}")
        elif choice == '5':
            print("\n>>> Lexical Error Log:")
            if not lexer.errors:
                print("Success: No lexical errors detected.")
            else:
                for err in lexer.errors:
                    print(err)
        elif choice == '6':
            print("Shutting down Lexical Analyzer...")
            break
        else:
            print("Error: Invalid selection. Please choose 1-6.")

if __name__ == "__main__":
    main()
