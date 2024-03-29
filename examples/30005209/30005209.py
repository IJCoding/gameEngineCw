#!/usr/bin/env python3

import pge, sys, math, random
from pygame.locals import *


#
#  bubble class which is used to record, colour, circle and children
#  children are bubbles which connect below the current bubble
#

class bubble:
    def __init__ (self, cir, col):
        self.circle = cir
        self.colour = col
        self.circle.fix ()
        self.circle.on_collision (bubble_hits_bubble)
        self.children = []  #  no bubbles attached below this bubble
    #
    #  addChild - adds bubble, b, as a child of self.
    #
    def addChild (self, b):
        self.children += [b]
    #
    #  removeChild - removes all bubbles in blist from the children field.
    #
    def removeChild (self, blist):
        if self.children != []:
            self.children = [x for x in self.children if x not in blist]


bubbleDict = {}  # allows us to obtain a bubble list from a pge circle
currentCircle = None
currentColour = None


#
#  printColour - print the colour string.
#

def printColour (c):
    global colourNames
    print(colourNames[c], end=' ')

def getColour(c):
    global colourNames
    return colourNames[c]

#
#  dumpData - display all bubble colours and their chains and children
#

def dumpData (message):
    print("dumpData", message)
    print("bubbleDict", bubbleDict)
    for c in list(bubbleDict.keys ()):
        print("pge circle", end=' ')
        print(" is in a list with: ", end=' ')
        for l in bubbleDict[c]:
            printColour (l.colour)
            if l.children != []:
                print(" [ children: ", end=' ')
                for c in l.children:
                    printColour (c.colour)
                    print(", ", end=' ')
                print("]", end=' ')
            print(", ", end=' ')
        print(" ")

#
#  removeChildren - remove all bubbles in blist from all children in all bubbles.
#

def removeChildren (blist):
    for circle in list(bubbleDict.keys ()):
        for b in bubbleDict[circle]:
            b.removeChild (blist)

#
#  unfreezeList - unfreeze all bubbles in blist and return any children bubbles
#                 of these bubbles.  Remove any reference to these circles/bubbles
#                 as they will be deleted as soon as they hit the bottom edge.
#

def unfreezeList (blist):
    todo = []
    for b in blist:
        print("bubble", b, "should be unfixed")
        b.circle.unfix ()
        if b.circle in bubbleDict:
            todo += bubbleDict[b.circle]
            del bubbleDict[b.circle]
        todo += b.children
        removeChildren (todo)
    return todo


#
#  unfreezeAll - unfreeze all bubbles attached to circle (via children)
#

def unfreezeAll (circle):
    global bubbleDict
    print("unfreezeAll", circle)
    dumpData ("unfreezeAll")
    blist = bubbleDict[circle]
    while blist != []:
        blist = unfreezeList (blist)
    currentCircle.unfix ()
    dumpData ("finished unfreeze")

#
#  bubble_hits_bar - the callback for the bubble hitting the top edge.
#

def bubble_hits_bar (o, e):
    global bubbleDict, currentCircle
    print("bubble_hits_bar", currentCircle)
    if currentCircle != None:
        if currentCircle in bubbleDict:
            print("odd the bubble is already registered")
        else:
            initChain (currentCircle, currentColour)
    currentCircle = None
    dumpData ("end of bubble_hits_bar")

#
#  initChain - create an initial bubble in a chain of one.
#

def initChain (circle, colour):
    global bubbleDict
    b = bubble (circle, colour)
    bubbleDict[circle] = [b]   # the first bubble in a chain is keyed via a circle


#
#  updateChains - adds currentCircle/currentColour bubble to the chain specified by circle.
#

def updateChains (circle):
    global bubbleDict
    print("updateChains")
    blist = bubbleDict[circle]
    print("blist", blist, "len (blist) =", len (blist))
    blist += [bubble (currentCircle, currentColour)]
    print("blistis now", blist, "len (blist) =", len (blist))
    # and update all circle -> chain entries
    for b in blist:
        bubbleDict[b.circle] = blist


#
#  addBubble - Prerequiste  :  circle is a pge object which has not been deleted.
#              Postrequisite:  assuming that circle is already known in the bubbleDict
#                              and if the collided chain has two bubbles of the same colour
#                              then unfreeze these bubble and their children.
#                              A same colour collision is appended to the chain.
#                              A different colour collision creates a new chain with
#                              a single bubble.
#

def addBubble (circle):
    global bubbleDict
    print("addBubble")
    if circle in bubbleDict:
        blist = bubbleDict[circle]
        print(blist, len (blist))
        if blist[0].colour == currentColour:
            print("same colour", blist)
            if len (blist) == 2:
                unfreezeAll (circle)
                return
            else:
                print("not enough of the same colour bubbles to unfreeze them")
                updateChains (circle)
        else:
            print("bubble hit is a different colour")
            b = bubble (currentCircle, currentColour)
            blist[-1].addChild (b)
            bubbleDict[currentCircle] = [b]
        dumpData ("end of addBubble")
    else:
        print("addBubble - does not know about circle", circle)

#
#  bubble_hits_bubble - call back for a circle hitting a frozen bubble.
#

def bubble_hits_bubble (o, e):
    global currentCircle
    print("bubble hits bubble, currentCircle =", currentCircle)
    if currentCircle != None:
        b = e.collision_between ()
        for o in b:
            if o.is_fixed ():
                print("object, o, is fixed", o)
            else:
                print("object, o, is not fixed", o)
            if not currentCircle.is_fixed ():
                addBubble (o)
        currentCircle = None
    dumpData ("end of bubble_hits_bubble")

print("starting frozenbubble")
pge.interactive ()
# pge.batch ()
pge.record ()

t = pge.rgb (1.0/2.0, 2.0/3.0, 3.0/4.0)
#wood_light = pge.rgb (166.0/256.0, 124.0/256.0, 54.0/256.0)
#wood_dark = pge.rgb (76.0/256.0, 47.0/256.0, 0.0)
#red = pge.rgb (0.65, 0.1, 0.2)
#steel = pge.rgb (0.5, 0.5, 0.5)
#copper = pge.rgb (0.5, 0.3, 0.2)
#gold = pge.rgb (0.8, 0.6, 0.15)
ball_size = 0.02
boarder = 0.01
#green = pge.rgb (0.1, 0.6, 0.2)
#blue = pge.rgb (0.0, 0.0, 1.0)
#blue = pge.rgb (0.0, 100.0/255.0, 1.0)

# Colours
white       = pge.rgb(1.00, 1.00, 1.00)
dark_blue   = pge.rgb(0.17, 0.24, 0.31)
blue        = pge.rgb(0.16, 0.50, 0.73)
green       = pge.rgb(0.15, 0.68, 0.38)
red         = pge.rgb(0.75, 0.22, 0.17)
cloud       = pge.rgb(0.96, 0.94, 0.95)
silver      = pge.rgb(0.74, 0.76, 0.78)
concrete    = pge.rgb(0.58, 0.65, 0.65)
abestos     = pge.rgb(0.50, 0.55, 0.55)
orange      = pge.rgb(0.95, 0.61, 0.07)

gap = 0.01
previous = None
seconds_left = None
bonus = None
score = 0
back = None
scoreboard = None
loading = None      ## Used to check if gun is currently loading
gun = None
gun_angle = 0
gun_type_cur = 1    ## Current gun loadout (1-red, 2-blue, 3-green)
can_fire = True     ## Used to enable / disable ability to fire
bound = True        ## Used to enable / disable allowed angle of rotation
setup = False

slowdown = 5
simulatedtime = 60
colourNames = { dark_blue   : "dark_blue",
                blue        : "blue",
                green       : "green",
                red         : "red",
                cloud       : "cloud",
                silver      : "silver",
                concrete    : "concrete" ,
                abestos     : "abestos",
                orange      : "orange"  }


def finish_game (event, param):
    #Close the program
    sys.exit (0)

def placeBoarders (thickness, color):
    print("placeBoarders")
    n = pge.box (0.0, 1.0-thickness-0.1, 1.0, thickness, color).fix ()
    e = pge.box (1.0-thickness, 0.0, thickness, 1.0, color).fix ()
    s = pge.box (0.0, 0.0, 1.0, thickness, color).fix ()
    w = pge.box (0.0, 0.0, thickness, 1.0, color).fix ()
    return n, e, s, w

def fire (e, colour):
    global currentColour, currentCircle, gun_angle
    mouse = pge.pyg_to_unit_coord (e.pos)
    currentColour = colour
    currentCircle = pge.circle (0.5, 0.21, 0.03, currentColour).mass (1.0)
    currentCircle.put_yvel (7*mouse[1])
    currentCircle.put_xvel (math.sin(gun_angle/180.0)*-6.0)


def fire_circle (e):
    if e.button == 1:
        fire (e, red)
    elif e.button == 2:
        fire (e, blue)
    elif e.button == 3:
        fire (e, green)


def mouse_press (e):
    #global currentCircle, currentColour
    print(pge.pyg_to_unit_coord (e.pos))
    #if currentCircle == None:
    #    fire_circle (e)


def myquit (e):
    print("goodbye, dumping world")
    pge.dump_world ()
    sys.exit (0)

def delete_ball (o, e):
    global score
    print("delete_ball called")
    p = e.collision_between ()
    if p != None and p != []:
        for i in p:
            if i != o:
                update_score(10)
                i.rm ()

def fire_bubble_key(e = None, f = None):
    global currentCircle, gun, currentColour, seconds_left
    
    #Provided the game isn't over set the variables from gun
    if currentCircle == None and seconds_left > 0:
        currentColour = gun.get_colour()
        currentCircle = pge.circle (0.5, 0.21, 0.03, currentColour)
        currentCircle.mass (1.0)
        currentCircle.put_yvel(8.5)

        #Notably the elasticity...
        currentCircle.set_elasticity(gun.get_elasticity())

        #...and the Gravity on a per obj basis
        currentCircle.set_gravity(gun.get_gravity())      

        #Print some info to terminal
        print("GRAVITY: ", currentCircle.get_gravity())
        print(gun.get_elasticity())

        scale = (gun_angle - 180.0) / 180.0
        #print("scale = ", scale)
        scale *= -20.0
        #print ("vec =[", scale, ", 7.0]")
        currentCircle.put_xvel(scale)
        update_score(-5)

def fire_bubble ():
    global currentCircle, currentColour, score
    if currentCircle == None:
        currentColour = red
        currentCircle = pge.circle (0.5, 0.1, 0.03, currentColour)
        currentCircle.mass (1.0)
        currentCircle.put_yvel (8.0)
        # pge.dump_world ()S

def reload(e = None, f = None):
    global gun, can_fire
    
    #Update ability to fire
    display_fire()
    can_fire = True

def increment_gun(e = None, f = None):
    global gun_type_cur
    # Increment the current gun to be another setting
    gun_type_cur += 1 
    
    #Should it exceed the current max of settings - loop to 0
    if gun_type_cur > 3:
        gun_type_cur = 1

    #Ouput change in terminal
    print("increment_gun called: ", gun_type_cur)
    
    #Change gun to new setting
    change_gunType(gun_type_cur)

def key_pressed (e):
    global gun, gun_angle, gun_types, gun_type_cur, can_fire, bound
    temp_a = gun_angle
    if e.key == K_ESCAPE:
        myquit (e)

    #Press down to change the ammo/gun type
    elif e.key == K_DOWN:
        increment_gun()

    #Press up to fire
    elif e.key == K_UP:
        #If allowed to fire
        if can_fire:
            fire_bubble_key()
            display_loading()          
            can_fire = False
            pge.at_time(2.0, reload)

    #Press right to turn one way
    elif e.key == K_RIGHT:
        gun_angle += 5
    
    #Press left to turn the other way
    elif e.key == K_LEFT:
        gun_angle -= 5
    
    #So long as the gun is bound keep it between 100 and 260
    if bound:    
        if gun_angle < 100:
            gun_angle = 100
        elif gun_angle > 260:
            gun_angle = 260
    if temp_a != gun_angle:
        gun_angle %=360
        gun.rotate (gun_angle * math.pi / 180.0)
        #print(gun_angle)

def place_bubble (x, colour):
    global currentColour, currentCircle, gun
    
    #Change gun type based on colour provided
    if colour == red:
        change_gunType(1)
    elif colour == blue:
        change_gunType(2)
    elif colour == green:
        change_gunType(3)
    
    # Set local variable to information from gun
    currentColour = gun.get_colour()
    currentCircle = pge.circle (0.5, 0.21, 0.03, currentColour).mass (1.0)
    currentCircle.put_yvel(8.5)
    currentCircle.put_xvel ((0.5-x)*-6.0)
    pge.run (0.2)

def change_gunType(new_gun_type):
    global gun, gun_type, currentColour, setup
    
    #Update the gun_type to the passed variable
    gun_type = new_gun_type
    
    #Set variables based on gun_type - both colour and elasticity
    if gun_type == 1:
        gun.set_colour(red)
        gun.set_elasticity(0.98)
        gun.set_gravity(-9.8)
    elif gun_type == 2:
        gun.set_colour(blue)
        gun.set_elasticity(0.80)
        gun.set_gravity(-15.0)
    elif gun_type == 3:
        gun.set_colour(green)
        gun.set_elasticity(0.70)
        gun.set_gravity(-20.0)

    if setup:        
        gun.set_elasticity(0.98)
        gun.set_gravity(-9.8)
    
    #Print function to show changes if reading terminal for an error.    
    print("Change_gunType called:", getColour(gun.get_colour()), "|", gun.get_elasticity())
#
#
#
def display_bonus (e = None, f = None):
    global bonus
    
    # Check there is no bonus currently in play (delete if there is)
    if bonus is None:
        # Display text denoting a bonus has been scored
        bonus = pge.text (0.3, 0.3, "bonus score", white, 100, -1)
        pge.at_time(1.0, display_bonus)
    else:
        bonus.rm()
        bonus = None

def delete_me(pge_obj, pge_event):
    global score, bonus
    #Removes the object from the scene
    pge_obj.rm()
    
    #Adds score
    update_score(2)
    #display_bonus()

def chair(x,y,width,height, is_left):
    thickness = 0.01
    #Create the object out of the back, seat and leg - facing the correct way
    if is_left:    
        back = pge.box(x + width - thickness, y, thickness, height, cloud).fix()
        seat = pge.box(x, y+height/2 -thickness/2, width, thickness, cloud).fix()
        leg = pge.box(x, y, thickness, height/2 - thickness/2, cloud).fix()
    else:
        back = pge.box(x,y, thickness, height, cloud).fix()
        seat = pge.box(x, y + height / 2, width, thickness, cloud).fix()
        leg = pge.box(x + width - thickness, y, thickness, height/2, cloud).fix()  
    #Define what happens on collisions 
    back.on_collision (delete_me)
    seat.on_collision (delete_me)
    leg.on_collision (delete_me)

def board(x,y):
    #Create a horizontal box for level creation
    width, height = 0.6, 0.05
    thickness = 0.05
    pge.box(x,y, width, height, orange).fix()

def net(x,y):
    #Create a thinner than board horizontal box for level creation (and testing)
    width, height = 1.0, 0.005
    thickness = 0.05
    pge.box(x,y, width, height, white).fix()

def display_score():
    global score, back, scoreboard
    
    #Create a blue box to act as the backing for a scoreboard
    back = pge.box(0.01, 0.9, 0.98, 1.0, blue).fix()
    
    #If a scoreboard has been made delete it
    if scoreboard != None:
        scoreboard.rm()
    
    #Create scoreboard containing the score written as white text on the top layer
    scoreboard = pge.text(0.01, 1.0, "Score:" + str(score), white, 100, 1)

def display_loading():
    global score, back, loading

    #Create a blue box to act as the backing for a scoreboard
    back = pge.box(0.01, 0.9, 0.98, 1.0, blue).fix()

    #If a loading sign has been made delete it
    if loading != None:
        loading.rm()

    #Create loading sign containing the score written as white text on the top layer
    loading = pge.text(0.65, 1.0, "Loading", white, 100, 1)

def display_fire():
    global score, back, loading

    #Create a blue box to act as the backing for a scoreboard
    back = pge.box(0.01, 0.9, 0.98, 1.0, blue).fix()

    #If a loading sign has been made delete it
    if loading != None:
        loading.rm()

    #Create loading sign containing the score written as white text on the top layer
    loading = pge.text(0.65, 1.0, "Shoot!!", white, 100, 1)

def randomise_gun():
    #Calls the chang gun function with a randomised value
    change_gunType(random.randrange(1,4))

def update_score(i):
    global score
    #Add the given variable to the score
    score += i

    #Redisplay the new score
    display_score()

def createLevel (e = None, f = None):
    global gun, setup
    # Create an alternating list of bubbles across the screen across three rows
    # Increments are done so that colours dont fall upon making three of them.
    setup = True
    for x in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.805]:
        place_bubble (x, gun.get_colour())
        increment_gun()        
    for x in [0.16, 0.27, 0.38, 0.49, 0.60, 0.72]:
        place_bubble (x+0.07, gun.get_colour())
        increment_gun()
    #Extra increments were made as without them created a 3 line combination
    increment_gun()    
    increment_gun()  
    for x in [0.25, 0.38, 0.50, 0.62, 0.75]:
        place_bubble (x, gun.get_colour())
        increment_gun()
    setup = False
    increment_gun()

def timer (e = None, f = None):
    global seconds_left, previous   
    #Check seconds_left is higher than 0
    if seconds_left >= 0:

        #recursivly call this function
        pge.at_time (1.0, timer)
        s = "%d" % seconds_left

        #destroy the previous implementation of 'previous'
        if previous != None:
            previous.rm ()

        #Set previous to new text value and decrement seconds_left
        previous = pge.text (0.8, 0.9, s, white, 100, 1)
        seconds_left -= 1

    #Once seconds_left reaches zero call 'out_of_time
    if seconds_left == 0:
        out_of_time()

def spin_gun():
    global bound
    #Make it so the gun is no longer restricted in its turning arc
    bound = False
    
    #Start spinning
    spin_callback()

def spin_callback(e = None, f = None):
    global gun, gun_angle, bound
    
    #Increment the angle of the gun
    gun_angle +=1
    
    #Output to the terminal to show changes
    print("called spin_callback, angle=", gun_angle)
    
    #Call this again recursivley
    pge.at_time (4.0 / 360.0, spin_callback)

    #Cap it using the modulus operator to stop the value getting too high
    # and so harder to read in the terminal
    gun_angle %=360
    
    #Rotate the gun based on it's new value relative to pi/180
    gun.rotate(gun_angle * math.pi / 180.0)

def out_of_time ():
    global score
    #Ouptut text showing the score
    pge.text (0.3, 0.7, "Score: " + str(score), white, 100, 1)
    
    #After 4 seconds finish the game
    pge.at_time (4.0, finish_game)

def place_gun():
    global gun, gun_angle, gun_type
    thickness = 0.02
    height = 0.1
    gun_angle = 180

    #Create a box with the given variables
    gun = pge.box(0.5, 0.03, thickness, height, cloud).fix()
    
    #Set the defaulted gun type to 1 (red)
    change_gunType(1)

def elastic_test(e = None, f = None):
    global gun

    # Place a net in the way to help further should the elasticity
    net(0.01, 0.01)

    #Fire three of one type then increment
    pge.at_time(0.5,fire_bubble_key)
    pge.at_time(1.5,fire_bubble_key)
    pge.at_time(2.5,fire_bubble_key)
    pge.at_time(2.6, increment_gun)

    #Fire three of one type then increment
    #pge.at_time(4.5,fire_bubble_key)
    #pge.at_time(5.5,fire_bubble_key)
    #pge.at_time(6.5,fire_bubble_key)    
    #pge.at_time(6.6, increment_gun)

    #Fire three of one type then increment
    #pge.at_time(10.5,fire_bubble_key)
    #pge.at_time(12.5,fire_bubble_key)
    #pge.at_time(14.5,fire_bubble_key)
   
def make_chairs():
    chair(0.1,0.1,0.05, 0.05, True)
    chair(0.2,0.2,0.05, 0.05, False) 
    chair(0.3,0.1,0.05, 0.05, True)
    chair(0.7,0.1,0.05, 0.05, True) 
    chair(0.8,0.2,0.05, 0.05, False) 
    chair(0.9,0.1,0.05, 0.05, True) 

def main ():
    global g, concrete, slowdown, seconds_left, gun

    n, e, s, w = placeBoarders (boarder, concrete)
    s.on_collision (delete_ball)
    n.on_collision (bubble_hits_bar)  
    print("before run")
    pge.gravity ()
    pge.dump_world ()
    pge.draw_collision (False, False)
    pge.slow_down (6.0)  # slows down real time by a factor of
    pge.fps (200)
    pge.display_set_mode ([800, 800])
    pge.register_handler (mouse_press, [MOUSEBUTTONDOWN])
    pge.register_handler (myquit, [QUIT])
    pge.register_handler (key_pressed, [KEYDOWN])
    
    display_score()
    display_fire()

    place_gun()
    
    make_chairs()

    #Decomment/comment to show testing for elastic as gravity test
    #elastic_test()

    #Decomment/comment to create level - make sure other tests are commented
    createLevel()

    #Decomment/comment to spin gun - make sure other tests/level creation
    #are commented
    #spin_gun()
    

    seconds_left = 10 * slowdown
    timer ()
    
    pge.run (simulatedtime)
    pge.run (10.0)
    pge.finish_record ()




print("before main()")
main ()
