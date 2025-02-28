#!/usr/bin/env python3
# Version 1.0.0
# Date: 2025-02-27

#      _                _                           _
#     | |              | |                         (_)                                _____
#   __| |  ___    _____| |       ___  ___       __  _  _____    ___    _____ ____    /  ___\
#  / _` | / _ \  /   _/| |___   / _ \ \  \  _  /  /| | | __ \  / _ \  /  __/|  _ \  _| |_    
# | (_| || |_| | \  \  |  __ \ | |_| | |  \/ \/  | | | | |_| || |_| | \  \  | |_| |[_   _]
#  \__,_| \___/ |____/ |_,| |_| \___/   \___/\__/  |_| | ___/  \___/ |____/ | ___/   | |
#                                                      | |                  | |      |_|
#                                                      |_|                  |_|

# This is a script to create and decode base64x encoded strings.
# It can help en/decode base64 that has been encoded multiple times.

import base64

baseString = '' # Edit this base String to encode/decode
bytes_object = baseString.encode('utf-8')

def main():
    print("Would you like to encode or decode?")
    print("1. Encode")
    print("2. Decode")
    choice = input("Enter your choice: ")

    if choice == '1':
        print("Encoding")
        encoded = encode(bytes_object)
        
        # Write Encoded to a txt file
        with open('encoded.txt', 'w') as f:
            f.write(encoded.decode('utf-8'))

    elif choice == '2':
        print("Decoding")
        # Read Encoded from a txt file
        with open('encoded.txt', 'r') as f:
            data = f.read()
        
        # Convert the string data to bytes
        decoded = decode(data.encode('utf-8'))
        print(decoded.decode('utf-8'))

    else:
        print("Invalid choice")


def encode(data):
    for i in range(30):
        data = base64.b64encode(data)
    return data

def decode(data):
    for i in range(30):
        data = base64.b64decode(data)
    return data

main() # Run the main function