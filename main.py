import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

REEL_SYMBOLS = 3
NUM_OF_REELS = 3

symbol_count = {
    "A": 3,
    "B": 4,
    "C": 6,
    "D": 8,

}
symbol_value = {
    "A": 6,
    "B": 5,
    "C": 4,
    "D": 3,
}


# Example of data columns:
#     Before transposing: [A, B, C]
#                         [B, A, C]
#                         [C, D, C]
#     After:
#                         [A [B [C
#                          B  A  D
#                          C] C] C] WINNER

def checkWinnings(columns, lines, bet, values):
    winnings = 0
    winningLines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbolToCheck = column[line]
            if symbol != symbolToCheck:
                break
        else:
            winnings += values[symbol] * bet
            winningLines.append(line + 1)

    return winnings, winningLines


def getSlotMachineSpin(count, amount, symbols):
    all_symbols = []
    for symbol, symbolCount in symbols.items():
        for _ in range(symbolCount):
            all_symbols.append(symbol)
    columns = []
    for _ in range(amount):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(count):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)

    return columns


def printSlotMachine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="\n")
        print()


def deposit():
    while True:
        amount = input("What amount would you like to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a number")

    return amount


def getNumberOfLines():
    while True:
        lines = input("Enter the number of lines to bet on (1-" + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Amount must be within 1-" + str(MAX_LINES) + ". ")
        else:
            print("Please enter a number")
    return lines


def getBet():
    while True:
        amount = input("What amount would you like to bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be within ${MIN_BET}-${MAX_BET}. ")
        else:
            print("Please enter a number")

    return amount


def spin(balance):
    lines = getNumberOfLines()
    while True:
        bet = getBet()
        totalBet = lines * bet

        if totalBet > balance:
            print(f"You do not have enough balance to bet ${totalBet}, your current balance is ${balance}. ")
        else:
            break

    print(
        f"You are betting ${bet} on {lines} lines. Your total bet is equal to: ${totalBet}")

    slots = getSlotMachineSpin(REEL_SYMBOLS, NUM_OF_REELS, symbol_count)
    printSlotMachine(slots)
    winnings, winningLines = checkWinnings(slots, lines, bet, symbol_value)
    if winnings > 0:
        print(f"You won ${winnings}!! ")
        print(f"You won on lines:", *winningLines)
    else:
        print(f"Sorry, you did not win.")
    return winnings - totalBet


def main():
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        play = input("Press enter to play (q to quit).")
        if play == 'q':
            break
        balance += spin(balance)

    print(f"You left with ${balance}")


main()
