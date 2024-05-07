import textwrap
import pygame
import pygame.freetype

from config import SCREEN_HEIGHT


class NPC:
    def __init__(self, portrait_path, small_portrait_path, dialog_box_path, dialog):
        self.portrait = pygame.image.load(portrait_path)
        self.dialog_box = pygame.image.load(dialog_box_path)
        self.small_portrait = pygame.image.load(small_portrait_path)
        self.dialog = dialog
        self.portrait_rect = self.portrait.get_rect(center=(400, 300))
        self.small_portrait_rect = self.small_portrait.get_rect(bottomleft=(30, SCREEN_HEIGHT - 30))
        self.dialog_box_rect = self.dialog_box.get_rect(bottomleft=(0, SCREEN_HEIGHT))
        
    def update_dialog(self, dialog):
        self.dialog = dialog
        
    def draw(self, screen):
        screen.blit(self.portrait, self.portrait_rect)
        screen.blit(self.dialog_box, self.dialog_box_rect)
        screen.blit(self.small_portrait, self.small_portrait_rect)
        self.render_text(screen, self.dialog)
        self.render_npc_text(screen)

    def render_text(self, screen, text):
        font_size = 20
        font = pygame.freetype.SysFont("googlesans", font_size)
        
        wraplen = 60
        count = 0
        my_wrap = textwrap.TextWrapper(width=wraplen)
        wrap_list = my_wrap.wrap(text=text)
        
        x = self.small_portrait_rect.right + 40  # Start text after the portrait
        y = self.dialog_box_rect.top + 50  # A bit of margin from the top of the dialog box
        # Draw one line at a time further down the screen
        for i in wrap_list:
            text_surface, _ = font.render(f"{i}", (0, 0, 0))  # Black text
            screen.blit(text_surface, (x, y))
            count += 1
            y = y + 20
        # Position the text
        
    def render_npc_text(self, screen):
        font_size = 20
        text = "NPC"
        font = pygame.freetype.SysFont("googlesans", font_size, True)
        # Set font to be bold
        text_surface, _ = font.render(text, (0, 0, 0))  # Black text
        x = self.small_portrait_rect.right + 40  # Start text after the portrait
        y = self.dialog_box_rect.top + 25  # A bit of margin from the top of the dialog box
        screen.blit(text_surface, (x, y))