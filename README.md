## Console Game Project (For LightIT)
*Bohdan Snurnitsyn. bogdan171000@gmail.com*

#


Console game has two ***Clases***: **Player** and **ConsoleGame** which has privat param-list whith PlayerObjects

# So how to start..
**At first you should to download files "ConsoleGame.py" and the starting file "SecondTour.py"**

**So if you have downloaded "SecondTour.py" you can just run it**
#
# Another way is below..
#

1. You must create GamObject: 

       game = ConsoleGame(log_to_file=True)
   
   log_to_file meaning rhat all the game info will be saved to the file
   

2. Then you can set up game settings:
	One of the features of this ConsoleGame is that you can add Players as mush as you want 
	(In fact HR manager Julia said that it will be good if more then 2 players)
	
    
	First variant - set up settings like maxHealth, middleScores, sleepTime between steps and amount of Players in consoleMode:
    
	    game.console_game_set_up_settings()
	
    
	Second variant - you can set then up by yourself like:
    
        Player.maxHealth = 100
        Player.middleHitScore = 22
        Player.middleRecoveryScore = 22
   	    ConsoleGame.stepSleepSeconds = 5	
        game.add_player("Computer", is_comp=True)
    	game.add_player("Human")
    	game.add_player("John")
		
		# # You can add also more players :D
    	# game.add_player("John")
    	# game.add_player("Snack")
    	# game.add_player("Julia")
    	# game.add_player("Din")`
		
3. At the end you must start the game using method 

       game.start_game()
       
**The end.**
#
#
**Soo.. The code we have in the main file (starting file):**
#
#
    from ConsoleGame import *

    ask = input("Do you want change game settings? (Y/N)")
    game = ConsoleGame(log_to_file=True)

    if ask.lower() == 'y':
        game.console_game_set_up_settings()
    else:
        # _____ Player Settings
        Player.maxHealth = 100
        Player.middleHitScore = 22
        Player.middleRecoveryScore = 22

        # _____ ConsoleGame Settings
        ConsoleGame.stepSleepSeconds = 5

        game.add_player("Computer", is_comp=True)
        game.add_player("Human")
        game.add_player("John")

        # # You can add also more players :D
        # game.add_player("John")
        # game.add_player("Snack")
        # game.add_player("Julia")
        # game.add_player("Din")

    game.start_game()


	
	
		
		


