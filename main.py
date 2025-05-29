import pygame #import pygame untuk mengakses fungsi pygame

#import class Game dari file game.py
from game import Game

#titik masuk untuk program
if __name__ == '__main__':
    play_again = True # flag untuk menentukan apakah permainan akan diulang
    # loop untuk menjalankan permainan
    while play_again:
        game = Game() # buat instance dari class Game
        #Loop utama program - akan terus berjalan selama permainan masih berjalan
        if game.is_running:
            # Jalankan game, yang akan mengatur semua aspek permainan
            play_again = game.run() 
        else: 
            # Jika permainan tidak berjalan, setel play_again ke False
            play_again = False # Don't try to play again

    pygame.quit() #setelah semua permainan selesai, keluar dari pygame