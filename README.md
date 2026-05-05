Assembler Case Study (Hack Assembly to Binary Translator)

📌 Overview

This project is a case study focused on building an assembler for the Hack computer platform.
It converts Hack assembly language (".asm") programs into binary machine code (".hack").

The implementation is based on concepts of system-level programming and assembly translation discussed during classroom sessions.

---

🎯 Objectives

- To understand low-level programming concepts
- To implement an assembler for Hack architecture
- To translate assembly instructions into binary machine code
- To handle symbols, labels, and variables

---

⚙️ Features

- Converts ".asm" files into ".hack" binary files
- Supports:
  - A-instructions ("@value")
  - C-instructions ("dest=comp" and "comp;jump")
- Handles:
  - Predefined symbols (SP, LCL, R0–R15, etc.)
  - Labels "(LOOP)"
  - Variables (allocated dynamically)
- Removes comments and unnecessary whitespace
- Generates 16-bit binary instructions

---

🛠️ Technologies Used

- Python
- File handling
- Dictionaries for symbol tables

---

🧠 Concepts Applied

- Assembly language parsing
- Symbol table management
- Binary encoding
- String manipulation
- Two-pass assembler logic
- Control flow handling (labels and jumps)

---

📂 Project Structure

Assembler_Case_Study/
│
├── hack_assembler.py     # Main assembler implementation
├── ASM_Programs/
│   ├── add/
│   │   └── Add.asm
│   ├── max/
│   │   └── Max.asm
│   └── ...               # Other test programs
├── README.md

---

▶️ How It Works

🔹 Step 1: Preprocessing

- Reads ".asm" file
- Removes comments ("//")
- Removes empty lines

🔹 Step 2: Label Handling

- Identifies labels "(LABEL)"
- Stores them with correct instruction addresses

🔹 Step 3: Instruction Translation

A-instruction ("@value")

- Converts:
  - Numbers → binary directly
  - Symbols → resolved using symbol table

C-instruction

- "dest=comp" → uses "comp", "dest", "jump" tables
- "comp;jump" → encodes jump instructions

🔹 Step 4: Output

- Generates ".hack" file
- Each instruction is 16-bit binary

---

▶️ How to Run

1. Place your ".asm" file in the project directory
2. Update file path in code (if needed):

filename = r"C:\Assembler_case_study\ASM_Programs\add\Add.asm"

3. Run the program:

python hack_assembler.py

---

📷 Output

- Generates a ".hack" file in the same directory
- Example:

Add.asm → Add.hack

---

📚 Example Translation

Assembly:

@2
D=A
@3
D=D+A

Binary Output:

0000000000000010
1110110000010000
0000000000000011
1110000010010000

---

📚 Conclusion

This project demonstrates how high-level assembly instructions are translated into machine-level binary code. It provides a strong foundation in computer architecture, compilers, and low-level system design.

---

👨‍🏫 Acknowledgement

This case study was developed based on concepts and guidance provided during classroom sessions by the instructor.
