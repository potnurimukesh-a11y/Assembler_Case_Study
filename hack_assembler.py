
comp = {'0': "1110101010", '1':'1110111111', '-1':'1110111010','D':'1110001100','A':'1110110000','!D':'1110001101','!A':'1110110001',
        '-D':'1110001111','-A':'1110110011','D+1': '1110011111','A+1':'1110110111','D-1':'1110001110','A-1':'1110110010','D+A':'1110000010',
        'D-A':'1110010011','A-D':'1110000111','D&A':'1110000000','D|A':'1110010101','M':'1111110000','!M':'1111110001','M+1':'1111110111',
        'M-1':'1111110010','D+M':'1111000010','D-M':'1111010011','M-D':'1111000111','D&M':'1111000000','D|M':'1111010101'}

dest = {'null':'000',"M": "001","D": "010","MD": "011","A": "100","AM": "101","AD": "110","AMD": "111"}

jump= {
    'null': "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

symbol_table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,

    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,

    "SCREEN": 16384,
    "KBD": 24576
}

looping_list = {}


def loop_lines(refined_lines):
    '''
    This loop scans through the refined assembly instructions to identify label
    declarations in Hack assembly.

    Labels are written in the format (LABEL) and represent symbolic addresses
    used for jumps and branching.

    Process:
    1. Iterate through all instructions in refined_lines.
    2. Print each instruction and its index for debugging.
    3. Check if the instruction starts with '(' indicating a label.
    4. Extract the label name from between '(' and ')'.
    5. Store the label in the dictionary `looping_list` with its corresponding
    instruction address.

    Since label declarations do not translate into machine instructions,
    their address is adjusted by subtracting the number of labels already
    encountered (i - len(looping_list)).
    '''
    for i, line in enumerate(refined_lines):

        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]
            looping_list[label] = i - len(looping_list)

    return looping_list


def get_address(address, address_dict, obj):

    if address_dict.get(obj, 'None') != 'None':
        return address, address_dict[obj]

    elif looping_list.get(obj, 'None') != 'None':
        return address, looping_list[obj]
    else:
        address_dict[obj] = address
        return address+1, address


def convert_attherate(address, obj, address_dict):
    '''
    This block determines the binary address for an A-instruction (@value).

    Process:
    1. Check if the symbol exists in the label table (looping_list).
    If present, return its stored ROM address in 16-bit binary format.

    2. If not found in labels, check the predefined symbol table (symbol_table).
    If present, return the corresponding address in 16-bit binary.

    3. If the value is an alphabetic string, it represents a new variable.
    Allocate the next available RAM address (starting from 16) and
    return its 16-bit binary representation.

    4. Otherwise, treat the value as a numeric constant and convert it
    directly to a 16-bit binary number.
    '''

    if obj in looping_list:
        return address, format(looping_list[obj], '016b')

    elif obj in symbol_table:
        return address, format(symbol_table[obj], '016b')

    elif obj.isalpha():
        address, value = get_address(address, address_dict, obj)
        return address, format(value, '016b')

    else:
        return address, format(int(obj), '016b')


def assembly_2_binary(refined_lines):
    binary_lines = []
    '''
    This block converts cleaned Hack assembly instructions (refined_lines)
    into their corresponding binary machine code instructions.

    address = 16
    Starting memory address for variables in Hack architecture.

    address_dict
    A dictionary used as a symbol table to store variable names
    and their allocated memory addresses.

    binary_lines
    A list that stores the final translated binary instructions.

    For each line in refined_lines:

    1. A-instruction (@value)
        - If the line starts with '@', it represents an address instruction.
        - get_address() resolves the symbol or variable address.
        - convert_attherate() converts the address into 16-bit binary.

    2. C-instruction (dest=comp)
        - Splits the instruction using '='.
        - Looks up binary codes for computation (comp) and destination (dest).
        - Jump bits are set to '000'.

    3. C-instruction (comp;jump)
        - Splits the instruction using ';'.
        - Looks up computation (comp) and jump bits from dictionaries.
        - Destination bits are set to '000'.

    Each translated instruction is appended to binary_lines with a newline.
    '''

    address = 16
    address_dict = {}

    for line in refined_lines:

        if line.startswith("@"):
            obj = line[1:]

            address, binary = convert_attherate(address, obj, address_dict)

            binary_lines.append(binary + "\n")

        elif line.startswith("("):
            continue

        elif "=" in line:
            dest_part, comp_part = line.split("=")

            comp_bits = comp[comp_part]
            dest_bits = dest[dest_part]
            jump_bits = jump["null"]

            binary = comp_bits + dest_bits + jump_bits
            binary_lines.append(binary + "\n")

        elif ";" in line:
            comp_part, jump_part = line.split(";")

            comp_bits = comp[comp_part]
            dest_bits = dest["null"]
            jump_bits = jump[jump_part]

            binary = comp_bits + dest_bits + jump_bits
            binary_lines.append(binary + "\n")

    return binary_lines


def refine_lines(all_lines):
    refined_lines = []
    """
        Processes a list of lines and removes comments and empty lines.

        Steps performed:
        1. Skips lines that start with '//' (full-line comments).
        2. Skips empty lines.
        3. Removes inline comments that appear after '//'.
        4. Strips newline characters and extra spaces.
        5. Stores the cleaned instructions in the list `refined_lines`.

        This is useful for preprocessing assembly/code files before further parsing.
    """

    for line in all_lines:

        line = line.strip()

        if line == "":
            continue

        if line.startswith("//"):
            continue

        if "//" in line:
            line = line.split("//")[0].strip()

        refined_lines.append(line)

    return refined_lines


def extractlines(filename):
    with open(filename,'r') as file_pointer:
        lines = file_pointer.readlines()
    return lines

# def main():
#     file_path = "/Users/cxrlabs/Downloads/nand2tetris/projects/6/max/"
#     #file_path = ""
#     filename = file_path+"Max.asm"
#     all_lines = extractlines(filename)
#     refined_lines = refine_lines(all_lines)
#     print(refined_lines)
#     loop_lines(refined_lines)
#     print(looping_list)
#     binary_lines = assembly_2_binary(refined_lines)
#     with open("Max.hack",'w') as file_pointer:
#         file_pointer.writelines(binary_lines)


# if __name__ == "__main__":
#     main()

if __name__ == "__main__":

    filename = r"C:\Assembler_case_study\ASM_Programs\add\Add.asm"

    all_lines = extractlines(filename)

    refined_lines = refine_lines(all_lines)

    loop_lines(refined_lines)

    binary_lines = assembly_2_binary(refined_lines)

    output_file = filename.replace(".asm", ".hack")

    with open(output_file, "w") as f:
        f.writelines(binary_lines)

    print("Translation complete : ", output_file)