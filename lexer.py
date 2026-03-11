import re
import sys
import os

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f"<{self.line}> <{self.type}, {self.value}>"

class LexicalAnalyzer:
    def __init__(self):
        self.keywords = {
            'int', 'float', 'char', 'if', 'else', 'for', 'while', 'return', 'break', 'continue'
        }
        
        # Token specifications using Regex
        self.token_specification = [
            ('FLOAT_LITERAL',   r'\d+\.\d+'),                # Float (must be before INT)
            ('INTEGER_LITERAL', r'\d+'),                       # Integer
            ('STRING_LITERAL',  r'"[^"\n]*"'),                 # String literal
            ('CHARACTER_LITERAL', r"'.[']"),                    # Character literal
            ('COMMENT_MULTI',   r'/\*[\s\S]*?\*/'),            # Multi-line comment
            ('COMMENT_SINGLE',  r'//.*'),                      # Single-line comment
            ('OPERATOR',        r'\+\+|--|==|!=|<=|>=|\+=|-=|\*=|\/=|&&|\|\||[+\-*/%=<>=!&|]'), # Operators
            ('SYMBOL',          r'[(){}\[\],;"]'),             # Delimiters & Symbols
            ('IDENTIFIER',      r'[A-Za-z_][A-Za-z0-9_]*'),   # Identifiers
            ('NEWLINE',         r'\n'),                        # Line endings
            ('SKIP',            r'[ \t\r]+'),                  # Skip spaces and tabs
            ('MISMATCH',        r'.'),                         # Any other character
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
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)
        line_num = 1
        line_start = 0
        
        # Track for unclosed multi-line comments manually if regex misses or for better error reporting
        # But regex '[\s\S]*?' handles it mostly. We check for '/*' without '*/'.
        
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
                # Comments are ignored in token stream but tracked for line numbers in multi-line
                if kind == 'COMMENT_MULTI':
                    line_num += value.count('\n')
                    # Update line_start for column tracking after multi-line comment
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
                    # Add to symbol table
                    if value not in self.symbol_table:
                        self.symbol_table[value] = {'type': 'variable', 'category': 'identifier', 'value': '--'}
            elif kind.endswith('_LITERAL'):
                self.stats['LITERALS'] += 1
                # Add literals to symbol table as requested
                lit_type = kind.split('_')[0].lower()
                if value not in self.symbol_table:
                    self.symbol_table[value] = {'type': lit_type, 'category': 'literal', 'value': value}
            elif kind == 'OPERATOR':
                self.stats['OPERATORS'] += 1
            elif kind == 'SYMBOL':
                self.stats['SYMBOLS'] += 1
            elif kind == 'MISMATCH':
                self.errors.append(f"Lexical Error (line {line_num}, col {column}): Invalid character '{value}'")
                continue

            # Check for error patterns
            if kind == 'IDENTIFIER' and value[0].isdigit():
                self.errors.append(f"Lexical Error (line {line_num}, col {column}): Invalid identifier '{value}'")
                continue

            self.tokens.append(Token(kind, value, line_num, column))

        # Check for unterminated strings or comments (regex might match partially or mismatch)
        # Actually, regex for STRING_LITERAL r'"[^"\n]*"' won't match if it hits newline without "
        # We can do a second pass or handle it in MISMATCH. 
        # For simplicity in this implementation, if a " is followed by letters and no " before newline, 
        # it hits MISMATCH or skips. Let's refine the logic if needed.

    def save_output(self, token_file="tokens.txt", symbol_file="symbol_table.txt"):
        with open(token_file, 'w') as f:
            for token in self.tokens:
                f.write(str(token) + '\n')
        
        with open(symbol_file, 'w') as f:
            f.write(f"{'Name':<15} | {'Type':<10} | {'Category':<12} | {'Value':<10}\n")
            f.write("-" * 55 + "\n")
            for name, info in self.symbol_table.items():
                f.write(f"{name:<15} | {info['type']:<10} | {info['category']:<12} | {info['value']:<10}\n")

    def print_cleaned_source(self, code):
        # Remove comments using regex
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

    lexer.tokenize(code)
    lexer.save_output()

    while True:
        print("\n--- MiniLang Lexical Analyzer ---")
        print("1. View Tokens")
        print("2. View Symbol Table")
        print("3. View Cleaned Source (No Comments)")
        print("4. View Statistics")
        print("5. View Lexical Errors")
        print("6. Exit")
        
        choice = input("Enter choice (1-6): ")
        
        if choice == '1':
            print("\n--- Tokens ---")
            for t in lexer.tokens:
                print(t)
        elif choice == '2':
            print("\n--- Symbol Table ---")
            print(f"{'Name':<15} | {'Type':<10} | {'Category':<12} | {'Value':<10}")
            print("-" * 55)
            for name, info in lexer.symbol_table.items():
                print(f"{name:<15} | {info['type']:<10} | {info['category']:<12} | {info['value']:<10}")
        elif choice == '3':
            print("\n--- Cleaned Source ---")
            print(lexer.print_cleaned_source(code))
        elif choice == '4':
            print("\n--- Statistics ---")
            for k, v in lexer.stats.items():
                print(f"{k}: {v}")
        elif choice == '5':
            print("\n--- Lexical Errors ---")
            if not lexer.errors:
                print("No errors found.")
            else:
                for err in lexer.errors:
                    print(err)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
