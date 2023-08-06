from Agui.readData import User_Text_Field
def show_text_fields(surface,cursor=(0,0)):
    for txt in User_Text_Field:
        txt.draw(surface,cursor)
