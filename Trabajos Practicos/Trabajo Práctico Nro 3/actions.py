from pydoc import classname
from tkinter import BooleanVar
from typing import Tuple, Union
from human import Human, Barbarian,Knight,Ninja
import player
import random
import mapping

numeric = Union[int, float]
    
def is_in_dungeon(xy:tuple) -> bool:
    '''
    Analyze if the player's movement is within the limits of the map.

    Parameters
    ----------
    xy : tuple
        Represents player movement.
   
    Returns
    -------
        True or False

    '''  
    if xy[0] in list(range(0,80)) and xy[1] in list(range(0,25)):
        return True
    return False


def attack(do_damage:object, recive_damage:object):
    '''
    Determines between the gnome and the human who does damage and who resives them.

    Parameters
    ----------
    do_damage : object
        Represents who deals damage when player and gnome fight.

    recive_damage : object
        Represents who takes damage when the player and the gnome fight.
        
    '''
    generate_damage=do_damage.damage()
    recive_damage.recive_damage(generate_damage)

    
def move_to(player: player.Player, location = [numeric, numeric]) :
    '''
    Determines the player's final position. 

    Parameters
    ----------
    player : object
        Represents who deals damage when player and gnome fight.
    
    location : tuple
        Represents a location on the map.

    Returns
    -------
        Final player's position.

    '''
    player.move_to(location)
    return player

    
def move_up(positionxy: tuple) -> tuple:
    '''
    Makes an upward movement.

    Parameters
    ----------
    positionxy : tuple
        Represents the player's position in the dungeon.
   
    Returns
    -------
        New positionxy.

    '''
    positionxy=(positionxy[0],positionxy[1]-1)
    return positionxy


def move_down(positionxy: tuple) -> tuple:
    '''
    Makes a downward movement.

    Parameters
    ----------
    positionxy : tuple
        Represents the player's position in the dungeon.
   
    Returns
    -------
        New positionxy.
        
    '''
    positionxy=(positionxy[0],positionxy[1]+1)
    return positionxy


def move_left(positionxy: tuple) -> tuple:
    '''
    Make a movement to the left. 

    Parameters
    ----------
    positionxy : tuple
        Represents the player's position in the dungeon.
   
    Returns
    -------
        New positionxy

    '''
    positionxy=(positionxy[0]-1,positionxy[1])
    return positionxy


def move_right(positionxy: tuple) -> tuple:
    '''
    Make a movement to the right. 

    Parameters
    ----------
    positionxy : tuple
        Represents the player's position in the dungeon.
   
    Returns
    -------
        New positionxy

    '''
    positionxy=(positionxy[0]+1,positionxy[1])
    return positionxy


def move_gnomo(position_xy_gnomo: tuple,position_xy_human: tuple,dungeon:classname,pickaxe:object
    ,amulet:object,sword:object,movements=[]) -> tuple:
    '''
    Generate the movement of the gnomes in the dungeon.

    Parameters
    ----------
    position_xy_gnomo : tuple
        Represents the gnomo's position in the dungeon.
    
    position_xy_human : tuple
        Represents the player's position in the dungeon.

    dungeon : class
        It's where all the information on the map is located. This is updated and saved with each change.
    
    player1 : object
        Represents the player. 

    amulet : object
        Represents the object amulet.

    sword : object
        Represents the object sword.
   
    Returns
    -------
        New position_xy_gnomo

    '''
    i=0
    while i<6:

            old_position=position_xy_gnomo

            if position_xy_human[0]>position_xy_gnomo[0] and 'right' not in movements:
                position_xy_gnomo=move_right(position_xy_gnomo)
                movements.append('right')
            elif position_xy_human[0]<position_xy_gnomo[0] and 'left' not in movements:
                position_xy_gnomo=move_left(position_xy_gnomo)
                movements.append('left')  
            elif position_xy_human[1]>position_xy_gnomo[1] and 'down' not in movements:
                position_xy_gnomo=move_down(position_xy_gnomo)
                movements.append('down')
            elif position_xy_human[1]<position_xy_gnomo[1] and 'up' not in movements:
                position_xy_gnomo=move_up(position_xy_gnomo)
                movements.append('up')  
            else:
                position_xy_gnomo=random.choice([move_up(position_xy_gnomo),
                move_down(position_xy_gnomo),move_right(position_xy_gnomo),move_left(position_xy_gnomo)])

            if (is_in_dungeon(position_xy_gnomo) 
                and dungeon.is_walkable(position_xy_gnomo) 
                and position_xy_gnomo!=pickaxe.loc()
                and position_xy_gnomo!=amulet.loc()
                and position_xy_gnomo!=sword.loc()
                and dungeon.loc(position_xy_gnomo).face !='<'
                and dungeon.loc(position_xy_gnomo).face !='>'):
                break
            #if it can't move to either side, it will serch another place on the map. 
            elif (not dungeon.is_walkable(move_up(position_xy_gnomo)) 
                and not dungeon.is_walkable(move_down(position_xy_gnomo)) 
                and not dungeon.is_walkable(move_right(position_xy_gnomo)) 
                and not dungeon.is_walkable(move_left(position_xy_gnomo))):
                position_xy_gnomo=old_position
                break
            i+=1
            position_xy_gnomo=old_position      
    return position_xy_gnomo


def climb_stair(dungeon:classname,player1: object):
    '''
    Produces a change to the previous dungeon when the player climbs the stairs.
    
    Parameters
    ----------
    dungeon : class
        It's where all the information on the map is located. This is updated and saved with each change.
    
    player1 : object
        Represents the player. 

    '''
    dungeon.level-=1

    if dungeon.level>=0:
        space_left=(dungeon.index(mapping.STAIR_DOWN)[0]-1,dungeon.index(mapping.STAIR_DOWN)[1])
        space_right=(dungeon.index(mapping.STAIR_DOWN)[0]+1,dungeon.index(mapping.STAIR_DOWN)[1])
        if is_in_dungeon(space_right):
            dungeon.dig(space_right)
            player1.move_to(space_right)
        else:
            dungeon.dig(space_left)
            player1.move_to(space_left)


def descend_stair(dungeon:classname,player1: object):
    '''
    Produces a change to the next dungeon when the player goes down the stairs.

    Parameters
    ----------
    dungeon : class
        It's where all the information on the map is located. This is updated and saved with each change.
    
    player1 : object
         Represents the player. 

    '''
    dungeon.level+=1

    space_left=(dungeon.index(mapping.STAIR_UP)[0]-1,dungeon.index(mapping.STAIR_UP)[1])
    space_right=(dungeon.index(mapping.STAIR_UP)[0]+1,dungeon.index(mapping.STAIR_UP)[1])
    
    if is_in_dungeon(space_left):
        dungeon.dig(space_left)
        player1.move_to(space_left)
    else:
        dungeon.dig(space_right)
        player1.move_to(space_right)


def stairs(dungeon:classname,player1:object):
    '''
    Determines when the player goes up or down the stairs.

    Parameters
    ----------
    dungeon : class
        It's where all the information on the map is located. This is updated and saved with each change.

    player1 : object
         Represents the player.         

    '''
    if dungeon.loc(player1.loc()).face =='<':
            climb_stair(dungeon,player1)
            
    elif dungeon.loc(player1.loc()).face =='>':
            descend_stair(dungeon,player1)


def pickup(dungeon:classname,player1: object,pickaxe: object,sword: object,amulet: object):
    '''
    Determines that the player has collected an item.

    Parameters
    ----------
    dungeon : class
        It's where all the information on the map is located. This is updated and saved with each change.
    
    player1 : object
        Represents the player. 

    sword : object
        Represents the object sword.
    
    amulet : object
        Represents the object amulet.

    '''
    dungeon.get_items(player1.loc())
    if player1.loc()==pickaxe.loc() and dungeon.level==0:
            player1.tool=True
    elif player1.loc()==sword.loc() and dungeon.level==1:
            player1.has_sword()
    elif player1.loc()==amulet.loc() and dungeon.level==2:
            player1.treasure=True


def human_is_dead(player1: object) -> bool:
    '''
    Changes the Player's status to dead when it loses all its HP.

    Parameters
    ----------
    player1 : object
        Represents the player.         

    Returns
    -------
        True or False

    '''
    if player1.hp<=0:
        player1.kill()
    if not player1.alive:
        return True
    return False


def gnomo_is_dead(gnome: object) -> bool:
    '''
    Changes the Gnome's status to dead when it loses all its HP.

    Parameters
    ----------
    gnome : object
        Represents the npc Gnomo.         

    Returns
    -------
        True or False

    '''
    if gnome.hp<=0:
            gnome.kill()
            return True
    return False


def player_movements(key: str,position_xy_human: tuple) -> tuple:
    '''
    Allows the player to control the movement of the Human with the keys w-a-s-d.

    Parameters
    ----------
    key : str
        Represents the keys the user uses to move the character.

    position_xy_human : tuple
        Represents the player's position in the dungeon.

    Returns
    -------
        New position_xy_human

    '''
    if key=="w":
        position_xy_human=move_up(position_xy_human)
    elif key=="s":
        position_xy_human=move_down(position_xy_human)
    elif key=="d":
        position_xy_human=move_right(position_xy_human)
    elif key=="a":
        position_xy_human=move_left(position_xy_human)
    return position_xy_human


def gnomo_move_and_attack(player1: object,gnome: object,position_xy_human: tuple,position_xy_gnomo: tuple):
    '''
    Determines when the gnome can move and attack the player.

    Parameters
    ----------
    player1 : object
         Represents the player.  

    gnome : object
        Represents the npc Gnomo. 

    position_xy_human : tuple
        Represents the player's position in the dungeon.

    position_xy_gnomo : tuple
        Represents the gnomo's position in the dungeon.
    
    '''
    if position_xy_gnomo!=position_xy_human and gnome.alive:
        gnome.move_to(position_xy_gnomo)
    elif gnome.alive:
        #Gnome attack towards Player
        attack(gnome, player1)


def player_move_and_attack(dungeon: classname,player1: object,gnome: object,position_xy_human: tuple,position_xy_gnomo: tuple):
    '''
    Determines when the player can move and attack the gnome.

    Parameters
    ----------
    dungeon : class
        It's where all the information on the map is located. This is updated and saved with each change.

    player1 : object
         Represents the player.  

    gnome : object
        Represents the npc Gnomo. 

    position_xy_human : tuple
        Represents the player's position in the dungeon.

    position_xy_gnomo : tuple
        Represents the gnomo's position in the dungeon.

    '''
    if is_in_dungeon(position_xy_human) and position_xy_human!=position_xy_gnomo:
        if dungeon.is_walkable(position_xy_human) :
            player1=move_to(player1,position_xy_human)
        elif player1.tool:
            dungeon.dig(position_xy_human)
            player1=move_to(player1,position_xy_human)
    elif is_in_dungeon(position_xy_human) and dungeon.is_walkable(position_xy_human):
        #Player attack towards Gnome
        attack(player1, gnome)


def select_gnome(level: int,gnomo1: object,gnomo2: object,gnomo3: object) -> object:
    '''
    Puts all the Gnomes in their corresponding level.
    
    Parameters
    ----------
    level : int
        Represents the level where the gnomes are placed.

    gnomo1 : object
        Represents the gnomo Kobold.

    gnomo2 : object
        Represents the gnomo Knoker.

    gnome3 : object
        Represents the gnomo Spriggan.
    
    Returns
    -------
        New gnomo

    '''
    if level == 0:
        gnome=gnomo1
    if level == 1:
        gnome=gnomo2
    if level == 2:
        gnome=gnomo3
    return gnome


def gnomo_unlocks(dungeon: classname,gnome: object,player1: object,amulet: object,sword: object):
    '''
    Changes the Gnome's faces when they change their status to dead.

    Parameters
    ----------
    dungeon : class
        It's where all the information on the map is located. This is updated and saved with each change.
    
    player1 : object
        Represents the player. 

    amulet : object
        Represents the object amulet.

    sword : object
        Represents the object sword.
    
    '''
    if gnomo_is_dead(gnome) and dungeon.level==0:
        gnome.face='%'
    if gnomo_is_dead(gnome) and player1.treasure==False and dungeon.level==2:
        gnome.face='%'
        dungeon.add_item(amulet, amulet.loc(),3)
    if gnomo_is_dead(gnome) and player1.weapon==False and dungeon.level==1:
        gnome.face='%'
        dungeon.add_item(sword, sword.loc(),2)

def select_player(name_player1,choose_player,dungeon):
    '''
    Select one of the three game's characters.

    Parameters
    ----------
    name_player1 : str
        Stores the name the player wants to have throughout the game.
    
    choose_player : int
        Stores the character chosen by the user.
    
    Returns
    -------
        The user's chosen character (object).
    
    '''
    if choose_player==1:
        game_player = Barbarian(name_player1, dungeon.find_free_tile())
    elif choose_player==2:
        game_player = Knight(name_player1, dungeon.find_free_tile())  
    else:
        game_player = Ninja(name_player1, dungeon.find_free_tile()) 
        
    return game_player