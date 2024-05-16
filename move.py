import random
import math

class Move:
    """
    Move object that represents a single move a Pokemon can use from Gen 1.
    ATTRIBUTES:
        name (str):     Name of move
        type (str):     Type of move (e.g. Fire, Water)
        cat (str):      Category of move (e.g. Physical, Special)
        pp (int):       Number of times a move can be used in a single battle
        pow (int):      Power of move, used in damage calculation
        acc (float):    Chance move will actually hit target
        desc (str):     Webscraped description of move
        effects (dict): Dictionary that houses dictionaries that represent individual effects
    METHODS:
        __init__:           Initializes object
        __str__:            Creates string representation of object
        _generate_effects:  Populates effects dictionary based on description
        calc_damage:        Calculates damage dealt by move
        check_status:       Checks if status is procced by move
        activate_move:      Goes through and runs entire move (damage, status)
    """

    # Global variables for important info
    TYPE_ADVANTAGE = {
        "Normal": {"Normal": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 1, "Fighting": 1, "Poison": 1,
                   "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 0.5, "Ghost": 0, "Dragon": 1, "Dark": 1,
                   "Steel": 0.5, "Fairy": 1},
        "Fire": {"Normal": 1, "Fire": 0.5, "Water": 0.5, "Grass": 2, "Electric": 1, "Ice": 2, "Fighting": 1,
                 "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 2, "Rock": 0.5, "Ghost": 1, "Dragon": 0.5,
                 "Dark": 1, "Steel": 2, "Fairy": 1},
        "Water": {"Normal": 1, "Fire": 2, "Water": 0.5, "Grass": 0.5, "Electric": 1, "Ice": 1, "Fighting": 1,
                  "Poison": 1, "Ground": 2, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 2, "Ghost": 1, "Dragon": 0.5,
                  "Dark": 1, "Steel": 1, "Fairy": 1},
        "Grass": {"Normal": 1, "Fire": 0.5, "Water": 2, "Grass": 0.5, "Electric": 1, "Ice": 1, "Fighting": 1,
                  "Poison": 0.5, "Ground": 2, "Flying": 0.5, "Psychic": 1, "Bug": 0.5, "Rock": 2, "Ghost": 1,
                  "Dragon": 0.5, "Dark": 1, "Steel": 0.5, "Fairy": 1},
        "Electric": {"Normal": 1, "Fire": 1, "Water": 2, "Grass": 0.5, "Electric": 0.5, "Ice": 1, "Fighting": 1,
                     "Poison": 1, "Ground": 0, "Flying": 2, "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1,
                     "Dragon": 0.5, "Dark": 1, "Steel": 1, "Fairy": 1},
        "Ice": {"Normal": 1, "Fire": 0.5, "Water": 0.5, "Grass": 2, "Electric": 1, "Ice": 0.5, "Fighting": 1,
                "Poison": 1, "Ground": 2, "Flying": 2, "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1, "Dragon": 2,
                "Dark": 1, "Steel": 0.5, "Fairy": 1},
        "Fighting": {"Normal": 2, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 2, "Fighting": 1,
                     "Poison": 0.5, "Ground": 1, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 2, "Ghost": 0,
                     "Dragon": 1, "Dark": 2, "Steel": 2, "Fairy": 0.5},
        "Poison": {"Normal": 1, "Fire": 1, "Water": 1, "Grass": 2, "Electric": 1, "Ice": 1, "Fighting": 1,
                   "Poison": 0.5, "Ground": 0.5, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 0.5, "Ghost": 0.5,
                   "Dragon": 1, "Dark": 1, "Steel": 0, "Fairy": 2},
        "Ground": {"Normal": 1, "Fire": 2, "Water": 1, "Grass": 0.5, "Electric": 2, "Ice": 1, "Fighting": 1,
                   "Poison": 2, "Ground": 1, "Flying": 0, "Psychic": 1, "Bug": 0.5, "Rock": 2, "Ghost": 1, "Dragon": 1,
                   "Dark": 1, "Steel": 2, "Fairy": 1},
        "Flying": {"Normal": 1, "Fire": 1, "Water": 1, "Grass": 2, "Electric": 0.5, "Ice": 1, "Fighting": 2,
                   "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 2, "Rock": 0.5, "Ghost": 1, "Dragon": 1,
                   "Dark": 1, "Steel": 0.5, "Fairy": 1},
        "Psychic": {"Normal": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 1, "Fighting": 2, "Poison": 2,
                    "Ground": 1, "Flying": 1, "Psychic": 0.5, "Bug": 1, "Rock": 1, "Ghost": 1, "Dragon": 1, "Dark": 0,
                    "Steel": 0.5, "Fairy": 1},
        "Bug": {"Normal": 1, "Fire": 0.5, "Water": 1, "Grass": 2, "Electric": 1, "Ice": 1, "Fighting": 0.5,
                "Poison": 0.5, "Ground": 1, "Flying": 0.5, "Psychic": 2, "Bug": 1, "Rock": 1, "Ghost": 0.5, "Dragon": 1,
                "Dark": 2, "Steel": 0.5, "Fairy": 0.5},
        "Rock": {"Normal": 1, "Fire": 2, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 2, "Fighting": 0.5, "Poison": 1,
                 "Ground": 0.5, "Flying": 2, "Psychic": 1, "Bug": 2, "Rock": 1, "Ghost": 1, "Dragon": 1, "Dark": 1,
                 "Steel": 0.5, "Fairy": 1},
        "Ghost": {"Normal": 0, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 1, "Fighting": 1, "Poison": 1,
                  "Ground": 1, "Flying": 1, "Psychic": 2, "Bug": 1, "Rock": 1, "Ghost": 2, "Dragon": 1, "Dark": 0.5,
                  "Steel": 1, "Fairy": 1},
        "Dragon": {"Normal": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 1, "Fighting": 1, "Poison": 1,
                   "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1, "Dragon": 2, "Dark": 1,
                   "Steel": 0.5, "Fairy": 0},
        "Dark": {"Normal": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 1, "Fighting": 0.5, "Poison": 1,
                 "Ground": 1, "Flying": 1, "Psychic": 2, "Bug": 1, "Rock": 1, "Ghost": 2, "Dragon": 1, "Dark": 0.5,
                 "Steel": 1, "Fairy": 0.5},
        "Steel": {"Normal": 1, "Fire": 0.5, "Water": 0.5, "Grass": 1, "Electric": 0.5, "Ice": 2, "Fighting": 1,
                  "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 2, "Ghost": 1, "Dragon": 1,
                  "Dark": 1, "Steel": 0.5, "Fairy": 2},
        "Fairy": {"Normal": 1, "Fire": 0.5, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 1, "Fighting": 2, "Poison": 1,
                  "Ground": 0.5, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1, "Dragon": 2, "Dark": 2,
                  "Steel": 0.5, "Fairy": 1},
        "True": {"Normal": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 1, "Fighting": 1, "Poison": 1,
                  "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1, "Dragon": 1, "Dark": 1,
                  "Steel": 1, "Fairy": 1}
    }
    STAGES = {-6: 0.35, -5: 0.28, -4: 0.33, -3: 0.4, -2: 0.5, -1: 0.66,
              0: 1, 1: 1.5, 2: 2, 3: 2.5, 4: 3, 5: 3.5, 6: 4}

    # Keywords for adding effects based on move description
    inflict_status = {'burn': 'Burn', 'freez': 'Freeze', 'paralyz': 'Paralyze', 'flinch': 'Flinch',
                      'poisoni': 'Poison', 'confus': 'Confuse'}
    boolean_vals = {'increased critical': 'High Crit', 'one-hit': 'Instakill', 'wild': 'Useless',
                    'recoil': 'Recoil', 'crash': 'Crash', ' following turn': 'Delayed',
                    'whatsoever': 'Useless'}
    stats = ['Attack', 'Defense', 'Special', 'Speed', 'accuracy', 'evasion']

    def __init__(self, stats):
        """
        Initializes a new move
        :param stats (list): List of values that represent a row from moves.csv, separated by commas
        """
        self.name = stats[1]
        self.type = stats[2]
        self.cat = stats[3]
        self.pp = int(stats[4])
        self.pow = int(stats[5])
        self.acc = float(stats[6])
        self.desc = stats[7].replace(';', '.')
        self.effects = {}
        self._generate_effects()

    def __str__(self):
        """
        Creates string representation of move
        :return (str): String representation of move for printing purposes
        """
        return f'{self.name}, a {self.type} {self.cat} move with {self.pow} POW. \nEffects: {str(self.effects)}'

    def _generate_effects(self):
        """
        Helper function that reads webscraped description of move and grabs info about special effects
        (e.g. status effects, move abilities) Effects are stored in effects dictionary. This is done by
        checking for associated keywords within the  description. For example, a sentence with the word freeze
        implies the move will proc freeze.
        :return: None
        """

        # Checks if there are secondary effects and splits description into sentences
        if 'no secondary effect' not in self.desc:
            sentences = self.desc.split('.')
            for sent in sentences:

                # Checks for simple status effects (Burn, Freeze, Paralysis, Flinch, Poison, Confuse)
                for phrase, effect in Move.inflict_status.items():
                    if phrase in sent:
                        if effect not in self.effects:
                            self.effects[effect] = {}

                        # Assumes that percentages refer to chance of status proccing
                        if '%' in sent and 'chance' not in self.effects[effect]:
                            self.effects[effect]['chance'] = float(
                                sent[(sent.index('%') - 3):sent.index('%')].strip()) / 100

                        # Checks for moves that cannot paralyze certain Pokemon types (e.g. electric, ghost)
                        if 'cannot paralyze' in sent:
                            self.effects['Paralyze']['immune'] = sent[
                                                                 sent.index('cannot paralyze') +
                                                                 16:sent.index('-type')]

                # Checks for simple move abilities (e.g. hits twice, recoil damage)
                for phrase, effect in Move.boolean_vals.items():
                    if phrase in sent and effect not in self.effects:
                        self.effects[effect] = {}

                # Checks if the move hits multiple times
                if 'multi-' in sent or 'Multihit' in self.effects:
                    if 'Multihit' not in self.effects:
                        self.effects['Multihit'] = {}
                    if 'twice' in sent:
                        self.effects['Multihit']['times'] = 'twice'
                    elif '2-5' in sent:
                        self.effects['Multihit']['times'] = 'multiple'

                # Checks if the move will directly change a stat (including the target, which stat, and by how much)
                if 'increases' in sent or 'decreases' in sent or 'lower' in sent or 'raise' in sent:
                    if 'StatChange' not in self.effects:
                        self.effects['StatChange'] = {'change': 1, 'chance': 1}
                    if 'target' in sent or 'opponent' in sent:
                        self.effects['StatChange']['target'] = 'opponent'
                    if 'user' in sent:
                        self.effects['StatChange']['target'] = 'user'
                    if 'two' in sent:
                        self.effects['StatChange']['change'] = 2
                    if 'decreases' in sent or 'lowering' in sent:
                        self.effects['StatChange']['change'] = abs(self.effects['StatChange']['change']) * -1
                    if 'lowering' in sent:
                        self.effects['StatChange']['chance'] = 0.33
                    for stat in Move.stats:
                        if stat in sent:
                            self.effects['StatChange']['stat'] = stat.lower()

                # Checks for damage over time move. Currently not implemented.
                if '2-5 turns' in sent and 'Multihit' not in self.effects:
                    if 'DOT' not in self.effects:
                        self.effects['DOT'] = {}

                # Extra code to check for poison proc
                if 'poisons' in sent and 'Poison' not in self.effects:
                    self.effects['Poison'] = {'chance': 1}

                # Checks for multi turn move that confuses attacker at end. Currently not implemented.
                if 'fatigue' in sent and 'Confuse' in self.effects:
                    del self.effects['Confuse']
                    self.effects['Fatigues'] = {}

                # Checks for self-destructive moves
                if 'user to faint' in sent and self.pow > 0:
                    if 'SelfDestruct' not in self.effects:
                        self.effects['SelfDestruct'] = {}

                # Checks for moves that cause sleep
                if 'sleep' in sent and 'only' not in sent:
                    if 'Sleep' not in self.effects:
                        self.effects['Sleep'] = {}
                    if 'target' in sent:
                        self.effects['Sleep']['target'] = 'opponent'
                    else:
                        self.effects['Sleep']['target'] = 'self'

                # Checks for moves that allow user to heal
                if 'restore' in sent and 'once' not in sent:
                    if 'Heal' not in self.effects:
                        self.effects['Heal'] = {}
                    if 'target' in sent:
                        self.effects['Heal']['type'] = 'lifesteal'
                    elif self.effects['Heal'] == {}:
                        self.effects['Heal']['type'] = 'selfheal'

    def calc_damage(self, attacker, defender):
        """
        Checks move type, checks whether the move it hits / is critical, and
        calculates the damage a move will do.
        :param attacker (Pokemon): Pokemon object using the move
        :param defender (Pokemon: Pokemon object being hit by move
        :return damage (int): Damage that move will do
        """
        log = ''

        # Checks category. If status, immediately checks for status procs and returns 0
        if self.cat == 'Physical':
            a = attacker.attack
            d = defender.defense
        elif self.cat == 'Special':
            a = attacker.spattack
            d = defender.spdefense
        else:
            log += self.check_status(attacker, defender)
            return 0, log

        # Checks if move connects, and whether it takes crash damage
        hit_check = self.acc * attacker.accuracy / defender.evasion
        if random.random() > hit_check:
            log += 'It missed!\n'
            if 'Crash' in self.effects:
                log += f'{attacker.name} took 1 HP of crash damage!\n'
                attacker.health -= 1
            return 0, log

        # Checks for critical chance
        crit_check = random.randint(0, 255)
        crit = 1
        if 'High Crit' in self.effects:
            crit_check = int(crit_check / 8)
        if crit_check < int(attacker.speed / 2):
            crit = 2
            log += 'Critical!\n'

        # Calculates damage using formula, accounts for STAB / type advantage
        damage = (((2 * attacker.lv * crit / 5 + 2) * self.pow * a/d)/50 + 2)

        if self.type in attacker.types:
            damage *= 1.5
        for poke_type in defender.types:
            change = Move.TYPE_ADVANTAGE[self.type][poke_type]
            damage *= change
            # print(f'{self.type} type move attacking {poke_type} type Pokemon. Modifier: {change}')

        damage *= random.randint(217, 255) / 255

        # Final damage calculations and checks for status proc
        damage *= random.randint(217, 255)/255
        damage = int(damage)
        log += f'{damage} damage dealt!\n'
        log += self.check_status(attacker, defender)

        return damage, log

    def check_status(self, attacker, defender):
        """
        Checks if the move causes to defender / attacker to gain a status effect or stat change
        If it successfully does inflict one of the above, add it to the status dictionary for
        the respective Pokemon
        :param attacker (Pokemon): Pokemon object using the move
        :param defender (Pokemon: Pokemon object being hit by move
        :return: None
        """
        log = ''

        # Checks if the move procs Burn
        if 'Burn' in self.effects and 'chance' in self.effects['Burn']:
            if 'Freeze' in defender.start_status:
                del defender.effects['Freeze']
                log += f'{defender.name} thawed out!\n'
            if random.random() < self.effects['Burn']['chance']:
                if 'Fire' in defender.types:
                    log += f'{defender.name} got burned, but they are immune!\n'
                elif 'Burn' in defender.start_status:
                    log += f'{defender.name} got burned, but they are already burnt!\n'
                else:
                    log += f'{defender.name} got burned!\n'
                    defender.start_status['Burn'] = {}
                    defender.end_status['Burn'] = {}

        # Checks if move procs Poison
        if 'Poison' in self.effects and 'chance' in self.effects['Poison']:
            if random.random() < self.effects['Poison']['chance']:
                if 'Poison' in defender.end_status:
                    log += f'{defender.name} got poisoned, but they are already poisoned!\n'
                else:
                    log += f'{defender.name} got poisoned!\n'
                    defender.end_status['Poison'] = {}

        # Checks if move procs Freeze
        if 'Freeze' in self.effects and 'chance' in self.effects['Freeze']:
            if random.random() < self.effects['Freeze']['chance']:
                if 'Freeze' in defender.start_status:
                    log += f'{defender.name} got frozen, but they are already frozen!\n'
                else:
                    log += f'{defender.name} got frozen!\n'

        # Checks if move procs Paralysis
        if 'Paralyze' in self.effects:
            if 'immune' not in self.effects['Paralyze'] or self.effects['Paralyze']['immune'] not in defender.types:
                if 'chance' not in self.effects['Paralyze'] or random.random() < self.effects['Paralyze']['chance']:
                    if 'Paralyze' in defender.start_status:
                        log += f'{defender.name} got paralyzed, but they are already paralyzed!\n'
                    else:
                        log += f'{defender.name} got paralyzed!\n'
                        defender.start_status['Paralyze'] = {}
                        defender.end_status['Paralyze'] = {}
            else:
                log += f'{defender.name} got paralyzed, but they are immune!\n'

        # Checks if move procs Flinch
        if 'Flinch' in self.effects and 'chance' in self.effects['Flinch']:
            if random.random() < self.effects['Flinch']['chance']:
                log += f'{defender.name} flinched!\n'
                defender.start_status['Flinch'] = {}

        # Checks if move procs Confuse
        if 'Confuse' in self.effects:
            if 'chance' not in self.effects['Confuse'] or random.random() < self.effects['Confuse']['chance']:
                if 'Confuse' in defender.start_status:
                    log += f'{defender.name} got confused, but they are already confused!\n'
                else:
                    log += f'{defender.name} got confused!\n'
                    defender.start_status['Confuse'] = {'turns': random.randint(1, 4)}

        # Checks if move procs Sleep
        if 'Sleep' in self.effects:
            user = attacker
            if self.effects['Sleep']['target'] != 'self':
                user = defender
            if 'Sleep' in user.start_status:
                log += f'{user.name} is already asleep!\n'
            else:
                log += f'{user.name} feel asleep\n'
                if self.name == 'Rest':
                    user.start_status['Sleep'] = {'turns': 2}
                else:
                    user.start_status['Sleep'] = {'turns': random.randint(1, 5)}

        # Checks if move changes stat
        if 'StatChange' in self.effects and len(self.effects['StatChange']) > 0 and 'target' in self.effects['StatChange']:
            if random.random() < self.effects['StatChange']['chance']:
                user = defender
                if self.effects['StatChange']['target'] == 'user':
                    user = attacker
                stat_change = [self.effects['StatChange']['stat']]
                if stat_change == ['special']:
                    stat_change = ['spattack', 'spdefense']

                # Adds respective stat change to effects dictionary
                for stat in stat_change:
                    if 'StatChange' not in user.start_status:
                        user.start_status['StatChange'] = {stat: self.effects['StatChange']['change']}
                        user.end_status['StatChange'] = {stat: self.effects['StatChange']['change']}
                    elif stat not in user.start_status['StatChange']:
                        user.start_status['StatChange'][stat] = self.effects['StatChange']['change']
                        user.end_status['StatChange'][stat] = self.effects['StatChange']['change']
                    else:
                        val = min(max(user.start_status['StatChange'][stat] + self.effects['StatChange']['change'], -6), 6)
                        user.start_status['StatChange'][stat] = val
                        user.end_status['StatChange'][stat] = val
                    log += f"{user.name}'s {stat} changed by {self.effects['StatChange']['change']}\n"
        return log

    def activate_move(self, attacker, defender):
        """
        Complete activates a move, including multi damage calculation / non-status effects
        :param attacker (Pokemon): Pokemon object using the move
        :param defender (Pokemon: Pokemon object being hit by move
        :return: None
        """
        log = ''
        if '!' in self.name:
            log += f'{attacker.name} {self.desc}\n'
            if 'onfu' in self.name:
                dmg, l = self.calc_damage(attacker, attacker)
                log += l
                attacker.health -= dmg
            return log

        log += f'{attacker.name} uses {self.name} against {defender.name}.\n'

        # Checks if the move actually does anything
        if 'Useless' in self.effects:
            log += 'It has no effect!\n'

        # Checks if move will activate on the second turn
        elif 'Delayed' in self.effects and 'Delayed' not in attacker.start_status:
            log += f'{attacker.name} is charging up!\n'
            attacker.start_status['Delayed'] = self.name

        # Checks if move can insta-kill the move
        elif 'Instakill' in self.effects:
            hit_check = self.acc * attacker.accuracy / defender.evasion
            if random.random() > hit_check or attacker.speed < defender.speed:
                log += 'It missed!\n'
            else:
                log += f'It hit! {defender.name} immediately fainted!\n'
                defender.health = 0

        # Checks if the move will hit multiple times
        elif 'Multihit' in self.effects and 'times' in self.effects['Multihit']:
            if self.effects['Multihit']['times'] == 'multiple':
                choice = [2, 3, 4, 5]
                times = random.choices(choice, weights=[3, 3, 1, 1], k=1)[0]
                log += f'It hits {times} times!\n'
                for i in range(times):
                    dmg, l = self.calc_damage(attacker, defender)
                    log += l
                    defender.health -= dmg

            # Case when the move hits only twice
            elif self.effects['Multihit']['times'] == 'twice':
                log += 'It hits 2 times!\n'
                dmg, l = self.calc_damage(attacker, defender)
                log += l
                defender.health -= dmg
                dmg, l = self.calc_damage(attacker, defender)
                log += l
                defender.health -= dmg

        # Checks moves that only strike once
        else:
            dmg, l = self.calc_damage(attacker, defender)
            log += l
            defender.health -= dmg

            # Checks if move will deal splash back damage against attacker
            if 'Recoil' in self.effects:
                recoil = int(dmg / 4)
                log += f'{attacker.name} took {recoil} damage as recoil!\n'
                attacker.health -= recoil

            # Checks if move will cause attacker to self destruct
            elif 'SelfDestruct' in self.effects:
                log += f'{attacker.name} fainted after the attack!\n'
                attacker.health = 0

            # Checks if move will heal attacker
            elif 'Heal' in self.effects:
                health = min(attacker.max_health - attacker.health, attacker.max_health // 2)
                if self.effects['Heal']['type'] == 'lifesteal':
                    health = min(attacker.max_health - attacker.health, dmg // 2)
                attacker.health += health
                log += f'{attacker.name} healed {health} HP!\n'
        return log
