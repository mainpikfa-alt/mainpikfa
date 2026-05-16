import pygame
from constants import *

class Button:
    """Класс для создания кнопок"""
    
    def __init__(self, x, y, width, height, text, color=(60, 80, 120), hover_color=(80, 100, 150)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, screen, font):
        """Отрисовка кнопки"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        """Проверка наведения мыши"""
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, event, sound_manager=None):
        """Проверка клика по кнопке"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pos):
                if sound_manager:
                    sound_manager.play_sound('button')
                return True
        return False


class VolumeSlider:
    """Класс для ползунка громкости"""
    
    def __init__(self, x, y, width, height, initial_value=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = initial_value
        self.dragging = False
        self.slider_width = 20
        
    def draw(self, screen, font_small):
        """Отрисовка ползунка"""
        # Рисуем фон ползунка
        pygame.draw.rect(screen, DARK_GRAY, self.rect, border_radius=5)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=5)
        
        # Рисуем заполненную часть
        filled_width = int(self.rect.width * self.value)
        filled_rect = pygame.Rect(self.rect.x, self.rect.y, filled_width, self.rect.height)
        pygame.draw.rect(screen, LIGHT_BLUE, filled_rect, border_radius=5)
        
        # Рисуем ползунок
        slider_x = self.rect.x + filled_width - self.slider_width // 2
        slider_rect = pygame.Rect(slider_x, self.rect.y - 5, self.slider_width, self.rect.height + 10)
        pygame.draw.rect(screen, WHITE, slider_rect, border_radius=3)
        pygame.draw.rect(screen, BLACK, slider_rect, 2, border_radius=3)
        
        # Рисуем иконку звука
        icon_x = self.rect.x - 35
        icon_y = self.rect.y + self.rect.height // 2