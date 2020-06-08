# Handy
## A Utility And Logbook Script For Programmers

This is a script meant to log stream of consciousness thoughts. In practice, I use this is a sort of lab-notebook for software and blog projects (and you can too!). 

To start, just launch handy with no arguments and start typing. It will create a file called handy.txt and start appending what you write as time stamped lines in that text file. The next time you launch handy, it will read in this file and pick up right where you left off. 

You can also specify the name of the file that the script writes to by providing the file name as the first command line argument: 

```powershell
python handy.py myfile.txt
```

It supports Windows and Mac (it might run on Linux too, but I don't have a linux box to check), and looks like this: 

![screenshot showing how it handles entering basic text strings](https://github.com/khalladay/handy/blob/master/example_images/text_example.png?raw=true)

## Additional Features
In addition to logging text, Handy also supports a number of utility features that I added to make my life easier. Here they are: 

* [Addition and Subtraction](#Addition-and-Subtraction)
* [Bit Shifting](#bit-shifting)
* [Radix Conversion](#radix-conversion)
* [Two's Complement Conversion](#2s-complement-conversion)
* [Ascii Values](#ascii-value-for-single-char)
* [Inline Comments](#inline-comments)
* [Clipboard Support](#clipboard-support)

---

### Addition/Subtraction
You can also do simple addition / subtraction between two numbers of different radixes (or the same radix, if you want to).

![screenshot showing how addition and subtraction works](https://github.com/khalladay/handy/blob/master/example_images/add_subtract.png?raw=true)

### Bit Shifting
Similar to above, you can compute the result of a bit shift operation using "<<" and ">>" operators between two numeric values. One potentially unexpected behavior with this is that if you right-shift a binary value, handy will left pad the result with zeroes so the result displayed has the same length as the original input being shifted. This behavior does not apply to left shifts (which will add digits to the binary value). 

![screenshot showing how bit shifting works](https://github.com/khalladay/handy/blob/master/example_images/bit_shift.png?raw=true)

### Radix Conversion
If you enter a hex, decimal, or binary string, handy will convert it to the other two radixes for you: 

![screenshot showing how radix conversion works](https://github.com/khalladay/handy/blob/master/example_images/radix_conversion.png?raw=true)

### 2s Complement Conversion
If you enter a negative integer, it will be represented as a 2's complement hex / binary string when converted. This only works within the range of a 32 bit signed int. This conversion only works from negative int -> Hex / Binary, you currently can't input a hex value and convert it to an int assuming it's a 2's complement val. 

![screenshot showing how converting a negative int to 2's complement hex/bin strings works](https://github.com/khalladay/handy/blob/master/example_images/negative_int.png?raw=true))

### Ascii Value For Single Char
Entering a single char, wrapped in single quotes (ie: 'A') will convert it to an ASCII byte value. You don't need to escape any value in between the leading and trailing quotes (so ''' is valid, as is '"'). Entering more than 1 char in between quotes won't work, and will be treated as a plain string. 

![screenshot showing how to get the ascii value for a char](https://github.com/khalladay/handy/blob/master/example_images/char_value.png?raw=true)

## Inline Comments
With both of the above, if you want to append a comment to the log after the conversion or calculation, you can use the "//" to specify text you'd like to append: 

![screenshot showing how to add comments to an input string](https://github.com/khalladay/handy/blob/master/example_images/appending_comments.png?raw=true)

This is just to aid in readability. You can omit the "//" and just start writing a string as well, it just formats differently.

## Clipboard Support
I haven't yet figured out a good way to make this thing detect ctrl+V for paste, so I've instead bound paste to the tab key. I know I've listed it here as a "feature" but really this is jank that needs to be fixed up at some point in the future when it bothers me enough.

## Required Disclaimer
My programmer ego requires that I caveat this with the disclaimer that I'm aware that this is truly awful python. I don't often write python, so it's probably not going to get better either. 