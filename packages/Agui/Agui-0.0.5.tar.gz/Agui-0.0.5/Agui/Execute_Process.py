import pygame
from Agui import readData
from Agui import Functions_Links
from Agui.Tools import active_color

BtnName=None

def clicked():
    click = pygame.mouse.get_pressed()
    return click[0]


def check_process():
    global BtnName
    for i in readData.User_Button_List:

        if active_color== i.color:
            BtnName=i.definition


def execute():
    global BtnName
    clicked_=clicked()
    if clicked_:
        check_process()
        process=BtnName
        if process is not None:
            Functions_Links.choose_process(process)
            BtnName=None
            while clicked():
                pygame.event.get()
