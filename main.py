# main.py
import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from objects.NPC import NPC
from objects.InputBox import InputBox
from dialog_manager import DialogManager

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    npc = NPC('shopkeeper.webp', 'small_shopkeeper.webp', 'dialog3.png', 'Selam!')
    dialog_manager = DialogManager(npc)
    input_box = InputBox(180, 400, 600, 40, dialog_manager)
    input_boxes = [input_box]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            for box in input_boxes:
                box.handle_event(event)
                
        for box in input_boxes:
            box.update()

        screen.fill((0, 0, 0))  # Clear the screen
        npc.draw(screen)
        
        for box in input_boxes:
            box.draw(screen)
        

        # updated_dialog = dialog_manager.check_dialog_timer(screen)
        # if updated_dialog is not None:
        #     npc.dialog = updated_dialog
            
        pygame.display.flip()
        clock.tick(60)  # Limit frames per second to 60

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
