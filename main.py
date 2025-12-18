import pygame
import time



def main():
    """Функция запуска игры"""
    try:
        print("Загрузка игры Морской Бой")
        #Pygame
        pygame.init()

        #Шрифт
        fonts = {}

    except:
        print()
    #Главное окно
    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption("Морской бой")