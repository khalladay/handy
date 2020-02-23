from blessed import Terminal
from datetime import datetime
import re 

term = Terminal()
command_history = []
cur_input = ""

# only redraws cur input to prevent flickering, triggers full redraw if curinput needs to grow to another line
def redraw_curinput(term, last_linecount):
    trimmed_input = cur_input.replace("\n", "")
    input_len = len(trimmed_input)

    input_lines = int(input_len / term.width) + 1
    if input_lines != last_linecount:
        redraw(term)
    else:
        output_len = len("> ") + input_len
        space_to_clear = term.width - output_len

        output = trimmed_input
        for i in range(0, space_to_clear):
            output += " "

    print(term.move_xy(0,term.height-input_lines) + "> "+ output, end="", flush=True)
    print(term.move_xy(input_len+2,term.height-input_lines),end="", flush=True)
    return input_lines

def redraw(term):
    """Redraw the screen"""
    print(term.clear)

    input_lines = int(len(cur_input.replace("\n", "")) / term.width) + 1
    print(term.move_y(term.height-input_lines) + "> "+ cur_input.replace("\n", ""), end="", flush=False)
    cursor_y = term.height - input_lines-1

    first_command = True
    for command in reversed(command_history):
        if command == "\n":
            continue
        cmd_string = command.replace("\n", "")

        string_len = len(cmd_string)
        string_height = int(string_len / term.width) +1
        
        #handle truncating multi line blocks near the top of visible history
        shows_date = True
        if cursor_y < string_height:
            diff = string_height-cursor_y
            line_len = term.width
            cmd_string = cmd_string[line_len*(diff)+1:]
            string_height -= diff
            shows_date = False

        if string_height > 1:
            cursor_y -= string_height-1
        
        if first_command:
            print(term.move_xy(0,cursor_y) + term.reverse(cmd_string))
            first_command = False
        else:
            if shows_date:
                print(term.move_y(cursor_y) + term.bright_red(cmd_string[0:18]) + cmd_string[18:], flush=False)
            else:
                print(term.move_y(cursor_y) + cmd_string, flush=False)
        cursor_y-=1
    
        if cursor_y <= 0:
            break

    print(term.move_y(0) + term.center("Handy"), flush=False)
    print(term.move_yx(term.height-2, 0), flush=True)

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
    if lc_input.startswith('0x') and is_hex(lc_input[2:]):
        return len(lc_input) > 2
    if lc_input.startswith('0b') and is_binary(lc_input[2:]):
        return len(lc_input) > 2
    return is_decimal(input_str)

def convert_to_decimal(val):
    if is_decimal(val):
        return (int(trim_prefix(val)))
    if val.startswith("0x") and is_hex(trim_prefix(val)):
        return (h2d(trim_prefix(val)))
    if val.startswith("0b") and is_binary(trim_prefix(val)):
        return (b2d(trim_prefix(val)))

def parse_numeric(value_str):
    lc_val = value_str.lower()
    radix = 10

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

def trim_prefix(val):
    if val.startswith("0x"):
        return val[2:]
    if val.startswith("0b"):
        return val[2:]
    return val

def parseNumericValue(valueStr):
    lc_val = valueStr.lower()
    radix = 10

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

def parse_input_pattern(split_input, input_str):
    #first we need to mark when a comment is added (if it is), since anything after that is moot
    comments_start = len(split_input)
    str_idx = 0
    for cur_str in split_input:
        if cur_str.startswith('//'):
            comments_start = str_idx
            break
        str_idx +=1

    input_str_comment_start = input_str.find("//")
    if input_str_comment_start == -1:
        input_str_comment_start = len(input_str)

    for i in range(1, comments_start-1):
        cur_str = split_input[i]
        if cur_str == "+":
            left = (split_input[i-1])
            right = (split_input[i+1])
            split_input[i] = (convert_to_decimal(left) + convert_to_decimal(right))

            if left.startswith("0x") and is_hex(trim_prefix(left)):
                hex_val = hex(int(split_input[i]))
                split_input[i] = str(hex_val)
            elif left.startswith("0b") and is_binary(trim_prefix(left)):
                bin_val = bin(int(split_input[i]))
                split_input[i] = str(bin_val)
            else:
                split_input[i] = str(split_input[i])

            del split_input[i-1]
            del split_input[i]
            comments_start -=2
            i -= 1
        if cur_str == "-":
            left = (split_input[i-1])
            right = (split_input[i+1])
            split_input[i] = (convert_to_decimal(left) - convert_to_decimal(right))

            if left.startswith("0x") and is_hex(trim_prefix(left)):
                hex_val = hex(int(split_input[i]))
                split_input[i] = str(hex_val)
            elif left.startswith("0b") and is_binary(trim_prefix(left)):
                bin_val = bin(int(split_input[i]))
                split_input[i] = str(bin_val)
            else:
                split_input[i] = str(split_input[i])

            del split_input[i-1]
            del split_input[i]
            comments_start -=2
            i -= 1

    out_str = input_str[0:input_str_comment_start] + " -> "
    for cur_str in split_input:
        out_str += cur_str + " "

    return out_str

def eval(input_str):    
    if len(input_str) == 0:
        return

    input_str = input_str.replace("+", " + ")
    input_str = input_str.replace("-", " - ")

    split_input = input_str.split()

    output_str = datetime.now().strftime("%d/%m/%y %H:%M:%S") +": "
    # there are only really two options, either an input string is a numeric operation
    # (meaning it starts with a numeric), or it's a string that we just write to the log
    if is_numeric(split_input[0]):
        if len(split_input) == 1: #if there's only 1 numeric value, just convert it
            output_str += split_input[0] + " -> "
            output_str += parseNumericValue(split_input[0])
        else: # otherwise we might have an arithmetic expression, or an inline comment, or both
            output_str += parse_input_pattern(split_input, input_str)
    else: #if the first input isn't numeric, it's just a string
        output_str += input_str
        
    return output_str

def resume_session(log_file):
    log_file.seek(0)
    line = log_file.readline()
    while line:
        command_history.append(line)
        line = log_file.readline()

def log(resolved_cmd, log_file):
    if resolved_cmd is None:
        return

    command_history.append(resolved_cmd)
    log_file.write(resolved_cmd + "\n\n")

def main():
    last_size_x = 0
    last_size_y = 0
    last_curinput_linecount = 1

    with open("handy.txt", "a+") as handy_file:
        resume_session(handy_file)
        try:
            with term.fullscreen(), term.cbreak():
                while 1:
                        val = term.inkey(0.5)
                        global cur_input
                        cur_input += str(val)
                        if cur_input.endswith("\n"):
                            log(eval(cur_input.replace("\n", "")), handy_file)
                            cur_input = ""
                            redraw(term)
                            last_curinput_linecount = 1
                            continue
                        elif val.name == 'KEY_BACKSPACE' :
                            cur_input = cur_input[0:len(cur_input)-2]
                        
                        if val:
                            last_curinput_linecount = redraw_curinput(term, last_curinput_linecount)

                        if last_size_x != term.width or last_size_y != term.height:
                            redraw(term)
                            last_size_x = term.width
                            last_size_y = term.height

        except(KeyboardInterrupt, SystemExit):
            exit(0)


if __name__ == "__main__":
    main()