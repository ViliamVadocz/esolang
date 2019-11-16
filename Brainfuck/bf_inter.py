"""Brainfuck Interpreter by Viliam Vadocz.
More on Brainfuck: https://en.wikipedia.org/wiki/Brainfuck

Usage:
    br_inter -h
    br_inter <file> [--max-len=<length>] [--max-num=<number>] [-t] [-c] 

Options:
    -h, --help          Show this screen.
    -t, --tape          Shows the tape and the command being executed.
    -c, --checkpoints   Shows parsed commands and checkpoints (used for loops).
    file                The Brainfuck file (.txt) to interpret.
    --max-len=<length>  The maximum length of tape (int) [default: 128].
    --max-num=<number>  Maximum allowed number on the tape (absolute value) [default: 256].
"""
from docopt import docopt
from collections import deque

if __name__ == '__main__':
    arguments = docopt(__doc__)

    max_len = int(arguments['--max-len'])
    max_num = int(arguments['--max-num'])
    debug_tape = True if arguments["--tape"] else False
    debug_cp = True if arguments["--checkpoints"] else False

    # Converting file to string.
    bf_file_name = arguments['<file>']
    bf_file = open(bf_file_name,'r')
    bf_str = ''.join(list(bf_file))

    # Parsing file string for commands.
    recognised_commands = ['>', '<', '+', '-', '.', ',', '[', ']']
    commands = [char for char in bf_str if char in recognised_commands]
    # Print commands (DEBUG).
    if debug_cp: print('commands', commands)

    # Setup
    tape = deque()
    tape.append(0)
    tape_index = 0
    checkpoints = []

    # Interpreter
    cmd_index = 0
    while cmd_index < len(commands):
        # Break if tape is too long.
        if len(tape) > max_len:
            print('Maximum tape length exceeded.')
            break

        cmd = commands[cmd_index]

        # >	increment the data pointer (to point to the next cell to the right).
        # <	decrement the data pointer (to point to the next cell to the left).

        # +	increment (increase by one) the byte at the data pointer.
        # -	decrement (decrease by one) the byte at the data pointer.

        # .	output the byte at the data pointer.
        # ,	accept one byte of input, storing its value in the byte at the data pointer.

        # [	if the byte at the data pointer is zero, 
        # then instead of moving the instruction pointer forward to the next command, 
        # jump it forward to the command after the matching ] command.

        # ]	if the byte at the data pointer is nonzero, 
        # then instead of moving the instruction pointer forward to the next command, 
        # jump it back to the command after the matching [ command.

        if cmd == '>':
            tape_index += 1
            if tape_index >= len(tape):
                tape.append(0)

        elif cmd == '<':
            if tape_index > 0:
                tape_index -= 1
            else:
                tape.appendleft(0)
        
        elif cmd == '+':
            tape[tape_index] += 1
            # Break if value to large.
            if abs(tape[tape_index]) > max_num:
                print('Maximum number exceeded.')
                break

        elif cmd == '-':
            tape[tape_index] -= 1
            # Break if value to large.
            if abs(tape[tape_index]) > max_num:
                print('Maximum number exceeded.')
                break

        elif cmd == '.':
            print(tape[tape_index])
        
        elif cmd == ',':
            tape[tape_index] = input('INPUT:')

        elif cmd == '[':
            # Skip ahead.
            if tape[tape_index] == 0:
                opens = 1
                closes = 0
                while opens != closes:
                    cmd_index += 1
                    if commands[cmd_index] == '[': opens += 1
                    elif commands[cmd_index] == ']': closes += 1
            
            # Begin loop.
            else:
                checkpoints.append(cmd_index)
                # Print checkpoints (DEBUG).
                if debug_cp: print('cp', checkpoints)

            
        elif cmd == ']':
            # Loop back.
            if tape[tape_index] != 0:
                cmd_index = checkpoints.pop() - 1
            # Remove checkpoint.
            else:
                checkpoints.pop()

            # Print checkpoints (DEBUG).
            if debug_cp: print('cp', checkpoints)
                

        # Shows tape (DEBUG).
        if debug_tape: print(f'({commands[cmd_index]})', list(tape))

        # Move onto next command.
        cmd_index += 1