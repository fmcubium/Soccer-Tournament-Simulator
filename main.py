import Tournaments.league
import Tournaments.knockout
import data
import util
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
        else:
            teams.append(team)

    print(teams)
    util.fix_team_names_list(teams)
    print("Team selection complete! Creating league...")
    # if len(teams) != 0 or len(teams) & (len(teams) - 1) != 0: //Wrong condition but will be useful later (checking
    # 2^n)
    if len(teams) == 0 or len(teams) % 2 != 0:
        raise ValueError
    print("Simulating...")

    Tournaments.league.simulate(_data, teams)


def create_ko(_data):
    # Input the teams and check for validity - remember to check for 2^n
    print("Now, you will input one team per line. Remember, knockouts require 2^n teams, where n is an integer. \n"
          "Enter a NEWLINE when done.")
    inserting = True
    teams = []
    while inserting:
        team = input(teams)
        if team == "":
            inserting = False
        else:
            teams.append(team)

    print(teams)
    util.fix_team_names_list(teams)
    print("Team selection complete! Creating knockout...")
    if len(teams) == 0 or (len(teams) & (len(teams) - 1) != 0):
        raise ValueError
    print("Simulating...")

    Tournaments.knockout.simulate(_data, teams)


def create_group_ko(_data):
    # Input the teams and check for validity - remember to check for 2^n and num teams >= 4
    print("Now, you will input one team per line. Remember, groups + knockouts require 2^n teams, where n is an \n"
          "integer. They also require at least 4 teams. Teams will be placed into groups in the order they are typed \n"
          "in, i.e. group A will be the first 4 teams inserted. Enter a NEWLINE when done.")
    inserting = True
    teams = []
    while inserting:
        team = input(teams)
        if team == "":
            inserting = False
        else:
            teams.append(team)

    print(teams)
    util.fix_team_names_list(teams)
    print("Team selection complete! Creating group + knockout...")
    if len(teams) < 4 or (len(teams) & (len(teams) - 1) != 0):
        raise ValueError
    print("Simulating...")

    # Group stage
    advanced_teams = []
    for i in range(len(teams))[::4]:
        advanced_teams.extend(Tournaments.league.simulate(_data, [teams[i], teams[i + 1], teams[i + 2], teams[i + 3]]))

    # KO stage
    Tournaments.knockout.simulate(_data, advanced_teams)


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
                        create_ko(_data)
                    case 3:
                        create_group_ko(_data)
            case 2:
                on = False
    # except ValueError:
    #
    #     print("You have an input error. Either you selected an invalid number, inserted an invalid number of \n"
    #           "teams into a tournament, or inserted a team into a tournament that is not in the data. \n"
    #           "Resetting...")


if __name__ == '__main__':
    main()
