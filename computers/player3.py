while get_orientation(self) != 0:
    rotateRight(self)



def obstacle():
    x,y = get_position(self)
    angle = get_orientation(self)
    
    # pour détecter les murs
    if angle <= 90 and (x > 1880 or y < 30):
        return True
    if angle >= 90 and angle <= 180 and (x < 30 or y < 30):
        return True
    if angle >= 180 and angle <= 270 and (x < 30 or y > 1050):
        return True
    if angle >= 270 and angle <= 360 and (x > 1880 or y > 1050):
        return True
    
    
    # regarde s'il y a un objet trop près
    l = detect(self)
    for (obj_type, dist) in l:
        if dist < 60:
            return True
    return False


while True:
    while not obstacle():
        move(self)
    
    #fire(self)
    n = random.randint(0,1)
    while obstacle():
        if n:
            rotateRight(self)
        else:
            rotateLeft(self)
        move(self)
