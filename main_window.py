# gui.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLineEdit, QListWidget, QTextEdit, QLabel, QMessageBox
)

from notes_manager import NotesManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.manager = NotesManager()
        self.current_note_id = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Умные заметки")
        self.resize(900, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # -----Верхняя панель: кнопка + поиск---------------------------------
        top_panel = QHBoxLayout()

        btn_new = QPushButton("Новая заметка")
        btn_new.clicked.connect(self.new_note)
        top_panel.addWidget(btn_new)

        lbl_search = QLabel("Поиск:")
        top_panel.addWidget(lbl_search)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите текст...")
        self.search_input.textChanged.connect(self.on_search_changed)
        top_panel.addWidget(self.search_input)

        btn_search = QPushButton("Поиск")
        btn_search.clicked.connect(self.on_search_changed)
        top_panel.addWidget(btn_search)

        main_layout.addLayout(top_panel)

        # ---- Центральная область: список заметок ---------
        self.note_list = QListWidget()
        self.note_list.itemClicked.connect(self.on_note_selected)
        main_layout.addWidget(self.note_list, stretch=3)

        # -------Нижняя область: форма редактирования заметки-------------
        edit_panel = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Текст заметки (макс. 500 символов)")
        self.text_edit.setMaximumHeight(120)
        edit_panel.addWidget(self.text_edit)

        tags_layout = QHBoxLayout()
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Теги через запятую (например: тег1, тег2, тег3)")
        tags_layout.addWidget(QLabel("Теги:"))
        tags_layout.addWidget(self.tags_input)
        edit_panel.addLayout(tags_layout)

        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Сохранить")
        btn_save.clicked.connect(self.save_note)
        btn_delete = QPushButton("Удалить")
        btn_delete.clicked.connect(self.delete_note)
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_delete)
        edit_panel.addLayout(btn_layout)

        main_layout.addLayout(edit_panel, stretch=1)

        self.update_note_list()

    # ────────────────────────────────────────────────
    # Методы-обработчики событий
    # ────────────────────────────────────────────────

    def update_note_list(self, notes=None):
        if notes is None:
            notes = self.manager.notes

        self.note_list.clear()

        for note in notes:
            preview = note["text"][:60] + "..." if len(note["text"]) > 60 else note["text"]
            tags_str = ", ".join(note["tags"]) if note["tags"] else ""
            tags_display = f"  #{tags_str}" if tags_str else ""
            item_text = f"ID:{note['id']} - {preview}{tags_display}"
            self.note_list.addItem(item_text)

    def on_note_selected(self, item):
        index = self.note_list.row(item)
        notes = self.manager.notes
        
        if 0 <= index < len(notes):
            note = notes[index]
            self.current_note_id = note["id"]
            self.text_edit.setPlainText(note["text"])
            self.tags_input.setText(", ".join(note["tags"]))

    def new_note(self):
        self.current_note_id = None
        self.text_edit.clear()
        self.tags_input.clear()
        self.text_edit.setFocus()

    def save_note(self):
        text = self.text_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Ошибка", "Текст заметки не может быть пустым")
            return
        if len(text) > 500:
            QMessageBox.warning(self, "Ошибка", "Текст заметки не должен превышать 500 символов")
            return

        tags_str = self.tags_input.text().strip()
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]

        try:
            if self.current_note_id is None:
                result = self.manager.add_note(text, tags)
                QMessageBox.information(self, "Успех", result)
            else:
                result = self.manager.update_note(self.current_note_id, text, tags)
                QMessageBox.information(self, "Успех", result)

            self.update_note_list()
            self.new_note()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def delete_note(self):
        if self.current_note_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите заметку для удаления")
            return

        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Удалить заметку #{self.current_note_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                result = self.manager.delete_note(self.current_note_id)
                self.update_note_list()
                self.new_note()
                QMessageBox.information(self, "Успех", result)
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", str(e))

    def on_search_changed(self):
        query = self.search_input.text().strip()
        found = self.manager.search_notes(query)
        self.update_note_list(found)