import json
import os
from datetime import datetime
from config import STRUCTURE_NOTE, FILE_PATH

class NotesManager():
    
    def __init__(self):
        self.filename = r"data\test_data.json"
        self.notes = self.load_notes()
        
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
        now_time = str(datetime.now())
        note_id = self.generate_id()
        new_note = STRUCTURE_NOTE
        new_note['id'] = note_id
        new_note['text'] = text
        new_note['tags'] = tags
        new_note['created'] = now_time
        print(new_note)
    
    def update_note(self, note_id, text, tags):
        #Надо как-то в этой функции влиять на прямую на json пока хз как 
        for note in self.notes:
            now_time = str(datetime.now())
            if note['id'] == note_id:
                note['text'] = text
                note['tags'] = tags
                note['new_note'] = now_time
            
    
    def delete_note(self, note_id):
        pass
    
    def search_notes(query):
        pass
    
    def generate_id(self):
        all_id = []
        for note in self.notes:
            id = note['id']
            all_id.append(id)
        for i in range(len(all_id)+1):
            if i in all_id:
                continue
            else:
                return i 
            
    
    # def __str__(self):
    #     print(self.filename)
    

x = NotesManager()

r = x.load_notes()

x.add_note('test test', ['test tag', 'test tag2'])

id = x.generate_id()

x.update_note(1, 'test update', ['update tag', 'test tag2'])