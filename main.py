import Tournaments.league
import data
from Tournaments import *


def create_league(_data):
    # Input the teams, and check if they are valid
    print("Now, you will input one team per line. Remember, leagues require an even number of teams. Enter a NEWLINE \n"
          "when done.")
    inserting = True
    teams = []
    while inserting:
        team = input(teams)
        if team == "":
            inserting = False
        elif (_data.train == team).any().any():
            teams.append(team)
        else:
            raise ValueError

    print(teams)
    print("Team selection complete! Creating league...")
    # if len(teams) != 0 or len(teams) & (len(teams) - 1) != 0: //Wrong condition but will be useful later (checking
    # 2^n)
    if len(teams) % 2 != 0:
        raise ValueError
    print("Simulating...")

    Tournaments.league.simulate(_data, teams)


def main():
    # Initialize match data
    print("Initializing data...")
    _data = data.Data()
    print("Data initialized! \n")

    print("Welcome to soccer tournament simulator!")
    # Program loop
    on = True
    while on:
        # try:
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
                    match sel2:
                        case 1:
                            create_league(_data)
                        case 2:
                            pass
                        case 3:
                            pass
                case 2:
                    on = False
        # except ValueError:
        #
        #     print("You have an input error. Either you selected an invalid number, inserted an invalid number of \n"
        #           "teams into a tournament, or inserted a team into a tournament that is not in the data. \n"
        #           "Resetting...")


if __name__ == '__main__':
    main()
