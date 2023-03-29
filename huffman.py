import re
import numpy as np
from PIL import Image
import base64

def bitstring_to_encoded64(s):
    s="1"+s                     # add '1' before s      // because front '0' is ignored when convert string to int.
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8

    encoded64_bytes=base64.b64encode(bytes(b[::-1]))
    encoded64_string=encoded64_bytes.decode('ascii')
    return encoded64_string

def encoded64_to_bitstring(encoded64_string):
    decoded64_string=encoded64_string.encode('ascii')
    decoded64_byte=base64.b64decode(decoded64_string)
    decoded64_int=int.from_bytes(decoded64_byte, "big")
    return bin(decoded64_int)[2:]


print("Huffman Compression Program")
print("=================================================================")

my_string = str(input("Enter your string : "))

letters = []
only_letters = []
for letter in my_string:
    if letter not in letters:
        frequency = my_string.count(letter)             #frequency of each letter repetition
        letters.append(frequency)
        letters.append(letter)
        only_letters.append(letter)

nodes = []
while len(letters) > 0:
    nodes.append(letters[0:2])
    letters = letters[2:]                               # sorting according to frequency
nodes.sort()
huffman_tree = []
huffman_tree.append(nodes)                             #Make each unique character as a leaf node

def combine_nodes(nodes):
    pos = 0
    newnode = []
    if len(nodes) > 1:
        nodes.sort()
        nodes[pos].append("1")                       # assigning values 1 and 0
        nodes[pos+1].append("0")
        combined_node1 = (nodes[pos] [0] + nodes[pos+1] [0])
        combined_node2 = (nodes[pos] [1] + nodes[pos+1] [1])  # combining the nodes to generate pathways
        newnode.append(combined_node1)
        newnode.append(combined_node2)
        newnodes=[]
        newnodes.append(newnode)
        newnodes = newnodes + nodes[2:]
        nodes = newnodes
        huffman_tree.append(nodes)
        combine_nodes(nodes)
    return huffman_tree                                     # huffman tree generation

newnodes = combine_nodes(nodes)

huffman_tree.sort(reverse = True)

#print huffman tree
print("Huffman tree with merged pathways:")
checklist = []
for level in huffman_tree:
    for node in level:
        if node not in checklist:
            checklist.append(node)
        else:
            level.remove(node)
count = 0
for level in huffman_tree:
    print("Level", count,":",level)             
    count+=1
print()

#genrating binary code
letter_binary = []
if len(only_letters) == 1:
    lettercode = [only_letters[0], "0"]
    letter_binary.append(letter_code*len(my_string))
else:
    for letter in only_letters:
        code =""
        for node in checklist:
            if len (node)>2 and letter in node[1]:           
                code = code + node[2]
        lettercode =[letter,code]
        letter_binary.append(lettercode)

print("Binary code generated:")
print(letter_binary)
print()

# bitstring is 'compressed binary code'
bitstring =""
for character in my_string:
    for item in letter_binary:
        if character in item:
            bitstring = bitstring + item[1]
binary ="0b"+bitstring
print("Your raw compressed code:")
print(bitstring) # add '1' to bistring // because front '0' is ignored when converting to int
print()


#  bitstring -> encoded64
encoded64_string=bitstring_to_encoded64(bitstring)
print("Compressed string(Based64 encoded):")
print(encoded64_string)
print()


#  encoded64 -> bitstring
bistring=encoded64_to_bitstring(encoded64_string)
bitstring=bitstring[0:]


#print uncompressed result
uncompressed_string =""
code =""
for digit in bitstring:
    code = code+digit
    pos=0                                        #iterating and decoding
    for letter in letter_binary:
        if code ==letter[1]:
            uncompressed_string=uncompressed_string+letter_binary[pos] [0]
            code=""
        pos+=1

print("Your uncompressed data is:")
print(uncompressed_string)

print()
if uncompressed_string == my_string:
    print("Success")
else:
    print("Failed")