# handy
This is a script that I've started to keep running while I work on pretty much anything. Mostly, it serves the place of a paper log book, or lab notebook, that I use to document my thought processes as I work through problems. It's also useful to keeping track of bash one liners or command line strings that I want to use in the future (ie: the command line to build a specific config of a UE4 project). 

I keep a copy of this script in every project file, so each project has it's own handy.txt. There's no way to rename this file (or move where the script writes to), only because I haven't yet wanted to.

All input to the script is appended to a log file (that the script creates) called "handy.txt." This input is timestamped for easy searching through later. 

![screenshot showing how it handles entering basic text strings](https://github.com/khalladay/handy/blob/master/example_images/text_example.png?raw=true)

## Other Features
My plan is to add more features to this script as I discover common tasks that seem like a good fit. Here's a list of what I've added so far:

### Radix Conversion
If you enter a hex, decimal, or binary string, handy will convert it to the other two radixes for you: 

![screenshot showing how radix conversion works](https://github.com/khalladay/handy/blob/master/example_images/radix_conversion.png?raw=true)

### 2's Complement Conversion
If you enter a negative integer, it will be represented as a 2's complement hex / binary string when converted. This only works within the range of a 32 bit signed int. This conversion only works from negative int -> Hex / Binary, you currently can't input a hex value and convert it to an int assuming it's a 2's complement val. 

![screenshot showing how converting a negative int to 2's complement hex/bin strings works](https://github.com/khalladay/handy/blob/master/example_images/negative_int.png?raw=true))

### Addition/Subtraction
You can also do simple addition / subtraction between two numbers of different radixes (or the same radix, if you want to).

![screenshot showing how addition and subtraction works](https://github.com/khalladay/handy/blob/master/example_images/add_subtract.png?raw=true)

### Bit Shifting
Similar to above, you can compute the result of a bit shift operation using "<<" and ">>" operators between two numeric values. One potentially unexpected behavior with this is that if you right-shift a binary value, handy will left pad the result with zeroes so the result displayed has the same length as the original input being shifted. This behavior does not apply to left shifts (which will add digits to the binary value). 

![screenshot showing how bit shifting works](https://github.com/khalladay/handy/blob/master/example_images/bit_shift.png?raw=true)

### Ascii Value For Single Char
Entering a single char, wrapped in single quotes (ie: 'A') will convert it to an ASCII byte value. You don't need to escape any value in between the leading and trailing quotes (so ''' is valid, as is '"'). Entering more than 1 char in between quotes won't work, and will be treated as a plain string. 

![screenshot showing how to get the ascii value for a char](https://github.com/khalladay/handy/blob/master/example_images/char_value.png?raw=true)

## Inline Comments
With both of the above, if you want to append a comment to the log after the conversion or calculation, you can use the "//" to specify text you'd like to append: 

![screenshot showing how to add comments to an input string](https://github.com/khalladay/handy/blob/master/example_images/appending_comments.png?raw=true)

This is just to aid in readability. You can omit the "//" and just start writing a string as well, it just formats differently.

## Required Disclaimer
My programmer ego requires that I caveat this with the disclaimer that I'm aware that this is truly awful python. 