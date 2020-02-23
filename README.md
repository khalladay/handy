# handy
This is a script that I've started to keep running while I work on pretty much anything. Mostly, it serves the place of a paper log book, or lab notebook, that I use to document my thought processes as I work through problems. It's also useful to keeping track of bash one liners or command line strings that I want to use in the future (ie: the command line to build a specific config of a UE4 project). 

I keep a copy of this script in every project file, so each project has it's own handy.txt. There's no way to rename this file (or move where the script writes to), only because I haven't yet wanted to.

All input to the script is appended to a log file (that the script creates) called "handy.txt." This input is timestamped for easy searching through later. 

![basic usage](https://raw.githubusercontent.com/khalladay/handy/blob/master/example_images/text_example.png?raw=true)

## Other Features
My plan is to add more features to this script as I discover common tasks that seem like a good fit. Here's a list of what I've added so far:

### Radix Conversion
If you enter a hex, decimal, or binary string, handy will convert it to the other two radixes for you: 

![radix conversion](https://raw.githubusercontent.com/khalladay/handy/blob/master/example_images/radix_conversion.png?raw=true)

### Addition/Subtraction
You can also do simple addition / subtraction between two numbers of different radixes (or the same radix, if you want to)

![addition and subtraction](https://raw.githubusercontent.com/khalladay/handy/blob/master/example_images/addition_subtraction.png?raw=true)

## Inline Comments
With both of the above, if you want to append a comment to the log after the conversion or calculation, you can use the "//" to specify text you'd like to append: 

![adding comments](https://raw.githubusercontent.com/khalladay/handy/blob/master/example_images/appending_comments.png?raw=true)

This is just to aid in readability. You can omit the "//" and just start writing a string as well, it just formats differently.

## Required Disclaimer
My programmer ego requires that I caveat this with the disclaimer that I'm aware that this is truly awful python. 