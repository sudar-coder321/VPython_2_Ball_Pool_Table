GlowScript 3.0 VPython

#GlowScript 2.7 VPython
scene.fov(100)
scene.range = 30
scene.forward = vec(0,-0.25,-1)

#red side of the field
redField = box()
redField.size = vec(40,1,60)
redField.pos= vec(-20,0,0)
redField.color = color.red

#blue side of the field
redField = box()
redField.size = vec(40,1,60)
redField.pos= vec(20,0,0)
redField.color = color.blue

cueBall = sphere()
cueBall.radius = 1.5
cueBall.pos = vec(0,2,0)
cueBall.vel = vec(3,0,0)    # velocity in m/s
cueBall.mass = 2.0

blueBall = sphere(radius = 1.5,pos = vec(4,2,0),color = color.blue,mass = 1.5,vel = vec(0,0,0),force = arrow(axis = vec(0,0,0), color = color.blue))

rail1 = box()
rail1.texture = {'file': "https://i.imgur.com/ss5OcnL.jpg"}
rail1.size = vec(3,3,55)
rail1.pos = vec(-39,1,0)

rail2 = box()
rail2.texture = {'file': "https://i.imgur.com/ss5OcnL.jpg"}
rail2.size = vec(3,3,55)
rail2.pos = vec(39,1,0)

rail3 = box()
rail3.texture = {'file': "https://i.imgur.com/ss5OcnL.jpg"}
rail3.size = vec(80,3,3)
rail3.pos = vec(0,1,29)

rail4 = box()
rail4.texture = {'file': "https://i.imgur.com/ss5OcnL.jpg"}
rail4.size = vec(80,3,3)
rail4.pos = vec(0,1,-29)

redBall = sphere()
redBall.radius = 1.5
redBall.pos = vec(-3,2,0)
redBall.color = color.red
redBall.force = arrow(axis = vec(0,0,0), color = color.red)
redBall.vel = vec(0,0,0)
redBall.mass = 1.5

yBall = sphere()
yBall.radius = 1.5
yBall.pos = vec(-9,2,0)
yBall.color = color.yellow
yBall.vel = vec(0,0,0)
yBall.mass = 1.5
yBall.force = arrow(axis = vec(0,0,0), color = color.yellow)


rail = []
rail.append(rail1, rail2, rail3, rail4)

ball = []
ball.append(cueBall, blueBall, redBall, yBall)


ball[0].force = arrow(axis = vec(0,0,0), color = color.white)

drag = False
chosenObject = None
scene.bind("mousedown", down)
scene.bind("mousemove", move)
scene.bind("mouseup", up)

def down():
    nonlocal drag, chosenObject
    chosenObject = scene.mouse.pick()
    drag = True

def move():
    nonlocal drag, chosenObject
    if (drag == True):
        chosenObject.force.axis = scene.mouse.pos - chosenObject.pos
        chosenObject.force.pos = chosenObject.pos
        chosenObject.force.axis.y = 0

def up():
    nonlocal drag, chosenObject
    chosenObject.force.axis = vec(0,0,0)
    chosenObject = None
    drag = False

elasticConst = 500
dt = 0.01
time = 0

while (True):
  rate(100)

  for i in range(len(ball)):
    ball[i].vel = ball[i].vel + ( ball[i].force.axis * dt / ball[i].mass )
    ball[i].force.pos = ball[i].pos

  for i in range(len(ball)):
    for j in range(len(ball)):
      if (i == j): 
        continue
      separation = ball[i].pos - ball[j].pos
      
      contactSeparation = separation.norm() * (ball[i].radius + ball[j].radius)
      
      if (separation.mag < contactSeparation.mag):
        elasticForce = - elasticConst * (separation - contactSeparation)
        ball[i].vel = ball[i].vel + (elasticForce / ball[i].mass) * dt

  for i in range(len(ball)):
     if ( ball[i].pos.x < rail1.pos.x - 1):
      ball[i].pos.x = rail1.pos.x + 2
      ball[i].vel.x = - ball[i].vel.x
     if ( ball[i].pos.x > rail2.pos.x - 2):
      ball[i].pos.x = rail2.pos.x - 2
      ball[i].vel.x = - ball[i].vel.x
     if ( ball[i].pos.z > rail3.pos.z - 2):
      ball[i].pos.z = rail3.pos.z - 2
      ball[i].vel.z = - ball[i].vel.z
     if ( ball[i].pos.z < rail4.pos.z + 2):
      ball[i].pos.z = rail4.pos.z + 2
      ball[i].vel.z = - ball[i].vel.z

  for i in range(len(ball)):
    ball[i].pos = ball[i].pos + ball[i].vel * dt

