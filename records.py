import json
import os
from datetime import datetime

class RecordManager:
    """Класс для управления рекордами игры"""
    
    def __init__(self):
        self.records_file = "battleship_records.json"
        self.records = self.load_records()
    
    def load_records(self):
        """Загрузка рекордов из файла"""
        try:
            if os.path.exists(self.records_file):
                with open(self.records_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки рекордов: {e}")
        
        # Структура рекордов по умолчанию
        return {
            "vs_computer": {
                "time": None,
                "date": None,
                "player_name": None
            },
            "vs_player": {
                "time": None,
                "date": None,
                "player_name": None
            }
        }
    
    def save_records(self):
        """Сохранение рекордов в файл"""
        try:
            with open(self.records_file, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения рекордов: {e}")
    
    def check_and_update_record(self, game_mode, time_seconds, player_name):
        """Проверка и обновление рекорда"""
        mode_key = "vs_computer" if game_mode else "vs_player"
        current_record = self.records[mode_key]
        
        # Если рекорда нет или новое время лучше
        if current_record["time"] is None or time_seconds < current_record["time"]:
            self.records[mode_key] = {
                "time": time_seconds,
                "date": datetime.now().strftime("%d.%m.%Y"),
                "player_name": player_name
            }
            self.save_records()
            return True
        return False
    
    def get_record_text(self, vs_computer):
        """Получение текста рекорда для отображения"""
        mode_key = "vs_computer" if vs_computer else "vs_player"
        record = self.records[mode_key]
        
        if record["time"] is None:
            return None
        
        minutes = int(record["time"] // 60)
        seconds = int(record["time"] % 60)
        mode_text = "Игра с ПК" if vs_computer else "Игра вдвоем"
        
        return f"Рекорд {mode_text}: {minutes}:{seconds:02d} - {record['player_name']} ({record['date']})"