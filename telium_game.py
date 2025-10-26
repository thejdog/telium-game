
#Telium - The game




import random

#Global vars

num_modules = 17
module = 1
last_module = 0
possible_moves = []
alive = True
won = False
redstone = 100
durability = 500
locked = 0
charged_creeper = 0
mine_shafts = []
info_signs = []
creepers = []

#procedure declarations

def load_module():
    global module, possible_moves
    possible_moves = get_modules_from(module)
    output_module()

def get_modules_from(module):
    moves = []
    text_file = open("module_" + str(module) + ".txt", "r")
    for counter in range(0,4):
        move_read = text_file.readline()
        move_read = int(move_read.strip())
        if move_read != 0:
            moves.append(move_read)
    text_file.close()
    return moves

def output_module():
    global module
    print()
    print("-----------------------------------------------------------------")
    print()
    print("You are in room",module)
    print()

def output_moves():
    global possible_moves
    print()
    print("From here you can move to rooms:  ",end='| ')
    for move in possible_moves:
        print(move,'| ',end='')
    print()

def get_action():
    global module, last_module, possible_moves
    valid_action = False
    while valid_action == False:
        print("What do you want to do next ? (MOVE, LOCK)")
        action = input(">")
        if action == "MOVE":
            move = int(input("Enter the room to move to: "))
            if move in possible_moves:
                valid_action = True
                last_module = module
                module = move
            else:
                print("The room must be connected to the current room.")
        
        if action == "LOCK":
            print("current redstone power: ",redstone, ".")
            command = input("Redstone prepared in hotbar. Enter command (LOCK): ")
            if command == "LOCK":
                lock()

def spawn_npcs():
    global num_modules, charged_creeper, mine_shafts, info_signs, creepers
    module_set = []
    for counter in range(2,num_modules + 1):
        module_set.append(counter)
    random.shuffle(module_set)
    i = 0
    charged_creeper = module_set[i]
    for counter in range(0,3):
        i=i+1
        mine_shafts.append(module_set[i])
    
    for counter in range(0,3):
        i=i+1
        info_signs.append(module_set[i])
    
    for counter in range(0,3):
        i=i+1
        creepers.append(module_set[i])

def check_mine_shafts():
    global num_modules, module, mine_shafts, durability
    if module in mine_shafts:
        print("There is an anvil here.")
        print("You use it to repair your flint and steel and sword.")
        durability_gained = 50
        print("Durability was ",durability,". It is now at ",durability+durability_gained,".")
        durability = durability + durability_gained
        print("You hear hissing from the surrounding doors!")
        print("There are creepers surrounding you.")
        print("They must have heard you using the anvil!")
        print("Your only escape is to start mining under the base.")
        print("You could end up anywhere.")
        print("You dig into the wooden floor and begin tunneling.")
        last_module = module
        module = random.randint(1,num_modules)
        load_module()

def lock():
    global num_modules, redstone, locked
    new_lock = int(input("Enter room to lock doors to:"))
    if new_lock < 0 or new_lock > num_modules:
        print("That is not a room.")
    elif new_lock == charged_creeper:
        print("Sorry but that room can not currently be locked...")
    else:
        locked = new_lock
        print("Mobs cannot enter room",locked)
        redstone_used = 25 + 5 * random.randint(0,5)
        redstone = redstone - redstone_used
        print("redstone power now: ", redstone, ".")

def move_charged_creeper():
    global num_modules, module, last_module, locked, charged_creeper, won, mine_shafts
    #if in same module as charged creeper...
    if module == charged_creeper:
        print("The charged creeper is in this room!")
        print("It has not spotted you.")
        #decide the amount of moves it should take
        moves_to_make = random.randint(1,3)
        can_move_to_last_module = False
        while moves_to_make > 0:
            #get moves cc can make
            moves = get_modules_from(charged_creeper)
            #remove current module
            if module in moves:
                moves.remove(module)
            #allow to double back
            if last_module in moves and can_move_to_last_module == False:
                moves.remove(last_module)
            #remove locked modules
            if locked in moves:
                moves.remove(locked)
            #if no escape...
            if len(moves) == 0:
                won = True
                moves_to_make = 0
                print("It cannot move anymore! Strike!")
            #otherwise move it to an ajacent module
            else:
                if moves_to_make == 1:
                    print("It moves on to another room. Phew.")
                charged_creeper = random.choice(moves)
                moves_to_make = moves_to_make - 1
                can_move_to_last_module = True
                #handle vent shafts
                while charged_creeper in mine_shafts:
                    if moves_to_make > 0:
                        print("It moves on to another room. Phew.")
                    print("You hear footsteps on the ceiling. It appears to be in the area where the redstone power travels in the base.")
                    valid_move = False
                    #cannot land in other mine shafts.
                    while valid_move == False:
                        valid_move = True
                        charged_creeper = random.randint(1,num_modules)
                        if charged_creeper in mine_shafts:
                            valid_move = False
                    #stop moving now travelled
                    moves_to_make = 0

def intuition():
    global possible_moves, creepers, mine_shafts
    #check possible moves...
    for connected_module in possible_moves:
        if connected_module in creepers:
            print("You hear footsteps and hissing coming from nearby...")
        if connected_module in mine_shafts:
            print("Your flint and steel feel like they could do with a repair... There must be an anvil somewhere nearby...")
        if connected_module in info_signs:
            print("You wish you could remember the layout of your base. Perhaps there is some way to find out?")

def normal_creepers():
    global module, creepers, durability, alive
    #output encounter
    if module in creepers:
        print("A creeper is in this room. It is not the charged creeper but has somehow entered the base.")
        print("It turns around, hisses and begins walking towards you.")
        #get action
        succesful_attack = False
        while succesful_attack == False:
            print("you can:")
            print()
            print("-----Hit it with a sword to push it backward so you can get out the room.")
            print("-----Use your flint and steel to force it to explode then run.")
            print()
            action = 0
            while action not in ("S", "F"):
                action = input("What will you do? sword:(S) flint+steel:(F)")
            print("How hard will you hit it? Current durability: ",durability, ".")
            dur_used = int(input(">"))
            durability = durability - dur_used
            #check if player has no durability... ;(
            if durability <= 0:
                print("You do not have enough durability to hit it hard enough and it explodes.")
                alive = False
                return
            #how much durability is needed
            if action == "S":
                dur_needed = 30 + 10*random.randint(0,3)
            if action == "F":
                dur_needed = 90 + 10*random.randint(0,3)
            #if not enough durability used: try again.
            if dur_used >= dur_needed:
                succesful_attack = True
            else:
                if action == "S":
                    print("You hit it but not hard enough. It is only knocked back a bit. You cannot escape in this window but you can hit it again.")
                if action == "F":
                    print("You strike your flint and steel but it only produses a few sparks. The creeper steps backwards and dodges, however, this gives you chance to strike again.")
        #if its successful...
        if action == "S":
            print("The creeper is launched backward into the corner of the room giving you chance to escape.")
        if action == "F":
            print("You light the creeper then run. You  see it detonate out of the corner of your eye. This room is now safe.")
            #remove it from the module.
            creepers.remove(module)
        print()

def information_signs():
    global module, info_signs, charged_creeper, mine_shafts, creepers
    if module in info_signs:
       print("You notice a sign stuck in the ground here. It appears to have some information written on it.")
       print()
       print("It reads:")
       print()
       print("The charged creeper is located in room:",charged_creeper)
       randnum = random.randint(0,3)
       if randnum == 1:
           print("Anvils are located in rooms",mine_shafts)
       elif randnum == 2:
          print("Informational signs are located in rooms:",info_signs)
       elif randnum == 3:
          print("Normal creepers are located in rooms:",creepers)





                
#-------------------------------------main program:-------------------------------------------


spawn_npcs()
print()
print("-----------------------------------------------------------------")
print("---------------TELIUM THE GAME (MINECRAFT EDITION)---------------")
print("-----------------------------------------------------------------")
print()
print("The story:")
print("One day, after a hard day of gathering resources, you arrive at your base and notice something:")
print("You left the door open!")
print("Worse, judging from the flash of green you see through a window, a CHARGED CREEPER has entered your base!")
print("You must try to get rid of it before it blows up anything valuable!")
print("Good luck! You will need it.")
go = "no"
while go == "no":
    go = input("Press (ENTER) to start game now.")

print()
print("-----------------------------------------------------------------")
print()
print("---------------------   GAME STARTS HERE   ----------------------")

#game loop:

while alive and not won:
    load_module()
    check_mine_shafts()
    move_charged_creeper()
    normal_creepers()
    information_signs()
    if won == False and alive == True:
        output_moves()
        intuition()
        get_action()

#if player wins or dies...

if alive == False:
    print("YOU DIED")

if won == True:
    print("The charged creeper is trapped and you detonate it with your flint and steel.")
    print()
    print("BOOM!")
    print()
    print("Luckily there was only a crafting table and furnace here. You can rebuild them easily.")
    print("YOU WIN")
