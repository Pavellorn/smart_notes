import json
import os
from datetime import datetime


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
            raise ValueError(f'Что-то не так с файлом {self.filename}')
            
    def save_notes(self, notes):
        #Полная перезапись файла
        if notes:
            with open(self.filename, 'w', encoding='utf8') as f:
                json.dump(notes, f)
            return f'Данные записаны в {self.filename}'
        else:
            return 'Добавьте данные что бы сохранить'
    
    def add_note(self, text: str, tags: list):
        if len(text) < 500:
        #Распаршиваем заметку в структуру json
            now_time = str(datetime.now())
            note_id = self.generate_id()
            new_note = {
                    "id": note_id,
                    "text": text,
                    "tags": tags,
                    "created": now_time,
                    "updated": ""
                }
            self.notes.append(new_note)
            self.save_notes(self.notes)
            return 'Заметка успешно добавлена'
        else:
            return 'Текст должен быть до 500 симоволов'
    
    def update_note(self, note_id, text, tags):
        #Надо как-то в этой функции влиять на прямую на json пока хз как 
        
        for i, note in enumerate(self.notes):
            new_note = {}
            if note['id'] == note_id:
                new_note['id'] = note['id']
                new_note['text'] = text
                new_note['tags'] = tags
                new_note['created'] = note['created']
                new_note['updated'] = str(datetime.now())
                self.notes[i] = new_note
                self.save_notes(self.notes)
                return 'Заметка успешно обновлена'
            

    def delete_note(self, note_id: int):
        self.notes = [note for note in self.notes if note['id'] != note_id]
        self.save_notes(self.notes)
        
    def search_notes(self, query):
        search_notes = []
        for note in self.notes:
            search_notes = []
            tags_to_str =  ' '.join(note['tags'])
            lst_query = query.split(' ')
            for word in lst_query:
                if word in tags_to_str or word in lst_query:
                    search_notes.append(note)
                
        return search_notes
        

    def generate_id(self):
        all_id = []
        for note in self.notes:
            note_id = note['id']
            all_id.append(note_id)
        for i in range(len(all_id)+1):
            if i in all_id:
                continue
            else:
                return i 
            
    def __str__(self):
        return f'Все записи({len(self.notes)}): {self.notes}'
    

x = NotesManager()

x.add_note('test test', ['test tag', 'test tag2'])

x.update_note(1, 'test update', ['update tag', 'test tag2'])

x.delete_note(0)

print(x.search_notes('update tag теория'))

x.add_note('testdfsfsdfsd test', ['test sdfsdftag', 'test tag2'])
x.add_note('testsdfsdfsdfsdfsdf test', ['AAAAAAAAAAAAAAAAAAAaAtest tag', 'test tag2'])