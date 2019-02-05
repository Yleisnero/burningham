#! python3

import cmd
import textwrap
import time

DESC = 'desc'
NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'
UP = 'up'
DOWN = 'down'
GROUND = 'ground'
SHOP = 'shop'
GROUNDDESC = 'grounddesc'
SHORTDESC = 'shortdesc'
LONGDESC = 'longdesc'
TAKEABLE = 'takeable'
EDIBLE = 'edible'
DESCWORDS = 'descwords'

SCREEN_WIDTH = 100

# Available Rooms
worldRooms = {
    'Homebase': {
        DESC: 'Nothing is here. Go out and solve some riddles and mysteries!',
        NORTH: 'Backyard',
        GROUND: []},
    'Backyard': {
        DESC: 'It\'s really dirty here!',
        SOUTH: 'Homebase',
        GROUND: ['Piece of Paper', 'Stone']},
    'Central Plaza': {
        DESC: 'This is the wonderful Central Plaza of Burningham (German: "brennender Schinken")',
        GROUND: []},
}

worldItems = {
    'Piece of Paper': {
        GROUNDDESC: 'A piece of paper lays on the ground',
        SHORTDESC: 'piece of paper',
        LONGDESC: "The piece of paper says: \"Solve the first task to prove you are strong enough to enter Burningham!"
                  "\"",
        TAKEABLE: True,
        DESCWORDS: ['piece', 'paper', 'pieceofpaper']},

    'Stone': {
        GROUNDDESC: 'There is a small round stone on the floor',
        SHORTDESC: 'small stone',
        LONGDESC: 'You can read "0x67 0x6F"',
        TAKEABLE: True,
        DESCWORDS: ['stone'],
    }
}

location = 'Homebase'  # start in homebase
inventory = []  # start with blank inventory
showFullExits = True


def displayLocation(loc):
    """A helper function for displaying an area's description and exits."""
    # Print the room name.
    print(loc)
    print('=' * len(loc))

    # Print the room's description (using textwrap.wrap())
    print('\n'.join(textwrap.wrap(worldRooms[loc][DESC], SCREEN_WIDTH)))

    # Print all the items on the ground.
    if len(worldRooms[loc][GROUND]) > 0:
        for item in worldRooms[loc][GROUND]:
            print(worldItems[item][GROUNDDESC])

    # Print all the exits.
    exits = []
    for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
        if direction in worldRooms[loc].keys():
            exits.append(direction.title())
    print()
    if showFullExits:
        for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
            if direction in worldRooms[location]:
                print('%s: %s' % (direction.title(), worldRooms[location][direction]))
    else:
        print('Exits: %s' % ' '.join(exits))


def moveDirection(direction):
    """A helper function that changes the location of the player."""
    global location

    if direction in worldRooms[location]:
        print('You move to the %s.' % direction)
        location = worldRooms[location][direction]
        displayLocation(location)
    else:
        print('You cannot move in that direction')


def getAllDescWords(itemList):
    """Returns a list of "description words" for each item named in itemList."""
    itemList = list(set(itemList))  # make itemList unique
    descWords = []
    for item in itemList:
        descWords.extend(worldItems[item][DESCWORDS])
    return list(set(descWords))


def getAllFirstDescWords(itemList):
    """Returns a list of the first "description word" in the list of
    description words for each item named in itemList."""
    itemList = list(set(itemList))  # make itemList unique
    descWords = []
    for item in itemList:
        descWords.append(worldItems[item][DESCWORDS][0])
    return list(set(descWords))


def getFirstItemMatchingDesc(desc, itemList):
    itemList = list(set(itemList))  # make itemList unique
    for item in itemList:
        if desc in worldItems[item][DESCWORDS]:
            return item
    return None


def getAllItemsMatchingDesc(desc, itemList):
    itemList = list(set(itemList))  # make itemList unique
    matchingItems = []
    for item in itemList:
        if desc in worldItems[item][DESCWORDS]:
            matchingItems.append(item)
    return matchingItems


def checkForStone():
    for item in inventory:
        if item == 'Stone':
            enterBurningham()


def enterBurningham():
    time.sleep(2)
    for i in range(0, 20):
        print("***\n")
        print("white flashlight")
        time.sleep(0.1)
    print("Wubba lubba dub dub ! \n")
    global location
    location = 'Central Plaza'
    displayLocation(location)


class TextAdventureCmd(cmd.Cmd):
    prompt = '\n> '

    # The default() method is called when none of the other do_*() command methods match.
    def default(self, arg):
        print('I do not understand that command. Type "help" for a list of commands.')

    # A very simple "quit" command to terminate the program:
    def do_quit(self, arg):
        """Quit the game."""
        return True  # this exits the Cmd application loop in TextAdventureCmd.cmdloop()

    def help_combat(self):
        print('Combat is not implemented in this program.')

    # These direction commands have a long (i.e. north) and show (i.e. n) form.
    # Since the code is basically the same, I put it in the moveDirection()
    # function.
    def do_north(self, arg):
        """Go to the area to the north, if possible."""
        moveDirection('north')

    def do_south(self, arg):
        """Go to the area to the south, if possible."""
        moveDirection('south')

    def do_east(self, arg):
        """Go to the area to the east, if possible."""
        moveDirection('east')

    def do_west(self, arg):
        """Go to the area to the west, if possible."""
        moveDirection('west')

    def do_up(self, arg):
        """Go to the area upwards, if possible."""
        moveDirection('up')

    def do_down(self, arg):
        """Go to the area downwards, if possible."""
        moveDirection('down')

    def do_go(self, arg):
        """You say go"""
        print('You said "go" with a mysterious voice')
        checkForStone()

    def do_help(self, arg):
        print("Documented commands:")
        print("====================")
        print("North: n\nSouth: s\nWest: w\nEast: e")
        print("Look around: look")
        print("Look at item: look <item>")
        print("Inventory: inv")
        print("Take item: take <item>\nDrop item: drop <item>")
        print("Eat item: eat <item>")
        print("Exit game: quit")

    def do_ascii(self, arg):
        print("   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |")
        print("-------------------------------------")
        print(" 0 |NUL|DLE|SPC| 0 | @ | P | ` | p |")
        print(" 1 |SOH|DC1| ! | 1 | A | Q | a | q |")
        print(" 2 |STX|DC2| \" | 2 | B | R | b | r |")
        print(" 3 |ETX|DC3| # | 3 | C | S | c | s |")
        print(" 4 |EQT|DC4| $ | 4 | D | T | d | t |")
        print(" 5 |ENQ|NAK| % | 5 | E | U | e | u |")
        print(" 6 |ACK|SQN| & | 6 | F | V | f | v |")
        print(" 7 |BEL|BTB| ' | 7 | G | W | g | w |")
        print(" 8 |BS |CAN| ( | 8 | H | X | h | x |")
        print(" 9 |HT |EM | ) | 9 | I | Y | i | y |")
        print(" A |LF |SUB| * | : | J | Z | j | z |")
        print(" B |VT |ESC| + | ; | K | [ | k | { |")
        print(" C |FF |FS | , | < | L | \\ | l | | |")
        print(" D |CR |GS | - | = | M | ] | m | } |")
        print(" E |SO |RS | . | > | N | ^ | n | ~ |")
        print(" F |SI |US | / | ? | O | _ | o |del|")

    # Since the code is the exact same, we can just copy the
    # methods with shortened names:
    do_n = do_north
    do_s = do_south
    do_e = do_east
    do_w = do_west
    do_u = do_up
    do_d = do_down

    def do_exits(self, arg):
        """Toggle showing full exit descriptions or brief exit descriptions."""
        global showFullExits
        showFullExits = not showFullExits
        if showFullExits:
            print('Showing full exit descriptions.')
        else:
            print('Showing brief exit descriptions.')

    def do_inventory(self, arg):
        """Display a list of the items in your possession."""

        if len(inventory) == 0:
            print('Inventory:\n  (nothing)')
            return

        # first get a count of each distinct item in the inventory
        itemCount = {}
        for item in inventory:
            if item in itemCount.keys():
                itemCount[item] += 1
            else:
                itemCount[item] = 1

        # get a list of inventory items with duplicates removed:
        print('Inventory:')
        for item in set(inventory):
            if itemCount[item] > 1:
                print('  %s (%s)' % (item, itemCount[item]))
            else:
                print('  ' + item)

    do_inv = do_inventory

    def do_take(self, arg):
        """"take <item> - Take an item on the ground."""

        # put this value in a more suitably named variable
        itemToTake = arg.lower()

        if itemToTake == '':
            print('Take what? Type "look" to see the items on the ground here.')
            return

        cantTake = False

        # get the item name that the player's command describes
        for item in getAllItemsMatchingDesc(itemToTake, worldRooms[location][GROUND]):
            if worldItems[item].get(TAKEABLE, True) == False:
                cantTake = True
                continue  # there may be other items named this that you can take, so we continue checking
            print('You take %s.' % (worldItems[item][SHORTDESC]))
            worldRooms[location][GROUND].remove(item)  # remove from the ground
            inventory.append(item)  # add to inventory
            return

        if cantTake:
            print('You cannot take "%s".' % (itemToTake))
        else:
            print('That is not on the ground.')

    def do_drop(self, arg):
        """"drop <item> - Drop an item from your inventory onto the ground."""

        # put this value in a more suitably named variable
        itemToDrop = arg.lower()

        # get a list of all "description words" for each item in the inventory
        invDescWords = getAllDescWords(inventory)

        # find out if the player doesn't have that item
        if itemToDrop not in invDescWords:
            print('You do not have "%s" in your inventory.' % (itemToDrop))
            return

        # get the item name that the player's command describes
        item = getFirstItemMatchingDesc(itemToDrop, inventory)
        if item != None:
            print('You drop %s.' % (worldItems[item][SHORTDESC]))
            inventory.remove(item)  # remove from inventory
            worldRooms[location][GROUND].append(item)  # add to the ground

    def complete_take(self, text, line, begidx, endidx):
        possibleItems = []
        text = text.lower()

        # if the user has only typed "take" but no item name:
        if not text:
            return getAllFirstDescWords(worldRooms[location][GROUND])

        # otherwise, get a list of all "description words" for ground items matching the command text so far:
        for item in list(set(worldRooms[location][GROUND])):
            for descWord in worldItems[item][DESCWORDS]:
                if descWord.startswith(text) and worldItems[item].get(TAKEABLE, True):
                    possibleItems.append(descWord)

        return list(set(possibleItems))  # make list unique

    def complete_drop(self, text, line, begidx, endidx):
        possibleItems = []
        itemToDrop = text.lower()

        # get a list of all "description words" for each item in the inventory
        invDescWords = getAllDescWords(inventory)

        for descWord in invDescWords:
            if line.startswith('drop %s' % (descWord)):
                return []  # command is complete

        # if the user has only typed "drop" but no item name:
        if itemToDrop == '':
            return getAllFirstDescWords(inventory)

        # otherwise, get a list of all "description words" for inventory items matching the command text so far:
        for descWord in invDescWords:
            if descWord.startswith(text):
                possibleItems.append(descWord)

        return list(set(possibleItems))  # make list unique

    def do_look(self, arg):
        """Look at an item, direction, or the area:
"look" - display the current area's description
"look <direction>" - display the description of the area in that direction
"look exits" - display the description of all adjacent areas
"look <item>" - display the description of an item on the ground or in your inventory"""

        lookingAt = arg.lower()
        if lookingAt == '':
            # "look" will re-print the area description
            displayLocation(location)
            return

        if lookingAt == 'exits':
            for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
                if direction in worldRooms[location]:
                    print('%s: %s' % (direction.title(), worldRooms[location][direction]))
            return

        if lookingAt in ('north', 'west', 'east', 'south', 'up', 'down', 'n', 'w', 'e', 's', 'u', 'd'):
            if lookingAt.startswith('n') and NORTH in worldRooms[location]:
                print(worldRooms[location][NORTH])
            elif lookingAt.startswith('w') and WEST in worldRooms[location]:
                print(worldRooms[location][WEST])
            elif lookingAt.startswith('e') and EAST in worldRooms[location]:
                print(worldRooms[location][EAST])
            elif lookingAt.startswith('s') and SOUTH in worldRooms[location]:
                print(worldRooms[location][SOUTH])
            elif lookingAt.startswith('u') and UP in worldRooms[location]:
                print(worldRooms[location][UP])
            elif lookingAt.startswith('d') and DOWN in worldRooms[location]:
                print(worldRooms[location][DOWN])
            else:
                print('There is nothing in that direction.')
            return

        # see if the item being looked at is on the ground at this location
        item = getFirstItemMatchingDesc(lookingAt, worldRooms[location][GROUND])
        if item != None:
            print('\n'.join(textwrap.wrap(worldItems[item][LONGDESC], SCREEN_WIDTH)))
            return

        # see if the item being looked at is in the inventory
        item = getFirstItemMatchingDesc(lookingAt, inventory)
        if item != None:
            print('\n'.join(textwrap.wrap(worldItems[item][LONGDESC], SCREEN_WIDTH)))
            return

        print('You do not see that nearby.')

    def complete_look(self, text, line, begidx, endidx):
        possibleItems = []
        lookingAt = text.lower()

        # get a list of all "description words" for each item in the inventory
        invDescWords = getAllDescWords(inventory)
        groundDescWords = getAllDescWords(worldRooms[location][GROUND])
        shopDescWords = getAllDescWords(worldRooms[location].get(SHOP, []))

        for descWord in invDescWords + groundDescWords + shopDescWords + [NORTH, SOUTH, EAST, WEST, UP, DOWN]:
            if line.startswith('look %s' % (descWord)):
                return []  # command is complete

        # if the user has only typed "look" but no item name, show all items on ground, shop and directions:
        if lookingAt == '':
            possibleItems.extend(getAllFirstDescWords(worldRooms[location][GROUND]))
            possibleItems.extend(getAllFirstDescWords(worldRooms[location].get(SHOP, [])))
            for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
                if direction in worldRooms[location]:
                    possibleItems.append(direction)
            return list(set(possibleItems))  # make list unique

        # otherwise, get a list of all "description words" for ground items matching the command text so far:
        for descWord in groundDescWords:
            if descWord.startswith(lookingAt):
                possibleItems.append(descWord)

        # otherwise, get a list of all "description words" for items for sale at the shop (if this is one):
        for descWord in shopDescWords:
            if descWord.startswith(lookingAt):
                possibleItems.append(descWord)

        # check for matching directions
        for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
            if direction.startswith(lookingAt):
                possibleItems.append(direction)

        # get a list of all "description words" for inventory items matching the command text so far:
        for descWord in invDescWords:
            if descWord.startswith(lookingAt):
                possibleItems.append(descWord)

        return list(set(possibleItems))  # make list unique

    def do_list(self, arg):
        """List the items for sale at the current location's shop. "list full" will show details of the items."""
        if SHOP not in worldRooms[location]:
            print('This is not a shop.')
            return

        arg = arg.lower()

        print('For sale:')
        for item in worldRooms[location][SHOP]:
            print('  - %s' % (item))
            if arg == 'full':
                print('\n'.join(textwrap.wrap(worldItems[item][LONGDESC], SCREEN_WIDTH)))

    def do_eat(self, arg):
        """"eat <item>" - eat an item in your inventory."""
        itemToEat = arg.lower()

        if itemToEat == '':
            print('Eat what? Type "inventory" or "inv" to see your inventory.')
            return

        if itemToEat == 'stone':
            print('You eat %s' % (itemToEat))
            print('The magical stone exploded in your mouth...')
            print("GAME OVER")
            time.sleep(2)
            return True

        cantEat = False

        for item in getAllItemsMatchingDesc(itemToEat, inventory):
            if worldItems[item].get(EDIBLE, False) == False:
                cantEat = True
                continue  # there may be other items named this that you can eat, so we continue checking
            # NOTE - If you wanted to implement hunger levels, here is where
            # you would add code that changes the player's hunger level.
            print('You eat %s' % (worldItems[item][SHORTDESC]))
            inventory.remove(item)
            return

        if cantEat:
            print('You cannot eat that.')
        else:
            print('You do not have "%s". Type "inventory" or "inv" to see your inventory.' % (itemToEat))

    def complete_eat(self, text, line, begidx, endidx):
        itemToEat = text.lower()
        possibleItems = []

        # if the user has only typed "eat" but no item name:
        if itemToEat == '':
            return getAllFirstDescWords(inventory)

        # otherwise, get a list of all "description words" for edible inventory items matching the command text so far:
        for item in list(set(inventory)):
            for descWord in worldItems[item][DESCWORDS]:
                if descWord.startswith(text) and worldItems[item].get(EDIBLE, False):
                    possibleItems.append(descWord)

        return list(set(possibleItems))  # make list unique


if __name__ == '__main__':
    print('Burningham booted...')
    print('====================\n')
    print('(Type "help" for commands.)\n')
    displayLocation(location)
    TextAdventureCmd().cmdloop()
