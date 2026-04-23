import pygame
import time
from constants import *
from board import Board
from ai_logic import ComputerAI
from sound_manager import SoundManager
from records import RecordManager
from ui_elements import Button, VolumeSlider, NameInput
from graphics import create_asset_images, load_image

class Game:
    """Основной класс игры"""
    
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        self.state = "menu"
        self.player_board = Board()
        self.opponent_board = Board()
        self.current_player = 0
        self.message = ""
        self.ship_placement_index = 0
        self.ship_horizontal = True
        self.vs_computer = True
        self.computer_ai = ComputerAI()
        
        # Для удаления кораблей
        self.removed_ships = []  # Список удаленных кораблей для возврата в пул
        
        # Имена игроков
        self.player1_name = ""
        self.player2_name = ""
        
        # Время начала игры
        self.game_start_time = None
        
        # Загрузка ресурсов
        self.background_image = load_image("images/sea_battle_bg.jpg", WINDOW_WIDTH, WINDOW_HEIGHT)
        self.game_assets = create_asset_images()
        
        # Менеджеры
        self.sound_manager = SoundManager()
        self.record_manager = RecordManager()
        
        # UI элементы
        self.name_input = NameInput(WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2, 300, 50)
        
        # Кнопки
        self.button_vs_computer = Button(WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 - 80, 300, 80, "Игра с компьютером")
        self.button_vs_player = Button(WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 + 20, 300, 80, "Игра с человеком")
        self.button_rotate = Button(WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT - 150, 300, 50, "Повернуть корабль (R)")
        self.button_random = Button(WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT - 80, 300, 50, "Случайная расстановка")
        self.button_exit = Button(WINDOW_WIDTH - 150, 20, 130, 40, "Выход (ESC)", RED, DARK_RED)
        self.button_back = Button(WINDOW_WIDTH//2 - 75, WINDOW_HEIGHT - 80, 150, 50, "В меню")
        self.volume_slider = VolumeSlider(WINDOW_WIDTH - 250, WINDOW_HEIGHT - 40, 150, 20, 0.5)
        self.button_music = Button(WINDOW_WIDTH - 300, WINDOW_HEIGHT - 50, 40, 40, "♪")
        self.button_confirm_name = Button(WINDOW_WIDTH//2 - 75, WINDOW_HEIGHT//2 + 80, 150, 50, "Подтвердить")
        
        # Новая кнопка для удаления кораблей
        self.button_remove_ship = Button(WINDOW_WIDTH//2 + 170, WINDOW_HEIGHT - 150, 200, 50, "Удалить корабль", ORANGE, RED)
        self.remove_mode = False  # Режим удаления кораблей
        
        # Запускаем фоновую музыку
        self.sound_manager.start_music()
        
    def reset_game(self):
        """Сброс игры к начальному состоянию"""
        self.player_board = Board()
        self.opponent_board = Board()
        self.current_player = 0
        self.message = ""
        self.ship_placement_index = 0
        self.ship_horizontal = True
        self.computer_ai = ComputerAI()
        self.game_start_time = None
        self.removed_ships = []
        self.remove_mode = False
        
    def start_game_vs_computer(self):
        """Начало игры против компьютера"""
        self.reset_game()
        self.vs_computer = True
        self.state = "enter_name"
        self.name_input.text = ""
        self.name_input.active = True
        
    def start_game_vs_player(self):
        """Начало игры против человека"""
        self.reset_game()
        self.vs_computer = False
        self.state = "enter_name"
        self.name_input.text = ""
        self.name_input.active = True
        
    def place_ships_randomly_for_current_player(self):
        """Случайная расстановка кораблей для текущего игрока"""
        if self.current_player == 0:
            self.player_board.place_ships_randomly()
            self.ship_placement_index = len(SHIPS)
            self.removed_ships = []  # Очищаем список удаленных кораблей
        else:
            self.opponent_board.place_ships_randomly()
            self.ship_placement_index = len(SHIPS)
            self.removed_ships = []
            
        if self.vs_computer and self.current_player == 0:
            # Компьютер размещает свои корабли
            self.current_player = 1
            self.opponent_board.place_ships_randomly()
            self.current_player = 0
            self.state = "game"
            self.game_start_time = time.time()
        elif not self.vs_computer:
            if self.current_player == 0:
                # Переход к игроку 2
                self.current_player = 1
                self.ship_placement_index = 0
                self.ship_horizontal = True
                self.state = "enter_name"
                self.name_input.text = ""
                self.name_input.active = True
            else:
                # Начинаем игру
                self.current_player = 0
                self.state = "game"
                self.game_start_time = time.time()
    
    def get_available_ships(self):
        """Получить список доступных для размещения кораблей"""
        # Начинаем со всех кораблей
        available = SHIPS.copy()
        
        # Удаляем уже размещенные корабли
        board = self.player_board if self.current_player == 0 else self.opponent_board
        for ship in board.ships:
            ship_length = len(ship)
            if ship_length in available:
                available.remove(ship_length)
        
        # Добавляем удаленные корабли обратно в список
        for ship_length in self.removed_ships:
            available.append(ship_length)
        
        # Сортируем по убыванию
        available.sort(reverse=True)
        return available
    
    def try_place_ship(self, x, y):
        """Попытка разместить корабль"""
        board = self.player_board if self.current_player == 0 else self.opponent_board
        
        # Получаем доступные корабли
        available_ships = self.get_available_ships()
        
        if not available_ships:
            return False
            
        # Берем первый доступный корабль
        ship_length = available_ships[0]
        
        # Переводим координаты мыши в индексы сетки
        grid_x = (x - BOARD1_X) // CELL_SIZE
        grid_y = (y - BOARD1_Y) // CELL_SIZE
        
        if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
            if board.place_ship(ship_length, grid_x, grid_y, self.ship_horizontal):
                self.sound_manager.play_sound('place_ship')
                
                # Удаляем корабль из списка удаленных, если он там был
                if ship_length in self.removed_ships:
                    self.removed_ships.remove(ship_length)
                
                # Проверяем, все ли корабли размещены
                if not self.get_available_ships():
                    self.finish_ship_placement()
                    
                return True
        return False
    
    def try_remove_ship(self, x, y):
        """Попытка удалить корабль"""
        board = self.player_board if self.current_player == 0 else self.opponent_board
        
        # Переводим координаты мыши в индексы сетки
        grid_x = (x - BOARD1_X) // CELL_SIZE
        grid_y = (y - BOARD1_Y) // CELL_SIZE
        
        if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
            removed_length = board.remove_ship_at(grid_x, grid_y)
            if removed_length:
                self.sound_manager.play_sound('remove_ship')
                self.removed_ships.append(removed_length)
                return True
        return False
    
    def finish_ship_placement(self):
        """Завершение расстановки кораблей"""
        if self.vs_computer and self.current_player == 0:
            # Компьютер размещает свои корабли
            self.current_player = 1
            self.opponent_board.place_ships_randomly()
            self.current_player = 0
            self.state = "game"
            self.game_start_time = time.time()
        elif not self.vs_computer:
            if self.current_player == 0:
                # Переход к игроку 2
                self.current_player = 1
                self.ship_placement_index = 0
                self.ship_horizontal = True
                self.removed_ships = []
                self.remove_mode = False
                self.state = "enter_name"
                self.name_input.text = ""
                self.name_input.active = True
            else:
                # Начинаем игру
                self.current_player = 0
                self.state = "game"
                self.game_start_time = time.time()
        else:
            self.state = "game"
            self.game_start_time = time.time()
    
    def try_shoot(self, x, y):
        """Попытка выстрела"""
        # Проверяем, чья очередь стрелять
        if (self.current_player == 0 and x < WINDOW_WIDTH // 2) or (self.current_player == 1 and x > WINDOW_WIDTH // 2):
            return False
            
        board_to_shoot = self.opponent_board if self.current_player == 0 else self.player_board
        
        # Переводим координаты мыши в индексы сетки
        if self.current_player == 0:
            grid_x = (x - BOARD2_X) // CELL_SIZE
            grid_y = (y - BOARD2_Y) // CELL_SIZE
        else:
            grid_x = (x - BOARD1_X) // CELL_SIZE
            grid_y = (y - BOARD1_Y) // CELL_SIZE
            
        if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
            hit, message = board_to_shoot.shoot(grid_x, grid_y)
            
            if message == "Недопустимый ход":
                return False
                
            self.message = message
            
            # Воспроизводим звуки (убрали звук выстрела)
            if hit:
                if message == "Потоплен!":
                    self.sound_manager.play_sound('sunk')
                else:
                    self.sound_manager.play_sound('hit')
            else:
                self.sound_manager.play_sound('miss')
            
            # Если не попал, передаем ход
            if not hit:
                self.current_player = 1 - self.current_player
                
                # Если сейчас ход компьютера
                if self.vs_computer and self.current_player == 1:
                    self.computer_turn()
            
            # Проверяем на победу
            if board_to_shoot.all_ships_sunk():
                self.end_game()
                
            return True
        return False
    
    def computer_turn(self):
        """Ход компьютера"""
        pygame.display.flip()
        time.sleep(0.5)
        
        target = self.computer_ai.get_next_shot(self.player_board)
        
        if target:
            grid_x, grid_y = target
            hit, message = self.player_board.shoot(grid_x, grid_y)
            self.message = "Компьютер: " + message
            
            # Обновляем экран
            self.draw_game()
            self.draw_ui_elements()
            pygame.display.flip()
            
            if hit:
                if message == "Потоплен!":
                    self.sound_manager.play_sound('sunk')
                    self.computer_ai.register_sunk()
                else:
                    self.sound_manager.play_sound('hit')
                    self.computer_ai.register_hit(grid_x, grid_y)
            else:
                self.sound_manager.play_sound('miss')
                self.computer_ai.register_miss(grid_x, grid_y)
            
            # Если не попал, передаем ход игроку
            if not hit:
                self.current_player = 0
            
            # Проверяем на победу
            if self.player_board.all_ships_sunk():
                self.end_game()
                
            # Если попал и игра не окончена, компьютер стреляет снова
            elif hit and self.state != "game_over":
                time.sleep(0.5)
                self.computer_turn()
    
    def end_game(self):
        """Завершение игры"""
        if self.game_start_time:
            game_time = time.time() - self.game_start_time
            self.game_start_time = None
        else:
            game_time = 0
        
        # Определяем победителя
        if self.current_player == 0:
            winner_name = self.player1_name
            if self.vs_computer:
                self.message = f"{winner_name} победил компьютер!"
                self.sound_manager.play_sound('victory')
            else:
                self.message = f"{winner_name} победил!"
                self.sound_manager.play_sound('victory')
        else:
            if self.vs_computer:
                winner_name = "Компьютер"
                self.message = "Компьютер победил!"
                self.sound_manager.play_sound('defeat')
            else:
                winner_name = self.player2_name
                self.message = f"{winner_name} победил!"
                self.sound_manager.play_sound('victory')
        
        # Проверяем рекорд
        if winner_name != "Компьютер":
            is_new_record = self.record_manager.check_and_update_record(self.vs_computer, game_time, winner_name)
            if is_new_record:
                self.message += " НОВЫЙ РЕКОРД!"
        
        self.state = "game_over"
    
    def confirm_name(self):
        """Подтверждение введенного имени"""
        if self.vs_computer:
            self.player1_name = self.name_input.text.strip()
            self.player2_name = "Компьютер"
            self.state = "place_ships"
        else:
            if self.current_player == 0:
                self.player1_name = self.name_input.text.strip()
                self.state = "place_ships"
            else:
                self.player2_name = self.name_input.text.strip()
                self.state = "place_ships"
    
    def draw_menu(self):
        """Отрисовка главного меню"""
        self.screen.blit(self.background_image, (0, 0))
        
        # Полупрозрачная панель
        panel = pygame.Surface((WINDOW_WIDTH, 250), pygame.SRCALPHA)
        panel.fill((20, 20, 50, 180))
        self.screen.blit(panel, (0, 30))
        
        # Заголовок
        title_text = self.fonts['big'].render("МОРСКОЙ БОЙ", True, WHITE)
        self.screen.blit(title_text, (WINDOW_WIDTH//2 - title_text.get_width()//2, 50))
        
        # Подзаголовок
        subtitle = self.fonts['medium'].render("Лучшие результаты", True, YELLOW)
        self.screen.blit(subtitle, (WINDOW_WIDTH//2 - subtitle.get_width()//2, 100))
        
        # Отображаем рекорды
        vs_computer_record = self.record_manager.get_record_text(True)
        vs_player_record = self.record_manager.get_record_text(False)
        
        y_offset = 140
        if vs_computer_record:
            record_text = self.fonts['small'].render(vs_computer_record, True, WHITE)
            self.screen.blit(record_text, (WINDOW_WIDTH//2 - record_text.get_width()//2, y_offset))
            y_offset += 30
        else:
            no_record_text = self.fonts['small'].render("Игра с ПК: рекордов пока нет", True, GRAY)
            self.screen.blit(no_record_text, (WINDOW_WIDTH//2 - no_record_text.get_width()//2, y_offset))
            y_offset += 30
            
        if vs_player_record:
            record_text = self.fonts['small'].render(vs_player_record, True, WHITE)
            self.screen.blit(record_text, (WINDOW_WIDTH//2 - record_text.get_width()//2, y_offset))
        else:
            no_record_text = self.fonts['small'].render("Игра вдвоем: рекордов пока нет", True, GRAY)
            self.screen.blit(no_record_text, (WINDOW_WIDTH//2 - no_record_text.get_width()//2, y_offset))
        
        # Кнопки
        self.button_vs_computer.draw(self.screen, self.fonts['medium'])
        self.button_vs_player.draw(self.screen, self.fonts['medium'])
    
    def draw_enter_name(self):
        """Отрисовка экрана ввода имени"""
        self.screen.blit(self.background_image, (0, 0))
        
        # Полупрозрачная панель
        panel = pygame.Surface((600, 300), pygame.SRCALPHA)
        panel.fill((20, 20, 50, 200))
        self.screen.blit(panel, (WINDOW_WIDTH//2 - 300, WINDOW_HEIGHT//2 - 150))
        
        # Заголовок
        if self.vs_computer:
            title = "Введите ваше имя"
        else:
            title = f"Игрок {self.current_player + 1}: введите имя"
        
        title_text = self.fonts['big'].render(title, True, WHITE)
        self.screen.blit(title_text, (WINDOW_WIDTH//2 - title_text.get_width()//2, WINDOW_HEIGHT//2 - 100))
        
        # Поле ввода имени
        self.name_input.draw(self.screen, self.fonts['small'], self.fonts['medium'], "")
        
        # Кнопка подтверждения
        self.button_confirm_name.draw(self.screen, self.fonts['medium'])
    
    def draw_place_ships(self):

        """Отрисовка экрана расстановки кораблей"""
        self.screen.blit(self.background_image, (0, 0))
        
        # Полупрозрачная панель
        panel = pygame.Surface((WINDOW_WIDTH, 80), pygame.SRCALPHA)
        panel.fill((20, 20, 50, 180))
        self.screen.blit(panel, (0, 20))
        
        # Заголовок
        player_name = self.player1_name if self.current_player == 0 else self.player2_name
        player_text = f"{player_name}: разместите корабли"
        title_text = self.fonts['big'].render(player_text, True, WHITE)
        self.screen.blit(title_text, (WINDOW_WIDTH//2 - title_text.get_width()//2, 30))
        
        # Информация о кораблях
        available_ships = self.get_available_ships()
        if available_ships:
            ship_text = f"Доступные корабли: {', '.join(map(str, available_ships))}"
            ship_info = self.fonts['medium'].render(ship_text, True, WHITE)
            self.screen.blit(ship_info, (WINDOW_WIDTH//2 - ship_info.get_width()//2, 70))
        
        # Рисуем доску
        board = self.player_board if self.current_player == 0 else self.opponent_board
        board.draw(self.screen, BOARD1_X, BOARD1_Y, True, game_assets=self.game_assets, fonts=self.fonts)
        
        # Отображаем подсказку
        if self.remove_mode:
            mode_text = "Режим удаления: кликните на корабль для удаления"
            mode_color = RED
        else:
            orientation_text = "Горизонтально" if self.ship_horizontal else "Вертикально"
            mode_text = f"Режим размещения: {orientation_text}"
            mode_color = WHITE
            
        mode_info = self.fonts['small'].render(mode_text, True, mode_color)
        self.screen.blit(mode_info, (WINDOW_WIDTH//2 - mode_info.get_width()//2, WINDOW_HEIGHT - 200))
        
        # Кнопки
        self.button_rotate.draw(self.screen, self.fonts['medium'])
        self.button_random.draw(self.screen, self.fonts['medium'])
        self.button_remove_ship.draw(self.screen, self.fonts['medium'])
        
        # Превью корабля под курсором (только в режиме размещения)
        if not self.remove_mode and available_ships:
            mouse_pos = pygame.mouse.get_pos()
            grid_x = (mouse_pos[0] - BOARD1_X) // CELL_SIZE
            grid_y = (mouse_pos[1] - BOARD1_Y) // CELL_SIZE
            
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                ship_length = available_ships[0]
                valid_placement = board.can_place_ship(ship_length, grid_x, grid_y, self.ship_horizontal)
                
                # Отображаем превью корабля
                for i in range(ship_length):
                    if self.ship_horizontal:
                        cell_x = grid_x + i
                        cell_y = grid_y
                    else:
                        cell_x = grid_x
                        cell_y = grid_y + i
                    
                    if 0 <= cell_x < GRID_SIZE and 0 <= cell_y < GRID_SIZE:
                        cell_rect = pygame.Rect(
                            BOARD1_X + cell_x * CELL_SIZE, 
                            BOARD1_Y + cell_y * CELL_SIZE, 
                            CELL_SIZE, 
                            CELL_SIZE
                        )
                        color = YELLOW if valid_placement else RED
                        pygame.draw.rect(self.screen, color, cell_rect, 3)
    
    def draw_game(self):
        """Отрисовка игрового экрана"""
        self.screen.blit(self.background_image, (0, 0))
        
        # Полупрозрачная панель
        panel = pygame.Surface((WINDOW_WIDTH, 100), pygame.SRCALPHA)
        panel.fill((20, 20, 50, 180))
        self.screen.blit(panel, (0, 20))
        
        # Заголовок
        if self.current_player == 0:
            current_player_text = f"Ход {self.player1_name}"
        else:
            current_player_text = f"Ход {self.player2_name if not self.vs_computer else 'Компьютера'}"
        
        title_text = self.fonts['big'].render(current_player_text, True, WHITE)
        self.screen.blit(title_text, (WINDOW_WIDTH//2 - title_text.get_width()//2, 30))
        
        # Сообщение
        if self.message:
            message_text = self.fonts['medium'].render(self.message, True, WHITE)
            self.screen.blit(message_text, (WINDOW_WIDTH//2 - message_text.get_width()//2, 70))
        
        # Таймер
        if self.game_start_time:
            elapsed_time = time.time() - self.game_start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            timer_text = self.fonts['small'].render(f"Время: {minutes}:{seconds:02d}", True, WHITE)
            self.screen.blit(timer_text, (WINDOW_WIDTH//2 - timer_text.get_width()//2, 100))
        
        # Рисуем доски
        if self.vs_computer:
            player_hide_ships = False
            opponent_hide_ships = True
            in_multiplayer = False
        else:
            player_hide_ships = True
            opponent_hide_ships = True
            in_multiplayer = True
        
        self.player_board.draw(self.screen, BOARD1_X, BOARD1_Y, True, 
                              hide_ships=player_hide_ships, in_multiplayer=in_multiplayer, 
                              game_assets=self.game_assets, fonts=self.fonts)
        self.opponent_board.draw(self.screen, BOARD2_X, BOARD2_Y, False, 
                                hide_ships=opponent_hide_ships, in_multiplayer=in_multiplayer, 
                                game_assets=self.game_assets, fonts=self.fonts)
        
        # Кнопка возврата
        self.button_back.draw(self.screen, self.fonts['medium'])
    
    def draw_game_over(self):
        """Отрисовка экрана окончания игры"""
        self.screen.blit(self.background_image, (0, 0))
        
        # Полупрозрачная панель
        panel = pygame.Surface((WINDOW_WIDTH, 300), pygame.SRCALPHA)
        panel.fill((20, 20, 50, 200))
        self.screen.blit(panel, (0, WINDOW_HEIGHT//3))
        
        # Заголовок
        title_text = self.fonts['big'].render("ИГРА ОКОНЧЕНА", True, WHITE)
        self.screen.blit(title_text, (WINDOW_WIDTH//2 - title_text.get_width()//2, WINDOW_HEIGHT//3 + 50))
        
        # Сообщение о победителе
        if self.message:
            message_text = self.fonts['big'].render(self.message, True, YELLOW)
            self.screen.blit(message_text, (WINDOW_WIDTH//2 - message_text.get_width()//2, WINDOW_HEIGHT//3 + 120))
        
        # Время игры
        if self.game_start_time:
            elapsed_time = time.time() - self.game_start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            time_text = self.fonts['medium'].render(f"Время игры: {minutes}:{seconds:02d}", True, WHITE)
            self.screen.blit(time_text, (WINDOW_WIDTH//2 - time_text.get_width()//2, WINDOW_HEIGHT//3 + 180))
        
        # Кнопка возврата
        self.button_back.draw(self.screen, self.fonts['medium'])
    
    def draw_ui_elements(self):
        """Отрисовка UI элементов, которые видны всегда"""
        self.button_exit.draw(self.screen, self.fonts['medium'])
        self.volume_slider.draw(self.screen, self.fonts['small'])
        self.button_music.draw(self.screen, self.fonts['medium'])
    
    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            # Выход по ESC
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
                
            mouse_pos = pygame.mouse.get_pos()
            
            # Обработка ползунка громкости
            if self.volume_slider.handle_event(event):
                self.sound_manager.set_volume(self.volume_slider.value)
            
            # Кнопка выхода
            self.button_exit.check_hover(mouse_pos)
            if self.button_exit.is_clicked(mouse_pos, event, self.sound_manager):
                return False
            
            # Кнопка музыки
            self.button_music.check_hover(mouse_pos)
            if self.button_music.is_clicked(mouse_pos, event, self.sound_manager):
                self.sound_manager.toggle_music()
                if self.sound_manager.music_enabled:
                    self.button_music.color = (60, 80, 120)
                else:
                    self.button_music.color = (120, 60, 60)
            
            # Обработка в зависимости от состояния
            if self.state == "menu":
                self.button_vs_computer.check_hover(mouse_pos)
                self.button_vs_player.check_hover(mouse_pos)
                
                if self.button_vs_computer.is_clicked(mouse_pos, event, self.sound_manager):
                    self.start_game_vs_computer()
                elif self.button_vs_player.is_clicked(mouse_pos, event, self.sound_manager):
                    self.start_game_vs_player()
                    
            elif self.state == "enter_name":
                self.button_confirm_name.check_hover(mouse_pos)
                
                if self.name_input.handle_event(event):
                    if self.name_input.text.strip():
                        self.confirm_name()
                
                if self.button_confirm_name.is_clicked(mouse_pos, event, self.sound_manager):
                    if self.name_input.text.strip():
                        self.confirm_name()
                    
            elif self.state == "place_ships":
                self.button_rotate.check_hover(mouse_pos)
                self.button_random.check_hover(mouse_pos)
                self.button_remove_ship.check_hover(mouse_pos)
                
                if self.button_rotate.is_clicked(mouse_pos, event, self.sound_manager):
                    self.ship_horizontal = not self.ship_horizontal
                elif self.button_random.is_clicked(mouse_pos, event, self.sound_manager):
                    self.place_ships_randomly_for_current_player()
                elif self.button_remove_ship.is_clicked(mouse_pos, event, self.sound_manager):
                    self.remove_mode = not self.remove_mode
                    # Меняем цвет кнопки
                    if self.remove_mode:
                        self.button_remove_ship.text = "Режим размещения"
                        self.button_remove_ship.color = RED
                    else:
                        self.button_remove_ship.text = "Удалить корабль"
                        self.button_remove_ship.color = ORANGE
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Проверяем клик по доске
                    if not any([
                        self.button_rotate.rect.collidepoint(mouse_pos),
                        self.button_random.rect.collidepoint(mouse_pos),
                        self.button_remove_ship.rect.collidepoint(mouse_pos),
                        self.button_exit.rect.collidepoint(mouse_pos),
                        self.volume_slider.rect.collidepoint(mouse_pos),
                        self.button_music.rect.collidepoint(mouse_pos)
                    ]):
                        if self.remove_mode:
                            self.try_remove_ship(mouse_pos[0], mouse_pos[1])
                        else:
                            self.try_place_ship(mouse_pos[0], mouse_pos[1])
                    
                # Поворот корабля на R
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.ship_horizontal = not self.ship_horizontal
                    
            elif self.state == "game":
                self.button_back.check_hover(mouse_pos)
                
                if self.button_back.is_clicked(mouse_pos, event, self.sound_manager):
                    self.state = "menu"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not any([
                        self.button_back.rect.collidepoint(mouse_pos),
                        self.button_exit.rect.collidepoint(mouse_pos),
                        self.volume_slider.rect.collidepoint(mouse_pos),
                        self.button_music.rect.collidepoint(mouse_pos)
                    ]):
                        self.try_shoot(mouse_pos[0], mouse_pos[1])
                    
            elif self.state == "game_over":
                self.button_back.check_hover(mouse_pos)
                
                if self.button_back.is_clicked(mouse_pos, event, self.sound_manager):
                    self.state = "menu"
        
        return True
    
    def run(self):
        """Основной цикл игры"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            try:
                running = self.handle_events()
                
                # Отрисовка
                if self.state == "menu":
                    self.draw_menu()
                elif self.state == "enter_name":
                    self.draw_enter_name()
                elif self.state == "place_ships":
                    self.draw_place_ships()
                elif self.state == "game":
                    self.draw_game()
                elif self.state == "game_over":
                    self.draw_game_over()
                
                # UI элементы
                self.draw_ui_elements()
                
                pygame.display.flip()
                clock.tick(60)
                
            except Exception as e:
                print(f"Ошибка в игровом цикле: {e}")
                # Пытаемся продолжить
        
        return True