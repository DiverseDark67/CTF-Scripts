#!/usr/bin/env python3
# Version 1.0.0
# Date: 2025-02-27                                                   |_|                  |_|

# This is a script to decode pcap usb traffic which can often be found in CTFS.
# Credit goes to Oste's blog: https://05t3.github.io/posts/Dissecting-USB-Traffic/

# Import necessary modules
import os
import argparse


# USB HID Keycode to character mapping
KEY_CODES = {
    0x00: ['', ''],  # Reserved (no event indicated)
    0x04: ['a', 'A'],
    0x05: ['b', 'B'],
    0x06: ['c', 'C'],
    0x07: ['d', 'D'],
    0x08: ['e', 'E'],
    0x09: ['f', 'F'],
    0x0A: ['g', 'G'],
    0x0B: ['h', 'H'],
    0x0C: ['i', 'I'],
    0x0D: ['j', 'J'],
    0x0E: ['k', 'K'],
    0x0F: ['l', 'L'],
    0x10: ['m', 'M'],
    0x11: ['n', 'N'],
    0x12: ['o', 'O'],
    0x13: ['p', 'P'],
    0x14: ['q', 'Q'],
    0x15: ['r', 'R'],
    0x16: ['s', 'S'],
    0x17: ['t', 'T'],
    0x18: ['u', 'U'],
    0x19: ['v', 'V'],
    0x1A: ['w', 'W'],
    0x1B: ['x', 'X'],
    0x1C: ['y', 'Y'],
    0x1D: ['z', 'Z'],
    0x1E: ['1', '!'],
    0x1F: ['2', '@'],
    0x20: ['3', '#'],
    0x21: ['4', '$'],
    0x22: ['5', '%'],
    0x23: ['6', '^'],
    0x24: ['7', '&'],
    0x25: ['8', '*'],
    0x26: ['9', '('],
    0x27: ['0', ')'],
    0x28: ['\n', '\n'],  # Enter
    0x2C: [' ', ' '],    # Space
    0x2D: ['-', '_'],    # Hyphen and Underscore
    0x2E: ['=', '+'],    # Equal and Plus
    0x2F: ['[', '{'],    # Left Square Bracket and Left Curly Bracket
    0x30: [']', '}'],    # Right Square Bracket and Right Curly Bracket
    0x33: [';', ':'],    # Semicolon and Colon
    0x34: ["'", '"'],    # Single Quote and Double Quote
    0x36: [',', '<'],    # Comma and Less Than
    0x37: ['.', '>'],    # Period and Greater Than
    0x38: ['/', '?'],    # Slash and Question Mark
    0x29: ['ESC', 'ESC'],  # Escape
    0x2A: ['DEL', 'DEL'],  # Delete (Backspace)
    0x31: ['\\', '|'],   # Backslash and Vertical Bar
    0x35: ['`', '~'],    # Grave Accent and Tilde
    0x4F: ['→', '→'],    # Right Arrow
    0x50: ['←', '←'],    # Left Arrow
    0x51: ['↓', '↓'],    # Down Arrow
    0x52: ['↑', '↑'],    # Up Arrow
    # Additional keycodes for function keys, etc.
    0x39: ['Caps Lock', 'Caps Lock'],
    0x3A: ['F1', 'F1'], 0x3B: ['F2', 'F2'], 0x3C: ['F3', 'F3'], 0x3D: ['F4', 'F4'],
    0x3E: ['F5', 'F5'], 0x3F: ['F6', 'F6'], 0x40: ['F7', 'F7'], 0x41: ['F8', 'F8'],
    0x42: ['F9', 'F9'], 0x43: ['F10', 'F10'], 0x44: ['F11', 'F11'], 0x45: ['F12', 'F12'],
    0x46: ['PrintScreen', 'PrintScreen'], 0x47: ['Scroll Lock', 'Scroll Lock'],
    0x48: ['Pause', 'Pause'], 0x49: ['Insert', 'Insert'], 0x4A: ['Home', 'Home'],
    0x4B: ['PageUp', 'PageUp'], 0x4C: ['Delete Forward', 'Delete Forward'],
    0x4D: ['End', 'End'], 0x4E: ['PageDown', 'PageDown'], 0x53: ['Num Lock', 'Num Lock'],
    # Numeric Keypad keys
    0x54: ['/', '/'], 0x55: ['*', '*'], 0x56: ['-', '-'], 0x57: ['+', '+'],
    0x58: ['Enter', 'Enter'], 0x59: ['1', '1'], 0x5A: ['2', '2'], 0x5B: ['3', '3'],
    0x5C: ['4', '4'], 0x5D: ['5', '5'], 0x5E: ['6', '6'], 0x5F: ['7', '7'],
    0x60: ['8', '8'], 0x61: ['9', '9'], 0x62: ['0', '0'], 0x63: ['.', '.'],
    # Control Keys
    0xE0: ['Left Ctrl', 'Left Ctrl'], 0xE1: ['Left Shift', 'Left Shift'],
    0xE2: ['Left Alt', 'Left Alt'], 0xE3: ['Left GUI', 'Left GUI'],
    0xE4: ['Right Ctrl', 'Right Ctrl'], 0xE5: ['Right Shift', 'Right Shift'],
    0xE6: ['Right Alt', 'Right Alt'], 0xE7: ['Right GUI', 'Right GUI']
}


# Initialize argument parser
parser = argparse.ArgumentParser(description="USB Keyboard Decoder")
parser.add_argument("-f", "--file", required=True, help="Input file to decode keystrokes (e.g., hope.txt)")
args = parser.parse_args()

input_file = args.file  # File name is passed via the command line argument

# Check if the file exists
if not os.path.isfile(input_file):
    print(f"Error: The file '{input_file}' does not exist.")
    exit()

# Read the data from the file, ignoring non-ASCII characters
with open(input_file, 'rb') as file:
    data = file.read().decode('utf-16', errors='ignore')  # Decode as UTF-16 and ignore errors
    lines = data.splitlines()

output = ''  # Initialize an empty string for the decoded keystrokes
previous_keycode = None  # To avoid repeated characters

# Iterate through each line of the data file
for line in lines:
    if len(line) < 16:  # Skip any lines that are too short
        continue

    try:
        # Extract the modifier and key from the data (in hex)
        modifier = int(line[:2], 16)  # First byte for shift/ctrl
        keycode = int(line[4:6], 16)  # Third byte for the actual key
    except ValueError:
        # Skip lines that cannot be converted to integers (invalid data)
        continue

    if keycode == 0:
        continue  # Skip if no key was pressed

    # Handle Backspace (Delete)
    if keycode == 0x2A:  # Backspace
        output = output[:-1]  # Remove the last character
        continue

    # Ignore Arrow Keys
    if keycode in [0x4F, 0x50, 0x51, 0x52]:  # Arrow keys
        continue

    # Prevent repeated characters if the same keycode occurs twice
    if keycode == previous_keycode:
        continue

    previous_keycode = keycode  # Track the last processed keycode

    # Determine if Shift is held (bit 1 in modifier byte)
    shift = (modifier & 0x22) > 0  # Check for both Left Shift and Right Shift (0x02 and 0x20)

    # Translate the keycode to the actual character
    if keycode in KEY_CODES:
        output += KEY_CODES[keycode][shift]

# Print the final decoded output
print("Decoded Keystrokes:")
print(output)