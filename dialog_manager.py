# dialog_manager.py

from objects.NPC import NPC
from gemini_manager import generate_response

class DialogManager:
    def __init__(self, npc: NPC):
        self.npc = npc
        self.dialog_timer = None

    def handle_user_speak(self, text):
        if text and len(text.strip()) > 0:
            response = self.create_response(text)
            self.npc.update_dialog(response)
            return response

    def create_response(self, input_text):
        # Placeholder for a response generating function
        return generate_response(input_text)
