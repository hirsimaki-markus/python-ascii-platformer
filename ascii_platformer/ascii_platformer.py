"""simple platformer"""

import os
import time
import msvcrt
import random

class Creature:
    """defines Creature to be used in two dimensional list based board. NAME ARGUMENT SHOULD ALWAYS BE SAME AS VARIABLE NAME"""
    instance_reg = {} # keep track of all instace names, locations and icons for printing

    def __init__(self, name, icon, pos):
        self.name = name
        self.pos = pos
        self.icon = icon
        __class__.instance_reg[name] = self # add instance to dictionary with name


    def move(self, direction):
        """Moves Creature in specified direction by one step on 2d grid. physics dont apply. also flaps wings by chaging icon when moving"""
        if direction == None:
            return
        elif direction == "right": # right
            self.pos[1] += 1
        elif direction == "left": # left
            self.pos[1] -= 1
        elif direction == "up": # up
            self.pos[0] -= 1
        elif direction == "down": # down
            self.pos[0] += 1
        elif direction == "rUp":
            self.pos[1] += 1
            self.pos[0] -= 1
        elif direction == "lUp":
            self.pos[1] -= 1
            self.pos[0] -= 1
        elif direction == "rDown":
            self.pos[1] += 1
            self.pos[0] += 1
        elif direction == "lDown":
            self.pos[1] -= 1
            self.pos[0] += 1

    def get_tile(self, direction, board):
        """returns nieghbouring tile in given direction"""
        if direction == "right": # right
            tile = board[self.pos[0]][self.pos[1]+1]
            return tile
        elif direction == "left": # left
            tile = board[self.pos[0]][self.pos[1]-1]
            return tile
        elif direction == "up": # up
            tile = board[self.pos[0]-1][self.pos[1]]
            return tile
        elif direction == "down": # down
            tile = board[self.pos[0]+1][self.pos[1]]
            return tile
        elif direction == "rUp": # right and up
            tile = board[self.pos[0]-1][self.pos[1]+1]
            return tile
        elif direction == "lUp": # left and up
            tile = board[self.pos[0]-1][self.pos[1]-1]
            return tile
        elif direction == "rDown": # right and down
            tile = board[self.pos[0]+1][self.pos[1]+1]
            return tile
        elif direction == "lDown": # left and down
            tile = board[self.pos[0]+1][self.pos[1]-1]
            return tile
        else:
            raise DirectionError("Invalid direction. Use: right, left, up, down, rUp, lUp, rDown, lDown")

    def fly_ai(self, pos, board):
        """returns random direction that has air block. buzzes around like fly."""
        directions = ["up", "down", "left", "right", "rUp", "lUp", "rDown", "lDown"]
        random.shuffle(directions)
        for direction in directions:
            if self.get_tile(direction, board) == " ":
                return direction

    def spider_ai(self, pos, board):
        """returns direction that allows spider to walk on walls"""
        pass

    def death_check(self, instance_reg):
        """returns true if bullet has hit a fly. the register is the one that position is checked agai"""
        for key in instance_reg:
            if self.pos == instance_reg[key].pos:
                return True
        return False


class Player:
    """defines player and its attributes"""

    instance_reg = {} # keep track of all instace names, locations and icons for printing

    def __init__(self, icon="P", pos=[0,0], fall=True, jumps=0, dashes=0, name="player"): # self.fall is true if player should fall. jumping function itself however excludes that
        self.pos = pos
        self.icon = icon
        self.fall = fall
        self.jumps = jumps
        self.dashes = dashes
        self.name = name
        __class__.instance_reg[name] = self # add instance to dictionary with name

    def get_tile(self, direction, board):
        """returns nieghbouring tile in given direction"""
        if direction == "right": # right
            tile = board[self.pos[0]][self.pos[1]+1]
            return tile
        elif direction == "left": # left
            tile = board[self.pos[0]][self.pos[1]-1]
            return tile
        elif direction == "up": # up
            tile = board[self.pos[0]-1][self.pos[1]]
            return tile
        elif direction == "down": # down
            tile = board[self.pos[0]+1][self.pos[1]]
            return tile
        elif direction == "rUp": # right and up
            tile = board[self.pos[0]-1][self.pos[1]+1]
            return tile
        elif direction == "lUp": # left and up
            tile = board[self.pos[0]-1][self.pos[1]-1]
            return tile
        elif direction == "rDown": # right and down
            tile = board[self.pos[0]+1][self.pos[1]+1]
            return tile
        elif direction == "lDown": # left and down
            tile = board[self.pos[0]+1][self.pos[1]-1]
            return tile
        else:
            raise DirectionError("Invalid direction. Use: right, left, up, down, rUp, lUp, rDown, lDown")

    def move(self, control, board):
        """NOT TO BE CONFUSED WITH MOVE METHOD OF CREATURE. PHYSICS APPLY ON PLAYER
        updates players location by one tile and updates necessary flags
        Moves Creature in specified direction by one step on 2d grid
        """

        # WARNING! SPAGETHI AHEAD!

        # DROP PLAYER IF FALLING AND NOT JUMPING
        if self.fall == True and self.jumps == 0 and self.get_tile("down", board) == " ":
            self.pos[0] += 1

        # UPDATE JUMP, DASH AND FALLING FLAGS
        if control == "up" and self.fall == False and self.jumps == 0: # control up: jumps to 5 if not falling and not jumping
            self.jumps = 5
        if self.jumps != 0 and self.dashes == 0: # control left/right: dashes to 5 if jumping up and not already dashing
            if control == "left": self.dashes = -5
            if control == "right": self.dashes = 5
        if self.get_tile("down", board) == " ": # update falling flag. if ground is hit dashes drop to 0
            self.fall = True
        else:
            self.fall = False 
            self.dashes = 0

        # JUMP PLAYER
        if self.jumps > 0 and self.get_tile("up", board) == " ": # disregard falling flag. move up if jumps left and no air in way
            self.pos[0] -= 1
            self.jumps -= 1
        else:
            self.jumps = 0

        # MOVE LEFT/RIGHT
        if control == "right" and self.get_tile("right", board) == " ": # control right: move right if no air in way
            self.pos[1] += 1
        elif control == "left" and self.get_tile("left", board) == " ": # control left: move left if no air in way
            self.pos[1] -= 1

        # ALLOW CHAGING DASH DIRECTION MID AIR
        if self.dashes > 0 and control == "left": # dashing right, changing left
            self.dashes = -(self.dashes)
        if self.dashes < 0 and control == "right": # dashing left, chaging right
            self.dashes = -(self.dashes)

        # DASH PLAYER
        if self.dashes > 0 and self.get_tile("right", board) == " ":
            self.pos[1] += 1
            self.dashes -= 1
        if self.dashes < 0 and self.get_tile("left", board) == " ":
            self.pos[1] -= 1
            self.dashes += 1


    def death_check(self, instance_reg):
        """returns true if player has hit a fly"""
        for key in instance_reg:
            if self.pos == instance_reg[key].pos:
                return True
        return False




class Projectile:
    """class to hold all projectiles eg ammo"""

    instance_reg = {} # keep track of all instaces. Projectile register has no size limit but fire functions limits it to 1000 (000-999)

    def __init__(self, name, icon, pos, direction):
        self.pos = pos
        self.icon = icon
        self.name = name
        self.direction = direction
        __class__.instance_reg[name] = self # add instance to dictionary with name

    @classmethod # THIS ONLY DELETES ITEM FROM CLASS REGISTRY (allowing over writing) . NOT FROM MEMORY
    def delete(cls, name):
        del cls.instance_reg[name]

    @classmethod
    def move_all(cls, board):
        """moves all projectiles by one tick"""
        to_remove = []
        for key in cls.instance_reg:
            if cls.instance_reg[key].move(board) == False: # cls.instance_reg[key] calls the actual object without its name in main!!!
                to_remove.append(key)

        for key in to_remove:
            cls.delete(key) # NOT ACUTAL PYTHON DELETE BUT CLASS METHOD!!!


    @classmethod
    def fire(cls, control, icon, pos):
        """dynamically creates projectile object"""
        if control in "wazedx":
            if cls.instance_reg == {}:
                bullet_num = "0"
            else:
                list = []
                for key in cls.instance_reg:
                    list.append(int(key.strip("bullet"))) # strip numbers as in and sort
                list.sort()
                bullet_num = list[-1]+1

            if control == "w": direction = "lUp"
            elif control == "a": direction = "left"
            elif control == "z": direction = "lDown"
            elif control == "e": direction = "rUp"
            elif control == "d": direction = "right"
            elif control == "x": direction = "rDown"

            formatted = """bullet{} = Projectile("bullet{}", "{}", {}[:], "{}")""".format(bullet_num, bullet_num, icon, pos ,direction)
            exec(formatted) # forgive me



    def get_tile(self, direction, board):
        """returns nieghbouring tile in given direction"""
        if direction == None:
            return
        elif direction == "right": # right
            tile = board[self.pos[0]][self.pos[1]+1]
            return tile
        elif direction == "left": # left
            tile = board[self.pos[0]][self.pos[1]-1]
            return tile
        elif direction == "up": # up
            tile = board[self.pos[0]-1][self.pos[1]]
            return tile
        elif direction == "down": # down
            tile = board[self.pos[0]+1][self.pos[1]]
            return tile
        elif direction == "rUp": # right and up
            tile = board[self.pos[0]-1][self.pos[1]+1]
            return tile
        elif direction == "lUp": # left and up
            tile = board[self.pos[0]-1][self.pos[1]-1]
            return tile
        elif direction == "rDown": # right and down
            tile = board[self.pos[0]+1][self.pos[1]+1]
            return tile
        elif direction == "lDown": # left and down
            tile = board[self.pos[0]+1][self.pos[1]-1]
            return tile
        else:
            raise DirectionError("Invalid direction. Use: right, left, up, down, rUp, lUp, rDown, lDown")

    def move(self, board):
        """moves projectile by one tick, returns false if move fails and object should be removed."""
        direction = self.direction
        if self.get_tile(direction, board) == " ": # check if empty space
            if direction == None:
                return
            elif direction == "right": # right
                self.pos[1] += 1
            elif direction == "left": # left
                self.pos[1] -= 1
            elif direction == "up": # up
                self.pos[0] -= 1
            elif direction == "down": # down
                self.pos[0] += 1
            elif direction == "rUp":
                self.pos[1] += 1
                self.pos[0] -= 1
            elif direction == "lUp":
                self.pos[1] -= 1
                self.pos[0] -= 1
            elif direction == "rDown":
                self.pos[1] += 1
                self.pos[0] += 1
            elif direction == "lDown":
                self.pos[1] -= 1
                self.pos[0] += 1
        else:
            return False


def move_pending():
    """returns true/false if keyboard hit is pending in msvcrt buffer"""
    return msvcrt.kbhit()


def get_key():
    """get key. handles arrowkeys and most printable characters and enter"""
    key = msvcrt.getch()
    if ord(key) == 224: # arrow key escape code
        direction = ord(msvcrt.getch()) # actual key is read automatically as arrow keys return 2 values
        if direction == 72: return "up"
        elif direction == 75: return "left"
        elif direction == 77: return "right"
        elif direction == 80: return "down"
    elif chr(ord(key)) == "\r":
        return "enter"
    else:
        return chr(ord(key))


def load_level(level_name):
    """returns level data in 2d-list"""

    # === LEVEL DATA BLOCK START ===
    level_1_data = """
    ██████████████████████████████████████████████████
    █                                                █
    █                                                █
    █                                                █
    █                                                █
    █                                                █
    █                                                █
    █                                                █
    █                                                █
    █                                                █
    █                 █████                          █
    █                 █████                          █
    █                 █████                          █
    █           ███   █████                          █
    █                 █████                          █
    █                                                █
    █        █                                       █
    █                                                █
    █                                                █
    █                                                █
    █        █                                       █
    █                                                █
    █                                                █
    █                                                █
    ████████████                                     █
    █          ██                                    █
    █           █                                    █
    █             █                                  █
    █             ██                                 █
    █              ██                                █
    █            █  ██                               █
    █                ██                              █
    █                 ██                             █
    █                  ██                            █
    █            █      ██                           █
    █                    ██                          █
    █                     ██                         █
    █                      ██                        █
    █            █          ██                       █
    █                        ██                      █
    █                         ██                     █
    █                          ██                    █
    █            █              ██                   █
    █                            ██                  █
    █                             ██                 █
    █                                                █
    █            █                                   █
    █                              ███████████████████
    ██████████████                                   █
    █                                                █
    ██████████████████████████████████████████████████"""
    # === LEVEL DATA BLOCK END ===

    level_dict = {"level_1" : level_1_data}

    raw_data = level_dict[level_name] # fetch raw data of level chosen

    level = []
    for row in (raw_data.split("\n")[1:]): # convert to list. [1:] to allow newline at the start of level data
        row_tiles = []
        for tile in row[4:]: # convert to 2d list. [4:] to allow normal identation (strips 4 spaces)
            row_tiles.append(tile)
        level.append(row_tiles)

    return level


def clear_screen():
    """clear command line"""
    _ = os.system("cls") # use _ to catch return value 0 so its not printed to console


def print_level(board, data):
    """clears screen and prints board with player on it"""
    board_copy = [_[:] for _ in board] # temp copy to edit for printing

    for item in data:
        board_copy[item[0][0]][item[0][1]] = item[1]

    printable = "\n" # prepare printin before cleaning screen
    for row in board_copy:
        printable += (" "+"".join(row)+"\n")
    clear_screen()
    print(printable)


def parse_print_data(class_list):
    """takes list of classes containing name registers  and parses their instances to 
    return list of the following type:
    [[fly2.pos, fly2.icon], [player.pos, player.icon], ... ]
    to be used for printing board
    """
    print_list = []
    for class_ in class_list:
        for key in class_.instance_reg:
                print_list.append([class_.instance_reg[key].pos, class_.instance_reg[key].icon])
    return print_list



def debug_menu(show,):
    """prints debug menu if argument is true"""


def main():


    player = Player("¥", [45,45], name="player") # initialize player first so location is first item in Creature.pos_reg

    fly0 = Creature("fly0", "*", [27,27])
    fly1 = Creature("fly1", "*", [5,2])
    fly2 = Creature("fly2", "*", [5,2])
    fly3 = Creature("fly3", "*", [22,27])
    fly4 = Creature("fly4", "*", [6,7])
    fly5 = Creature("fly5", "*", [8,8])

    board = load_level("level_1")

    while True:
        control = get_key().lower()

        if control in "wazedx":
            Projectile.fire(control, "°", player.pos) # control is direction for bullet
        if control == "s":
            Projectile.fire("w", "°", player.pos)
            Projectile.fire("e", "°", player.pos)
            Projectile.fire("a", "°", player.pos)
            Projectile.fire("d", "°", player.pos)
            Projectile.fire("z", "°", player.pos)
            Projectile.fire("x", "°", player.pos)




        while not move_pending():

            # "small" debug "menu" start
            if control == "q": quit() # exit route
            if control == "r":
                try:
                    exec(input("\n  direct inject to main loop: "))
                    input("  enter to continue")
                except:
                    print("  ERROR HAPPENED. COMMAND NOT COMPLETED")
                    input("  enter to continue")
            # print("\n"*3,"     --- DEBUG ---\n\n")
            # print("  player")
            # print()
            # print("  │")
            # print("  ├─ player.pos:", player.pos)
            # print("  │")
            # print("  ├─ player.get_tile(up):", player.get_tile("up", board))
            # print("  │")
            # print("  ├─ player.fall:", player.fall)
            # print("  │")
            # print("  ├─ player.jumps:", player.jumps)
            # print("  │")
            # print("  └─ player.dashes:", player.dashes)
            # print("\n"*2)
            # print("  instances")
            # print()
            # print("  │")
            # print("  ├─ Creature.instance_reg:", Creature.instance_reg)
            # print("  │")
            # print("  ├─ Player.instance_reg:", Player.instance_reg)
            # print("  │")
            # print("  └─ Projectile.instance_reg:", Projectile.instance_reg)
            print("\n")
            print("  move - arrows")
            print("  fire - weadzx")
            print("  run  - r")
            print("  quit - q")

            time.sleep(0.04)

            fly5.move(fly5.fly_ai(fly5, board))
            fly4.move(fly4.fly_ai(fly4, board))
            fly3.move(fly3.fly_ai(fly3, board))
            fly2.move(fly2.fly_ai(fly2, board))
            fly1.move(fly1.fly_ai(fly1, board))
            fly0.move(fly0.fly_ai(fly0, board))

            Projectile.move_all(board)
            player.move(control, board)

            print_level(board, parse_print_data([Creature, Player, Projectile]))

            if player.death_check(Creature.instance_reg) == True: exit()

            dead_list = []
            for creature in Creature.instance_reg:
                if Creature.instance_reg[creature].death_check(Projectile.instance_reg) == True:
                    dead_list.append(creature) # add to list and delete all at once to avoid runtime error: dictionary size change
            for creature in dead_list:
                del Creature.instance_reg[creature]

            control = None # reset control so loop can continue normally without repeating control



if __name__ == "__main__":
    main()