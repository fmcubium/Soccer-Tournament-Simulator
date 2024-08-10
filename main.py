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
        sel1 = int(input("Enter: 1. Choose tournament type 2. Exit \n"))
        match sel1:
            case 1:
                print("this is a temporary insertion statement weeeeeeeee")
            case 2:
                on = False


if __name__ == '__main__':
    main()
