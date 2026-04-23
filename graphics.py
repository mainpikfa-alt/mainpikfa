import pygame
import random
import os
from constants import *

def create_asset_images():
    """Функция для создания изображений из ассетов"""
    try:
        assets = {}
        
        # Синее поле
        blue_grid = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
        blue_grid.fill((25, 25, 80))  # Темно-синий фон
        # Рисуем сетку
        for i in range(GRID_SIZE + 1):
            pygame.draw.line(blue_grid, (60, 150, 200), (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_SIZE), 1)
            pygame.draw.line(blue_grid, (60, 150, 200), (0, i * CELL_SIZE), (BOARD_SIZE, i * CELL_SIZE), 1)
        assets['blue_grid'] = blue_grid
        
        # Зеленое поле с радаром
        green_grid = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
        green_grid.fill((10, 50, 10))  # Темно-зеленый фон
        # Рисуем сетку
        for i in range(GRID_SIZE + 1):
            pygame.draw.line(green_grid, (20, 200, 20), (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_SIZE), 1)
            pygame.draw.line(green_grid, (20, 200, 20), (0, i * CELL_SIZE), (BOARD_SIZE, i * CELL_SIZE), 1)
        # Добавляем круг радара
        pygame.draw.circle(green_grid, (20, 150, 20), (BOARD_SIZE//2, BOARD_SIZE//2), BOARD_SIZE//3, 1)
        pygame.draw.circle(green_grid, (20, 150, 20), (BOARD_SIZE//2, BOARD_SIZE//2), BOARD_SIZE//2, 1)
        assets['green_grid'] = green_grid
        
        # Изображения кораблей
        ships = {}
        ship_sizes = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]
        
        for width, height in ship_sizes:
            ship_img = pygame.Surface((width * CELL_SIZE - 4, height * CELL_SIZE - 4), pygame.SRCALPHA)
            ship_img.fill((180, 180, 180))  # Серый цвет кораблей
            # Добавляем детали
            pygame.draw.rect(ship_img, (100, 100, 100), (width * CELL_SIZE // 4, height * CELL_SIZE // 4, 
                                                      width * CELL_SIZE // 2, height * CELL_SIZE // 2))
            ships[f"ship_{width}x{height}"] = ship_img
            
        assets['ships'] = ships
        
        return assets
    except Exception as e:
        print(f"Ошибка при создании ассетов: {e}")
        return {}

def load_image(filename, window_width, window_height):
    """Загрузка и масштабирование изображения"""
    try:
        if os.path.exists(filename):
            image = pygame.image.load(filename)
            return pygame.transform.scale(image, (window_width, window_height))
    except Exception as e:
        print(f"Ошибка при загрузке изображения {filename}: {e}")
    
    return create_backup_image(window_width, window_height)

def create_backup_image(window_width, window_height):
    """Создание резервного фонового изображения"""
    try:
        backup_image = pygame.Surface((window_width, window_height))
        backup_image.fill((100, 150, 200))  # Синий фон
        
        # Имитация морского боя на резервном изображении
        for _ in range(20):
            x, y = random.randint(0, window_width), random.randint(0, window_height)
            radius = random.randint(5, 20)
            color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            pygame.draw.circle(backup_image, color, (x, y), radius)
            
        return backup_image
    except Exception as e:
        print(f"Ошибка при создании фона: {e}")
        # Создаем простой фон
        simple_bg = pygame.Surface((window_width, window_height))
        simple_bg.fill((100, 150, 200))
        return simple_bg