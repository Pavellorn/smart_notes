import json
import os
import datetime
from config import STRUCTURE_NOTE, FILE_PATH

class NotesManager():
    
    def __init__(self):
        self.FILE_PATH = FILE_PATH
    
    def load_notes(self):
        #тут проверяем на наличие файла, если его нет, то создаём 
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf8') as f:
                json.dump([], f)
            return []
        #пытаемся ошибку на декодирование json a 
        try:
            with open(self.filename, 'r', encoding='utf8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f'Что-то не так с файлом {self.filename}')
            
    def save_notes(self, notes):
        #Полная перезапись файла
        if notes:
            with open(self.filename, 'w', encoding='utf8') as f:
                json.dump(notes, f)
            return f'Данные записаны в {self.filename}'
        else:
            return 'Добавьте данные что бы сохранить'
    
    def add_note(self, text: str, tags: list):
        #Распаршиваем заметку в структуру json
        new_note = STRUCTURE_NOTE
        new_note['id'] = ''
        new_note['text'] = text
        new_note['tags'] = tags
        new_note['created'] = str(datetime.now())
        print(new_note)
    
    def update_note(self, note_id, text, tags):
        pass
    
    def delete_note(self, note_id):
        pass
    
    def search_notes(query):
        pass
    
    def generate_id():
        pass
    
    # def __str__(self):
    #     print(self.filename)
    

x = NotesManager()

r = x.load_notes()
