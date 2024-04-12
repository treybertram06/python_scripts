def ascii_to_hex(ascii_string):
    hex_string = ""
    for char in ascii_string:
        hex_string += hex(ord(char))[2:]
    return hex_string

ascii_string = input("Input: ")
print("Hexadecimal String: ", ascii_to_hex(ascii_string))