from map_objects.tile import Tile
from map_objects.rectangle import Rect
from random import randint

from components.ai import BasicMonster
from components.fighter import Fighter

import libtcodpy as libtcod
from entity import Entity

from render_functions import RenderOrder

class GameMap:
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.tiles=self.initialize_tiles()

    def initialize_tiles(self):
        tiles=[[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles
    
    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player,entities,max_monsters_per_room):

        rooms=[]
        num_rooms=0

        for r in range(max_rooms):
            #rand width and height
            w=randint(room_min_size,room_max_size)
            h=randint(room_min_size,room_max_size)
            #random position in boundaries of map
            x=randint(0,map_width -w-1)
            y=randint(0,map_height -h-1)

            #makes rects easier to work with
            new_room=Rect(x,y,w,h)

            #check intersections
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                #room is now valid

                #create tiles
                self.create_room(new_room)

                #center coordinates of the new room
                (new_x,new_y)=new_room.center()

                if num_rooms==0:
                    #First room, where player starts
                    player.x=new_x
                    player.y=new_y
                else:
                     # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room,entities,max_monsters_per_room)

                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1
                
    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self,x1,x2,y):
        for x in range(min(x1,x2),max(x1,x2)+1):
            self.tiles[x][y].blocked=False
            self.tiles[x][y].block_sight=False
            
    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self,room,entities,max_monsters_per_room):
        #get rand no. of monsters
        number_of_monsters=randint(0,max_monsters_per_room)

        for i in range(number_of_monsters):
            #choose rand location
            x=randint(room.x1+1,room.x2-1)
            y=randint(room.y1+1,room.y2-1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0,100)<80:
                    fighter_component=Fighter(hp=10,defence=0,power=3)
                    ai_component=BasicMonster()
                    
                    monster=Entity(x,y,'o',libtcod.desaturated_green,'Orc',blocks=True,render_order=RenderOrder.ACTOR,fighter=fighter_component,ai=ai_component)
                else:
                    fighter_component=Fighter(hp=16,defence=1,power=4)
                    ai_component=BasicMonster()
                    
                    monster=Entity(x,y,'T',libtcod.darker_green,"Troll",blocks=True,render_order=RenderOrder.ACTOR,fighter=fighter_component,ai=ai_component)
                entities.append(monster)
            
    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    
