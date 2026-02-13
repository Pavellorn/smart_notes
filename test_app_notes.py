import pytest
from notes_manager import NotesManager
from pathlib import Path

BASE_DIR = Path(__file__).parent
file_path = BASE_DIR / "notes.json"



def test_reading_real_file():
    note_1 = NotesManager()
    note_1.filename = file_path

    note_1.load_notes()
    assert len(note_1.notes) == 2

    # Добавляю тестовую заметку
    note_1.add_note("Тестовая заметка №2", "#test1")
    assert len(note_1.notes) == 3

    # Поиск по квант в тексте Квантовый
    result = note_1.search_notes("квант")
    assert len(result) == 1
    assert result[0]["id"] == 1
    assert "квант" in result[0]["text"].lower()

    # Поиск по "зам"
    result2 = note_1.search_notes("зам")
    assert len(result2) >= 1
    assert "test1" in str(result2[-1]["tags"])

    # Удаление заметки
    note_1.delete_note(2)
    assert len(note_1.notes) == 2

    ids = [note["id"] for note in note_1.notes]
    assert 2 not in ids



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
