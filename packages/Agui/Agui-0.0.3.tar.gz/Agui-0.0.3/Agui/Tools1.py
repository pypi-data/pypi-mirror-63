import pygame
from Agui.Tools import text
from Agui.Tools import click_button
textFieldNumber=0
class TextField:
    def __init__(self, x_begin, y_begin, x_end, y_end):
        global textFieldNumber
        textFieldNumber+=1
        self.text_id=textFieldNumber
        self.x_begin = x_begin
        self.y_begin = y_begin
        self.x_end=x_end
        self.y_end=y_end
        self.width=self.x_end-self.x_begin
        self.height=self.y_end-self.y_begin
        self.capacitance = int(self.height/29)
        self.background_color=(134,134,134)
        self.text_object=text( txt="Text Field"+str(textFieldNumber), bg_color=self.background_color, color=(0, 0, 0), center=(0, 0))
        self.textObjectList=[self.text_object]
        self.set_center(self.text_object)
        self.lineList=[]
        self.designeALlTexts()
        self.linOrder=0
        self.up_button=click_button( self.x_end, self.y_begin, 15, 12, 0, color=(100,240,200), definition="")
        self.down_button=click_button( self.x_end, self.y_end-15, 15, 12, 0, color=(100,240,200), definition="")




    def draw(self,surface,cursor=(0,0)):
        pygame.draw.rect(surface,(134,134,134),(self.x_begin,self.y_begin,
                                               self.width,self.height))
        self.up_button.draw(surface,cursor)
        self.down_button.draw(surface,cursor)
        self.display_text(surface)


    def coor(self):
        return self.x_begin,self.y_begin,self.x_end,self.y_end


    def set_center(self,textObject,pady=0,onlyx=None):

        rendered = textObject.render()
        rect = rendered.get_rect()
        pad = rect[2] / 2
        textObject.set_center_((self.x_begin+pad,self.y_begin+14+pady),onlyx)

    def display_text(self,surface):
        for txt in self.textObjectList:
            txt.display(surface)

    def set_new_text(self,newText):
        self.breakDown(newText)
        self.setAllTexts()


    def breakDown(self,word):
        wordList=word.split()
        lineList=[]
        widthCap=self.width/16
        line=""
        for wrd in wordList:
            if len(line)+len(wrd)+2<widthCap:
                line=line+" "+wrd

            else:
                if len(wrd) > widthCap:
                    line=wrd[:int(widthCap)]
                    lineList.append(line)
                    line=wrd[int(widthCap):]
                    lineList.append(line)
                    line=""
                lineList.append(line)
                line=""
                line = line + wrd

        lineList.append(line)
        self.lineList=lineList

        for ttxt in lineList:
            if ttxt == '':
                lineList.remove('')


    def designeALlTexts(self):
        numberOfTexts=self.capacitance
        for nmbr in range(numberOfTexts-1):
            newText = self.text_object=text( txt="Text Field"+str(self.text_id), bg_color=self.background_color, color=(0, 0, 0), center=(0, 0))
            self.set_center(newText,(nmbr+1)*29)
            self.textObjectList.append(newText)

    def setAllTexts(self):
        currentOrder=self.linOrder
        for txtObj in self.textObjectList:
            if len(self.lineList)>currentOrder and currentOrder>=0:
                txtObj.set_new_text(self.lineList[currentOrder])
                self.set_center(txtObj,0,True)
            currentOrder+=1
