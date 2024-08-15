import data
from Tournaments import *


def main():
    # Initialize match data
    print("Initializing data...")
    _data = data.Data()
    print("Data initialized! \n")

    print("Welcome to soccer tournament simulator!")
    # Program loop
    on = True
    while on:
        try:
            sel1 = int(input("Enter: 1. Choose tournament type 2. Exit \n"))
            match sel1:
                case 1:
                    print("Now, choose your tournament format. \n"
                          "A league contains an even number of teams and all the teams play each other twice. Whoever "
                          "scores the most points wins. \n"
                          "A knockout contains 2^n (where n is an integer) teams. Teams are put into a bracket based on"
                          "seeding. The losers of each game are knocked out until only one team remains. \n"
                          "A group knockout contains 2^n (where n is an integer) teams. Teams are first divided into "
                          "groups that play similar to a league format and then the top two of each group move on to "
                          "the"
                          "knockout.\n\n"
                          "See the README for more details.\n\n")
                    sel2 = int(input("Enter: 1. League 2. Knockout 3. Group & Knockout \n"))
                case 2:
                    on = False
        except ValueError:
            print("Input error. Resetting...")


if __name__ == '__main__':
    main()
