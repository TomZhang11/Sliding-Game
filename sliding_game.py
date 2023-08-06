"""
Last modified 1/22/2023
Computer Science 30 Final Project
Original by Tom Zhang, did not receive any external help
"""
from random import randint
from time import sleep
from os import system


def slide(initial, final):
    board[final] = board[initial]
    board[initial] = " "
    return initial


def print_board():
    for i in range(3):
        print("|".join(board[i * 3 : i * 3 + 3]))


def pathing(current_spot, expected_spot, avoid_object):
    # returns the shortest path between two nodes in the form of a list while avoiding the designated node
    nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    # remove nodes that should be avoided
    nodes.remove(avoid_object)
    if board[avoid_object] == "4" and board[6:8] == ["4", "7"]:
        nodes.remove(7)
    # the dictionary to store the minimum moves to get to each node
    minMoves = {}
    # initialize the values to 10
    for i in nodes:
        minMoves[i] = 10
    minMoves[current_spot] = 0
    # the dictionary to store the previous node for each node in the shortest path
    via = {current_spot: current_spot}
    # the number of moves
    n = 0
    # temporary dictionaries to prevent dictionary sizes from changing during the loop
    newMinMoves = {}
    newVia = {}
    while not expected_spot in via:
        n += 1
        for i in via:
            for j in strongly_connected(nodes, i):
                if n < minMoves[j]:
                    newMinMoves[j] = n
                    newVia[j] = i
        # dumping items in the temporary dictionaries to the original dictionaries
        for i in newMinMoves:
            minMoves[i] = newMinMoves[i]
            via[i] = newVia[i]
        newMinMoves = {}
        newVia = {}
    # temporary list to store the path backwards
    movesTemp = []
    current = expected_spot
    while not current == current_spot:
        movesTemp.append(current)
        current = via[current]
    moves = []
    for i in range(len(movesTemp)):
        moves.append(movesTemp[-i - 1])
    return moves


def strongly_connected(l, n):
    # return all adjacent tiles
    list = []
    for i in [n - 3, n - 1, n + 1, n + 3]:
        if i >= 0 and i < 9 and abs(n % 3 - i % 3) < 2 and i in l:
            list.append(i)
    return list


def initialize():
    # shuffling
    empty_spot = 8
    for i in range(150):
        rnd = randint(0, 3)
        if rnd == 0:
            if empty_spot < 6:
                empty_spot = slide(empty_spot + 3, empty_spot)
        elif rnd == 1:
            if empty_spot % 3 != 2:
                empty_spot = slide(empty_spot + 1, empty_spot)
        elif rnd == 2:
            if empty_spot > 2:
                empty_spot = slide(empty_spot - 3, empty_spot)
        else:
            if empty_spot % 3 != 0:
                empty_spot = slide(empty_spot - 1, empty_spot)
    print_board()
    computer = input("do you want the computer to demonstrate? (yes, no) ")
    while computer != "yes" and computer != "no":
        computer = input("enter a valid answer: ")
    return (
        empty_spot,
        computer,
        [],
        {0: 0, 1: 1, 2: 3, 3: 3, 4: 0, 5: 0, 6: 1, 7: 0, 8: 0},
    )


board = []
for i in range(8):
    board.append(str(i + 1))
board.append(" ")
empty_spot, computer, to_do, guide = initialize()
while True:
    if computer == "no":
        inp = input("wasd: ")
        while not inp in ["w", "a", "s", "d"]:
            inp = input("wasd: ")
        if inp == "w":
            if empty_spot < 6:
                empty_spot = slide(empty_spot + 3, empty_spot)
        elif inp == "a":
            if empty_spot % 3 != 2:
                empty_spot = slide(empty_spot + 1, empty_spot)
        elif inp == "s":
            if empty_spot > 2:
                empty_spot = slide(empty_spot - 3, empty_spot)
        else:
            if empty_spot % 3 != 0:
                empty_spot = slide(empty_spot - 1, empty_spot)
    else:
        if len(to_do):
            empty_spot = slide(to_do[0], empty_spot)
            del to_do[0]
        else:
            for i in [0, 1, 2, 3, 6, 4, 5, 7, 8]:
                if board[i] != str(i + 1):
                    expected_spot = i
                    break
            current_spot = board.index(str(expected_spot + 1))
            if board[expected_spot + guide[expected_spot]] == str(expected_spot + 1):
                if expected_spot == 1 and board[5] != "3":
                    expected_spot = 5
                    current_spot = board.index("3")
                elif expected_spot == 3 and board[7] != "7":
                    expected_spot = 7
                    current_spot = board.index("7")
            else:
                expected_spot += guide[expected_spot]
            # find the path a number has to take to get from one spot to another
            moves = pathing(current_spot, expected_spot, current_spot)
            # for each spot in the path, create an empty spot, then, move the number in
            for i in pathing(empty_spot, moves[0], current_spot):
                to_do.append(i)
            to_do.append(current_spot)
            empty_spot = slide(to_do[0], empty_spot)
            del to_do[0]
            if board[1:3] == ["3", "2"]:
                for i in [0, 3, 6, 7, 8, 5, 4]:
                    to_do.append(i)
    if (
        computer == "yes"
        and len(to_do) < 10
        and expected_spot == 6
        and board[3] == "7"
        and board[6] == "4"
    ):
        for i in [4, 3, 6, 7, 4, 5, 8, 7, 6, 3, 4]:
            to_do.append(i)
    system("clear")
    print_board()
    win = True
    for i in range(8):
        if board[i] != str(i + 1):
            win = False
            break
    if win == True:
        again = input("you win, play again? (yes, no) ")
        while again != "yes" and again != "no":
            again = input("enter a valid response: ")
        if again == "yes":
            empty_spot, computer, to_do, guide = initialize()
            continue
        else:
            break
    if computer == "yes":
        sleep(1)