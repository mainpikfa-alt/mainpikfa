import random
import pygame
from constants import *

class Board:
    """Класс для управления игровой доской"""
    
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.shots = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.ships = []
        
    def can_place_ship(self, length, x, y, horizontal):
        """Проверка возможности размещения корабля"""
        if horizontal:
            if x + length > GRID_SIZE:
                return False
            # Проверяем область вокруг корабля
            for i in range(max(0, x-1), min(GRID_SIZE, x+length+1)):
                for j in range(max(0, y-1), min(GRID_SIZE, y+2)):
                    if self.grid[j][i] != 0:
                        return False
        else:
            if y + length > GRID_SIZE:
                return False
            # Проверяем область вокруг корабля
            for i in range(max(0, x-1), min(GRID_SIZE, x+2)):
                for j in range(max(0, y-1), min(GRID_SIZE, y+length+1)):
                    if self.grid[j][i] != 0:
                        return False
        return True
        
    def place_ship(self, length, x, y, horizontal):
        """Размещение корабля на доске"""
        if not self.can_place_ship(length, x, y, horizontal):
            return False
            
        # Размещение корабля
        ship_cells = []
        if horizontal:
            for i in range(length):
                self.grid[y][x+i] = 1
                ship_cells.append((x+i, y))
        else:
            for i in range(length):
                self.grid[y+i][x] = 1
                ship_cells.append((x, y+i))
                
        self.ships.append(ship_cells)
        return True
    
    def remove_ship_at(self, x, y):
        """Удаление корабля в указанной позиции"""
        # Проверяем, есть ли корабль в этой клетке
        if self.grid[y][x] == 0:
            return None
            
        # Находим корабль, которому принадлежит эта клетка
        for ship in self.ships:
            if (x, y) in ship:
                # Удаляем корабль с доски
                for ship_x, ship_y in ship:
                    self.grid[ship_y][ship_x] = 0
                
                # Удаляем корабль из списка
                self.ships.remove(ship)
                
                # Возвращаем длину удаленного корабля
                return len(ship)
        
        return None
            
    def place_ships_randomly(self):
        """Случайная расстановка всех кораблей"""
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.ships = []
        
        for ship_length in SHIPS:
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                x = random.randint(0, GRID_SIZE-1)
                y = random.randint(0, GRID_SIZE-1)
                horizontal = random.choice([True, False])
                if self.place_ship(ship_length, x, y, horizontal):
                    placed = True
                attempts += 1
    
    def shoot(self, x, y):
        """Выстрел по клетке"""
        if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE or self.shots[y][x] != 0:
            return False, "Недопустимый ход"
        
        self.shots[y][x] = 1
        
        if self.grid[y][x] == 1:
            # Проверка, потоплен ли корабль
            for ship in self.ships:
                if (x, y) in ship:
                    # Проверяем, все ли клетки корабля поражены
                    all_hit = True
                    for sx, sy in ship:
                        if self.shots[sy][sx] == 0:
                            all_hit = False
                            break
                    
                    if all_hit:
                        # Корабль потоплен, отмечаем клетки вокруг
                        for sx, sy in ship:
                            for dx in [-1, 0, 1]:
                                for dy in [-1, 0, 1]:
                                    nx, ny = sx + dx, sy + dy
                                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and self.shots[ny][nx] == 0:
                                        self.shots[ny][nx] = 2
                        return True, "Потоплен!"
                    return True, "Попадание!"
        
        return False, "Мимо!"
    
    def all_ships_sunk(self):
        """Проверка, все ли корабли потоплены"""
        for ship in self.ships:
            for x, y in ship:
                if self.shots[y][x] == 0:
                    return False
        return True

    def draw(self, screen, x, y, is_player, hide_ships=False, in_multiplayer=False, game_assets=None, fonts=None):
        """Отрисовка доски"""
        # Рисуем фон игрового поля
        if game_assets:
            if is_player:
                bg = game_assets.get('blue_grid', None)
            else:
                bg = game_assets.get('green_grid', None)
                
            if bg:
                screen.blit(bg, (x, y))
        
        if not game_assets or not bg:
            # Рисуем сетку, если нет изображения
            for i in range(GRID_SIZE + 1):
                pygame.draw.line(screen, BLACK, (x, y + i * CELL_SIZE), (x + BOARD_SIZE, y + i * CELL_SIZE), 2)
                pygame.draw.line(screen, BLACK, (x + i * CELL_SIZE, y), (x + i * CELL_SIZE, y + BOARD_SIZE), 2)
        
        # Буквы и цифры
        letters = "АБВГДЕЖЗИК"
        for i in range(GRID_SIZE):
            # Буквы
            letter_text = fonts['small'].render(letters[i], True, WHITE)
            screen.blit(letter_text, (x + i * CELL_SIZE + CELL_SIZE//2 - letter_text.get_width()//2, y - 25))
            
            # Цифры
            number_text = fonts['small'].render(str(i+1), True, WHITE)
            screen.blit(number_text, (x - 25, y + i * CELL_SIZE + CELL_SIZE//2 - number_text.get_height()//2))
        
        # Рисуем корабли и выстрелы
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell_rect = pygame.Rect(x + col * CELL_SIZE, y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                # Заполняем ячейку
                if self.shots[row][col] == 1 and self.grid[row][col] == 1:
                    # Попадание
                    pygame.draw.rect(screen, RED, cell_rect)
                    pygame.draw.line(screen, BLACK, cell_rect.topleft, cell_rect.bottomright, 2)
                    pygame.draw.line(screen, BLACK, (cell_rect.left, cell_rect.bottom), (cell_rect.right, cell_rect.top), 2)
                elif self.shots[row][col] == 1:
                    # Промах
                    pygame.draw.circle(screen, WHITE, cell_rect.center, CELL_SIZE//6)
                elif self.shots[row][col] == 2:
                    # Отмеченные клетки вокруг потопленного корабля
                    pygame.draw.circle(screen, LIGHT_GRAY, cell_rect.center, CELL_SIZE//8)
                elif not hide_ships and self.grid[row][col] == 1 and not in_multiplayer:
                    # Корабль
                    pygame.draw.rect(screen, GREEN, cell_rect)
        
        # Надпись над доской
        board_title = "Ваша доска" if is_player else "Доска противника"
        title_text = fonts['medium'].render(board_title, True, WHITE)
        screen.blit(title_text, (x + BOARD_SIZE//2 - title_text.get_width()//2, y - 50))