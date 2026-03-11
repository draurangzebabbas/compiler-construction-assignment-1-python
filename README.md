# Compiler Construction: Assignment 1
## Project: Robust Lexical Analyzer for MiniLang

### 📋 Student Information
- **Name:** Aurangzeb Abbas
- **Roll No:** S23NDOCS1M01044
- **Program:** BS Computer Science (BsCs)
- **Semester:** Spring 2026

### 🎓 Submission Details
- **Assignment:** #1 - Lexical Analyzer Design & Implementation
- **Course:** Compiler Construction
- **Submitted To:** Iffat Maa'am
- **Submission Date:** March 11, 2026

---

## 🚀 Project Overview
This project involves the design and implementation of a robust **Lexical Analyzer (Scanner)** for a proprietary C-like language called **MiniLang**. The scanner reads source code, identifies various tokens based on predefined regular expressions, constructs a symbol table, and handles lexical errors gracefully.

### Key Features
- **Token Identification:** Keywords, Identifiers, Operators, Literals (String, Char, Float, Int), and Symbols.
- **Error Detection:** Reports invalid characters and illegal identifier patterns (e.g., `9var`) with line and column tracking.
- **Symbol Table:** Automatically populates a table with unique identifiers and literals found in the code.
- **Comment Handling:** Supports both single-line (`//`) and multi-line (`/* ... */`) comments.
- **CLI Dashboard:** An interactive menu to view token streams, statistical summaries, and cleaned source code.

---

## 📁 File Structure
- `lexer.py`: The core Python implementation of the lexical analyzer.
- `test.mini`: Sample MiniLang source file used for testing.
- `tokens.txt`: Output file containing the generated token stream.
- `symbol_table.txt`: Output file containing the constructed symbol table.
- `Report.md`: A technical report detailing regex patterns and the scanner's flow logic.
- `README.md`: This documentation file.

---

## 🛠️ How to Run
1. Ensure you have **Python 3.x** installed on your system.
2. Place your MiniLang code in `test.mini`.
3. Run the following command in your terminal:
   ```bash
   python lexer.py
   ```
4. Follow the on-screen menu to explore the analysis results.

---

## 📊 Token Specification
| Category | Pattern / Examples |
| :--- | :--- |
| **Keywords** | `int`, `float`, `char`, `if`, `else`, `for`, `while`, `return`, etc. |
| **Identifiers** | `[A-Za-z_][A-Za-z0-9_]*` (e.g., `counter`, `_val`) |
| **Literals** | `"String"`, `'c'`, `3.14`, `100` |
| **Operators** | `++`, `==`, `>=`, `&&`, `||`, `+=`, etc. |
| **Symbols** | `(`, `)`, `{`, `}`, `[`, `]`, `,`, `;` |

---

## 🛡️ Error Handling
The lexer identifies and reports:
- **Invalid Characters:** Symbols not recognized by the MiniLang specification (e.g., `@`, `#`).
- **Invalid Identifiers:** Identifiers starting with a digit (e.g., `1variable`).
- **Contextual Tracking:** Each error includes the exact line and column number for easy debugging.

---
**Developed by Aurangzeb Abbas** 🎓
