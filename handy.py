from blessed import Terminal
from signal import signal, SIGWINCH
from datetime import datetime
from enum import Enum
import re 

term = Terminal()
command_history = []

class Pattern(Enum):
    Arithemtic = 1,
    ArithmeticWithComment = 2

class Operator(Enum):
    NotAnOperator = 0,
    Addition = 1,
    Subtraction = 2

def resize_handler(signum, frame):
    """handles terminal resize"""
    redraw(term)

def redraw(term):
    """Redraw the screen"""
    print(term.clear)
    print(term.move_y(0) + term.center("Handy"))

    cursor_y = 1
    for command in command_history:
        print(term.move_y(cursor_y) + command)
        cursor_y+=1

def h2d(hex_str):
    return (int(hex_str,16))

def h2b(hex_str):
    return (bin(int(hex_str,16)))

def d2b(dec_str):
    return (bin(int(dec_str, 10)))

def d2h(dec_str):
    return (hex(int(dec_str,10)))

def b2h(bin_str):
    return (hex(int(bin_str,2)))

def b2d(bin_str):
    return (int(bin_str,2))

def parse_operator(input_str):
    if input_str == '+':
        return Operator.Addition
    
    if input_str == "-":
        return Operator.Subtraction
    
    return Operator.NotAnOperator

def full_match(reg_pattern, input_str):
    match = re.match(reg_pattern, input_str)
    return match and match.end() == len(input_str)

def is_hex(input_str):
    return full_match("[a-f0-9]+",input_str.lower())

def is_binary(input_str):
    return full_match("[0-1]+", input_str.lower())

def is_decimal(input_str):
    return full_match("[0-9]+", input_str.lower())

def is_numeric(input_str):
    lc_input = input_str.lower()
    if lc_input.startswith('0x') or lc_input.startswith('0b'):
        return True
    return is_decimal(input_str)

def parseNumericValue(valueStr):
    lc_val = valueStr.lower()
    radix = 10;

    if (lc_val.startswith('0x')):
        if is_hex(lc_val[2:]):
            radix = 16
        else:
             return "Invalid Hex Number"
    
    if (lc_val.startswith('0b')):
        if is_binary(lc_val[2:]):
            radix = 2
        else:
            return "Invalid Binary Number"

    if radix == 10 and is_decimal(lc_val) == False:
        return "Invalid Decimal Number"

    parse_funcs = {16: [h2d, h2b], 10: [d2h, d2b], 2: [b2d, b2h]}

    return str(parse_funcs[radix][0](lc_val)) + ", " + str(parse_funcs[radix][1](lc_val))

def eval(inputStr):
    split_input = inputStr.split()
    outputStr = datetime.now().strftime("%d/%m/%y %H:%M:%S") +": "

    # there are only really two options, either an input string is a numeric operation
    # (meaning it starts with a numeric), or it's a string that we just write to the log
    if is_numeric(split_input[0]):
        if len(split_input) == 1: #if there's only 1 numeric value, just convert it
            outputStr += split_input[0] + " -> "
            outputStr += parseNumericValue(split_input[0])
        else: # otherwise we might have an arithmetic expression, or an inline comment, or both
            outputStr += inputStr
    else: #if the first input isn't numeric, it's just a string
        outputStr += inputStr
        
    command_history.append(outputStr)

def main():
    signal(SIGWINCH, resize_handler)
    with term.fullscreen():
        while 1 :
            redraw(term)
            eval(input(term.move_y(term.height) + "Handy: "))


if __name__ == "__main__":
    main()