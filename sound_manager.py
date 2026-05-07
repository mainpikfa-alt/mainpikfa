import pygame
import os

class SoundManager:
    """Класс для управления звуками и музыкой в игре"""
    
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        self.music_enabled = True
        self.volume = 0.5
        
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.load_sounds()
        except Exception as e:
            print(f"Ошибка инициализации звуковой системы: {e}")
            
    def load_sounds(self):
        """Загрузка всех звуковых файлов"""
        sound_files = {
            'hit': 'sound/hit.wav',
            'miss': 'sound/miss.wav',
            'sunk': 'sound/sunk.wav',
            'button': 'sound/button.wav',
            'place_ship': 'sound/place_ship.wav',
            'victory': 'sound/victory.wav',
            'defeat': 'sound/defeat.wav'
        }
        
        for sound_name, file_path in sound_files.items():
            try:
                if os.path.exists(file_path):
                    self.sounds[sound_name] = pygame.mixer.Sound(file_path)
                    self.sounds[sound_name].set_volume(self.volume)
                else:
                    print(f"Звуковой файл не найден: {file_path}")
            except Exception as e:
                print(f"Ошибка загрузки звука {sound_name}: {e}")
        
        # Загрузка фоновой музыки
        music_path = 'sound/background_music.mp3'
        try:
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.volume * 0.3)
            else:
                print(f"Файл фоновой музыки не найден: {music_path}")
        except Exception as e:
            print(f"Ошибка загрузки фоновой музыки: {e}")
    
    def play_sound(self, sound_name):
        """Воспроизведение звука"""
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Ошибка воспроизведения звука {sound_name}: {e}")