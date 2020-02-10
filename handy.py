from blessed import Terminal
from signal import signal, SIGWINCH
from datetime import datetime
import re 

term = Terminal()
command_history = []

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

def parseNumericValue(valueStr, radix, regex_pattern):
    lc_val = valueStr.lower()
    reg_match = re.match(regex_pattern, lc_val)

    parse_funcs = {16: [h2d, h2b], 10: [d2h, d2b], 2: [b2d, b2h]}

    if reg_match and reg_match.end() == len(lc_val):
        return str(parse_funcs[radix][0](lc_val)) + ", " + str(parse_funcs[radix][1](lc_val))
    else:
        return "Invalid Hex Input" if radix == 16 else "Invalid Binary Input" if radix == 2 else "Invalid Decimal Input"

def eval(inputStr):
    split_input = inputStr.split()
    outputStr = datetime.now().strftime("%d/%m/%y %H:%M:%S") +": "

    if len(split_input) == 1:
        lc_input = split_input[0].lower()

        if lc_input.startswith('0x'):
            outputStr += split_input[0] + " -> "
            outputStr += parseNumericValue(lc_input[2:], 16, "[a-f0-9]+")

        elif lc_input.startswith('0b'):
            outputStr += split_input[0] + " -> "
            outputStr += parseNumericValue(lc_input[2:], 2, "[0-1]+")
        else:
            reMatch = re.match("[0-9]+", lc_input)
            if reMatch and reMatch.end() == len(lc_input):
                outputStr += split_input[0] + " -> "
                outputStr += parseNumericValue(lc_input, 10, "[0-9]+")
            else:
                outputStr += inputStr
    else:
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