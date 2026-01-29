

class NotesManager():
    
    def load_notes(self, filename) -> list[dict]:
        with open(filename, 'r') as f:
            file = f.readline()
            print(file)
        return file
        
    
    def save_notes(self, notes, filename):
        pass
    
    def add_note(self, text, tags):
        pass
    
    def update_note(self, note_id, text, tags):
        pass
    
    def delete_note(self, note_id):
        pass
    
    def search_notes(query):
        pass
    
    def generate_id():
        pass
    
x = NotesManager
