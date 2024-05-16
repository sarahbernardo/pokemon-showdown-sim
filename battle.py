# Creating a battle
from pokemon import Pokemon
from move import Move
import random
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc


# Moves that replace Pokemon's current move based on status effect
paralyzed = Move([-1, '!Paralysis', 'Normal', 'Status', '999', '0', '100', 'is stunned!', {}])
asleep = Move([-1, '!Asleep', 'Normal', 'Status', '999', '0', '100', 'is sleeping...', {}])
confused = Move([-1, '!Confuse', 'Normal', 'Physical', '999', '40', '100', 'hurt itself in confusion!', {}])
blank = Move([-1, '!Blank', 'Normal', 'Status', '999', '0', '100', 'does nothing.', {}])
frozen = Move([-1, '!Freeze', 'Ice', 'Status', '999', '0', '100', 'is encased in ice...', {}])
flinched = Move([-1, '!Flinch', 'Normal', 'Status', '999', '0', '100', 'is too scared to move!', {}])


def game_round(poke1, poke2, poke1_move, poke2_move):
    """
    Simulates a round passing with both Pokemon using a move against each other

    Args:
        poke1 (Pokemon): First Pokemon (usually) user
        poke2 (Pokemon): Second Pokemon
        poke1_move (Move): Move that the first Pokemon plans to move
        poke2_move (Move): Move that the second Pokemon plans to move

    Returns:
        log (str): Log of the battle

    """

    # Creates log and Pokemon move dictionary
    log = ''
    mdict = {poke1: poke1_move, poke2: poke2_move}

    # check paralysis on both Pokemon since it affects speed and therefore who goes first
    if "Paralyze" in poke1.start_status.keys():
        poke1.speed = poke1.speed // 2

    if "Paralyze" in poke2.start_status.keys():
        poke2.speed = poke2.speed // 2

    # define a faster and slower Pokemon to determine which one goes first
    if poke1.speed >= poke2.speed:
        faster = poke1
        slower = poke2
    else:
        faster = poke2
        slower = poke1

    # check start statuses for the faster Pokemon
    if "Burn" in faster.start_status.keys():
        # burn cuts attack in half
        faster.attack = faster.attack // 2

    if "Paralyze" in faster.start_status.keys():
        # paralysis has a 25% chance of not allowing the Pokemon to move
        if random.random() < .25:
            mdict[faster] = paralyzed

    if "Sleep" in faster.start_status.keys():
        # sleep can run for 1-4 turns and the Pokemon cannot move during it
        if faster.start_status["Sleep"]["turns"] > 0:
            faster.start_status["Sleep"]["turns"] -= 1
            mdict[faster] = asleep
        else:
            del faster.start_status['Sleep']
            log += f'{faster.name} woke up!\n'

    if "Freeze" in faster.start_status.keys():
        # there's a 20% chance of thawing and the Pokemon cannot move while frozen
        if random.random() < .2:
            del faster.start_status["Freeze"]
            log += f'{faster.name} thawed out!'
        else:
            mdict[faster] = frozen

    if "Confuse" in faster.start_status.keys():
        # Confuse can last 1-4 turns and has a 50% chance of having the user hurt themselves
        if faster.start_status["Confuse"]["turns"] > 0:
            faster.start_status["Confuse"]["turns"] -= 1
        if random.random() < .5:
            mdict[faster] = confused

    if "Delayed" in faster.start_status.keys():
        # these moves will take place next turn, so we keep track of what they are for next turn
        if faster == poke1:
            poke1_next_move = poke1.start_status["Delayed"]
            poke1_move = blank
        else:
            poke2_next_move = poke1.start_status["Delayed"]
            poke2_move = blank
        del faster.start_status["Delayed"]

    # The faster Pokemon uses its move
    log += mdict[faster].activate_move(faster, slower)

    # Check to see if either Pokemon fainted, ending the battle
    if faster.health <= 0:
        log += str(slower.name) + " Wins!\n"
        return log
    elif slower.health <= 0:
        log += str(faster.name) + " Wins!\n"
        return log

    # Check the Slower Pokemon's starting Status
    if "Burn" in slower.start_status.keys():
        # burn cuts attack in half
        slower.attack = slower.attack // 2

    if "Paralyze" in slower.start_status.keys():
        # paralysis has a 25% chance of not letting them move
        if random.random() < .25:
            mdict[slower] = paralyzed

    if "Sleep" in slower.start_status.keys():
        # sleep lasts for 1-5 turns and the Pokemon can't move while inflicted
        if slower.start_status["Sleep"]["turns"] > 0:
            slower.start_status["Sleep"]["turns"] -= 1
            mdict[slower] = asleep
        else:
            del slower.start_status['Sleep']
            log += f'{slower.name} woke up!\n'

    if "Freeze" in slower.start_status.keys():
        # has a 20% chance of thawing and the Pokemon cannot move while inflicted
        if random.random() < .2:
            del slower.start_status["Freeze"]
            log += f'{slower.name} thawed out!'
        else:
            mdict[slower] = frozen

    if "Confuse" in slower.start_status.keys():
        # can last 1-4 turns and has a 50% chance of the User hurting themselves
        if slower.start_status["Confuse"]["turns"] > 0:
            slower.start_status["Confuse"]["turns"] -= 1
        if random.random() < .5:
            mdict[slower] = confused

    if "Delayed" in slower.start_status.keys():
        # these moves will take place next turn, so we keep track of what they are for next turn
        if slower == poke2:
            poke2_next_move = poke2.start_status["Delayed"]
            poke2_move = blank
        else:
            poke1_next_move = poke1.start_status["Delayed"]
            poke1_move = blank
        del lower.start_status["Delayed"]

    if "Flinch" in slower.start_status.keys():
        # if a Pokemon has the Flinch status they cannot move that turn
        mdict[slower] = flinched
        del slower.start_status["Flinch"]

    # Have the slower Pokemon use its move
    log += mdict[slower].activate_move(slower, faster)

    # Check to see if either Pokemon Fainted, ending the battle
    if faster.health <= 0:
        log += str(slower.name) + " Wins!\n"
        return log
    elif slower.health <= 0:
        log += str(faster.name) + " Wins!\n"
        return log

    # Check end of turn statuses for each Pokemon
    # At the end of the turn poison and burn both take away 1/16th of the
    # effected Pokemon's total hp
    if "Burn" in poke1.end_status.keys() or "Poison" in poke1.end_status.keys():
        dmg = poke1.max_health // 16
        poke1.health -= dmg
        log += f'{poke1.name} took {dmg} damage from a status!\n'

    if "Burn" in poke2.end_status.keys() or "Poison" in poke2.end_status.keys():
        dmg = poke1.max_health // 16
        poke2.health -= poke2.max_health // 16
        log += f'{poke2.name} took {dmg} damage from a status!\n'

    # Check to see if either Pokemon Fainted, ending the battle
    if faster.health <= 0:
        log += str(slower.name) + " Wins!\n"
        return log
    elif slower.health <= 0:
        log += str(faster.name) + " Wins!\n"
        return log

    return log