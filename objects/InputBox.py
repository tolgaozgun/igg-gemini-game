       
import pygame
import pygame.freetype

from dialog_manager import DialogManager

class InputBox:

    def __init__(self, x, y, w, h, dialog_manager: DialogManager, text=''):
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        # self.font = pygame.freetype.SysFont("googlesans", 32, True)
        self.font = pygame.font.SysFont('arial', 20)  # Example using a system font
        self.dialog_manager = dialog_manager
        self.color = self.color_inactive
        self.text = text
        self.txt_surface = self.font.render(text, True, pygame.Color('black'))
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # If text is not empty
                    if self.text:
                        self.dialog_manager.handle_user_speak(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, pygame.Color('black'))

    def update(self):
        # Resize the box if the text is too long.
        
        # txt_surface is a Tuple[Surface, Rect]
        # Get the width of the text surface
        txt_width = self.txt_surface.get_width()
        width = max(self.w, txt_width + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.fill(pygame.Color('white'), self.rect)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)