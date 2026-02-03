# main.py
import sys
from main_window import MainWindow
from notes_manager import NotesManager
from PyQt6.QtWidgets import QApplication


def add_sample_notes():
    """Добавляет примеры заметок при первом запуске"""
    manager = NotesManager()
    if len(manager.notes) == 0:  # Если нет заметок
        manager.add_sample_notes()
        print("Добавлены примеры заметок")


def main():
    add_sample_notes()  # Добавляем примеры при запуске
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()