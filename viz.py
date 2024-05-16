"""
This file originally aimed to incorporate more data visualization into our project by
creating a heatmap visualization that would show the probability of each Pokemon winning against every
other Pokemon in a battle over a user-specified number of battle simulations per pairing. We were unable to
fully implement it in time, but this is a likely next step in further developing this program.
"""

import plotly.graph_objects as go


from driver import moves, pokemons
from battle import game_round
import copy

def get_heatmap():
    """
    Gives heatmap of each pokemon winning against all other pokemon
    :param:
    :returns:

    """

    pass

def _do_rounds(poke1, poke2, k=100):
    """
    Args:
        poke1: pokemon name
        poke2: pokemon name
        k: number of battles to simulate

    Returns: number of battles pokemon 1 won

    """
    wins = 0
    for i in range(k):
        # print(f'Round {i+1}')
        a = copy.deepcopy(poke1)
        # print(a)
        b = copy.deepcopy(poke2)
        # print(b)
        while a.health > 0 and b.health > 0:
            amove = moves[a.choose_random_move()]
            bmove = moves[b.choose_random_move()]
            game_round(a, b, amove, bmove)
        if a.health > 0:
            wins += 1
    # print(wins)
    return wins


def get_many_battles(k):
    """
    Runs k battles for each pairing
    Returns: a list of lists, where each list is for one Pokemon and each value within

    """
    outer = []
    lst_poke = list(pokemons.keys())
    lst_poke.remove("Ditto")
    for i in lst_poke:
        inner = []
        for j in lst_poke:
            inner.append(_do_rounds(pokemons[i], pokemons[j], k))
        outer.append(inner)
        print(f'done with {i}')
    return outer

def main():
    please = get_many_battles(100)
    print(please)

main()
