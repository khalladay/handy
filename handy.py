from blessed import Terminal
from datetime import datetime
import math
import re 

term = Terminal()
command_history = []
cur_input = ""

# only redraws cur input to prevent flickering, triggers full redraw if curinput needs to grow to another line
def redraw_curinput(term, last_linecount):
    trimmed_input = cur_input.replace("\n", "").replace("\r", "")
    input_len = len(trimmed_input) +2

    input_lines = int(input_len / term.width) + 1
    if input_lines != last_linecount:
        redraw(term)
        return input_lines
    else:
        output_len = input_len
        space_to_clear = term.width*input_lines - output_len
        
        output = trimmed_input
        for i in range(0, space_to_clear):
            output += " "

    cursor_x = (input_len) % term.width

    print(term.move_xy(0,term.height-input_lines) + "> "+ output, end="", flush=True)
    print(term.move_xy(cursor_x,term.height),end="", flush=True)
    return input_lines

def redraw(term):
    print(term.clear)
    trimmed_input = cur_input.replace("\n", "").replace("\r", "")
    input_len = len(trimmed_input) + len("> ")
    input_lines = int(input_len / term.width) + 1
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
                date_len = len(date_string())
                print(term.move_y(cursor_y) + term.bright_red(cmd_string[0:date_len]) + cmd_string[date_len:], flush=False)
            else:
                print(term.move_y(cursor_y) + cmd_string, flush=False)
        cursor_y-=1
    
        if cursor_y <= 0:
            break

    print(term.move_y(0) + term.center("Handy"), flush=False)

    redraw_curinput(term, input_lines)

def full_match(reg_pattern, input_str):
    match = re.match(reg_pattern, input_str)
    if match is None:
        return False
    return match and match.end() == len(input_str)

def is_hex(input_str):
    return full_match("[a-f0-9]+",input_str.lower())

def is_binary(input_str):
    return full_match("[0-1]+", input_str.lower())

def is_decimal(input_str):
    return full_match("\-?[0-9]+", input_str.lower())

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
        return (int(val,16))
    if val.startswith("0b") and is_binary(trim_prefix(val)):
        return (int(val,2))

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

    out_str = ""
    if radix == 16:
        out_str = str(int(lc_val,16)) + ", " + str(bin(int(lc_val,16)))
    elif radix == 2:
        out_str = str(int(lc_val,2)) + ", " + str(hex(int(lc_val,2)))
    else:
        #if it's a negative integer, we need to convert it first to two's complement, then display hex/binary
        if valueStr[0] == '-':
            pos_int = int(lc_val[1:], 10) #drop the sign
            if pos_int > 2147483648: #if we're outside the range of a 32 bit signed int, bail
                out_str = "Signed Int > 32 bits, Skipping Conversion"
                return out_str
            bin_str_noprefix = format(pos_int, "032b") #format num as a 0 padded 32 bit binary string
            flipped_bin_str = bin_str_noprefix.replace("0", "@").replace("1", "0").replace("@","1") #janky bit flip
            out_val = int(flipped_bin_str, 2) #convert back to int
            out_val +=1
            out_str = format(out_val, "#010x") + ", " + format(out_val, "#034b") #need 34 digits (32 + 2 for "0b")
        else:
            out_str = str(hex(int(lc_val,10))) + ", " + str(bin(int(lc_val, 10)))
    return out_str

def parse_input_pattern(split_input, input_str):
    #first we need to mark when a comment is added (if it is), since anything after that is moot
    comments_start = len(split_input)-1
    str_idx = 0
    for cur_str in split_input:
        if cur_str.startswith('//'):
            comments_start = str_idx
            break
        str_idx +=1

    found_error = False

    input_str_comment_start = input_str.find("//")
    if input_str_comment_start == -1:
        input_str_comment_start = len(input_str)

    for i in range(0, comments_start):
        #comments_start can be modified at loop time
        if i > comments_start:
            break

        cur_str = split_input[i]
        if cur_str == "+" or cur_str == "-" or cur_str == "<<" or cur_str == ">>":

            left = (split_input[i-1])
            right = (split_input[i+1])

            #if one of the operands isn't the right type, just bail on the whole expression
            if is_numeric(left) == False or is_numeric(right) == False:
                found_error = True
                break

            if cur_str == "+":
                split_input[i] = (convert_to_decimal(left) + convert_to_decimal(right))
            elif cur_str == "-":
                split_input[i] = (convert_to_decimal(left) - convert_to_decimal(right))
            elif cur_str == ">>":
                split_input[i] = (convert_to_decimal(left) >> convert_to_decimal(right))
            elif cur_str == "<<":
                split_input[i] = (convert_to_decimal(left) << convert_to_decimal(right))

            if left.startswith("0x") and is_hex(trim_prefix(left)):
                hex_val = hex(int(split_input[i]))
                split_input[i] = str(hex_val)
            elif left.startswith("0b") and is_binary(trim_prefix(left)):
                bin_val = bin(int(split_input[i]))
                # if we are bit shifting a binary left-val, I want to preserve length when right shifting
                if cur_str == "<<" or cur_str == ">>":
                    out_len = len(left)
                    if left[0] == "-" and str(bin_val)[0] != "-":
                        out_len -=1
                    format_str = "#0" + str(out_len) + "b"
                    split_input[i] = format(int(split_input[i]), format_str)
                else: 
                    split_input[i] = str(bin_val)
            else:
                split_input[i] = str(split_input[i])

            del split_input[i-1]
            del split_input[i]
            comments_start -=2
            i -= 1
    

    out_str = input_str

    if found_error == False:
        out_str = input_str[0:input_str_comment_start] + " -> "
        for cur_str in split_input:
            out_str += cur_str + " "

    return out_str

def date_string():
    return datetime.now().strftime("%d/%m/%y %H:%M:%S")

def eval(input_str):    
    if len(input_str) == 0:
        return

    output_str = date_string() +": "


    #handle the "I want to know the char code for this" case
    if input_str.startswith("\'") and input_str.endswith('\'') and len(input_str) == 3:
        output_str += input_str +" -> "+str(ord(input_str[1])) + ", " + str(hex(ord(input_str[1])))
        return output_str


    #expand minus sign so the string splits properly, unless it's the first
    #shar in the string...since then it might be a negative int for conversion
    input_str = input_str.replace("-", " - ")

    if input_str[0:3] == " - ":
        input_str = input_str.replace(" - ", "-", 1)

    input_str = input_str.replace("+", " + ")
    input_str = input_str.replace("<<", " << ")
    input_str = input_str.replace(">>", " >> ")


    split_input = input_str.split()

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
    log_file.flush()

def main():
    last_size_x = 0
    last_size_y = 0
    last_curinput_linecount = 1

    with open("handy.txt", "a+") as handy_file:
        resume_session(handy_file)
        try:
            with term.fullscreen(), term.cbreak():
                while 1:
                        val = term.inkey(1.5)
                        global cur_input
                        
                        if val.isprintable() or val.name == 'KEY_ENTER':
                            cur_input += str(val)
    
                        if cur_input.endswith("\n") or cur_input.endswith("\r"):
                            trimmed_input = cur_input.replace("\n", "").replace("\r", "")
                            log(eval(trimmed_input), handy_file)
                            cur_input = ""
                            redraw(term)
                            last_curinput_linecount = 1
                            continue
                        elif val.name == 'KEY_BACKSPACE' :
                            cur_input = cur_input[0:len(cur_input)-1]
                        
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
