import pytest
from notes_manager import NotesManager
from pathlib import Path

BASE_DIR = Path(__file__).parent
file_path = BASE_DIR / "data.json"






def test_reading_real_file():
    """
    Здесь проверяю основной функционал класса NotesManager:
    - добавление заметки
    - чтение заметки из файла
    - сохранение изменений в файле
    - удаление заметок
    - искать по фрагментам текста заметки и теги
    """
    note_1 = NotesManager()
    note_1.filename = file_path  # Передаю реальный файл

    note_1.load_notes()
    assert len(note_1.notes) == 3  # в моём реальном файле 3 заметки

    # Добавляю тестовую заметку
    note_1.add_note("Тестовая заметка №1", "#test1")
    assert len(note_1.notes) > 3

    result = note_1.search_notes("Идеи")
    assert len(result) == 1
    assert result[0]["id"] == 2
    assert "Идеи для улучшения интерфейса" in result[0]["text"]

    result2 = note_1.search_notes("интерфейс")
    assert "интерфейс" in result2[0]["tags"]

    # проверяю, что удалится запись 4, которую я добавлю в файл
    note_1.delete_note(4)
    assert len(note_1.notes) == 3
    assert (
        note_1.notes[2]["id"] != 4
    )  # здесь я проверяю, что третья записать осталась, а 4 удалилась, и id = 4 нет



# тест с временным файлом
def test_reading_tmp_json(tmp_path):
    test_file = tmp_path / "notes.json"
    test_file.write_text("[]", encoding="utf-8")
    
    # Создаю экземпляр класса
    note = NotesManager()
    note.filename = test_file
    note.notes = note.load_notes()
    
    assert len(note.notes) == 0
    
    note.add_note("Тестовая заметка №1", ["yep", "da"])
    assert len(note.notes) == 1
    
    note.add_note("Тестовая заметка №2", ["yes", "no"])
    
    result = note.search_notes("yep")
    assert len(result) == 1
    assert "yep" in result[0]["tags"]
    
    note.delete_note(2)
    assert len(note.notes) == 1
