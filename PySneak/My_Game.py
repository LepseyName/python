import pygame as PG
import time as T
import random, math, move
from const import *

class Segment():
    def __init__(self, Surf, color, position):
        self.surf = Surf
        self.color = color
        self.pos = position

class Segment_A(Segment):
    def __init__(self,Surf, color, position):
        super().__init__(Surf, color, position)
                                
    def display(self, position = (-1, -1)):
        if position != (-1, -1) : self.pos = position
        try:
            if self.color == ALL_COLO["sneak"]: self.surf.blit(ALL_BILD["bild_sneak"], self.pos )
            elif self.color == ALL_COLO["beetles"]:      self.surf.blit(ALL_BILD["bild_beetle"], self.pos )
            elif self.color == ALL_COLO["sneak_head"]:     self.surf.blit(ALL_BILD["bild_sneak_head"], self.pos)
            else: self.s = PG.draw.rect(self.surf, self.color, self.pos + ALL_SIZE["segment"], 2)
        except:
            self.s = PG.draw.rect(self.surf, self.color, self.pos + ALL_SIZE["segment"], 2)

class Segment_B(Segment):
    def __init__(self,Surf, color, position):
        super().__init__(Surf, color, position)

    def display(self, position = (-1, -1)):
        if position != (-1, -1): self.pos = position
        try:
            if self.color == ALL_COLO["wall"]:  self.surf.blit(ALL_BILD["bild_wall"], self.pos )
            elif self.color == ALL_COLO["eat"]: self.surf.blit(ALL_BILD["bild_eat"], self.pos )
            elif self.color == ALL_COLO["sneak_head"]: self.surf.blit(ALL_BILD["bild_sneak_head"], self.pos)
            else: self.s = PG.draw.rect(self.surf, self.color, self.pos + ALL_SIZE["segment"])
        except:
            self.s = PG.draw.rect(self.surf, self.color, self.pos + ALL_SIZE["segment"])

class Sneak():
    def __init__(self, Surf, begin_len, Font, level):
        self.level = level
        self.len = begin_len
        self.surf = Surf
        self.font = Font
        self.segments = []
        self.beetles = []
        self.eat = []
        self.barrikads = []

    def init(self):
        self.beetles = []
        self.eat = []
        self.barrikads = []
        self.beetles_eat = 0
        self.generation_barrikade(6 + self.level, int(5 + 4 * self.level ** 0.4))
        self.generation_sneak()

    def generation_sneak(self):
        self.segments = []
        att = 20
        while att:
            att -= 1
            x = random.random() * (ALL_SIZE["plain"][0]) // ALL_SIZE["segment"][0] * ALL_SIZE["segment"][0]
            y = random.random() * (ALL_SIZE["plain"][1]) // ALL_SIZE["segment"][0] * ALL_SIZE["segment"][1] + ALL_SIZE["label"][1]
            gut = True
            G = self.len + 1
            for i in range(G * -1, G + 1, 1):
                for j in range(G * -1, G + 1, 1):
                    X = x + i * ALL_SIZE["segment"][0]
                    Y = y + j * ALL_SIZE["segment"][0]
                    for barr in self.barrikads:
                        if barr.pos == (X, Y):
                            gut = False
                            break
                    if  X < 0 or X > ALL_SIZE["plain"][0] - ALL_SIZE["segment"][0] or Y < 0 + ALL_SIZE["label"][1] or Y > ALL_SIZE["plain"][1] + ALL_SIZE["label"][1] - ALL_SIZE["segment"][0]:
                        gut = False
                        break
            if not gut: continue
            self.segments.append(Segment_A(self.surf, ALL_COLO["sneak_head"], (x, y)))
            for i in range(self.len - 1):
                rand = random.randint(0, 3)
                if rand == 0: x -= ALL_SIZE["segment"][0]
                if rand == 1: x += ALL_SIZE["segment"][0]
                if rand == 2: y -= ALL_SIZE["segment"][0]
                if rand == 3: y += ALL_SIZE["segment"][0]
                self.segments.append(Segment_A(self.surf, ALL_COLO["sneak"], (x, y)))
                self.vector = VECT[rand]
            break
        else: self.init()

    def generation_barrikade(self, col, length):
        HORIZONTAL = True
        self.barrikads = []
        for i in range(col):
            x = random.random() * (ALL_SIZE["plain"][0]) // ALL_SIZE["segment"][0] * ALL_SIZE["segment"][0]
            y = random.random() * (ALL_SIZE["plain"][1]) // ALL_SIZE["segment"][0] * ALL_SIZE["segment"][1] + ALL_SIZE["label"][1]
            radius = 1
            gut = True
            for k in range(radius * -1, radius + 1, 1):
                for j in range(radius * -1, radius + 1, 1):
                    X = x + k * ALL_SIZE["segment"][0]
                    Y = y + j * ALL_SIZE["segment"][0]
                    for barr in self.barrikads:
                        if barr.pos == (X, Y):
                            gut = False
                            break
            if not gut:
                i -=1
                continue                        
            self.barrikads.append(Segment_B(self.surf, ALL_COLO["wall"], (x, y)))
            for i in range(length - 1):
                if HORIZONTAL:
                    if x > 0 and ((x - ALL_SIZE["segment"][0], y) not in self.barrikads):
                        x -= ALL_SIZE["segment"][0]
                    elif x < ALL_SIZE["plain"][0] and ((x + ALL_SIZE["segment"][0], y) not in self.barrikads):
                        x += ALL_SIZE["segment"][0]
                    else:
                        HORIZONTAL = False
                        i -=1
                        continue
                    self.barrikads.append(Segment_B(self.surf, ALL_COLO["wall"], (x, y)))
                else:
                    if y > 0 + ALL_SIZE["label"][1] and ((x, y - ALL_SIZE["segment"][0]) not in self.barrikads):
                        y -= ALL_SIZE["segment"][0]
                    elif y < ALL_SIZE["plain"][1] + ALL_SIZE["label"][1] and (
                        (x, y + ALL_SIZE["segment"][0]) not in self.barrikads):
                        y += ALL_SIZE["segment"][0]
                    else:
                        HORIZONTAL = True
                        continue
                    self.barrikads.append(Segment_B(self.surf, ALL_COLO["wall"], (x, y)))

            if HORIZONTAL: HORIZONTAL = False
            else:          HORIZONTAL = True

    def generation_eat(self, col):
        for i in range(col):
            x = random.random() * (ALL_SIZE["plain"][0]) // ALL_SIZE["segment"][0] * ALL_SIZE["segment"][0]
            y = random.random() * (ALL_SIZE["plain"][1]) // ALL_SIZE["segment"][0] * ALL_SIZE["segment"][1] + ALL_SIZE["label"][1]

            r = [self.barrikads, self.segments, self.beetles, self.eat]
            for i in r:
                for j in i:
                    if j.pos == (x, y): break
                else: continue
                break
            else: self.eat.append(Segment_B(self.surf, ALL_COLO["eat"], (x, y)))

    def delete_eat(self, col ):
        if len(self.eat) == 0 or col>=len(self.eat): return
        for i in range(col): del self.eat[int(random.random() * (len(self.eat) - 1))]

    def generation_beetles(self, col):
        for i in range(col):
            x = random.random() * (ALL_SIZE["plain"][0]) // ALL_SIZE["segment"][0] * ALL_SIZE["segment"][0]
            y = random.random() * (ALL_SIZE["plain"][1]) // ALL_SIZE["segment"][0] * ALL_SIZE["segment"][1] + ALL_SIZE["label"][1]
            r = [self.barrikads, self.segments, self.beetles, self.eat]
            for i in r:
                for j in i:
                    if j.pos == (x, y): break
                else: continue
                break
            else:   self.beetles.append(Segment_A(self.surf, ALL_COLO["beetles"], (x, y)))

    def delete_beetles(self, col):
        if len(self.beetles) == 0 or col>=len(self.beetles): return
        for i in range(len(self.beetles)):
            if math.fabs(self.beetles[i].pos[0] - self.segments[0].pos[0]) < 100 and math.fabs(
                        self.beetles[i].pos[1] - self.segments[0].pos[1]) < 100: continue
            del self.beetles[i]
            col -= 1
            if col ==0: return

    def move(self):
        x, y = self.segments[0].pos # #Получаем координаты головы
        x += self.vector[0] * ALL_SIZE["segment"][0]  # путём добавления к х и у размера сегмента по вектору
        y += self.vector[1] * ALL_SIZE["segment"][1]

        for i in range(len(self.eat)):
            if self.eat[i].pos == (x, y):
                try: ALL_SOUN["sound_eat"].play()
                except: pass
                del self.eat[i]
                break
        else:
            for i in range(len(self.beetles)) :
                if self.beetles[i].pos == (x, y) :
                    self.beetles_eat += 1
                    try: ALL_SOUN["sound_bittles"].play()
                    except: pass
                    del self.beetles[i]
                    break
            else : del self.segments[-1]

        for i in self.barrikads: i.display() # Отрисовка стен
        for i in self.eat: i.display()        # Отрисовка еды
        
        self.segments[0].color = ALL_COLO["sneak"]
        self.segments = [Segment_A(self.surf, ALL_COLO["sneak_head"], (x, y))] + self.segments  # Добавление головы и отрисовка змеи
        for i in range(len(self.segments)-1,-1,-1): self.segments[i].display()

        for i in self.beetles: i.display()  # Отрисовка жуков
            # Проверка на выход за пределы
        if x < 0 or y < 0 + ALL_SIZE["label"][1] or x > ALL_SIZE["plain"][0] - ALL_SIZE["segment"][0] or y > \
                                ALL_SIZE["plain"][1] - ALL_SIZE["segment"][1] + ALL_SIZE["label"][1]:
            try: ALL_SOUN["sound_exit"].play()
            except:  pass
            game_over(self.surf, self.font, self, " exit to sone!")

        for i in self.barrikads:
            if (x, y) == i.pos :
                try: ALL_SOUN["sound_wall"].play()
                except: pass
                game_over(self.surf, self.font, self, "stena!")  # Проверка на наезд на стену

    def move_beetles(self):
        head_x_y = self.segments[0].pos
        X_0 = 0
        X_max = ALL_SIZE["plain"][0] - ALL_SIZE["segment"][0]
        Y_0 = 0 + ALL_SIZE["label"][1]
        Y_max = ALL_SIZE["label"][1] + ALL_SIZE["plain"][1] - ALL_SIZE["segment"][0]
        for i in self.beetles:
            vect = [0, 0]
            if math.fabs(head_x_y[0] - i.pos[0]) < 10 * ALL_SIZE["segment"][0] and math.fabs(head_x_y[1] - i.pos[1]) < 10 * ALL_SIZE["segment"][0]:
                if head_x_y[0] > i.pos[0]:   vect[0] = -1
                elif head_x_y[0] < i.pos[0]: vect[0] = 1
                else:                        vect[0] = int(random.random() * 2) - 1
                if head_x_y[1] > i.pos[1]:   vect[1] = -1
                elif head_x_y[1] < i.pos[1]: vect[1] = 1
                else:                        vect[1] = int(random.random() * 2) - 1
                buffer = vect
                X = i.pos[0] + vect[0] * ALL_SIZE["segment"][0]
                Y = i.pos[1] + vect[1] * ALL_SIZE["segment"][0]
                if X < X_0 or X > X_max : vect[0] = 0
                if Y < Y_0 or Y > Y_max : vect[1] = 0
                r= [self.barrikads, self.segments, self.eat, self.beetles]
                for mass in r :
                    for element in mass:
                        if (X, i.pos[1]) == element.pos: vect[0] = 0
                        if (i.pos[0], Y) == element.pos: vect[1] = 0
                if vect == [0, 0]:
                    vect = [-1*buffer[0], -1*buffer[1]]
                    X = i.pos[0] + vect[0] * ALL_SIZE["segment"][0]
                    Y = i.pos[1] + vect[1] * ALL_SIZE["segment"][0]
                    if X < X_0 or X > X_max: vect[0] = 0
                    if Y < Y_0 or Y > Y_max: vect[1] = 0
                    r = [self.barrikads, self.segments, self.eat, self.beetles]
                    for mass in r:
                        for element in mass:
                            if (X, i.pos[1]) == element.pos: vect[0] = 0
                            if (i.pos[0], Y) == element.pos: vect[1] = 0
            else:
                vect[0] = int(random.random() * 2) - 1
                vect[1] = int(random.random() * 2) - 1
                X = i.pos[0] + vect[0] * ALL_SIZE["segment"][0]
                Y = i.pos[1] + vect[1] * ALL_SIZE["segment"][0]
                if X < X_0 or X > X_max : vect[0] = 0
                if Y < Y_0 or Y > Y_max : vect[1] = 0
                r= [self.barrikads, self.segments, self.eat, self.beetles]
                for mass in r :
                    for element in mass:
                        if (X, i.pos[1]) == element.pos: vect[0] = 0
                        if (i.pos[0], Y) == element.pos: vect[1] = 0

            if random.random() > 0.5 and vect[0] != 0: i.pos = (i.pos[0] + vect[0] * ALL_SIZE["segment"][0], i.pos[1])
            elif vect[1] != 0:    i.pos = (i.pos[0], i.pos[1] + vect[1] * ALL_SIZE["segment"][0])
            else:                 i.pos = (i.pos[0] + vect[0] * ALL_SIZE["segment"][0], i.pos[1])

def game_over(Surf, Font, sneak, call):
    global GAME, QUIT
    GAME = False
    points = 0
    if sneak.level > 1 :
        points += 100 * (sneak.level - 1) + int((sneak.beetles_eat/(1 +(sneak.level - 1)*3)) * 100) - len(sneak.segments)
    if points : record_add(Surf, Font, points)
    Call_over = Font.render(call, False, (0, 0, 0))
    PG.draw.rect(Surf, ALL_COLO["pause"],( ALL_SIZE["plain"][0]//2 - ALL_SIZE["pause"][0] //2,
                                        ALL_SIZE["plain"][1]//2 - ALL_SIZE["pause"][1] //2) +  ALL_SIZE["pause"])
    show =["="*15, "game over", "="*15, "", call, "", "", "points: " + str(points), "-"*20 , "pres space"]
    for i in range(len(show)):
        r = Font.render(show[i], False,(0,0,0))
        Surf.blit(r,  (ALL_SIZE["plain"][0] // 2 - r.get_width()//2 + ALL_SIZE["padding"][0], ALL_SIZE["plain"][1] // 2 - ALL_SIZE["pause"][1] //2 + i*r.get_height() + ALL_SIZE["padding"][1]))
    PG.display.update();
    while 1:
        for i in PG.event.get():
            if i.type==PG.QUIT:
                QUIT = True
                return
            elif i.type==PG.KEYDOWN and i.key==PG.K_SPACE :   return

def pause(Surf, Font, sneak):
    global GAME, QUIT
    is_move = False
    is_save = False
    punkt = 0
    Menu_punkt=[]

    Pause = PG.draw.rect(Surf, ALL_COLO["pause"],( ALL_SIZE["plain"][0]//2 - ALL_SIZE["pause"][0] //2,
                                                ALL_SIZE["plain"][1]//2 - ALL_SIZE["pause"][1] //2) +  ALL_SIZE["pause"])
    for i in range(len(ALL_TEXT["pause"])):
        Menu_punkt.append(Font.render(ALL_TEXT["pause"][i],False,(0,0,0)))
        if i == punkt: PG.draw.rect(Surf, ALL_COLO["menu_shadow"], (ALL_SIZE["plain"][0] // 2 - Menu_punkt[i].get_width() // 2,
                                       ALL_SIZE["plain"][1] // 2 - ALL_SIZE["pause"][1] // 2 + 2 * i * Menu_punkt[i].get_height())
                                      + (Menu_punkt[i].get_width() + 2 * ALL_SIZE["padding"][0],Menu_punkt[i].get_height() + 2 * ALL_SIZE["padding"][1]))
        Surf.blit(Menu_punkt[i],(ALL_SIZE["plain"][0]//2 - Menu_punkt[i].get_width()//2 + ALL_SIZE["padding"][0],
                                 ALL_SIZE["plain"][1]//2 - ALL_SIZE["pause"][1] //2 + 2*i*Menu_punkt[i].get_height() + ALL_SIZE["padding"][1]))
    PG.display.update(Pause);
    while 1:
        for i in PG.event.get():
            if i.type==PG.QUIT:
                QUIT = True
                GAME = False
                return
            elif i.type==PG.KEYDOWN and i.key==PG.K_RETURN :
                if ALL_TEXT["pause"][punkt] == "Continue" : return
                if ALL_TEXT["pause"][punkt] == "Exit" :
                    GAME = False
                    return
                if ALL_TEXT["pause"][punkt] == "Save" and not is_save and game_save(sneak):
                    is_save = True
                    is_move = True
            elif i.type==PG.KEYDOWN and i.key==PG.K_ESCAPE : return
            elif i.type==PG.KEYDOWN and i.key==PG.K_DOWN:
                 punkt+=1
                 is_move = True
            elif i.type==PG.KEYDOWN and i.key==PG.K_UP:
                 punkt-=1
                 is_move = True
        
        if is_move :
            Pause = PG.draw.rect(Surf, ALL_COLO["pause"],( ALL_SIZE["plain"][0]//2 - ALL_SIZE["pause"][0] //2,
                                ALL_SIZE["plain"][1]//2 - ALL_SIZE["pause"][1] //2) +  ALL_SIZE["pause"])
            
            if punkt >= len(ALL_TEXT["pause"]): punkt = 0
            if punkt < 0 : punkt = len(ALL_TEXT["pause"])-1

            for i in range(len(ALL_TEXT["pause"])):
                if i==punkt :   PG.draw.rect(Surf, ALL_COLO["menu_shadow"],(ALL_SIZE["plain"][0] // 2 - Menu_punkt[i].get_width() // 2 ,
                           ALL_SIZE["plain"][1] // 2 - ALL_SIZE["pause"][1] // 2 + 2 * i * Menu_punkt[i].get_height() )
                            + (Menu_punkt[i].get_width() + 2*ALL_SIZE["padding"][0], Menu_punkt[i].get_height() + 2*ALL_SIZE["padding"][1]))
                Surf.blit(Menu_punkt[i],(ALL_SIZE["plain"][0] // 2 - Menu_punkt[i].get_width() // 2 + ALL_SIZE["padding"][0],
                           ALL_SIZE["plain"][1] // 2 - ALL_SIZE["pause"][1] // 2 + 2 * i * Menu_punkt[i].get_height() + ALL_SIZE["padding"][1]))

            if is_save :
                PG.draw.rect(Surf, ALL_COLO["ok"],
                     ( ALL_SIZE["plain"][0]//2 ,
                       ALL_SIZE["plain"][1]//2 + 50,
                       35, 5))
                PG.draw.rect(Surf, ALL_COLO["ok"],
                     ( ALL_SIZE["plain"][0]//2 +15,
                       ALL_SIZE["plain"][1]//2 + 50 -15,
                       5, 35))
            is_move = False
            PG.display.update(Pause)

def game(Surf, Font, sneak = None):
    global GAME, QUIT 
    GAME = True
    if sneak == None:
        sneak = Sneak(Surf,3, Font, 1)
        sneak.init()
    while GAME:
        Surf.fill((255,255,255))
        eat_beetles_max = int(1 +(sneak.level - 1)*3)
        label_inf=[]
        timer = T.time()
        timer_eat = timer
        timer_beetles = timer
        timer_beetles_move = timer
        try:
            ALL_SOUN["music_game"] = PG.mixer.music.load(ALL_FILE["music_game"])
            PG.mixer.music.set_volume(0.1)
            PG.mixer.music.play(-1)
        except:  print("load music_game faled")
        try:     Surf.blit(ALL_BILD["bild_place"], (0, ALL_SIZE["label"][1] + 1))
        except:   PG.draw.rect(Surf, ALL_COLO["body"], (0, ALL_SIZE["label"][1] + 1) + ALL_SIZE["plain"], 0)
        sneak.move()
        Surf.blit(Font.render(ALL_TEXT["play"], False,(0,0,0)),(ALL_SIZE["plain"][0]//2 - 45, ALL_SIZE["plain"][1]//2))
        PG.display.update()
        i = 1
        while i:
            for i in PG.event.get():
                if i.type==PG.QUIT:
                    QUIT = True
                    return
                elif i.type==PG.KEYDOWN and i.key==PG.K_SPACE :
                    i = 0
                    break
        while GAME:
            if T.time()- timer_eat > ALL_TIME["eat"]:
                timer_eat = T.time()
                if len(sneak.eat) > ALL_LIFE["eat"] : sneak.delete_eat(len(sneak.eat) - ALL_LIFE["eat"])
                sneak.generation_eat(1)

            if T.time()- timer_beetles > ALL_TIME["beetles"]:
                timer_beetles = T.time()
                if len(sneak.beetles) > ALL_LIFE["beetles"] : sneak.delete_beetles(len(sneak.beetles) - ALL_LIFE["beetles"])
                sneak.generation_beetles(1)

            if T.time()- timer_beetles_move > ALL_TIME["beetles_move"]:
                timer_beetles_move = T.time()
                sneak.move_beetles()

            if T.time()- timer > ALL_TIME["FPS"]:
                Surf.fill((255,255,255))
                timer = T.time()
                try:   Surf.blit(ALL_BILD["bild_place"], (0,ALL_SIZE["label"][1] + 1))
                except: PG.draw.rect(Surf, ALL_COLO["body"],(0,ALL_SIZE["label"][1] + 1)+ALL_SIZE["plain"],0)

                label_inf=["Level: " +str(sneak.level), "Beetle: "+str(sneak.beetles_eat) + "/" + str(eat_beetles_max), "Length: "+str(len(sneak.segments))]
                for i in range(3):   Surf.blit( Font.render(str(label_inf[i]),False,(0,0,0)) ,(i*ALL_SIZE["label"][0],0))

                sneak.move()
                
                if eat_beetles_max <= sneak.beetles_eat:
                    sneak.level += 1
                    PG.display.update()
                    timer = T.time()
                    try: ALL_SOUN["sound_win"].play()
                    except: pass
                    while T.time() - timer <= ALL_TIME["win"] : pass
                    break;
                PG.display.update()
                #print("FPS: " + str(1/(T.time() - timer)))
                timer = T.time()

            for i in PG.event.get():
                if i.type==PG.QUIT:
                    QUIT = True
                    GAME = False
                    return
                elif i.type==PG.KEYDOWN and i.key==PG.K_ESCAPE :
                    pause(Surf, Font, sneak)
                elif i.type==PG.KEYDOWN and i.key==PG.K_LEFT:
                    sneak.vector = LEFT
                elif i.type==PG.KEYDOWN and i.key==PG.K_RIGHT:
                    sneak.vector = RIGHT
                elif i.type==PG.KEYDOWN and i.key==PG.K_UP:
                    sneak.vector = UP
                elif i.type==PG.KEYDOWN and i.key==PG.K_DOWN:
                    sneak.vector = DOWN
        sneak.init()

def records(Surf, Font):
    global QUIT
    is_records = True
    punkt = 0
    records_dict = records_read()
    all_records = list(records_dict.values())
    all_name = list(records_dict.keys())
    max_width_len = 25
    for i in range(len(all_name)):
        if len(all_name[i]): all_name[i] = all_name[i][0:len(all_name[i]) - 1]
        all_records[i] = str(all_records[i])
        if len(all_name[i]) + len(all_records[i]) < max_width_len:
            all_records[i] = (max_width_len - len(all_name[i]) - len(all_records[i])) * '-' + all_records[i]
        all_name[i] += all_records[i]
    records_punkt = []
    for i in range(len(all_name)): records_punkt.append(Font.render(all_name[i], False, (0, 0, 0)))
    if len(records_punkt): show = ALL_SIZE["body"][1] // 2 // records_punkt[0].get_height()
    while is_records:
        Surf.fill(ALL_COLO["menu"])
        for i in PG.event.get():
            if i.type == PG.QUIT:
                QUIT = True
                is_records = False
                break
            elif i.type == PG.KEYDOWN and i.key == PG.K_ESCAPE:
                is_records = False
                break
            elif i.type == PG.KEYDOWN and i.key == PG.K_DOWN: punkt += 1
            elif i.type == PG.KEYDOWN and i.key == PG.K_UP: punkt -= 1
            else:  continue

        if len(records_punkt):
            if punkt >= len(records_punkt): punkt = 0
            if punkt < 0: punkt = len(records_punkt) - 1

            index = 0
            first = (punkt // show) * show
            last = (punkt // show + 1) * show
            if last > len(records_punkt): last = len(records_punkt)
            for i in range(first, last, 1):
                if i == punkt:
                    PG.draw.rect(Surf, ALL_COLO["menu_shadow"], (ALL_SIZE["padding"][0],index * records_punkt[i].get_height()+ ALL_SIZE["padding"][1]) + (ALL_SIZE["body"][0]-2*ALL_SIZE["padding"][0], records_punkt[i].get_height()))
                Surf.blit(records_punkt[i],
                          (ALL_SIZE["body"][0] // 2 - records_punkt[i].get_width() // 2, 0 + index*records_punkt[i].get_height() + ALL_SIZE["padding"][1]))
                index += 1
        else:
            Surf.blit(Font.render(ALL_TEXT["not_saves"], False, (0, 0, 0)), (80, 100))
        PG.display.update()

def record_add(Surf, Font, points):
    global QUIT
    all_record = records_read().values()
    if len(all_record) != 0:
        for i in all_record:
            if i >= points: return
    try:
        name = ""
        is_enter = True
        while is_enter:
            PG.draw.rect(Surf, ALL_COLO["pause"], (ALL_SIZE["plain"][0] // 2 - ALL_SIZE["pause"][0] // 2,
                                                   ALL_SIZE["plain"][1] // 2 - ALL_SIZE["pause"][1] // 2) + ALL_SIZE["pause"])
            show = ["=" * 15, "new record", "=" * 15, "", "", "", "name: " + str(name), "-" * 20, "pres enter"]
            for i in range(len(show)):
                r = Font.render(show[i], False, (0, 0, 0))
                Surf.blit(r, (ALL_SIZE["plain"][0] // 2 - r.get_width() // 2 + ALL_SIZE["padding"][0],
                              ALL_SIZE["plain"][1] // 2 - ALL_SIZE["pause"][1] // 2 + i * r.get_height() +
                              ALL_SIZE["padding"][1]))
            PG.display.update();
            for i in PG.event.get():
                if i.type == PG.QUIT:
                    QUIT = True
                    return
                elif i.type == PG.KEYDOWN and i.key == PG.K_RETURN:
                    is_enter = False
                    break
                elif i.type == PG.KEYDOWN and i.key == PG.K_BACKSPACE:
                    if len(name):
                        name = name[0:len(name) - 1]
                elif i.type == PG.KEYDOWN:
                    if len(name) < 10: name += i.unicode

        Records = open(ALL_FILE["records"], 'a')
        Records.write(name + '\n' + str(points) + '\n')
        Records.close()
    except:
        print("Error write records")

def saves_read(Surf, Font):
    my_saves = {}
    name = ""
    try:
        Saves = open(ALL_FILE["saves"], 'r')
        i = 0
        for line in Saves:
            if i == 0:                                                                  #read name
                name = line
                if name[-1] == '\n': name = name[0:len(name) - 1]
            if i == 1:  my_saves[name] = Sneak(Surf, 3, Font, int(line))                #read level
            if i == 2:                                                                  #sneak
                segments = []
                last = 0
                for k in range(len(line)):
                    if line[k] == ' ':
                        segments.append(float(line[last:k]))
                        last = k
                my_saves[name].segments.append(Segment_A(Surf, ALL_COLO["sneak_head"], (segments[0], segments[1])))
                for k in range(2, len(segments), 2): my_saves[name].segments.append(Segment_A(Surf, ALL_COLO["sneak"], (segments[k], segments[k + 1])))
            if i == 3:                                                                  #vector
                vector = []
                last = 0
                for k in range(len(line)):
                    if line[k] == ' ':
                        vector.append(int(line[last:k]))
                        last = k
                my_saves[name].vector = vector
            if i == 4:
                beetles = []
                last = 0
                for k in range(len(line)):
                    if line[k] == ' ':
                        beetles.append(float(line[last:k]))
                        last = k
                for k in range(0, len(beetles), 2):
                    my_saves[name].beetles.append(Segment_A(Surf, ALL_COLO["beetles"], (beetles[k], beetles[k + 1])))
            if i == 5:
                barrikads = []
                last = 0
                for k in range(len(line)):
                    if line[k] == ' ':
                        barrikads.append(float(line[last:k]))
                        last = k
                for k in range(0, len(barrikads), 2):
                    my_saves[name].barrikads.append(Segment_B(Surf, ALL_COLO["wall"],(barrikads[k], barrikads[k + 1])))
            if i == 6:
                eat = []
                last = 0
                for k in range(len(line)):
                    if line[k] == ' ':
                        eat.append(float(line[last:k]))
                        last = k
                for k in range(0, len(eat), 2):
                    my_saves[name].eat.append(Segment_B(Surf, ALL_COLO["eat"],(eat[k], eat[k + 1])))
            if i == 7:                                                                  #beetles_eat
                my_saves[name].beetles_eat = int(line)
                i = -1
            i += 1
        Saves.close()
    except:
        print("error read records")
    return my_saves


def saves(Surf, Font):
    global QUIT
    is_rewrite = False
    is_saves = True
    punkt = 0
    saves_dict = saves_read(Surf, Font)
    all_saves = list(saves_dict.values())
    all_name = list(saves_dict.keys())
    saves_punkt = []
    print("read "+str(len(saves_dict))+" saves")
    for i in range(len(all_name)): saves_punkt.append((Font.render(all_name[i], False, (0, 0, 0)),
                                                       Font.render("Level: " + str(all_saves[i].level), False, (0, 0, 0))))
    if len(saves_punkt): show = ALL_SIZE["body"][1]//2//saves_punkt[0][0].get_height()
    
    while is_saves:
        Surf.fill(ALL_COLO["menu"])
        for i in PG.event.get():
            if i.type == PG.QUIT:
                QUIT = True
                is_saves = False
                break
            elif i.type == PG.KEYDOWN and i.key == PG.K_RETURN:
                LEVEL = all_saves[punkt].level
                try: PG.mixer.music.stop()
                except: pass
                game(Surf, Font, all_saves[punkt])
                try:
                    PG.mixer.music.load(ALL_FILE["music_ground"])
                    PG.mixer.music.play(-1)
                    PG.mixer.music.set_volume(0.1)
                except:  pass
                is_saves = False
                break
            elif i.type == PG.KEYDOWN and i.key == PG.K_DELETE:
                del all_name[punkt]
                del all_saves[punkt]
                del saves_punkt[punkt]
                is_rewrite = True
            elif i.type == PG.KEYDOWN and i.key == PG.K_ESCAPE:
                is_saves = False
                break
            elif i.type == PG.KEYDOWN and i.key == PG.K_DOWN: punkt += 1
            elif i.type == PG.KEYDOWN and i.key == PG.K_UP: punkt -= 1
            else:      continue

        if len(saves_punkt):
            if punkt >= len(saves_punkt): punkt = 0
            if punkt < 0: punkt = len(saves_punkt) - 1

            index = 0
            first = (punkt // show) * show
            last = (punkt // show + 1) * show
            if last > len(saves_punkt): last = len(saves_punkt)
            for i in range(first, last, 1):
                if i == punkt:
                    PG.draw.rect(Surf, ALL_COLO["menu_shadow"], (ALL_SIZE["padding"][0],index * saves_punkt[i][0].get_height()+ ALL_SIZE["padding"][1]) + (ALL_SIZE["body"][0]-2*ALL_SIZE["padding"][0], 2*saves_punkt[i][0].get_height()))
                Surf.blit(saves_punkt[i][0],
                          (ALL_SIZE["body"][0] // 2 - saves_punkt[i][0].get_width() // 2, 0 + index*saves_punkt[i][0].get_height() + ALL_SIZE["padding"][1]))
                Surf.blit(saves_punkt[i][1],
                          (ALL_SIZE["body"][0] // 2 - saves_punkt[i][1].get_width() // 2, 0 + (index + 1)*saves_punkt[i][1].get_height() + ALL_SIZE["padding"][1]))
                index += 2
        else:
            Surf.blit(Font.render(ALL_TEXT["not_saves"], False, (0, 0, 0)), (80, 100))
        PG.display.update()
    if is_rewrite:
        Saves = open(ALL_FILE["saves"], 'w')
        Saves.close()
        for i in range(len(all_name)):  game_save(all_saves[i], all_name[i])

def game_save(sneak, name = None ):
    if name == None: name = "#" + str(random.random()) + "#"
    try:
        Saves = open(ALL_FILE["saves"], 'a')
        Saves.write(name + '\n')
        Saves.write(str(sneak.level) + '\n')
        for i in sneak.segments:
            Saves.write(str(i.pos[0]) + ' ')
            Saves.write(str(i.pos[1]) + ' ')
        Saves.write('\n' + str(sneak.vector[0]) + ' ' + str(sneak.vector[1]) + ' \n')
        for i in sneak.beetles:
            Saves.write(str(i.pos[0]) + ' ')
            Saves.write(str(i.pos[1]) + ' ')
        Saves.write('\n')
        for i in sneak.barrikads:
            Saves.write(str(i.pos[0]) + ' ')
            Saves.write(str(i.pos[1]) + ' ')
        Saves.write('\n')
        for i in sneak.eat:
            Saves.write(str(i.pos[0]) + ' ')
            Saves.write(str(i.pos[1]) + ' ')
        Saves.write('\n' + str(sneak.beetles_eat) + '\n')

        Saves.close()
        return True
    except:
        print("Error write")
        return False


def records_read():
    all_records = {}
    try:
        Records = open(ALL_FILE["records"], 'r')
        i = 0
        for line in Records:
            if i == 0: name = line
            elif i == 1:
                all_records[name] = int(line)
                i = -1
            i += 1
        Records.close()
        print("read "+str(len(all_records))+" records")
    except:
        print("none records")
    return all_records


def menu():
    global GAME, LEVEL
    LEVEL = 1
    PG.init()
    PG.font.init()
    Surf = PG.display.set_mode(ALL_SIZE["body"])
    PG.display.set_caption(ALL_TEXT["title"])
    try:
        Font = PG.font.SysFont('UbuntuMono-R.ttf', SIZEx * 20)
    except:
        Font = PG.font.SysFont(None, SIZEx * 20)
        print("load font faled")
    try:
        bild_sneak = PG.image.load(ALL_FILE["bild_sneak"])
        bild_sneak = PG.transform.scale(bild_sneak, ALL_SIZE["segment"])
        ALL_BILD["bild_sneak"] = bild_sneak.convert()
    except:
        print("load sneak_bild faled")
        pass
    try:
        bild_sneak_head = PG.image.load(ALL_FILE["bild_sneak_head"])
        bild_sneak_head = PG.transform.scale(bild_sneak_head, ALL_SIZE["segment"])
        ALL_BILD["bild_sneak_head"] = bild_sneak_head.convert()
    except:
        print("load bild_sneak_head faled")
        pass
    try:
        bild_beetle = PG.image.load(ALL_FILE["bild_beetle"])
        bild_beetle = PG.transform.scale(bild_beetle, ALL_SIZE["segment"])
        ALL_BILD["bild_beetle"] = bild_beetle#.convert()
    except:
        print("load beetle_bild faled")
        pass
    try:
        bild_wall = PG.image.load(ALL_FILE["bild_wall"])
        bild_wall = PG.transform.scale(bild_wall, ALL_SIZE["segment"])
        ALL_BILD["bild_wall"] = bild_wall.convert()
    except:
        print("load wall_bild faled")
        pass
    try:
        bild_eat = PG.image.load(ALL_FILE["bild_eat"])
        bild_eat = PG.transform.scale(bild_eat, ALL_SIZE["segment"])
        ALL_BILD["bild_eat"] = bild_eat
    except:
        print("load wall_eat faled")
        pass
    try:
        bild_place = PG.image.load(ALL_FILE["bild_place"])
        bild_place = PG.transform.scale(bild_place, ALL_SIZE["plain"])
        ALL_BILD["bild_place"] = bild_place.convert()
    except:
        print("load place_bild faled")
        pass
    try:  ALL_SOUN["sound_eat"] = PG.mixer.Sound(ALL_FILE["sound_eat"])
    except:  print("load sound_eat faled")
    try:  ALL_SOUN["sound_bittles"] = PG.mixer.Sound(ALL_FILE["sound_bittles"])
    except:  print("load sound_bittles faled")
    try:  ALL_SOUN["sound_wall"] = PG.mixer.Sound(ALL_FILE["sound_wall"])
    except:  print("load sound_wall faled")
    try:  ALL_SOUN["sound_exit"] = PG.mixer.Sound(ALL_FILE["sound_exit"])
    except:  print("load sound_exit faled")
    try:  ALL_SOUN["sound_win"] = PG.mixer.Sound(ALL_FILE["sound_win"])
    except:  print("load sound_win faled")
    try:
        PG.mixer.music.load(ALL_FILE["music_ground"])
        PG.mixer.music.play(-1)
        PG.mixer.music.set_volume(0.1)
    except:  print("load music_ground faled")
    punkt = 0
    Menu_punkt = []

    for i in range(len(ALL_TEXT["menu"])): Menu_punkt.append(Font.render(ALL_TEXT["menu"][i], False, (0, 0, 0)))
    menu_padding = (ALL_SIZE["body"][1]//len(Menu_punkt)-Menu_punkt[0].get_height())//2
        #Surf.blit(Menu_punkt[i], (ALL_SIZE["body"][0] // 2 - Menu_punkt[i].get_width() // 2, 0 + i * Menu_punkt[i].get_height()))
    PG.display.update();
    while 1:
        Surf.fill(ALL_COLO["menu"])

        for i in PG.event.get():
            if i.type == PG.QUIT:
                PG.quit()
                exit()
                return
            elif i.type == PG.KEYDOWN and i.key == PG.K_RETURN:
                if ALL_TEXT["menu"][punkt] == "Game":
                    try: PG.mixer.music.stop()
                    except:  pass
                    game(Surf, Font)
                    try:
                        PG.mixer.music.load(ALL_FILE["music_ground"])
                        PG.mixer.music.play(-1)
                        PG.mixer.music.set_volume(0.1)
                    except:  pass
                if ALL_TEXT["menu"][punkt] == "Saves": saves(Surf, Font)
                if ALL_TEXT["menu"][punkt] == "Records": records(Surf, Font)
                if ALL_TEXT["menu"][punkt] == "ob": autor(Surf, Font)
                if ALL_TEXT["menu"][punkt] == "Exit":
                    PG.quit()
                    return
            elif i.type == PG.KEYDOWN and i.key == PG.K_DOWN: punkt += 1
            elif i.type == PG.KEYDOWN and i.key == PG.K_UP:   punkt -= 1
            else:             continue

        if QUIT:
            PG.quit()
            return

        if punkt >= len(ALL_TEXT["menu"]): punkt = 0
        if punkt < 0: punkt = len(ALL_TEXT["menu"]) - 1

        for i in range(len(ALL_TEXT["menu"])):
            if i == punkt:
                PG.draw.rect(Surf, ALL_COLO["menu_shadow"],
                             (ALL_SIZE["body"][0] // 2 - Menu_punkt[i].get_width() // 2 - 10, menu_padding + i *( Menu_punkt[i].get_height() + menu_padding) - ALL_SIZE["padding"][1]) + (
                             Menu_punkt[i].get_width() + 2*ALL_SIZE["padding"][0], Menu_punkt[i].get_height() + 2*ALL_SIZE["padding"][1]))
            Surf.blit(Menu_punkt[i], (ALL_SIZE["body"][0] // 2 - Menu_punkt[i].get_width() // 2, menu_padding + i *( Menu_punkt[i].get_height() + menu_padding)))

        PG.display.update()

def autor(Surf, Font):
    global QUIT
    is_autor = True
    Surf.fill(ALL_COLO["menu"])
    try:
        info = PG.image.load(ALL_FILE["info"]).convert()
        info = PG.transform.scale(info,(ALL_SIZE["plain"][0] - 80, ALL_SIZE["plain"][1] - 60 ))
        Surf.blit(info, (40,20))
    except:
        pass
    Surf.blit(Font.render("for BNTU",False,(0,0,0)),(10,ALL_SIZE["body"][1] - 40))
    Surf.blit(Font.render("Вадим Пугачёв",False,(0,0,0)),(ALL_SIZE["body"][0] - SIZEx*120, ALL_SIZE["body"][1] - 40))
    PG.display.update()
    while is_autor:
        for i in PG.event.get():
            if i.type==PG.QUIT:
                QUIT = True
                is_autor = False
                break
            elif i.type==PG.KEYDOWN and i.key==PG.K_ESCAPE :
                is_autor = False
                break
            else: continue


if __name__=="__main__":
    menu()
