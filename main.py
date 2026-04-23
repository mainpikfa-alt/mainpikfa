#!/usr/bin/env python3
"""
Игра "Морской бой"
"""

import pygame
import sys
import time
from constants import WINDOW_WIDTH, WINDOW_HEIGHT
from game import Game

def main():
    """Главная функция запуска игры"""
    try:
        print("Запуск игры Морской Бой...")
        
        # Инициализация Pygame
        pygame.init()
        pygame.font.init()
        
        # Создание окна
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Морской Бой')
        
        # Загрузка шрифтов
        fonts = {
            'big': pygame.font.SysFont('Arial', 36),
            'medium': pygame.font.SysFont('Arial', 28),
            'small': pygame.font.SysFont('Arial', 20)
        }
        
        # Создание и запуск игры
        game = Game(screen, fonts)
        game.run()
        
    except Exception as e:
        print(f"Критическая ошибка при запуске игры: {e}")
        time.sleep(5)
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()