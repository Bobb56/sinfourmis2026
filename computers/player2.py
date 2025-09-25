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
        if dist < 60:
            return obj_type
    return False








def orienter(theta):
    theta0 = get_orientation()
    diff = theta - theta0
    if diff < 0:
        diff += 360
    if diff >= 180:
        while abs(theta - get_orientation()) > 2:
            rotateRight()
        rotateRight()
    else:
        while abs(theta - get_orientation()) > 2:
            rotateLeft()
        rotateLeft()



def goto_until_obstacle(x,y):
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
    freq = 10
    count = 0
    while distance(get_position()[0], get_position()[1], x, y) > 10 and not obstacle():
        if count % freq == 0:
            orienter(alpha)
            if in_vision('tank'):
                fire()
        move()
        count += 1






def contourner_obstacle():
    # on recupère la nature de l'obstacle
    t = obstacle()
    
    if not t:
        return
    
    if t == 'wall':
        '''for i in range(90):
            rotateRight()
        for i in range(15):
            move()
        for i in range(90):
            rotateLeft()'''
        ori = get_orientation()
        for i in range(20):
            rotateLeft()
        
        
        if get_orientation() == ori:
            for i in range(20):
                rotateRight()
        
        move()
        
        return
    
    if t == 'tank':
        fire()
        return
    
    if t == 'tree': # nouvelle technique pour contourner un arbre
        fire()
        return
    
    # le premier element est l'angle qu'il faut tourner, ensuite la longueur du côté, puis la longueur pour traverser à coté de l'objet
    
    d = {
        'tower' : (45, 50, 70),
        'tree' : (55, 35, 60),
        'rock' : (50, 35, 60),
    }
    
    
    for i in range(d[t][0] + 5):
        rotateRight()
    
    for i in range(d[t][1]):
        move()
    
    contourner_obstacle()
    
    for i in range(d[t][0]):
        rotateLeft()
    
    for i in range(d[t][2]):
        move()
    
    contourner_obstacle()
    
    for i in range(d[t][0]):
        rotateLeft()

    for i in range(d[t][1]):
        move()
    
    for i in range(d[t][0]):
        rotateRight()



def goto(x,y):
    while True:
        goto_until_obstacle(x,y)
        if distance(get_position()[0], get_position()[1], x, y) > 10:
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


def locate(obj):
    theta0 = get_orientation()
    rotateRight()
    while abs(theta0 - get_orientation()) > 2 and not in_vision(obj):
        rotateRight()
        time.sleep(0.05)
    
    d = in_vision(obj)
    if not d:
        return False
    else:
        x, y = get_position()
        angle = get_orientation()/180*math.pi
        return (d * math.cos(angle) + x, d * math.sin(angle) + y)



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
        
        tirer(0.05)
        time.sleep(1)
        
        for i in range(55):
            rotateLeft()
            tirer(0.05)
        tirer(0.05)
    


while True:
    goto(1800, 50)
    tourelle(1, 999999999)