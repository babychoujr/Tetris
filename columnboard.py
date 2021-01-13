#Eric Chou 95408627
#PROJECT 5: The Fall of the World's Own Optimist (Part 2)
#
#columnboard.py (modified for project 5)
#  In this module, there are two classes.  fall_object class and the board class
# the board class is the data model for the column game.  The fall_object class is the
# faller object which moving on the game board.  The faller may eventually attach to the
# game board cells when it have nowhere to move.
#

class fall_object:
    def __init__(self, column, blocks, row_allowed):
        '''
        __init__
        :param column:
        :param blocks:
        :param row_allowed:
        constructor of the faller class
        '''
        self.bottom = -1
        self.column = column
        self.blocks = blocks
        self.row_allowed = row_allowed

    def drop(self):
        '''
        drop
        :return:
        move down the faller
        '''
        if (self.bottom < self.row_allowed-1): self.bottom = self.bottom + 1

    def reset(self):
        '''
        reset
        :return:
        reset the faller condition back to no_faller status
        '''
        self.bottom = -1
        self.column = 0
        self.blocks = []
        self.row_allowed = 0

    def change_column(self, col):
       '''
       change_column
       :param col:
       :return:
       change the current faller's column
       '''
       self.column = col

    def rotate(self):
        '''
        rotate
        :return:
        rotate the faller
        '''
        temp = self.blocks[len(self.blocks) - 1 ]
        new_blocks = self.blocks[0: len(self.blocks) - 1]
        new_blocks.insert(0, temp)
        self.blocks = new_blocks
    def __str__(self):
        '''
        __str__
        :return:
        oonvert a faller to string
        '''
        return str(self.column)+ " "+str(self.bottom)+" "+ str(self.row_allowed) + " " + str(self.blocks)

class board:
    def __init__(self, row, col):
        '''
        constructor
        :param row:
        :param col:
        constructor for the game board
        '''
        self.row = row
        self.column = col
        self.cell = [[" " for i in range(col)] for j in range(row)]
        self.fobj = fall_object(0, [], row)

    def draw(self, mode, debug):
        '''
        draw
        :param mode:
            mode == 0, normal mode
            mode == 1, when faller can no longer move
        :return:
        draw the game board
        '''

        self.cellx = [[" " for i in range(self.column)] for j in range(self.row)]
        for i in range(self.row):
            if (debug): print("|", end="")
            for j in range(self.column):
                self.cellx[i][j] = self.cell[i][j]
                if (j == self.fobj.column and (i>self.fobj.bottom-len(self.fobj.blocks) and i<= self.fobj.bottom)):
                    self.cellx[i][j] = self.fobj.blocks[len(self.fobj.blocks)-1-(self.fobj.bottom-i)].lower()
                if (debug):
                    if (self.cellx[i][j].islower()):
                        if (mode == 0):
                            print("[" + self.cellx[i][j].upper() + "]", end="")
                        elif (mode == 1):
                            print("|" + self.cellx[i][j].upper() + "|", end="")
                    else:
                        print(" " + self.cellx[i][j] + " ", end="")
            if (debug):
                print("|", end="")
                print()
        if (debug):
            bottom = "-" * (3 * self.column)
            print(" ", end="")
            print(bottom, end="")
            print(" ")
        return self.cellx

    def drop(self):
        '''
        drop
        :return:
        move the faller down
        '''
        success = False
        if (len(self.fobj.blocks)==0):  # no falling parts
            success = True
            return success
        if (self.fobj.bottom < self.fobj.row_allowed-1 and self.cell[self.fobj.bottom+1][self.fobj.column] == " "):
            self.fobj.drop()
            success = True
        return success

    def reset(self):
        '''
        reset
        :return:
        reset the game board
        '''
        self.cell = [[" " for i in range(self.column)] for j in range(self.row)]
        self.fobj = fall_object(0, [], self.row)

    def shift_right(self):
        '''
        shift_right
        :return:
        shift the faller to the right
        '''
        shift_OK = True
        j = self.fobj.column+1
        if j<0 or j > self.column-1:
            shift_OK = False

        if shift_OK:
            for i in range(self.fobj.bottom-len(self.fobj.blocks)+1, self.fobj.bottom+1):
                if self.cell[i][j] != ' ': shift_OK = False

        if shift_OK: self.fobj.column = self.fobj.column+1

    def shift_left(self):
        '''
        shift_left
        :return:
        shift the faller to the left
        '''
        shift_OK = True
        j = self.fobj.column-1
        if j<0 or j > self.column-1:
            shift_OK = False

        if shift_OK:
            for i in range(self.fobj.bottom-len(self.fobj.blocks)+1, self.fobj.bottom+1):
                if self.cell[i][j] != ' ': shift_OK = False

        if shift_OK: self.fobj.column = self.fobj.column-1

    def load(self):
        '''
        load
        :return:
        load the game board by rows of strings
        '''
        str_c = ["" for i in range(self.row)]
        for i in range(self.row):
            str_c[i] = input()
            if len(str_c[i]) != self.column:
                print("Loading wrong contents!")
                return
        for i in range(self.row):
            for j in range(self.column):
                self.cell[i][j] = str_c[i][j]

    def attach(self):
        '''
        attach
        :return:
        when the faller can no longer move down, attach the faller back to the game board
        '''
        t=[]
        for i in range(self.row):
            r = []
            for j in range(self.column):
                if (j == self.fobj.column and (i>self.fobj.bottom-len(self.fobj.blocks) and i<= self.fobj.bottom)):
                    a = self.fobj.blocks[len(self.fobj.blocks)-1-(self.fobj.bottom-i)]
                else:
                    a = self.cell[i][j]
                r.append(a)
            t.append(r)
        self.cell = t
        self.fobj.reset()

    def no_faller(self):
        '''
        no_faller
        :return:
        check if the game board currently has no faller
        '''
        no = False
        if (len(self.fobj.blocks)==0):
            no = True
        return no

    def inbound(self, p):
        '''
        inbound
        :param p:
        :return:
        Check if a location is inbound of the game board.
        '''
        i = False
        if (p[0]>=0 and p[0]<self.row and p[1]>=0 and p[1]<self.column):
            i = True
        return i

    def move_cell(self, amap):
        '''
        move_cell
        :param amap: marked locations to be removed
        :return: none
        pack the whole board by dropping all of the blocks down and fall over the marked locations
        The partial results, all of the columns are packed.
        Then, each column is assigned back to the board cells.
        '''
        pack = []
        for j in range(self.column):
            c = []
            for i in range(self.row-1, -1, -1):
                if amap[i][j]!=1:
                    c.append(self.cell[i][j])
            pack.append(c)

        self.cell = [[" " for i in range(self.column)] for j in range(self.row)]
        pj = 0
        pi = 0
        for j in range(self.column):              # for each column
            pi = 0
            for i in range(self.row-1, -1, -1):   # from the bottom of the table to the toop
                if (pj<len(pack) and pi<len(pack[pj])):
                    self.cell[i][j] = pack[pj][pi]
                pi = pi+1
            pj = pj+1

    def mark(self, p0, p1, p2, amap):
        '''
        mark
        :param p0:
        :param p1:
        :param p2:
        :param amap:
        :return:
        mark the blocks to be removed
        '''
        changed = False
        if (self.inbound(p0) and self.inbound(p1) and self.inbound(p2)):
            to_check = True
            if (self.cell[p0[0]][p0[1]] == ' '): to_check = False
            if (self.cell[p1[0]][p1[1]] == ' '): to_check = False
            if (self.cell[p2[0]][p2[1]] == ' '): to_check = False

            if (to_check and self.cell[p0[0]][p0[1]] == self.cell[p1[0]][p1[1]] and self.cell[p1[0]][
                p1[1]] == self.cell[p2[0]][p2[1]]):
                amap[p0[0]][p0[1]] = 1
                amap[p1[0]][p1[1]] = 1
                amap[p2[0]][p2[1]] = 1
                changed = True
        return amap, changed

    def adjust(self):
        '''
        adjust
        :return:
        adjust the game board by removing all marked blocks
        '''
        amap = [[0 for i in range(self.column)] for j in range(self.row)]
        changed = False
        for i in range(self.row):
            for j in range(self.column):
                # check horizontal
                p0 = (i, j)
                p1 = (i, j + 1)
                p2 = (i, j + 2)
                amap, cc = self.mark(p0, p1, p2, amap)
                if (cc): changed = True
                # check vertical
                p0 = (i, j)
                p1 = (i + 1, j)
                p2 = (i + 2, j)
                amap, cc = self.mark(p0, p1, p2, amap)
                if (cc): changed = True
                # check diagonal 1
                p0 = (i, j)
                p1 = (i + 1, j + 1)
                p2 = (i + 2, j + 2)
                amap, cc = self.mark(p0, p1, p2, amap)
                if (cc): changed = True
                # check diagonal 2
                p0 = (i, j)
                p1 = (i + 1, j - 1)
                p2 = (i + 2, j - 2)
                amap, cc = self.mark(p0, p1, p2, amap)
                if (cc): changed = True

        rtn = True
        if (changed):
            self.move_cell(amap)
            rtn = False
        elif (not changed):
            rtn = True

        return rtn

    def check_game(self):
        '''
        check_game
        :return:
        check if a game is over
        '''
        over = False
        if (self.fobj.bottom-(len(self.fobj.blocks)-1)<0):
            over = True
        return over
