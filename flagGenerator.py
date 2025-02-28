#!/usr/bin/env python3
# Version 1.0.0
# Date: 2025-02-27

import random
import string

def generate_flag():
    # Define the character set for the random part of the flag
    charset = string.ascii_letters + string.digits
    
    # Generate a random string of 32 characters
    random_part = ''.join(random.choices(charset, k=32)) # Edit to change the length of the random part of the flag 
    
    # Construct the flag
    flag = f"{flag_root}{{{random_part}}}"
    
    return flag

# Generate and print flags
if __name__ == "__main__": 
    num_flags = int(input("How many flags would you like to generate? "))

    flag_root = str(input("What would you like as your Flag root?(Ex. PersonalCTF{...}) "))

    for _ in range(num_flags):
        print(generate_flag())