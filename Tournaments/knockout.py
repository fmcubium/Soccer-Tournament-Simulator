# Nodes for our tournament tree
import math


class Node:
    def __init__(self):
        self.val = ""
        self.left = None
        self.right = None

    def __init__(self, value):
        self.val = value
        self.left = None
        self.right = None


# Our actual knockout tournament code

def preorder_builder(node: Node, h):
    #if h == 0 do nothing
    if h == 0:
        return

    node.left = Node()
    node.right = Node()

    preorder_builder(node.left, h - 1)
    preorder_builder(node.right, h - 1)

def create_tree(root: Node, teams: list):
    # determine the height: since our tree is always perfect, h = 1 + log_2(n)
    # where n = number of nodes at the bottom layer = number of teams
    height = 1 + math.log2(len(teams))

    # construct a perfect tree of height h. The nodes that are not on the bottom layer will have None/"" as their val
    # nodes at the bottom contain the teams, as listed in the list.

    # return the completed tree given a root with None as its val.


def sim_helper(node: Node):
    if node.left is None:
        return

    sim_helper(node.left)
    sim_helper(node.right)

    home = node.left.val
    away = node.right.val

    # create match, look at league code

    # simulate it

    winner = "" # fix later
    node.val = winner


def simulate(data, teams: list):
    pass
    # PHASE 1: Prepare team data and seed teams

    # PHASE 2: Create our tree and dataframe for simulating

    # PHASE 3: Run the simulation
