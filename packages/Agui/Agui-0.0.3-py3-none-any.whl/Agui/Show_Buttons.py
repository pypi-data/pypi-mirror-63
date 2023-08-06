import pygame
from Agui.readData import User_Button_List

def show_buttons(display,cursor):
    for i in User_Button_List:
        i.draw(display,cursor)
