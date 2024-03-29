from typing import Optional
from game.logic.base import BaseLogic
from game.models import Board,GameObject,Position,Config
from typing import Optional
import random
import time

# Tubes Stima 1 Point :
# 1. Utamain diamond terdekat dan diamond merah kalo bisa
# 2. Kalo ada base terdekat dan jauh dari diamond dan inventory tidak kosong balik ke base
# 3. menjauh dari pemain lawan atau ambil inventorynya
# 4. optimalin teleport dan red button

# Developing note :
# Cari diamond banyak yang deket sama base aja, rata rata max point yang didapet itu cuman 10
#error pas inevntory == 4 terus dapet red diamond
#fungsi buat calculate jarak ke tiap goal point
#masih banyak keliling gajelas perlu kalkulasi lama jalan sama waktu sisa biar optimal
#buat metode untuk atur prioritas untuk balik ke base dulu atau tetep jalan ngambilin diamond
#tiap satu langkah kira kira makan 1 detik
#ukuran table masih fix 15*15 padahal ganentu
#belum optimal fitur red button sama teeport
#buat fungsi menghindari teleport agar tidak looping
#kalo diamond abis, auto ke generate diamond, pilihannya klo sisa 1 diamond, pencet red button atau ambil diamond
#algoritma kalo dia lagi jalan menuju suatu goal position (bukan base dan invontory !=0) terus ngelewatin base, mampir aja

##algortima nextmove
class kangTackle(BaseLogic):
    def __init__(self):
        #Intialize attribute necessary
            self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            self.block_in = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
            self.goal_position: Optional[Position] = None
            self.current_direction = 0
            #sisanya apa 

    def boundary(self, n, smallest, largest):
        return max(smallest, min(n, largest))
    
    def get_way(self, current_x, current_y, dest_x, dest_y):
        delta_x = self.boundary(dest_x - current_x, -1, 1)
        delta_y = self.boundary(dest_y - current_y, -1, 1)
        if delta_x != 0:
            delta_y = 0
        if delta_x==0 and delta_y==0: #buat tele 
            #case kalo teleport di tiap pojok?
            if(current_x == 0):
                delta_y = 1
            elif(current_x == 14):
                delta_y = -1
            elif(current_y == 0):
                delta_x = 1
            elif(current_y == 14):
                delta_x = -1
            else:
                 delta_x = -1
            

        return (delta_x, delta_y)
    def culik_currentBlock(self, board_bot: GameObject, board: Board,current_position,mybotname):
        whichBlock_x = current_position.x//5
        whichBlock_y=current_position.y//5
        block_start_row = whichBlock_x * 5
        block_end_row = (whichBlock_x + 1) * 5
        block_start_col = whichBlock_y * 5
        block_end_col = (whichBlock_y + 1) * 5
        self.goal_position=None
        for k in range(block_start_row,block_end_row):
                for l in range(block_start_col,block_end_col):
                    for bot in board.game_objects:
                        if (bot.properties.can_tackle==True and bot.properties.diamonds>=2 and bot.position.x==k and bot.position.y==l and bot.properties.name !=mybotname):
                            print("MASUK CULIKK\n")
                            self.goal_position=bot.position
                            print(f"x: {self.goal_position.x}, y : {self.goal_position.y}\n")
                            print(f"Name : {bot.properties.name}, Diamond : {bot.properties.diamonds}")
                            # return self.goal_position
        return self.goal_position
            

    def culik_allblock(self,start_position,mybotname,board: Board,board_bot:GameObject):
        totaleveryblock=[]
        base = board_bot.properties.base
        for i in range(3):
             for j in range(3):
                    block_start_row = 5 * i
                    block_end_row = (1 + i) * 5
                    block_start_col = j * 5
                    block_end_col = (1 + j) * 5
                    totalpointblock=0
                    listrangediamond=[]
                    for k in range(block_start_row,block_end_row):
                            for l in range(block_start_col,block_end_col):
                                for bot in board.game_objects:
                                    if (bot.properties.can_tackle==True and bot.position.x==k and bot.position.y==l and bot.properties.name !=mybotname):
                                        totalpointblock+=bot.properties.diamonds
                                        print(f"total :\n",bot.properties.diamonds)
                                        listrangediamond.append((abs(abs(bot.position.x - start_position.x) + abs(bot.position.y - start_position.y)), bot.position))
                    sorted_listrangediamond = sorted(listrangediamond,key=lambda x: x[0]) #sort berdasar jarak atau jumlah point?
                    if sorted_listrangediamond:
                        distance,locationdiamond=sorted_listrangediamond[0]
                        totaleveryblock.append((totalpointblock,distance,locationdiamond))
        if totaleveryblock:
            sorted_totaleveryblock = sorted(totaleveryblock, key=lambda x: x[1])
            _, _, self.goal_position = sorted_totaleveryblock[0]
            return self.goal_position
        else:
            self.goal_position=base
            return self.goal_position


    def next_move(self, board_bot: GameObject, board: Board):
            props = board_bot.properties
            mybotname = board_bot.properties.name
            print(f"Time left : {props.milliseconds_left/1000} sec\n")
            # Analyze new state
            base = board_bot.properties.base
            current_position = board_bot.position
            distanceToBase = abs(abs(base.x- current_position.x) + abs(base.y - current_position.y))
            if props.diamonds == 5 or props.diamonds == 4  or ( (distanceToBase +1 == (props.milliseconds_left/1000)) and props.diamonds !=0) or (distanceToBase == (props.milliseconds_left/1000)) : #error pas inventory diamond = 4 terus dapet diamond merah
                # Move to base
                print("OTW Base\n")
                base = board_bot.properties.base
                self.goal_position = base
                
                delta_x, delta_y = self.get_way(
                    current_position.x,
                    current_position.y,
                    self.goal_position.x,
                    self.goal_position.y,
                )
            else:
                    if (self.culik_currentBlock(board_bot,board,current_position,mybotname)):
                         print(f"culik\n")
                         self.goal_position = self.culik_currentBlock(board_bot,board,current_position)
                    else:
                        self.goal_position = self.culik_allblock(current_position,mybotname,board,board_bot)

                    delta_x, delta_y = self.get_way(
                        current_position.x,
                        current_position.y,
                        self.goal_position.x,
                        self.goal_position.y,
                    )
            return delta_x,delta_y
    




















           #kode sementara
                    # start_time = time.time()
                    # for diamond in diamond_objects:
                    #         listrangediamond.append((abs(abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y)), diamond.position))
                    
                    # sorted_listrangediamond = sorted(listrangediamond, key=lambda x: x[0])
                    # _,self.goal_position=sorted_listrangediamond[0]