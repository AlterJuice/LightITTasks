from ConsoleGame import *

ask = input("Do you want to change game settings? (Y/N)")
game = ConsoleGame(log_to_file=True)

if ask.lower() == 'y':
    game.console_game_set_up_settings()
else:
    # Player Settings
    Player.maxHealth = 100
    Player.middleHitScore = 22
    Player.middleRecoveryScore = 22

    # ConsoleGame Settings
    ConsoleGame.stepSleepSeconds = 1

    game.add_player("Computer", is_comp=True)
    game.add_player("Human")
    game.add_player("John")

    # # You can also add more players
    # game.add_player("John")
    # game.add_player("Snack")
    # game.add_player("Julia")
    # game.add_player("Din")

game.start_game()
