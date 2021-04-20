from random import randint as random_randint
from random import choice as random_choice
from time import sleep as time_sleep


def get_int_in_bounds(left_bound: int, right_bound: int, value: int):
    # leftBound=0; rightBound=9; func=max(left, min(right, x));
    # in: -1; result of max(0, min(9, -1)) is 0
    # in: 10; result of (max(0, min(9, 10)) is 9
    # in: 5; result of max(0, min(9, 5)) is 5
    return max(left_bound, min(right_bound, value))


class Event:
    STEP_STR = "Step {0}. "
    EVENT_RECOVERED = "{0} recovered for {1} points."
    EVENT_HIT = "{0} hits {1}: -{2} dmg."
    EVENT_KILLED = "{0} killed {1}."

    def __init__(self, step: int, event_str: str, *args):
        """
        :param step: The step of an action
        :param event_str: Declared string from Event class
        :param args: args for formatting event string
        """
        self.__args = args
        self.__event_str = event_str
        self.__step = step

    @classmethod
    def HIT(cls, step, attacker: 'Player', opponent: 'Player', damage) -> "Event":
        return cls(step, cls.EVENT_HIT, attacker, opponent, damage)

    @classmethod
    def KILL(cls, step, killer: 'Player', victim: 'Player') -> "Event":
        return cls(step, cls.EVENT_KILLED, killer.name, victim)

    @classmethod
    def RECOVER(cls, step, player: 'Player', score) -> "Event":
        return cls(step, cls.EVENT_RECOVERED, player, score)

    def get_step_int(self) -> int:
        """
        :return: Returns the step integer
        """
        return self.__step

    @property
    def step_formatted(self) -> str:
        """
        :return: Returns formatted string of step
        """
        return f"Step {self.__step}."

    def get_info(self):
        return self.step_formatted + self.__event_str.format(*self.__args)

    def __str__(self):
        return self.get_info()


class Player:
    """
    You can change such staticVars of Class Player:

    maxHealth - Max health of each PlayerObj (default 100)
    middleHitScore - Middle Int Damage Score (default 22)
    middleRecoveryScore - Middle Int Recovery Score (default 22)

    Just import Player class and than:

    Player.maxHealth = {yourValue}
    middleHitScore = {your Value}
    middleRecoveryScore = {your Value}

    Hits and recover points will be calculated in Player#calculate_score_value
    They are used as offsets from middle scores to give each time different value
    hitWeakPercents = 25 # it means that final hit will be from 75 to 125 points if middleHit=100
    hitStrongPercents
    recoverPercents
    """
    maxHealth: int = 100
    middleHitScore: int = 22
    middleRecoveryScore: int = 22

    # Hits and recover points will be calculated in {@see Player#calculate_score_value }
    hitWeakPercents = 25
    hitStrongPercents = 50
    recoverPercents = 30

    def __init__(self, name: str, player_is_computer: bool, player_id: int):
        """
        :param name: Player's name
        :param player_is_computer: Player is Computer
        """
        self.__name: str = name
        self.__health: int = Player.maxHealth
        self.__is_comp: bool = player_is_computer
        self.__is_died: bool = False
        self.__id: int = player_id
        self.__killer: 'Player' = None
        self.__max_random_state: int = 6
        self.__kill_event: Event = None
        self.__last_event: Event = None

    @property
    def name(self) -> str:
        return f"{self.__name}#{self.__id}"

    @property
    def health(self) -> int:
        return self.__health

    @health.setter
    def health(self, health_: int):
        if not self.__is_died:
            self.__health = get_int_in_bounds(0, Player.maxHealth, health_)

    @property
    def is_died(self) -> bool:
        return self.__is_died

    @property
    def id(self) -> int:
        return self.__id

    @property
    def is_comp(self) -> bool:
        return self.__is_comp

    def act_random(self, opponent: 'Player', step: int):
        """
        Randomizes Player's deed and manipulates with health

        :param step: game step#ID
        :param opponent: Another PlayerObj (self != opponent)
        """
        if self.__is_comp:
            self.__max_random_state = 9 if self.health <= round(Player.maxHealth * 0.35) else 6
            # Increasing chance of healing for computer

        deed_state = random_randint(1, self.__max_random_state)
        if deed_state in (1, 2):
            self.__set_last_event(self.hit_opponent(step, opponent, self.hitWeakPercents))
        elif deed_state in (3, 4):
            self.__set_last_event(self.hit_opponent(step, opponent, self.hitStrongPercents))
        else:  # elif deed_state >= 3
            self.__set_last_event(self.recover_yourself(step))

    def __set_last_event(self, event):
        """Sets the last event like Hot or recovery"""
        self.__last_event = event

    def get_last_event(self):
        """:returns: Player's last deed, like hit or recovery """
        return self.__last_event

    @staticmethod
    def calculate_score_value(middle_score: int, score_percentage: int):
        """Calculates final score that depends on 'Player. ...Percents' value and middleScores"""
        score_offset = random_randint(-score_percentage, +score_percentage) / 100
        score = int(middle_score + (middle_score * score_offset) + 1)
        return score

    def hit_opponent(self, step: int, opponent: 'Player', hit_bounds_percentage: int) -> Event:
        """
        Decreases opponent's health with range
        :param hit_bounds_percentage:
        :param step: game step#ID
        :param opponent: Another PlayerObj (self != opponent)
        :returns: Last Player's Deed (attacker hits opponent)
        """
        damage = self.calculate_score_value(Player.middleHitScore, hit_bounds_percentage)
        opponent.health -= damage
        return Event.HIT(step, self, opponent, damage)

    def recover_yourself(self, step: int) -> Event:
        """
        Increases Player's health;

        :param step: game step#ID
        :returns: Last Player's Deed (Recovery)
        """
        score = self.calculate_score_value(Player.middleRecoveryScore, self.recoverPercents)
        self.health += score
        return Event.RECOVER(step, self, score)

    def kill_by(self, killer: 'Player', step: int):
        """Sets player's death info and :returns: get_kill_event()"""
        self.__is_died = True
        self.__killer = killer
        self.__kill_event = Event.KILL(step, killer, self)
        return self.__kill_event

    def get_info(self) -> str:
        """:returns: Player's current information"""
        if self.__is_died:
            return f"{self.name} (was killed by {self.__killer.name})"
        return f"{self.name}({self.health}/{self.maxHealth})"

    def __repr__(self) -> str:
        return "{0}({1}/{2})".format(self.name, self.health, Player.maxHealth)


class ConsoleGame:
    """
    You can change such staticVars of Class ConsoleGame:
    stepSleepSeconds - Used to make program sleep for any time (default 5sec)
    """
    __GAME_OVER_RESULT = 'Game Over!\nTotal players: {0}\nWinner: {1}\nLosers:\n{2}'
    __ALIVE_PLAYERS = "Alive players: {0}\n\n"
    stepSleepSeconds = 5

    def __init__(self, log_to_file: bool = True):
        """Inits ConsoleGame object."""
        self.__players: "list[Player]" = list()
        # List of Player objs
        self.__count_players = 0
        self.__step = 0
        self.__log_to_file = log_to_file
        self.__losers = list()
        self.__winner = None
        # Only one winner

    @property
    def winner(self):
        return self.__winner

    @property
    def losers(self):
        return self.__losers

    def console_game_set_up_settings(self):
        """Setting Up game configurations with console"""

        def int_input(prompt):
            temp = input(prompt)
            while not temp.isdigit():
                temp = input("Try again, must be integers! " + prompt)
            return int(temp)

        Player.maxHealth = int_input(f"Write Player max health. (default {Player.maxHealth}): ")
        Player.middleHitScore = int_input(f"Write middle score of damage. (default {Player.middleHitScore}): ")
        Player.middleRecoveryScore = int_input(f"Write middle recovery score. (default {Player.middleRecoveryScore}): ")
        ConsoleGame.stepSleepSeconds = int_input(f"Write sleepTime btw. steps. (default {self.stepSleepSeconds}): ")
        len_players = int_input("How many players do you want to add (except Comp)?: ")

        self.add_player("Computer", True)
        for i in range(len_players):
            self.add_player(input(f'Give name for Player#{i + 2}: '), True)

        input("\nWrite something to start the game!\n\n")

    def add_player(self, name: str, is_comp: bool = False):
        """
        :param name: New Player's name
        :param is_comp: bool player is computer
        """
        self.__count_players += 1
        self.__players.append(Player(name, is_comp, self.__count_players))

    def start_game(self):
        """Method starts game"""
        assert len(self.__players) >= 2, "Must be 2 players at least!"
        assert any(obj.is_comp for obj in self.__players), "Must be at least 1 Computer Player!"
        alive_pl_indexes = list(range(len(self.__players)))
        # alive players indexes

        if ConsoleGame.stepSleepSeconds == 0:
            ConsoleGame.stepSleepSeconds = 0.2

        while len(alive_pl_indexes) != 1:
            self.__step += 1
            # Increasing Game.__step

            attacker_ind = random_choice(alive_pl_indexes)
            opponent_ind = random_choice(alive_pl_indexes)
            # random choice of alive players indexes

            while opponent_ind == attacker_ind:
                opponent_ind = random_choice(alive_pl_indexes)
                # for preventing cases when attacker == opponent

            attacker = self.__players[attacker_ind]
            opponent = self.__players[opponent_ind]
            attacker.act_random(opponent, self.__step)
            # Process random deeds with opponent (or healing himself)

            self.log(attacker.get_last_event().get_info())

            # Check if opponent's health less then 0
            if opponent.health <= 0:
                alive_pl_indexes.remove(opponent_ind)
                kill_event = opponent.kill_by(attacker, self.__step)
                self.__losers.append(opponent.get_info())
                self.log(kill_event.get_info())

            self.log(self.__ALIVE_PLAYERS.format(self.get_alive_players_info()))
            time_sleep(ConsoleGame.stepSleepSeconds)
            # Sleep between steps
        else:
            # Code when it is left one player
            self.__winner = self.__players[alive_pl_indexes[0]].get_info()
            result_text = self.__GAME_OVER_RESULT.format(self.__count_players, self.winner, '\n'.join(self.losers))
            self.log(result_text)

    def log(self, string_info: str):
        """:param string_info: string logging information"""
        print(string_info)
        if self.__log_to_file:
            with open("ConsoleGame.txt", 'a') as log_file:
                print(string_info, file=log_file)

    def set_log_to_file(self, log_to_file: bool) -> None:
        self.__log_to_file = log_to_file

    def get_alive_players_info(self) -> str:
        """:returns: alive Players"""
        return ', '.join(map(Player.get_info, self.get_alive_players()))

    def get_alive_players(self) -> 'list[Player]':
        return [obj for obj in self.get_players() if not obj.is_died]

    def get_players(self) -> 'list[Player]':
        """:returns: ListPlayers"""
        return self.__players
