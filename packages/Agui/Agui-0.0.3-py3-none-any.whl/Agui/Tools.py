active_color = (0, 0, 150)
background_color = (203, 212, 218)
import os
import pygame
import Agui.free as fr
path = os.path.dirname(os.path.realpath(fr.__file__))

class button:

    def __init__(self, x, y, height, width, thickness, color, definition="button"):
        self.x_beginner = x
        self.y_beginner = y
        self.height = height
        self.width = width
        self.thickness = thickness
        self.main_color = color
        self.color = color
        self.active_frame = False
        self.passive_color = self.color
        self.On_Text = False
        self.dynamic = True
        self.definition = definition
        self.button_status = 0
        self.txt = text(bg_color=self.color,
                        txt=self.definition,
                        color=(0, 0, 0)
                        , center=(self.x_beginner + self.width / 2,
                                  self.y_beginner + self.height / 2),
                        )

    def coor(self):
        return (self.x_beginner,
                self.y_beginner,
                self.x_beginner + self.width,
                self.y_beginner + self.height)

    def draw(self, display, cursor=(0, 0)):
        if self.dynamic:
            self.status_check(cursor)
        pygame.draw.rect(display, self.color,
                         (self.x_beginner,
                          self.y_beginner,
                          self.width,
                          self.height),
                         self.thickness)
        if self.dynamic:
            self.txt.bg_color = self.color
            self.txt.display(display)

        elif self.On_Text:
            self.txt.bg_color = self.color
            self.txt.display(display)
        elif self.active_frame:
            self.txt.bg_color = background_color
            self.txt.display(display)

    def active(self):
        self.color = active_color

    def On_Text_Process(self):
        self.On_Text = True
        self.dynamic = False
        self.color = active_color

    def color_edit(self, color):
        self.main_color = color
        self.color = color
        self.passive_color = color

    def passive(self):
        self.color = self.passive_color

    def status_check(self, cursor):
        if self.x_beginner <= cursor[0] <= self.x_beginner + self.width:
            if self.y_beginner <= cursor[1] <= self.y_beginner + self.height:
                self.active()
            else:
                self.passive()
        else:
            self.passive()

    def is_a_frame(self):
        self.dynamic = False

    def is_a_active_frame(self):
        self.dynamic = False
        self.color = active_color
        self.active_frame = True

    def is_dynamic(self):
        self.dynamic = True
        self.color = self.main_color
        self.passive_color = self.main_color
        self.On_Text = False


    def set_color(self, color):
        self.color = color
        self.main_color = color
        self.passive_color = color

    def set_thickness(self, size):
        self.thickness = size

    def set_definiton(self,definition):
        self.definition=definition


class click_button(button):
    def __init__(self,x, y, height, width, thickness, color, definition):
        super().__init__(x, y, height, width, thickness, color, definition)
        self.txt=None

    def draw(self, display, cursor=(0, 0)):
        if self.dynamic:
            self.status_check(cursor)
        pygame.draw.rect(display, self.color,
                         (self.x_beginner,
                          self.y_beginner,
                          self.width,
                          self.height),
                         self.thickness)





class line:
    def __init__(self, x1, y1, x2, y2, color=(0, 0, 0)):
        self.x_start = x1
        self.y_start = y1
        self.x_end = x2
        self.y_end = y2
        self.color = color

    def draw(self, screen):
        pygame.draw.line(screen, self.color, (self.x_start, self.y_start), (self.x_end, self.y_end), 2)

    def set_begin(self, pos):
        self.x_start = pos[0]
        self.y_start = pos[1]

    def set_end(self, pos):
        self.x_end = pos[0]
        self.y_end = pos[1]


class text:

    def __init__(self, font=None, txt="", size="20", bg_color=(0, 0, 0), color=(0, 0, 0), center=(0, 0)):
        global path
        self.text = txt
        self.bg_color = bg_color
        self.font_size = size
        self.color = color
        self.center = center
     #   self.font = pygame.font.SysFont('arial',20)
        self.font = pygame.font.Font(path+"/COMIC.TTF", 20)

    def display(self, screen):
        rendered = self.render()
        rect = rendered.get_rect()
        rect.center = self.center
        screen.blit(rendered, rect)

    def render(self):
        text_rendered = self.font.render(self.text, True, self.color, self.bg_color)
        return text_rendered
    def set_font_size(self,size):
        global path
        self.font = pygame.font.Font(path+"/COMIC.TTF", 20)
    def add_word(self,word):
        self.text=self.text+word
    def set_new_text(self,txt):
        self.text=txt
    def set_center_(self,center,onlyx=None):
        if onlyx :
            self.center=(center[0],self.center[1])
        else:
            self.center=center

class ProcessButton(button):
    def __init__(self, x, y, height, width, thickness, color, definition="button"):
        super().__init__(x, y, height, width, thickness, color, definition)
        self.txt.bg_color = background_color
        
    def draw(self, display, cursor=(0, 0)):
        if self.dynamic:
            self.status_check(cursor)
        if self.active_frame:
            self.thickness=2
        else:
            self.thickness=1
        pygame.draw.rect(display, self.color,
                         (self.x_beginner,
                          self.y_beginner,
                          self.width,
                          self.height),
                         self.thickness)
        self.txt.display(display)

    def is_dynamic(self):
        self.dynamic = True
        self.color = self.main_color
        self.passive_color = self.main_color
        self.On_Text = False
        self.active_frame=False
        
class save_button(ProcessButton):
    def draw(self, display, cursor=(0, 0)):
        if self.dynamic:
            self.status_check(cursor)

        if self.active_frame:
            pass
        pygame.draw.rect(display, self.color,
                         (self.x_beginner,
                          self.y_beginner,
                          self.width,
                          self.height),
                         self.thickness)
        self.txt.display(display)
        
    def active(self):
        self.color = active_color
        self.thickness=2
    def passive(self):
        self.color = self.passive_color
        self.thickness=1
    def status_check(self, cursor):
        if self.x_beginner <= cursor[0] <= self.x_beginner + self.width:
            if self.y_beginner <= cursor[1] <= self.y_beginner + self.height:
                self.active()
            else:
                self.passive()
        else:
            self.passive()

