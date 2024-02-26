""" removes unnecessary move in the scramble/solution """

def clean_moves(scramble):
    # split the string generated for scramble into individual moves
    split_scramble = scramble.split()
    # pointer for iteration through the list of moves
    seq = 0

    # Go through The splot
    while seq < len(split_scramble):
        try:
            # if it's the same move next to each other
            if split_scramble[seq][0] == split_scramble[seq + 1][0]:
                # minus seq by 1 to cancel the +1 if we had to clean a move
                # if first move is normal
                if not is_prime(split_scramble[seq]) and not is_double(split_scramble[seq]):
                    # second move is normal (quarter turn in clockwise direction)
                    if not is_prime(split_scramble[seq + 1]) and not is_double(split_scramble[seq + 1]):
                        # Simplify to double move (by changing the first move into a half turn and remove the second move)
                        del split_scramble[seq + 1]
                        split_scramble[seq] += "2"

                    # second move is prime, that is, the first and second moves are identical but in opposite directions
                    elif is_prime(split_scramble[seq + 1]):
                        # They cancel each other out; so both of them should be removed
                        del split_scramble[seq], split_scramble[seq]

                    # second move is double, that is, we make a quarter turn followed by a half turn in the same direction
                    # this is equivalent to the first move in opposite direction
                    elif is_double(split_scramble[seq + 1]):
                        # Add prime to the first move (to invert its direction of rotation) and remove the second move
                        del split_scramble[seq + 1]
                        split_scramble[seq] += "'"

                # if first move is prime
                elif is_prime(split_scramble[seq]):
                    # second move is normal
                    if not is_prime(split_scramble[seq + 1]) and not is_double(split_scramble[seq + 1]):
                        # Cancels out
                        del split_scramble[seq], split_scramble[seq]

                    # second move is prime
                    elif is_prime(split_scramble[seq + 1]):
                        # Combime into double move
                        del split_scramble[seq + 1]
                        split_scramble[seq] = split_scramble[seq][0] + "2"

                    # second move is double
                    elif is_double(split_scramble[seq + 1]):
                        # Cancels out in a modulus style
                        del split_scramble[seq + 1]
                        split_scramble[seq] = split_scramble[seq][0]


                # if first move is double
                elif is_double(split_scramble[seq]):
                    # second move is normal
                    if not is_prime(split_scramble[seq + 1]) and not is_double(split_scramble[seq + 1]):
                        # remove the first move
                        del split_scramble[seq]
                        # replace 2 of the second move with ' to make it a quarter turn with inverted direction
                        split_scramble[seq] = split_scramble[seq][0] + "'"

                    # second move is prime
                    elif is_prime(split_scramble[seq + 1]):
                        # Cancels out in a modulus style
                        del split_scramble[seq + 1]
                        split_scramble[seq] = split_scramble[seq][0]

                    # second move is double; two half turns will get the cube back to initial state
                    elif is_double(split_scramble[seq + 1]):
                        # They cancel each other out; so both have to be removed
                        del split_scramble[seq], split_scramble[seq]
                
                # minus seq by 1 to cancel the +1 if we had to clean a move
                seq -= 1
        # in case of IndexError, terminate the loop
        except IndexError:
            break
        # increment the pointer to proceed to the next move of the list
        seq += 1

    # join the moves of the cleaned list into a single string (separated by single space)
    return " ".join(split_scramble)

# To check if the face/cube rotation is a half turn
# If the move notation ends with 2, returns True
# otherwise returns False
def is_double(move):
    try:
        # A move is double if it ends in 2
        if move[1] == "2":
            return True
        else:
            return False
    except IndexError:
        return False


# To check if the face/cube rotation is in counter-clockwise direction
# If the move notation ends with ', returns True
# otherwise returns False
def is_prime(move):
    try:
        # A move is prime (inverse) if it ends with "'"
        if move[1] == "'":
            return True
        else:
            return False
    except IndexError:
        return False


# Code to test the functions above
if __name__ == "__main__":
    ''' # all possible cases
    print(clean_moves("U U D D' U U2"))
    print(clean_moves("U' U D' D' U' U2"))
    print(clean_moves("U2 U D2 D' U2 U2"))

    print("Correct output is")
    print("U2 U'")
    print("D2 U")
    print("U' D")
    '''
    #print(clean_moves("B R2 B F2 L2 D D2 F2 D2 L B D U2 D2 D2 R R2 L F2 U2"))
