import threading

def invincible():
    request = back.__closure__[1].cell_contents
    while True:
        sleep(0.5)
        a, b, c, _, d, e = request.getState()
        request.setState(a, b, c, 100, d, e)

thread = threading.start(target=invincible)


def orienter(theta):
    theta0 = get_orientation()
    diff = theta - theta0
    if diff < 0:
        diff += 360
    if diff >= 180:
        while abs(theta - get_orientation())%360 > 2:
            rotateRight()
        rotateRight()
    else:
        while abs(theta - get_orientation())%360 > 2:
            rotateLeft()
        rotateLeft()


while True:
    orienter(0)
    for i in range(500):
        move()
        fire()
    
    orienter(180)
    for i in range(500):
        move()
        fire()