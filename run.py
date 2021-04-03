from getpass import getpass
import stdiomask
import os
import base64
import hashlib
import random
import re
import sys
import math

def input_yes_no(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    postfix = " [Y/n]" if default is not valid[default] else " [N/y]" if default is valid[default] else " [y/n]"

    while True: 
        sys.stdout.write(question + postfix + '\t: ')
        choice = input().lower()

        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("You can only respond with 'y' or 'n'")

def input_number(question, default=16):
    postfix = " [" + str(default) + "]"

    while True:
        sys.stdout.write(question + postfix + '\t: ')
        try:
            return int(input())
        except:
            return int(default)

def input_notnul(question):
    while True:
        sys.stdout.write(question + ': ')
        choice = input()
        if choice:
            return choice
        else:
            sys.stdout.write("Input cannot be null\n")

def nato_spell(toBeSpell):
    retVal = ""

    l =  {  "A": "Alpha",  "B": "Bravo",   "C": "Charlie",
            "D": "Delta",  "E": "Echo",    "F": "Foxtrot",
            "G": "Golf",   "H": "Hotel",   "I": "India",
            "J": "Juliett","K": "Kilo",    "L": "Lima",
            "M": "Mike",   "N": "November","O": "Oscar",
            "P": "Papa",   "Q": "Quebec",  "R": "Romeo",
            "S": "Sierra", "T": "Tango",   "U": "Uniform",
            "V": "Victor", "W": "Whiskey", "X": "X-ray",
            "Y": "Yankee", "Z": "Zulu" }
    
    for c in toBeSpell:
        if c.upper() in l:
            temp = ''.join([l[x] for x in [c.upper()]])
            if c.islower():
                retVal += temp.lower()
            else:
                retVal += temp.upper()
        else:
            retVal += c

        retVal += " "

    return retVal

def main():   
    os.system("cls" if os.name=="nt" else "clear")

    password_length = input_number("Password Length  ")
    include_lwrcase = input_yes_no("Include Lowercase")
    include_uprcase = input_yes_no("Include Uppercase")
    include_numbers = input_yes_no("Include Numbers  ")
    include_symbols = input_yes_no("Include Symbols  ")

    domain = input_notnul("Domain\t\t\t")
    username = input_notnul("Username\t\t")
    keyword = stdiomask.getpass("Key\t\t\t: ")

    raw_seed = domain + username + keyword 

    random.seed(raw_seed)

    sha512_seed = hashlib.sha512(raw_seed.encode("ascii")).hexdigest()

    b64_seed = base64.b64encode(sha512_seed.encode("ascii")).decode("utf-8").replace("=", "")

    b64_seed_in_letter = "".join([i for i in b64_seed if not i.isdigit()])
    b64_seed_in_number = "".join([i for i in b64_seed if i.isdigit()])

    arr_symbols = ["!", "<", ">", "#", "$", "%", "&", "*", "+", "-", "=", "?", "@", "_", "{", "}", "[", "]", "(", ")", "/", "~", ";", ":", "."]

    percentage_of_lwrcase = 30
    percentage_of_uprcase = 30
    percentage_of_numbers = 20
    percentage_of_symbols = 20

    total = 0

    if include_lwrcase:
        total += percentage_of_lwrcase
    else:
        percentage_of_lwrcase = 0
        
    if include_uprcase:
        total += percentage_of_uprcase
    else:
        percentage_of_uprcase = 0
        
    if include_numbers:
        total += percentage_of_numbers
    else:
        percentage_of_numbers = 0

    if include_symbols:
        total += percentage_of_symbols
    else:
        percentage_of_symbols = 0

    len_of_lwrcase = math.ceil((percentage_of_lwrcase / total) * password_length)
    len_of_uprcase = math.ceil((percentage_of_uprcase / total) * password_length)
    len_of_numbers = math.floor((percentage_of_numbers / total) * password_length)
    len_of_symbols = math.floor((percentage_of_symbols / total) * password_length)

    if include_lwrcase:
        len_of_lwrcase += password_length - (len_of_lwrcase + len_of_uprcase + len_of_numbers + len_of_symbols)
    elif include_uprcase:
        len_of_uprcase += password_length - (len_of_lwrcase + len_of_uprcase + len_of_numbers + len_of_symbols)
    elif include_numbers:
        len_of_numbers += password_length - (len_of_lwrcase + len_of_uprcase + len_of_numbers + len_of_symbols)
    elif include_symbols:
        len_of_symbols += password_length - (len_of_lwrcase + len_of_uprcase + len_of_numbers + len_of_symbols)

    selected_lwrcase = b64_seed_in_letter[0:len_of_lwrcase].lower()
    selected_uprcase = b64_seed_in_letter[len_of_lwrcase:len_of_lwrcase+len_of_uprcase].upper()
    selected_numbers = str(b64_seed_in_number[0:len_of_numbers])
    selected_symbols = ""

    for i in range(len_of_symbols):
        selected_symbols += str(arr_symbols[random.randrange(len(arr_symbols))])

    output = selected_lwrcase + selected_uprcase + selected_numbers + selected_symbols

    final = "".join(random.sample(output,len(output)))

    print("\nPassword\t\t: " + final)
    print("\nNATO Spelling\t\t: " + nato_spell(final))





if __name__=="__main__":
    main()