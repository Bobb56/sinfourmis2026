'''
Améliorations à apporter :
Mettre en place un controle de la vitesse du tank qui lui dit d'arrêter de tirer s'il est trop lent

'''

import threading


def death():
    t0 = time.monotonic()
    while time.monotonic() - t0 < 120:
        fire()
        time.sleep(0.1)






def forward(dist):
    x0, y0 = get_position()
    pos = x0, y0
    
    while dist_to_obj(x0, y0) < dist:
        defend()
        move()
        anc = pos
        pos = get_position()
        if anc == pos:
            break
    



def backward(dist):
    x0, y0 = get_position()
    pos = x0, y0
    while dist_to_obj(x0, y0) < dist:
        defend()
        anc = pos
        back()
        pos = get_position()
        if anc == pos:
            break




def turnRight(angle):
    angle = (get_orientation() - angle)%360
    while abs(angle - get_orientation())%360 > 2:
        rotateRight()
        defend()


def turnLeft(angle):
    angle = (get_orientation() + angle)%360
    while abs(angle - get_orientation())%360 > 2:
        rotateLeft()
        defend()





def obstacle():
    x,y = get_position()
    angle = get_orientation()
    
    # pour détecter les murs
    if angle <= 90 and (x > 1880 or y < 30):
        return 'wall'
    if angle >= 90 and angle <= 180 and (x < 30 or y < 30):
        return 'wall'
    if angle >= 180 and angle <= 270 and (x < 30 or y > 1050):
        return 'wall'
    if angle >= 270 and angle <= 360 and (x > 1880 or y > 1050):
        return 'wall'
    
    
    # regarde s'il y a un objet trop près
    l = detect()
    for (obj_type, dist) in l:
        if dist < 60 and obj_type != 'box':
            return obj_type
    return False







def defend():
    if close('tank'):
        fire()




def orienter(theta):
    theta0 = get_orientation()
    diff = theta - theta0
    if diff < 0:
        diff += 360
    if diff >= 180:
        while abs(theta - get_orientation())%360 > 2:
            rotateRight()
            defend()
        rotateRight()
    else:
        while abs(theta - get_orientation())%360 > 2:
            rotateLeft()
            defend()
        rotateLeft()



def dist_to_obj(x,y):
    x0, y0 = get_position()
    return distance(x,y,x0,y0)



class Function:
    def __init__(self, initial_value):
        self.value = initial_value
    
    def decrementing(self,value):
        bo = value <= self.value
        self.value = value
        return bo





def goto_until_obstacle(x,y):
    
    while dist_to_obj(x,y) > 10 and not obstacle():
        x0, y0 = get_position()
        
        if x0 == x:
            alpha = -180
        else:
            alpha = math.atan(-(y0-y)/(x0-x))*180/math.pi
        if alpha < 0:
            alpha += 360
        
        if x < x0:
            alpha += 180
            if alpha >= 360:
                alpha -= 360
        
        orienter(alpha)
        freq = 100
        count = 0
        
        f = Function(dist_to_obj(x,y))
        
        while f.decrementing(dist_to_obj(x,y)) and not obstacle():
            if count % freq == 0:
                orienter(alpha)
                pass
            
            move()
            defend()
            count += 1
    
    






def contourner_obstacle():
    # on recupère la nature de l'obstacle
    t = obstacle()
    
    if not t:
        return
    
    if t == 'wall':
        n = random.randint(0,2)
        
        if n == 0:
            ori = get_orientation()
            turnLeft(100)
            
            if get_orientation() == ori:
                turnRight(100)
            
            forward(20)
        elif n == 1:
            backward(random.randint(15, 30))
            turnLeft(100)
        
        elif n == 2:
            backward(random.randint(15, 30))
            turnRight(100)
            
    
    elif t == 'tank':
        fire()
    
    elif t == 'tree': # nouvelle technique pour contourner un arbre
        fire()
    
    # le premier element est l'angle qu'il faut tourner, ensuite la longueur du côté, puis la longueur pour traverser à coté de l'objet
    else:
        d = {
            'tower' : (100, 160),
            'tree' : (70, 120),
            'rock' : (70, 140),
        }
        
        # on recule
        backward(15)
        
        n = random.randint(0,1) # on décide si on contourne par la droite ou la gauche
        
        if n == 0: # on contourne par la droite
            turnRight(90)
            fire()
            forward(d[t][0])
            contourner_obstacle()
            turnLeft(90)
            fire()
            
            forward(d[t][1])
            
            contourner_obstacle()
            turnLeft(90)
            fire()
            forward(d[t][0])
            turnRight(90)
            
        else: # on contourne par la gauche
            
            turnLeft(90)
            fire()
            forward(d[t][0])
            contourner_obstacle()
            turnRight(90)
            fire()
            
            forward(d[t][1])
            
            contourner_obstacle()
            turnRight(90)
            fire()
            forward(d[t][0])
            turnLeft(90)


def goto(x,y, error = 10):
    while True:
        goto_until_obstacle(x,y)
        if distance(get_position()[0], get_position()[1], x, y) > error:
            contourner_obstacle()
            continue
        else:
            break





def in_vision(obj):
    l = detect()
    for (t,d) in l:
        if t == obj:
            return d
    return False




def in_vision_dist(obj, dist):
    l = detect()
    for (t,d) in l:
        if t == obj and d <= dist:
            return d
    return False



def close(obj):
    d = in_vision(obj)
    if d:
        return d < 1200
    else:
        return False



def sym_angle(theta):
    if theta > 180:
        return theta - 360
    else:
        return theta







def locate_one_time(obj, dist):
    if dist == -1: # localisation indépendamment de la distance
        vision_function = in_vision
    else:
        vision_function = lambda obj : in_vision_dist(obj, dist)
    
    theta0 = get_orientation()
    rotateRight()
    while abs(theta0 - get_orientation())%360 > 2 and not vision_function(obj):
        rotateRight()
        defend()
    
    delta_theta = 0
    while vision_function(obj):
        rotateRight()
        defend()
        delta_theta += 1
    
    for i in range(int(delta_theta/2)):
        rotateLeft()
        defend()
    
    d = vision_function(obj)
    if not d:
        return False
    else:
        x, y = get_position()
        angle = get_orientation()/180*math.pi
        
        return (x + d * math.cos(angle), y - d * math.sin(angle))



def locate(obj):
    d = locate_one_time(obj, -1)
    while not d:
        d = locate_one_time(obj, -1)
    return d




'''
def scan_map(): # fonction qui renvoie des tuples de type (orientation, objet, distance) pour toutes les orientations et tous les objets
    objects = []
    angle_0 = get_orientation()
    rotateLeft()
    while abs(get_orientation() - angle)%360 > 2:
        defend()
        l = detect()
        for i in range(len(l)):
            l[i] = (get_orientation(), l[i][0], l[i][1])
        objects += l
        
        rotateLeft()
    
    return objects



def mean_scan(objects):
    '''








def tirer(proba):
    x = random.random()
    if x <= proba:
        fire()





def tourelle(index, delta_t):
    t0 = time.monotonic()
    if index == 0: # en bas à droite
        orienter(190)
    if index == 1: # en haut à droite
        orienter(280)
    if index == 2: # en bas à gauche
        orienter(100)
    if index == 3: # en haut à gauche
        orienter(10)
    
    while time.monotonic() - t0 < delta_t:
        for i in range(55):
            rotateRight()
            tirer(0.05)
        
        fire()
        time.sleep(1)
        
        for i in range(55):
            rotateLeft()
            tirer(0.05)
        fire()


def pivot(delta_t):
    t0 = time.monotonic()
    while time.monotonic() - t0 < delta_t:
        rotateRight()
        defend()



def take_box():
    bo = False
    x,y = locate('box')
    
    while not bo:
        goto(x,y)
        bo = grab_box()
        
        if not bo:
            # re-détecter la position de la boite, sinon en prendre une autre
            coord = locate_one_time('box', 50)
            if not coord: # la boite que l'on convoitait n'existe plus
                x,y = locate('box') # on en prend une nouvelle
            else:
                x,y = coord
    
    add_wall()



def try_box():
    bo = False
    coord = locate_one_time('box', -1)

    if coord == False:
        return
    else:
        x, y = coord
    
    while not bo:
        goto(x,y)
        bo = grab_box()
        
        if not bo:
            # re-détecter la position de la boite, sinon en prendre une autre
            coord = locate_one_time('box', 50)
            if not coord: # la boite que l'on convoitait n'existe plus
                x,y = locate('box') # on en prend une nouvelle
            else:
                x,y = coord
    
    add_wall()



def new_spot():
    return random.randint(50, 1900), random.randint(50, 1000)


def strat1():
    while True:        
        index = 0
        coins = [
            (1600, 1000),
            (1800, 50),
            (50, 1000),
            (200,50)
        ]
        delta_t = 40 # on change de coin toutes les 20 secondes
        
        while True:
            take_box()
            
            goto(*coins[index])
            
            tourelle(index, delta_t)
            
            index = (index + 1) % 4


def strat2():
    t0 = time.monotonic()
    while time.monotonic() - t0 < 15:
        orienter(0)
        orienter(120)
        orienter(240)
    
    xd, yd = locate('tank')
    thread = threading.Thread(target = death)
    thread.start()
    goto(xd, yd)




def strat3():
    while True:                
        try_box()
        x, y = new_spot()
        goto(x, y, error=100)
        pivot(random.randint(0, 20))


#strat1()
#strat2()
strat3()
