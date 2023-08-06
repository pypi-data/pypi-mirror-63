
import pygame
pygame.init()

display_background_color=(203, 212, 218)

display = pygame.display.set_mode((1000,480))
from Agui.Execute_Process import execute


from Agui.Show_Buttons import show_buttons
from Agui.showTextFields import show_text_fields
display.fill(display_background_color)
pygame.display.flip()

clock =pygame.time.Clock()


while True:
    click = pygame.mouse.get_pressed()
    cursor_present = pygame.mouse.get_pos()
    execute()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
    show_buttons(display,cursor_present)
    show_text_fields(display,cursor_present)
    pygame.display.update()
    clock.tick(30)



