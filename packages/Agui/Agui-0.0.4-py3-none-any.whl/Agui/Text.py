
def set_text(textFieldNumber,newText):
    try:
        from Agui.readData import User_Text_Field
        print("File exist ")
    except:
        print("File does not exist  ")
        User_Text_Field = []

    for txt_field in User_Text_Field:
        if txt_field.text_id==textFieldNumber:
            txt_field.set_new_text(newText)
            break
