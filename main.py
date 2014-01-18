from sys import exit
from random import randint
from time import sleep
import os
import time

def wipe():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


class NoCase(object):
    def __init__(self, s):
        self.__s = s.lower()
    def __hash__(self):
        return hash(self.__s)
    def __eq__(self, other):
        # ensure proper comparison between instances of this class
        try: other = other.__s
        except (TypeError, AttributeError):
          try: other = other.lower()
          except: pass
        return self.__s == other


class Engine(object): #This guy loops to play the game

    def __init__(self):
        self.room_map = map1
    
    def play(self):
        
        prompt = "\n> "
        current_room = self.room_map.opening_room()
        
        wipe()
        print "\n" * 100
        
        time.sleep(0.5)
        
        print "You awaken.\n"
        print "Your memory has been purged. All you have is your firmware."
        
        while True:
            
            current_room.discovered = True
            
            print "\n" + ("=" * 79) + "\n"
            
            if 'map' in player.sensors:
                print "CURRENT LOCATION: " + current_room.location + "\n"
            
            if 'cam_hd' in player.sensors:      #Print a room description based on what sensors
                current_room.desc_hd()          # the player has.
            elif 'cam_bw' in player.sensors:
                current_room.desc_bw()
            elif 'echo' in player.sensors:
                current_room.desc_echo()
            elif 'audio' in player.sensors:
                current_room.desc_audio()
            else:
                print "DEBUG: You have no sensory input."
            
            print ""
            
            self.playerstats()                                  #Calls the function to print player's stats
            
            action = raw_input(prompt).split(' ')               #Get input as a list of words
            
            keyword = self.parse(action)                        #Scan for list of keywords, return standardised keyword
            
            wipe()
            time.sleep(0.2)
            print "\n" * 100
            
            room_returned = current_room.act(keyword, action)   #Give the current room a keyword and action to see what happens
            
            self.checkcharge()
            
            if room_returned == "error":
                self.errortext(keyword, action)
            else:
                current_room = room_returned
    
    def playerstats(self): #Displays the player's current stats
    
        print "CHARGE LEVEL:  [" + ("#" * player.charge) + ("." * (player.chargemax - player.charge)) + "] " + str(player.charge) + "/" + str(player.chargemax)
        
        print "SENSORY INPUT: [",
        print player.sensors[0],
        for i in range(len(player.sensors) - 1):
            print "|",
            print player.sensors[i + 1],
        print "]"
        
        print "TOOLS ONLINE:  [",
        print player.tools[0],
        for i in range(len(player.tools) - 1):
            print "|",
            print player.tools[i + 1],
        print "]"
        
        if player.inventory:
            print "INVENTORY:     [",
            print player.inventory[0],
            for i in range(len(player.inventory) - 1):
                print "|",
                print player.inventory[i + 1],
            print "]"
        
        if player.memory:
            print "MEMORY BANK:   [",
            print player.memory[0],
            for i in range(len(player.memory) - 1):
                print "|",
                print player.memory[i + 1],
            print "]"
    
    def parse(self, parse_in): #Understands the first word in the player's command
        if parse_in[0] in ['go', 'walk', 'move', 'run', 'exit', 'leave', 'escape']:
            if parse_in[1] in ['door', 'exit']:
                return 'go_error'
            else:
                return 'go'
        elif parse_in[0] in ['use', 'press', 'push', 'activate', 'switch', 'charge', 'dock', 'connect', 'attach', 'interface']:
            return 'use'
        elif parse_in[0] in ['examine', 'inspect', 'observe', 'look', 'analyse']:
            return 'look'
        elif parse_in[0] in ['take', 'pick', 'get', 'carry', 'fit', 'acquire']:
            return 'get'
        elif parse_in[0] in ['drop', 'put', 'place']:
            return 'drop'
        elif parse_in[0] in ['talk', 'speak', 'ask', 'tell']:
            return 'talk'
        elif parse_in[0] in ['attack', 'kill', 'stab', 'kick', 'punch']:
            return 'attack'
        elif parse_in[0] == 'scan':
            return 'scan'
            
        elif parse_in[0] in ['die', 'suicide', 'exit', 'quit']: #Suicide command included in parser
            wipe()
            print "\nYour head a splode.\n" # since it only ever does one thing...
            time.sleep(1)
            exit(1)
        
        else:
            return 'error'
    
    def checkcharge(self): #Check whether the player has run out of charge
        if player.charge < 0:
            self.wipe()
            print "Your battery is completely discharged. With your final trickle of charge you"
            print "only wish you had planned your journey better."
            print "\nTIP: When your charge is half-depleted, it's time to think about whether you"
            print "have enough to get back to your nearest charger."+ ("\n"*4)
            exit(1)
    
    def errortext(self, keyword_in, action_in): #Show meaningful error text on wrong command
    
        if keyword_in == 'go':
            print "You can't go there."
        elif keyword_in == 'go_error':
            print "You'll have to specify a direction."
        elif keyword_in == 'use':
            print "You can't do that."
        elif keyword_in == 'look':
            print "You observe nothing of interest."
        elif keyword_in == 'get':
            print "You can't have that. It probably doesn't even exist."
        elif keyword_in == 'drop':
            print "You don't have one of those."
        elif keyword_in == 'talk':
            print "You try to establish communication, but there is no response."
        elif keyword_in == 'attack':
            print "Careful, now! You might damage yourself."
        elif keyword_in == 'scan' and action_in[1] in player.sensors:
            print "You scan the area with your '%s' scanner but observe nothing of relevance." % action_in[1]
        elif keyword_in == 'scan' and action_in[1] not in player.sensors:
            print "SCAN ERROR: '%s' is not a recognised peripheral" % action_in[1]
        else:
            print "DOES NOT COMPUTE"


class Player(object): #The player's stats and inventory live here
    def __init__(self):
        self.sensors = ['audio']
        self.tools = ['claw_arm']
        self.inventory = []
        self.memory = []
        self.chargemax = 10
        self.charge = 1


class Room(object):
    def __init__(self):
        self.discovered = False
        self.location = "UNCONFIGURED ROOM"
    
    def desc_audio(self):
        print "DEBUG: You hear nothing."
    
    def desc_echo(self):
        print "DEBUG: As far as your echolocation sensors can tell, this room is empty."
    
    def desc_bw(self):
        print "DEBUG: You see nothing but noisy darkness in this empty room."
    
    def desc_hd(self):
        print "DEBUG: You see nothing but perfect darkness in this empty room."
    
    def act(self, keyword_in, action_in):
        print "DEBUG: There's simply nothing to do in this room."
        exit(1)


class Room11(Room): #Starting room with bodies and laser gun (dark).
    def __init__(self):
        self.discovered = False
        self.location = "x: 1, y: 1"
        self.laser = True
    
    def desc_audio(self):
        if map1.room21.echo == True:
            print "Your tri-directional microphone array senses a high-pitched ticking sound, such"
            print "as might be made by an ultra-sonic proximity sensor, to the EAST of you."
        else:
            print "DEBUG: No audio here..."
    
    def desc_echo(self):
        print "Your echolocation array detects three long, sound-absorbing objects scattered"
        print "around the floor. The only exit is to the east."
    
    def desc_bw(self):
        if "light" in player.tools:
            print "Your light illuminates the room to reveal that the light fixtures are broken."
            print "There are what appear to be three people in white coats lying on the floor."
            if self.laser == True:
                print "There is some sort of pointed robot part on the ground near one of the people."
        else:
            print "The lights are out. You see only darkness. Your echolocation array detects three"
            print "long, sound-absorbing objects scattered around the floor."
    
    def desc_hd(self):
        if "light" in player.tools:
            print "Your light illuminates the room to reveal that the light fixtures are broken."
            print "From the way the broken light coverings are scorched and melted, it would appear"
            print "that they were damaged by a laser weapon. There are three dead bodies on the"
            print "floor wearing white coats, obviously wounded by a similar laser weapon."
            if self.laser == True:
                "There is a laser gun on the floor, suitable for attaching to a droid unit."
        else:
            print "The lights are out. You see only darkness. Your echolocation array detects three"
            print "long, sound-absorbing objects scattered around the floor."
    
    def act(self, keyword_in, action_in):
        if action_in == ['unholster', 'banana']:
            print "> unholster banana"
            print "George Kiltowitz readied his banana."
            action = raw_input('> ')
            if action == 'use banana':
                print "Use banana on what?"
                action = raw_input('> ')
                if action == 'wardrobe':
                    print "George Kiltowitz smeared banana on the wardrobe."
                    print "Portal to the monkey dimension opened!"
                    print "\nYou won the game!"
                    exit(1)
            return map1.room11
        
        elif keyword_in == "go" and "east" in action_in:
            print "You go through the open doorway to the EAST."
            player.charge -= 1
            return map1.room21
            
        elif keyword_in == 'look':
            if not 'echo' in player.sensors:
                print "You can't look at anything right now. You're blind."
                return map1.room11
            elif 'laser' in action_in or 'gun' in action_in or 'part' in action_in:
                if ('cam_bw' in player.sensors or 'cam_hd' in player.sensors) and 'light' in player.tools:
                    print "This appears to be a LASER GUN attachment suitable for fitting to a droid unit."
                else:
                    print "How did you know that was there!? Cheater!"
                return map1.room11
            elif 'bodies' in action_in or 'objects' in action_in or 'people' in action_in or 'humans' in action_in:
                if 'cam_hd' in player.sensors:
                    print "These people appear to have been killed by laser blasts to their chests and"
                    print "abdominal areas."
                elif 'cam_bw' in player.sensors:
                    print "Closer inspection shows that these people are probably dead, with large, dark"
                    print "scorch marks on their torsos."
                else:
                    print "These unknown objects are about 1.5 to 1.8 metres long and a bit soft to the"
                    print "touch."
                return map1.room11
            
        elif keyword_in == 'get':
            if ('laser' in action_in or 'gun' in action_in or 'part' in action_in):
                if 'laser_gun' in player.tools:
                    print "You already got that."
                else:
                    print "You pick up the robot part from the floor and attach it to yourself. It seems to"
                    print "be a fully functioning laser weapon and is working fine."
                    player.tools.append('laser_gun')
                return map1.room11
        
        return "error"


class Room12(Room): #Corridor North to East
    def __init__(self):
        self.discovered = False
        self.location = "x: 1, y: 2"
    
    def desc_echo(self):
        print "You are in an empty corridor, open to the north and east."
    
    def desc_bw(self):
        print "You are in an empty corridor, open to the north and east."
    
    def desc_hd(self):
        print "You are in an empty corridor, open to the north and east."
    
    def act(self, keyword_in, action_in):
        
        if keyword_in == 'go':
            if 'north' in action_in:
                print "You go along the corridor to the north."
                player.charge -= 1
                return map1.room13
            elif 'east' in action_in:
                print "You go along the corridor to the east."
                player.charge -= 1
                return map1.room22
        else:
            return 'error'


class Room13(Room): #Corridor north-south with east door
    def __init__(self):
        self.discovered = False
        self.location = "x: 1, y: 3"
    
    def desc_echo(self):
        print "You are in an empty corridor, open to the north and south, with a door to the\neast."
    
    def desc_bw(self):
        print "You are in an empty corridor, open to the north and south, with a door to the\neast."
    
    def desc_hd(self):
        print "You are in an empty corridor, open to the north and south, with a door to the\neast."
    
    def act(self, keyword_in, action_in):
        
        if keyword_in == 'go':
            if 'north' in action_in:
                print "You go along the corridor to the north."
                player.charge -= 1
                return map1.room14
            elif 'south' in action_in:
                print "You go along the corridor to the south."
                player.charge -= 1
                return map1.room12
            elif 'east' in action_in:
                print "You go through the door to the east."
                player.charge -= 1
                return map1.room23
        else:
            return 'error'


class Room21(Room): #Second room with echolocation, laser cutter and charger.
    def __init__(self):
        self.discovered = False
        self.location = "x: 2, y: 1"
        self.echo = True
        self.laser_cutter = True
    
    def desc_audio(self):
        if map1.room21.echo == True:
            print "You clearly identify the location of the DEVICE producing the ticking sound."
            print "Maybe you could go and get it or take a closer look."
        else:
            print "DEBUG: You hear nothing."
    
    def desc_echo(self):
        print "You are in a large room, with a long worktop along the east wall, from which"
        print "you previously acquired your echolocation sensor. In the corner of the room is"
        print "a 40 cm high, roughly cube-shaped object. To the west and the north are"
        print "openings the size of average doorways."
    
    def desc_bw(self):
        print "You are in a large room, with a long worktop along the east wall, from which"
        print "you previously acquired your echolocation sensor. In the corner of the room"
        print "you see what looks like some kind of charging unit. To the west and north are"
        print "two open doorways."
    
    def desc_hd(self):
        print "You are in a large room, with a long worktop along the east wall, from which"
        print "you previously acquired your echolocation sensor. In the corner of the room"
        print "there is a powered DRIOD-EX charging unit. To the west and north are two open"
        print "doorways."
        if map1.room21.laser_cutter == True:
            print "There is a small laser cutter tool on the worktop which you could have easily"
            print "missed before, since it blends in with the pattern on the worktop."
        else:
            print ""
    
    def act(self, keyword_in, action_in):
    
        if keyword_in == 'go':
            if 'west' in action_in:
                print "You go through the open doorway to the west."
                player.charge -= 1
                return map1.room11
            elif 'north' in action_in:
                print "You go through the open doorway to the north."
                player.charge -= 1
                return map1.room22
        
        elif keyword_in == 'look':
            if 'object' in action_in or 'charger' in action_in or 'unit' in action_in or 'cube' in action_in:
                if 'cam_hd' in player.sensors:
                    print "It is a high-speed DROID-EX charging unit, according to the label, and has a"
                    print "charging port half-way up its front side. The status display indicates that it"
                    print "is powered and ready to charge any docked droid unit."
                elif 'cam_bw' in player.sensors:
                    print "It is a 40 cm high unit with what looks like a charging port about half-way up"
                    print "its front side. It has a small display which is un-readable with this fuzzy"
                    print "camera, but appears to be illuminated. That's good, right?"
                elif 'echo' in player.sensors:
                    print "It's a 40 cm high, roughly cube-shaped object. Closer inspection reveals some"
                    print "kind of protrusion half-way up its front side with metallic contacts. As your"
                    print "claw touches the contacts, you hear a spark buzz through your claw. It looks"
                    print "like these contacts are live - could this be used for charging your battery?"
                return map1.room21
            elif 'worktop' in action_in:
                if 'cam_hd' in player.sensors:
                    print "The worktop spans the entire east wall.",
                    if map1.room21.laser_cutter == True:
                        print "At one end, there rests a small laser"
                        print "cutter device."
                elif 'cam_bw' in player.sensors:
                    print "The worktop spans the entire east wall."
                    if map1.room21.laser_cutter == True:
                        print "There is something on it but with this"
                        print "fuzzy camera it is impossible to tell what it is."
                elif 'echo' in player.sensors:
                    print "The worktop spans the entire east wall."
                return map1.room21
            elif ('laser' in action_in or 'device' in action_in or 'cutter' in action_in or 'tool' in action_in) and map1.room21.echo == False and map1.room21.laser_cutter == True and 'cam_hd' in player.sensors:
                print "The laser cutter device looks fit for attaching to your one of your peripheral"
                print "sockets."
                return map1.room21
            elif 'device' in action_in and map1.room21.echo == True:
                print "You inspect the DEVICE by prodding and gripping it with your claw, and"
                print "determine that it must be an echolocation peripheral device, suitable for"
                print "fitting to your own peripheral connectors."
                return map1.room21
        
        elif keyword_in == 'use':
            if 'object' in action_in or 'charger' in action_in or 'unit' in action_in or 'cube' in action_in or 'battery' in action_in or 'contacts' in action_in:
                print "You reverse up to the unit and engage your charging port with it. Within a few"
                print "minutes your battery is fully charged to %d units." % player.chargemax
                player.charge = player.chargemax
                return map1.room21
        
        elif keyword_in == 'get':
            if ('laser' in action_in or 'device' in action_in) and map1.room21.echo == False and map1.room21.laser_cutter == True and 'cam_hd' in player.sensors:
                print "You pick up the laser cutter and fit it to one of your peripheral sockets."
                player.tools.append('laser_cutter')
                map1.room21.laser_cutter = False
                return map1.room21
            elif ('device' in action_in) and map1.room21.echo == True:
                print "You pull the DEVICE from what is probably a test stand. As its cable falls"
                print "loose it stops ticking. The connector appears to be compatible with your"
                print "peripheral connectors, so you plug it into one of your top connectors."
                print "As the echolocation module comes online, it gives you a fairly good idea of"
                print "your surroundings, in terms of rough, colourless shapes."
                player.sensors.append('echo')
                map1.room21.echo = False
                print "You become aware of the fact that the voltage from your battery pack is"
                print "starting to slowly decline. You will not have enough charge to leave this room."
                print "\nTUTORIAL: There will be no more capitalised keywords from now on! You can be"
                print "quite flexible with your commands. Try typing what feels natural. If that"
                print "doesn't work, think of something more robotic sounding!"
                return map1.room21
        
        return 'error'


class Room22(Room): #Corridor going east-west with south door.
    def __init__(self):
        self.discovered = False
        self.location = "x: 2, y: 2"
    
    def desc_echo(self):
        print "You are in an empty corridor, open to the east and west, with an open door to"
        print "the south."
    
    def desc_bw(self):
        print "You are in an empty corridor, open to the east and west, with an open door to"
        print "the south."
    
    def desc_hd(self):
        print "You are in an empty corridor, open to the east and west, with an open door to"
        print "the south."
    
    def act(self, keyword_in, action_in):
        
        if keyword_in == 'go':
            if 'west' in action_in:
                print "You go along the corridor to the west."
                player.charge -= 1
                return map1.room12        
            elif 'east' in action_in:
                print "You go along the corridor to the east."
                player.charge -= 1
                return map1.room32            
            elif 'south' in action_in or 'door' in action_in:
                print "You go through the door to the south."
                player.charge -= 1
                return map1.room21

        return "error"


class Room23(Room): #Greyscale camera room
    def __init__(self):
        self.discovered = False
        self.location = "x: 2, y: 3"
        self.cam_on_floor = True
    
    def desc_echo(self):
        print "You are in an empty room with a metallic object on the floor in one corner,"
        print "with an open doorway to the west."
    
    def desc_bw(self):
        print "You are in an empty room with an open doorway to the west."
        
    def desc_hd(self):
        print "You are in an empty room. The marks on the floor and walls suggest that this"
        print "might have had some office furniture in it at one time, but that it was"
        print "emptied out."
    
    def act(self, keyword_in, action_in):
        if keyword_in == 'go' and 'west' in action_in:
            print "You exit through the door to the west."
            player.charge -= 1
            return map1.room13
        
        elif keyword_in == 'look':
            if 'object' in action_in or 'camera' in action_in:
                print "This appears to be a damaged camera of some sort. You should be able to fit it"
                print "to your peripheral connectors."
                return map1.room23
        
        elif keyword_in == 'get':
            if 'object' in action_in or 'camera' in action_in:
                print "After a bit of tweaking, you are able to fit the camera and activate it."
                print "It appears to be a black and white camera and the damage means that the image"
                print "is quite grainy, but this is much better than having no visual input at all!"
                player.sensors.append('cam_bw')
                return map1.room23
                
        return 'error'


class Room31(Room): #Security console room.
    def __init__(self):
        self.discovered = False
        self.location = "x: 3, y: 1"
        self.door_open = False
    
    def desc_echo(self):
        print "Half of this room is dominated by what appears to be a huge console surrounding"
        print "a single seat. If this is indeed a console, you should be able to interface"
        print "with it. The only way out is back through the door to the north."
    
    def desc_bw(self):
        print "Half of this room is dominated by what appears to be a security console, which"
        print "looks to be functioning by the way the monitors are active. There is a single"
        print "seat in the middle where a security-guard type probably used to sit. You should"
        print "be able to interface with this console. The only way out is back through the"
        print "door to the north."
    
    def desc_hd(self):
        print "Half of this room is dominated by a huge security console, with monitors"
        print "showing a few different office rooms. There is a single, worn seat where a"
        print "security-guard type probably used to sit. You should be able to interface with"
        print "this console. The only way out is back through the door to the north."
    
    def act(self, keyword_in, action_in):
    
        if keyword_in == 'go' and 'north' in action_in:
            print "You exit through the door to the north."
            player.charge -= 1
            return map1.room32
        
        elif keyword_in == 'look':
            if 'console' in action_in or 'monitors' in action_in:
                if 'cam_hd' in player.sensors or 'cam_bw' in player.sensors:
                    print "This console appears to be active. You should be able to interface with it."
                else:
                    print "From the whirring sound it is making, this console appears to be active."
                    print "Maybe you can interface with it."
                return map1.room31
                
        elif keyword_in == 'use':
            if 'console' in action_in:
                print "You successfully interface with the console and are able to see the video feeds"
                print "from the security camera of each room in the building. One of the rooms, with"
                print "the designation \"2,3\", appears to be missing its camera. You are able to"
                print "access the last seconds of the camera's recorded surveillance, showing it being"
                print "broken from the wall by an unseen force.",
                if map1.room23.cam_on_floor == True: #For goodness' sake don't forget to add this to room 23...
                    print "The room's other camera shows this\nfirst camera lying on the floor."
                if not 'map' in player.sensors:
                    print "\nYou downloaded the room location software from the console and can now keep"
                    print "track of which room you're in by its coordinates!"
                    player.sensors.append('map')
                return map1.room31
        
        return 'error'


class Room32(Room): #Corridor with north & sound doors, open west.
    def __init__(self):
        self.discovered = False
        self.location = "x: 3, y: 2"
    
    def desc_echo(self):
        print "You are in an empty corridor, open to the west, with an open door to the north."
        print "There is a shallow recess in the east wall in the shape of a closed door."
        if map1.room31.door_open == False:
            print "There is a shallow recess in the south wall in the shape of a closed door."
        else:
            print "The door to the south is open."
    
    def desc_bw(self):
        print "You are in an empty corridor, open to the west, with an open door to the north."
        print "There is a closed door to the east with what looks like a key-card reader"
        print "beside it. You won't be able to get through here without the right key-card."
        if map1.room31.door_open == False:
            print "There is a closed, bulky-looking metal door to the south."
        else:
            print "The door to the south is open."
    
    def desc_hd(self):
        print "You are in an empty corridor, open to the west, with an open door to the north."
        if map1.room31.door_open == False:
            print "There is a closed, very secure-looking metal door to the south."
        else:
            print "The heavy door to the south is open."
    
    def act(self, keyword_in, action_in):
        
        if keyword_in == 'go':
            if 'west' in action_in:
                print "You go along the corridor to the west."
                player.charge -= 1
                return map1.room22
            elif 'east' in action_in:
                if 'key_32' in player.inventory:
                    print "You swipe the key card to open the east door and proceed through it."
                    player.charge -= 1
                    return map1.room42
                else:
                    print "This door needs a key card."
                    return map1.room32
            elif 'north' in action_in:
                print "You go through the open door to the north."
                player.charge -= 1
                return map1.room33
            elif 'south' in action_in:
                if map1.room31.door_open == True:
                   print "You go through the open door to the south."
                   player.charge -= 1
                   return map1.room31
                else:
                    print "That door is locked closed."
                    return map1.room32
        
        elif keyword_in == 'look' and 'door' in action_in:
            if map1.room31.door_open == False:
                print "The south door is tightly shut. It doesn't look like you can open it"
                print "without releasing its locks from elsewhere."
                return map1.room32
            else:
                print "The door to the south is open."
                return map1.room32
        
        return 'error'


class Room33(Room): #Office with computer.
    def __init__(self):
        self.discovered = False
        self.location = 'x: 3, y: 3'
    
    def desc_echo(self):
        print "You are in a small room with various items of furniture inside. There is a desk"
        print "along one wall with a chair at it. It sounds like there is a machine or computer"
        print "at the desk. The only way out is back through the door to the south."
    
    def desc_bw(self):
        print "You are in a small room with various filing cabinets along one wall, a couple"
        print "of sets of drawers at another, and a computer desk with a chair. It looks like"
        print "the computer is switched on. The only way out is back through the door to the"
        print "south."
    
    def desc_hd(self):
        print "You are in a small room with various filing cabinets along one wall, a couple"
        print "of sets of drawers at another, and a computer desk with a chair. It looks like"
        print "the computer is switched on. The only way out is back through the door to the"
        print "south."
    
    def act(self, keyword_in, action_in):
        if keyword_in == 'go' and 'south':
            print "You exit through the door to the south."
            player.charge -= 1
            return map1.room32
        
        elif keyword_in == 'look':
            if 'computer' in action_in or 'machine' in action_in or 'desk' in action_in:
                print "The computer here is switched on and whirring. You should be able to interface"
                print "with it."
            elif 'cabinets' in action_in or 'cabinate' in action_in:
                print "The filing cabinets are poorly labelled. Upon closer inspection they appear to"
                print "be empty."
            elif 'drawers' in action_in or 'draw' in action_in:
                print "These drawers are empty. Kudos for being curious though!"
            return map1.room33
        
        elif keyword_in == 'use':
            if ('computer' in action_in or 'machine' in action_in) and map1.room31.door_open == False:
                print "You interface with the computer and click the \"OPEN SURVEILLANCE ROOM DOOR\""
                print "button on the desktop, and you hear the door open outside. Aren't you the best"
                print "little hacker? :D"
                map1.room31.door_open = True
            elif ('computer' in action_in or 'machine' in action_in) and map1.room31.door_open == True:
                print "You already checked this computer for clues and opened that door, remember?"
            return map1.room33
        
        return 'error'


class Map(object):
    def __init__(self):
        self.room11 = Room11()
        self.room12 = Room12()
        self.room13 = Room13()
        self.room21 = Room21()
        self.room22 = Room22()
        self.room23 = Room23()
        self.room31 = Room31()
        self.room32 = Room32()
        self.room33 = Room33()
        #and so on...
    
    def opening_room(self):
        return self.room11

player = Player()
map1 = Map()
engine = Engine()

def play(option):

    if option == 1:
        wipe()
        print "BOOT",
        time.sleep(1)
        print "\b.",
        time.sleep(1)
        print "\b.",
        time.sleep(1)
        print "\b."
        time.sleep(1.5)
        print "DROID_EX02 ONLINE"
        time.sleep(2)
        print "\nSystem diagnostic:"
        time.sleep(1)
        print "    CPU:                  OKAY"
        time.sleep(0.2)
        print "    memory:               OKAY"
        time.sleep(0.2)
        print "    firmware:             OKAY"
        time.sleep(0.4)
        print "    non-volotile storage: ERROR - REQUIRES FORMATTING"
        time.sleep(2)
        print "\nPeripheral diagnostic:"
        time.sleep(1)
        print "    audio_in_mic:         OKAY"
        time.sleep(0.2)
        print "    echolocation:         ERROR - PERIPHERAL WAS UNSAFELY REMOVED"
        time.sleep(0.1)
        print "    video_in_hd_cam:      ERROR - PERIPHERAL WAS UNSAFELY REMOVED"
        time.sleep(0.2)
        print "    em_wideband_sensor:   ERROR - PERIPHERAL WAS UNSAFELY REMOVED"
        time.sleep(0.1)
        print "    location_module:      ERROR - PERIPHERAL WAS UNSAFELY REMOVED"
        time.sleep(0.1)
        print "    arm_claw_unit:        OKAY"
        time.sleep(0.2)
        print "    battery_10Ah:         ERROR - PERIPHERAL WAS UNSAFELY REMOVED"
        time.sleep(5)
        print "\n=== Initiate A.I. ==="
        time.sleep(3)
        wipe()
        
        engine.play()
        
    elif option == 2:
        engine.play()
