Buttons=[]
from Agui import free as Fr
import os
import __main__
user_module_path=os.path.realpath(__main__.__file__)
path = os.path.dirname(os.path.realpath(Fr.__file__))


def bind(func,Button_Name):
    global  path
    global user_module_path
    module_path=user_module_path
    current_path = path + "\\Binded_Functions.py"
    module = user_module_path[find_slash(user_module_path) + 1:]
    global Buttons
    link_up(Button_Name,func)

    if len(Buttons)==0:
        file_on=open(current_path,"w")
        file_on.write("encoded_path= "+str(module_path.encode("utf-8"))+"\n")
        file_on.write("main_path = str(encoded_path,'utf-8')\n")

        
        file_on.write("import sys")

        file_on.write("\n")
        file_on.write("sys.path.insert(1, main_path)\n")
        


        #module_path = module_path[:find_slash(module_path)]
        #module_path=add_back_slash_to_path(module_path)
        #file_on.write(module_path + "')\n")
        file_on.close()

    Buttons.append(Button_Name)

    file_on=open(current_path,"a")
    module=module[:-3]
    
    file_on.write("\nfrom "+module+" import "+func)
    file_on.close()

    file_on=open(current_path,"a")
    file_on.write("\ndef "+Button_Name+"():")
    file_on.write("\n    "+func+"()")

    file_on.close()




def find_slash(word):
    for i in range(len(word)):
        if word[-(i+1)]=='\\':
            return len(word)-(i+1)


def link_up(Button_Name,function):
    global path
    file_ = open(path+"\\Functions_Links.py", "a")
    #file_.write("from Binded_Functions import *\n")

    file_.write("def "+Button_Name+"():\n")
    file_.write("    "+function+"()")

    file_.write("\n")

    file_.close()


def finish():
    global user_module_path
    module_path=user_module_path
    global path
    global Buttons
    module_path = module_path[:find_slash(module_path)]
    package_directory=path+"\\readData.py"
    file_data=open(package_directory,"w")
    
    module_path = module_path.encode("utf-8")
    module_path = str(module_path)
    file_data.write("encoded_path ="+module_path+"\n"+"module_path=str(encoded_path,'utf-8')\n")
    file_data.write("import sys\nsys.path.insert(1, "+"module_path"+")\n")
    file_data.write("from Aproject import *\nfrom Agui.Tools import *\nfrom Agui.Tools1 import *\nUser_Button_List=[]\nUser_Text_Field=[]\n")
    file_data.write("\n\nfor i in Button_Lst:\n")
    file_data.write("    new_Button=button(i['x_beginner']-150,i['y_beginner']-20,i['height'],i['width'],i['thickness'],i['color'],i['definition'])\n")
    file_data.write("    User_Button_List.append(new_Button)")

    file_data.write("\n\nfor i in TextFieldList:\n")
    file_data.write(
        '    new_text_field=TextField(i["x_begin"]-150,i["y_begin"]-20,i["x_end"]-150,i["y_end"]-20)\n')
    file_data.write("    User_Text_Field.append(new_text_field)")

    file_data.close()
    file_ = open(path+"\\Functions_Links.py", "w")
    file_.write("from Agui.Binded_Functions import *\n")

    file_.write("def "+"choose_process"+"(funct):\n")
    for pr in Buttons:
        file_.write("    " + "if funct =="+'"'+pr +'"'+ ":\n")
        file_.write("        " + pr + "()\n")
    file_.close()


    print("\nAll functions binded !!!")




def add_back_slash_to_path(word_):
    turn =0
    list=[]
    path=""
    for let in word_:
        if let =="\\":
            list.append(turn)
        turn+=1
    for i in range(len(word_)):
        path=path+word_[i]
        if i in list:
            path=path+"\\"
    return path
