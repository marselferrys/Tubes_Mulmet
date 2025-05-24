import pygame # Import pygame to handle quit outside Game class

from game import Game

if __name__ == '__main__':
    play_again = True
    while play_again:
        game = Game()
        if game.is_running: # Only run if webcam initialized successfully
            play_again = game.run() # game.run() now returns True for play again, False for quit
        else: # If game couldn't even start (e.g., webcam error)
            play_again = False # Don't try to play again

    pygame.quit() # Ensure pygame is quit after all game sessions are done
