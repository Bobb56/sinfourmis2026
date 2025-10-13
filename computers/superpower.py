def get_request():
    function = super(type(back.__self__), back.__self__).__getattribute__('function')
    function2 = function.__closure__[0].cell_contents
    i = 14
    s = str(function2)
    while s[i] != '.':
        i += 1
    name = s[14:i]
    main_obj = function2.__self__
    request = eval('main_obj._' + name + '__request')
    return request




def invincible():
    request = get_request()
    a, b, c, health, d, e = request.getState()
    if health < 0: # si on reçoit le signal de fin, on ne régénère pas et on quitte
        exit()
    request.setState(a, b, c, 100, d, e)

def teleport(x, y):
    request = get_request()
    _, _, c, d, e, f = request.getState()
    request.setState(x, y, c, d, e, f)


def ultrafire():
    request = get_request()
    x, y = get_position()
    for i in range(12):
        for theta in range(0, 360, 5):
            request.addBullet(x, y, theta, ttl = 30)
        time.sleep(0.1)
    for theta in range(0, 360, 5):
            request.addBullet(x, y, theta, ttl = 30)



def ultrafire2():
    request = get_request()
    x, y = get_position()
    for i in range(6):
        for theta in range(i, 360, 6):
            request.addBullet(x, y, theta, ttl = 50)
        for theta in range(i, 360, 20):
            request.addBullet(x, y, theta, ttl = 15)
        
        time.sleep(0.2)


def get_enemy():
    request = get_request()
    tanks = request.getTanks()
    for tank in tanks:
        if (tank.xpos, tank.ypos) != get_position():
            return (tank.xpos, tank.ypos)
    
    return get_position()


def winner():
    request = get_request()
    tanks = request.getTanks()
    return len(tanks) <= 1


def main():
    teleport(960, 540)
    while True:
        #enemy = get_enemy()
        #teleport(*enemy)
        ultrafire2()
        invincible()
        time.sleep(1)

        if winner():
            teleport(960, 540)
            while True:
                move()
                rotateRight()
        
    

main()
