# notes_manager.py
import json
import os
from datetime import datetime


class NotesManager():
    def __init__(self, filename="notes.json"):
        self.filename = filename
        self.notes = self.load_notes()

    def load_notes(self):
        # Проверяем на наличие файла, если его нет, то создаём
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
            return []

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f'Что-то не так с файлом {self.filename}')

    def save_notes(self, notes):
        # Полная перезапись файла
        if notes:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(notes, f, ensure_ascii=False, indent=2)
            return f'Данные записаны в {self.filename}'
        else:
            return 'Добавьте данные чтобы сохранить'

    def add_note(self, text: str, tags: list):
        if len(text) < 500:
            # Распаршиваем заметку в структуру json
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
            return 'Текст должен быть до 500 символов'

    def update_note(self, note_id, text, tags):
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
        return 'Заметка не найдена'

    def delete_note(self, note_id: int):
        for index, note in enumerate(self.notes):
            if note_id == note['id']:
                del self.notes[index]
                self.save_notes(self.notes)
                return f'Заметка #{note_id} удалена'
        return 'Заметка не найдена'

    def search_notes(self, query: str) -> list[dict]:
        if not query.strip():
            return self.notes

        result = []
        words = [w.lower() for w in query.split() if w.strip()]

        for note in self.notes:
            text = note["text"].lower()

            # Приводим теги к единой строке
            tags = note["tags"]
            if isinstance(tags, list):
                tags_text = " ".join(tags).lower()
            else:
                tags_text = str(tags).lower()

            for word in words:
                if word in text or word in tags_text:
                    result.append(note)
                    break

        return result


    def generate_id(self):
        ids = [note.get("id", 0) for note in self.notes if isinstance(note, dict)]
        return max(ids, default=0) + 1
    

    def get_note_by_id(self, note_id):
        for note in self.notes:
            if note['id'] == note_id:
                return note
        return None

    def __str__(self):
        return f'Все записи({len(self.notes)}): {self.notes}'
    
    def add_sample_notes(self):
        """Добавление примеров заметок (опционально)"""
        sample_notes = [
            ("Решение уравнения Шрёдингера для частицы в коробке", ["квантовая механика", "Шрёдингер", "волновая функция"]),
            ("Эйнштейн открыл теорию относительности", ["Теория относительности", "Физика"]),
            ("Нильс Бор создал первую квантовую теории атома и был активным участником разработки основ квантовой механики", ["квантовая механика", "атомная физика", "модель атома"]),
            ("Для частицы в бесконечной одномерной яме (ширина L) собственные функции имеют вид ψ_n(x) = √(2/L) sin(nπx/L), а энергии E_n = (n²π²ℏ²)/(2mL²). Важно: на границах ψ=0, что приводит к дискретному спектру. Это базовый пример квантования энергии.", ["квантовая механика", "бесконечная яма", "волновая функция", "энергия"]),
            ("Неравенства Белла показывают, что локальный скрытый параметр невозможен при нарушении неравенства CHSH: |⟨A₁B₁ + A₁B₂ + A₂B₁ - A₂B₂⟩| ≤ 2. Эксперименты Aspect, Zeilinger и др. дают значение ~2.8, что подтверждает квантовую нелокальность и запутанность.", ["квантовая информация", "неравенства Белла", "ЭПР", "запутанность"]),
            ("В теории струн бозонные струны требуют 26 измерений, суперструны — 10. Компактификация 6 измерений на многообразиях Калаби–Яу позволяет получить 4-мерное пространство-время. Проблема ландшафта: ~10⁵⁰⁰ вакуумов → антропный принцип?", ["теория струн", "суперструны", "Калаби–Яу", "ландшафт струн"]),
            ("Физика она как магия, за гранью понимания обычного человека.", ["волшебство", "магия"])
        ]
        
        for text, tags in sample_notes:
            self.add_note(text, tags)