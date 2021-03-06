from GUI.Board import *
from GeneticAlgorithm import *
import pyautogui
import pygame

screen_width, screen_height = pyautogui.size()

class MainWindow:
    """This class creates the GUI Window and its components"""
    __instance = None
    __bg_image = pygame.image.load("images/background.jpg")
    __done = False
    __WIDTH = screen_width
    __HEIGHT = int(screen_height*0.9)

    @staticmethod
    def get_instance():
        if MainWindow.__instance is None:
            MainWindow()
        return MainWindow.__instance

    def __init__(self):

        if MainWindow.__instance is not None:
            raise Exception("There's already a Window running!")

        else:
            MainWindow.__instance = self
            self.__create_window()

    def __create_window(self):

        pygame.init()
        screen = pygame.display.set_mode((self.__WIDTH, self.__HEIGHT))

        pygame.display.set_caption('BomberTEC')
        board = Board.get_instance(self.__WIDTH, self.__HEIGHT)
        board.enemies.update()
        genetic_algorithm = GeneticAlgorithm()
        #board.matrix.enemy0.update()
        #board.matrix.enemy1.update()

        while not self.__done:
            screen.blit(self.__bg_image, (0, 0))
            board.check_alive_players()
            if not board.end_game:
                board.draw_base(screen)
                board.draw_board(screen)
                board.draw_stats(screen)
                board.draw_titles(screen)
                actual_time = pygame.time.get_ticks()
                board.create_power_up(actual_time)
                genetic_algorithm.crossover(actual_time)  # executes crossover
                board.change_velocity(actual_time)
                board.change_detonation_time(actual_time)
                board.users.update()

            else:
                board.draw_end_window(board.winner_player, screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
